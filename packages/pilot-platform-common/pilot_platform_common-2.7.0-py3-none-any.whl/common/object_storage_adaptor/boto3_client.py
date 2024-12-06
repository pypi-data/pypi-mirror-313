# Copyright (C) 2022-2024 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.

import json
import os
from datetime import datetime
from datetime import timedelta
from datetime import timezone
from typing import Any
from typing import Optional
from typing import Union

import aioboto3
import httpx
import xmltodict
from botocore.client import Config

from common.object_storage_adaptor.base_client import BaseClient

_SIGNATURE_VERSTION = 's3v4'


class TokenError(Exception):
    pass


async def get_boto3_client(
    endpoint: str, token: str = None, access_key: str = None, secret_key: str = None, https: bool = False
):
    mc = Boto3Client(endpoint, token, access_key, secret_key, https)
    await mc.init_connection()

    return mc


class Boto3Client(BaseClient):
    """
    Summary:
        The object client for minio operation. This class is based on
        the keycloak token to make the operations, including:
            - download object
            - presigned-download-url
            - copy object
            - presigned-upload-url
            - part upload
            - combine parts on server side
        The initialization will require either jwt token or access key +
        secret key from object storage
    """

    def __init__(
        self, endpoint: str, token: str = None, access_key: str = None, secret_key: str = None, https: bool = False
    ) -> None:
        """
        Parameter:
            - endpoint(string): the endpoint of minio(no http schema)
            - token(str): the user token from SSO
            - access_key(str): the access key of object storage
            - secret key(str): the secret key of object storage
            - https(bool): the bool to indicate if it is https connection
        """
        client_name = 'Boto3Client'
        super().__init__(client_name)

        self.endpoint = ('https://' if https else 'http://') + endpoint

        if token is None and access_key is None and secret_key is None:
            raise Exception('Either token or credentials is necessary for client')
        self.token = token
        self.access_key = access_key
        self.secret_key = secret_key
        self.session_token = None

        self._config = Config(signature_version=_SIGNATURE_VERSTION)
        self._session: Optional[aioboto3.Session] = None

    async def init_connection(self):
        """
        Summary:
            The async function to setup connection session to minio.

        return:
            - None
        """
        self.logger.info('Initialize object storage connection')

        # if we receive token by first time
        # ask minio to give the temperary credentials
        if self.token is not None:
            self.logger.info('Get temporary credentials')
            temp_credentials = await self._get_sts(self.token)
            self.logger.info('Temporary credentials: %s', json.dumps(temp_credentials))

            self.access_key = temp_credentials.get('AccessKeyId')
            self.secret_key = temp_credentials.get('SecretAccessKey')
            self.session_token = temp_credentials.get('SessionToken')

        self._session = aioboto3.Session(
            aws_access_key_id=self.access_key,
            aws_secret_access_key=self.secret_key,
            aws_session_token=self.session_token,
        )

        return

    async def _get_sts(self, jwt_token: str, duration: int = 86000) -> dict:
        """
        Summary:
            The function will use the token given to minio and
            get a temporary credential:
                - AccessKeyId
                - SecretAccessKey
                - SessionToken
            Note there is a special constrain for such temporary credentials.
            Its expirey time cannot be longer than jwt_token. for futher info
            check:
                https://docs.min.io/minio/baremetal/security/openid-external-identity-management/AssumeRoleWithWebIdentity.html
                Paremeter `DurationSeconds` has RFC 7519 4.1.4: Expiration Time Claim

        Parameter:
            - jwt_token(str): The token get from SSO
            - duration(int): how long the temporary credential
                will expire

        return:
            - dict
        """
        self.logger.info('Get sts from %s', self.endpoint)
        try:
            async with httpx.AsyncClient() as client:
                result = await client.post(
                    self.endpoint,
                    params={
                        'Action': 'AssumeRoleWithWebIdentity',
                        'WebIdentityToken': jwt_token.replace('Bearer ', ''),
                        'Version': '2011-06-15',
                        'DurationSeconds': duration,
                    },
                )

                if result.status_code == 400:
                    raise TokenError(f'Get temp token with {result.status_code} error: {result.text}')
                elif result.status_code != 200:
                    raise Exception(f'Get temp token with {result.status_code} error: {result.text}')

        except Exception as e:
            error_msg = str(e)
            self.logger.error('Error when getting sts token: %s', error_msg)
            raise e

        # TODO add the secret
        sts_info = (
            xmltodict.parse(result.text)
            .get('AssumeRoleWithWebIdentityResponse', {})
            .get('AssumeRoleWithWebIdentityResult', {})
            .get('Credentials', {})
        )

        return sts_info

    async def download_object(self, bucket: str, key: str, local_path: str) -> None:
        """
        Summary:
            The function is the boto3 wrapup to download the file from object storage

        Parameter:
            - bucket(str): the bucket name
            - key(str): the object path of file
            - local_path(str): the local path to download the file

        return:
            - None
        """
        self.logger.info('Downlaod object %s/%s to local path %s', bucket, key, local_path)

        # here create directory tree if not exist
        directory = os.path.dirname(local_path)
        if not os.path.exists(directory):
            self.logger.info('Directory %s does not exist. Create the path', directory)
            os.makedirs(directory)

        async with self._session.client('s3', endpoint_url=self.endpoint, config=self._config) as s3:
            await s3.download_file(bucket, key, local_path)

    async def upload_object(self, bucket: str, key: str, body: str) -> None:
        """
        Summary:
            The function is the boto3 wrapup to upload the file to object storage

        Parameter:
            - bucket(str): the bucket name
            - key(str): the object path of file
            - body(str): the content of the file

        return:
            - None
        """
        self.logger.info('Upload object to %s/%s', bucket, key)

        async with self._session.client('s3', endpoint_url=self.endpoint, config=self._config) as s3:
            await s3.put_object(Bucket=bucket, Key=key, Body=body)

    async def upload_file(self, bucket: str, filename: str, key: str, **kwds: Any) -> None:
        """
        Summary:
            The function is the boto3 wrapup to upload the local file to object storage

        Parameter:
            - bucket(str): the bucket name
            - filename(str): the path to the file to upload
            - key(str): the object path of file

        return:
            - None
        """

        self.logger.info(f'Upload file "{filename}" to "{bucket}/{key}"')

        async with self._session.client('s3', endpoint_url=self.endpoint, config=self._config) as s3:
            await s3.upload_file(Filename=filename, Bucket=bucket, Key=key, ExtraArgs=kwds)

    async def copy_object(self, source_bucket: str, source_key: str, dest_bucket: str, dest_key: str):
        """
        Summary:
            The function is the boto3 wrapup to copy the file on server side.
            Note here the single copy will only allow the upto 5GB

        Parameter:
            - source_bucket(str): the name of source bucket
            - source_key(str): the key of source path
            - dest_bucket(str): the name of destination bucket
            - dest_key(str): the key of destination path

        return:
            - object meta
        """
        self.logger.info('Copy object %s/%s to destination %s/%s', source_bucket, source_key, dest_bucket, dest_key)

        source_file = os.path.join(source_bucket, source_key)
        async with self._session.client('s3', endpoint_url=self.endpoint, config=self._config) as s3:
            res = await s3.copy_object(Bucket=dest_bucket, CopySource=source_file, Key=dest_key)

        return res

    async def delete_object(self, bucket: str, key: str) -> dict:
        """
        Summary:
            The function is the boto3 wrapup to delete the file on server.

        Parameter:
            - bucket(str): the name of bucket
            - key(str): the key of source path

        return:
            - object meta: contains the version_id
        """
        self.logger.info('Delete object %s/%s', bucket, key)

        async with self._session.client('s3', endpoint_url=self.endpoint, config=self._config) as s3:
            res = await s3.delete_object(Bucket=bucket, Key=key)

        return res

    async def stat_object(self, bucket: str, key: str) -> dict:
        """
        Summary:
            The function is the boto3 wrapup to get the file metadata.

        Parameter:
            - bucket(str): the name of bucket
            - key(str): the key of source path

        return:
            - object meta: contains the version_id
        """
        self.logger.info('Stat object %s/%s', bucket, key)

        async with self._session.client('s3', endpoint_url=self.endpoint, config=self._config) as s3:
            res = await s3.get_object(Bucket=bucket, Key=key)

        return res

    async def get_download_presigned_url(self, bucket: str, key: str, duration: int = 3600) -> str:
        """
        Summary:
            The function is the boto3 wrapup to generate a download presigned url.
            The user can directly download the file by open the url

        Parameter:
            - bucket(str): the bucket name
            - key(str): the object path of file
            - duration(int): how long the link will expire

        return:
            - presigned url(str)
        """
        self.logger.info('Get download presigned url %s/%s', bucket, key)

        async with self._session.client('s3', endpoint_url=self.endpoint, config=self._config) as s3:
            presigned_url = await s3.generate_presigned_url(
                'get_object', Params={'Bucket': bucket, 'Key': key}, ExpiresIn=duration
            )

        return presigned_url

    async def prepare_multipart_upload(
        self, bucket: str, keys: list[str], expire_time: Union[datetime, None] = None
    ) -> list[str]:
        """
        Summary:
            The function is the boto3 wrapup to generate a multipart upload presigned url.
            This is the first step to do the multipart upload.

            NOTE: The api has been changed to adapot the batch operation. The prepare
            upload api is a batch operation to create all jobs and lock in advance. If
            not, the performance will decrease that every iteration will try to connect
            with endpoints

        Parameter:
            - bucket(str): the bucket name
            - keys(list of str): the object path of file
            - expire_time(datetime): when the multipart upload will expire

        return:
            - upload_id(list): list of upload id will be used in later two apis
        """
        self.logger.info('Prepare multipart upload for bucket: %s, keys: %s', bucket, str(keys))

        # add the default expire time as utc now + 1 day
        if expire_time is None:
            expire_time = datetime.now(tz=timezone.utc) + timedelta(days=1)

        upload_id_list = []
        async with self._session.client('s3', endpoint_url=self.endpoint, config=self._config) as s3:
            for key in keys:
                res = await s3.create_multipart_upload(Bucket=bucket, Key=key, Expires=expire_time)
                upload_id_list.append(res.get('UploadId'))

        self.logger.info('Result upload ids: %s', str(upload_id_list))

        return upload_id_list

    async def part_upload(self, bucket: str, key: str, upload_id: str, part_number: int, content: str) -> dict:
        """
        Summary:
            The function is the boto3 wrapup to upload a SINGLE part.
            This is the second step to do the multipart upload.

        Parameter:
            - bucket(str): the bucket name
            - key(str): the object path of file
            - upload_id(str): the hash id generate from `prepare_multipart_upload` function
            - part_number(int): the part number of current chunk (which starts from 1)
            - content(str/byte): the file content

        return:
            - dict: will be collected and used in third step
        """
        self.logger.info('Upload object %s/%s with upload id: %s', bucket, key, upload_id)
        self.logger.info('Part number: %s with size: %s', part_number, len(content))

        presigned_url = await self.generate_presigned_url(bucket, key, upload_id, part_number)
        async with httpx.AsyncClient() as client:
            self.logger.info('Send part to server')
            res = await client.put(presigned_url, data=content, timeout=60)

            if res.status_code != 200:
                error_msg = f'Fail to upload the chunk {part_number}: {str(res.text)}'
                self.logger.error(error_msg)
                raise Exception(error_msg)

        etag = res.headers.get('ETag').replace("\"", '')

        return {'ETag': etag, 'PartNumber': part_number}

    async def generate_presigned_url(self, bucket: str, obj_path: str, upload_id: str, part_number: int) -> str:
        """
        Summary:
            The function is the boto3 wrapup to generate a presigned url of SINGLE part.
            This will allow client side to directly upload into minio.
            This is the second step to do the multipart upload.

        Parameter:
            - bucket(str): the bucket name
            - key(str): the object path of file
            - upload_id(str): the hash id generate from `prepare_multipart_upload` function
            - part_number(int): the part number of current chunk (which starts from 1)

        return:
            - str: the presigned url of parts
        """
        async with self._session.client('s3', endpoint_url=self.endpoint, config=self._config) as s3:
            signed_url = await s3.generate_presigned_url(
                ClientMethod='upload_part',
                Params={'Bucket': bucket, 'Key': obj_path, 'UploadId': upload_id, 'PartNumber': part_number},
            )

            return signed_url

    async def list_chunks(self, bucket: str, obj_path: str, upload_id: str) -> list[dict]:
        """
        Summary:
            The function is the boto3 wrapup to list uploaded parts on server side.

        Parameter:
            - bucket(str): the bucket name
            - key(str): the object path of file
            - upload_id(str): the hash id generate from `prepare_multipart_upload` function.

        return:
            - list: the list of {'ETag': <etag>, 'PartNumber': <part_number>} which collects
                from second step.
        """
        self.logger.info(f'List the chunks info for {bucket}/{obj_path} with id {upload_id}')

        async with self._session.client('s3', endpoint_url=self.endpoint, config=self._config) as s3:
            s3_parts_info = await s3.list_parts(Bucket=bucket, Key=obj_path, UploadId=upload_id)
            return s3_parts_info

    async def combine_chunks(self, bucket: str, key: str, upload_id: str, parts: list) -> dict:
        """
        Summary:
            The function is the boto3 wrapup to combine parts on server side.
            This is the third step to do the multipart upload.

        Parameter:
            - bucket(str): the bucket name
            - key(str): the object path of file
            - upload_id(str): the hash id generate from `prepare_multipart_upload` function
            - parts(list): the list of {'ETag': <etag>, 'PartNumber': <part_number>} which
                collects from second step.

        return:
            - dict
        """
        self.logger.info('Combine chunks %s/%s with upload id: %s', bucket, key, upload_id)
        self.logger.info('Number of chunks: %s', len(parts))

        async with self._session.client('s3', endpoint_url=self.endpoint, config=self._config) as s3:
            res = await s3.complete_multipart_upload(
                Bucket=bucket, Key=key, MultipartUpload={'Parts': parts}, UploadId=upload_id
            )

        return res
