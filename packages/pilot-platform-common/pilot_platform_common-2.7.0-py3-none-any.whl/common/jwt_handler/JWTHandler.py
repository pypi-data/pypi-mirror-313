# Copyright (C) 2022-2024 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.

from typing import Any

import httpx
import jwt
from starlette.requests import Request

from common.jwt_handler.jwt_handler_exception import JWTHandlerError
from common.jwt_handler.jwt_handler_exception import JWTHandlerException
from common.jwt_handler.models import User
from common.logging import logger


class JWTHandler:
    def __init__(self, public_key: str) -> None:
        self.public_key = public_key

    def _get_token_from_authorization(self, request: Request) -> str:
        token = request.headers.get('Authorization')
        if token:
            result = token.split()[1]
            logger.debug(f'Got token from authorization: {result}')
            return result

    def _get_token_from_cookies(self, request: Request) -> str:
        cookies = request.headers.get('cookie')
        if cookies:
            cookies = cookies.split(';')
            for cookie in cookies:
                cookie = cookie.strip()
                if cookie.startswith('AUTH='):
                    result = cookie[5:]
                    logger.debug(f'Got token from cookies: {result}')
                    return result

    def get_token(self, request: Request) -> str:
        token = self._get_token_from_authorization(request)
        if not token:
            token = self._get_token_from_cookies(request)
            if not token:
                logger.error(f'Failed to get token from headers: {request.headers}')
                raise JWTHandlerException(JWTHandlerError.GET_TOKEN_ERROR)
        return token

    def decode_validate_token(self, encoded_token: str) -> dict:
        try:
            expected_audience = ['minio', 'account']
            decoded_token = jwt.decode(
                jwt=encoded_token,
                key=self.public_key,
                algorithms='RS256',
                audience=expected_audience,
                options={
                    'verify_signature': True,  # cryptographic signature
                    'verify_aud': True,  # audience
                    'verify_iss': True,  # issuer
                    'verify_exp': True,  # expiration
                    'verify_iat': True,  # issued at
                    'verify_nbf': True,  # not before
                },
            )
            return decoded_token
        except Exception as e:
            logger.error(f'Failed to validate token: {e}')
            raise JWTHandlerException(JWTHandlerError.VALIDATE_TOKEN_ERROR)

    async def get_current_identity(self, auth_service: str, decoded_token: dict[str, Any]) -> User:
        username: str = decoded_token.get('preferred_username')
        if not username:
            return None

        # get user data from Auth service
        async with httpx.AsyncClient() as client:
            response = await client.get(f'{auth_service}/v1/admin/user', params={'username': username, 'exact': True})
        if response.status_code != 200:
            msg = f'Failed to get user {username} from Auth service ({response.status_code})'
            logger.error(msg)
            raise Exception(msg)
        user = response.json()['result']
        if not user or user['attributes'].get('status') != 'active':
            logger.error(f'User {username} is not active')
            return None

        return User(
            user_id=user['id'],
            username=username,
            role=user['role'],
            email=user['email'],
            first_name=user['first_name'],
            last_name=user['last_name'],
            realm_roles=user['realm_roles'],
        )

    async def get_current_identity_stateless(self, decoded_token: dict[str, Any]) -> User:
        realm_roles: list = decoded_token.get('realm_access', {}).get('roles')

        if 'platform-admin' in realm_roles:
            role = 'admin'
        else:
            role = 'member'
        return User(
            user_id=decoded_token['sub'],
            username=decoded_token['preferred_username'],
            role=role,
            email=decoded_token['email'],
            first_name=decoded_token['given_name'],
            last_name=decoded_token['family_name'],
            realm_roles=realm_roles,
        )
