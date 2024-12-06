# Copyright (C) 2022-2024 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.

import asyncio
import json
from typing import Union

import httpx
from redis.asyncio.utils import from_url
from redis.exceptions import ConnectionError  # noqa: A004

from common.logging import logger

from .project_exceptions import ProjectException
from .project_exceptions import ProjectNotFoundException

CACHE_PREFIX = 'project_client-'
CACHE_EXPIRY = 300


class ProjectObject:
    attributes = [
        'id',
        'code',
        'name',
        'description',
        'image_url',
        'tags',
        'system_tags',
        'is_discoverable',
        'created_at',
        'updated_at',
        'is_favourite',
        'state',
        'created_by',
        'deleted_at',
    ]

    def __init__(self, data, project_client):
        self.project_client = project_client
        for attr in self.attributes:
            setattr(self, attr, data.get(attr))

    def __repr__(self):
        return f'<Project {self.code}>'

    async def json(self):
        result = {}
        for attr in self.attributes:
            result[attr] = getattr(self, attr, '')
        return result

    async def update(
        self,
        code=None,
        name=None,
        description=None,
        image_url=None,
        tags=None,
        system_tags=None,
        is_discoverable=None,
        state=None,
        notify_users=None,
    ):
        await self.project_client.connect_redis()
        data = {
            'code': code,
            'name': name,
            'description': description,
            'image_url': image_url,
            'tags': tags,
            'system_tags': system_tags,
            'is_discoverable': is_discoverable,
            'state': state,
            'notify_users': notify_users,
        }
        # remove blank items
        data = {k: v for k, v in data.items() if v is not None}

        async with httpx.AsyncClient() as client:
            response = await client.patch(self.project_client.base_url + f'/v1/projects/{self.id}', json=data)
        if response.status_code == 404:
            raise ProjectNotFoundException
        elif response.status_code != 200:
            raise ProjectException(status_code=response.status_code, error_msg=response.json())

        await self.project_client.redis.delete(CACHE_PREFIX + self.id)
        await self.project_client.redis.delete(CACHE_PREFIX + self.code)
        for attr in self.attributes:
            setattr(self, attr, response.json().get(attr))
        return self

    async def upload_logo(self, image_data):
        data = {'base64': image_data}
        async with httpx.AsyncClient() as client:
            response = await client.post(self.project_client.base_url + f'/v1/projects/{self.id}/logo', json=data)
        if response.status_code == 404:
            raise ProjectNotFoundException
        elif response.status_code != 200:
            raise ProjectException(status_code=response.status_code, error_msg=response.json())
        return self


class ProjectClient:
    def __init__(self, project_url, redis_url, enable_cache=True, is_async=True):
        self.base_url = project_url
        self.enable_cache = enable_cache
        self.redis_url = redis_url
        if is_async:
            self.project_object = ProjectObject
        else:
            self.project_object = ProjectObjectSync

    async def connect_redis(self):
        self.redis = await from_url(self.redis_url)

    async def search(
        self,
        page=None,
        page_size=None,
        order_by=None,
        order_type=None,
        name=None,
        code=None,
        description=None,
        is_discoverable=None,
        tags_all=None,
        code_any=None,
        created_at_start=None,
        created_at_end=None,
        favourite_by=None,
        guacamole: bool = False,
        superset: bool = False,
        jupyterhub: bool = False,
        state=None,
    ):
        data = {
            'page': page,
            'page_size': page_size,
            'sort_by': order_by,
            'sort_order': order_type,
            'name': name,
            'code': code,
            'description': description,
            'is_discoverable': is_discoverable,
            'tags_all': tags_all,
            'code_any': code_any,
            'created_at_start': created_at_start,
            'created_at_end': created_at_end,
            'favourite_by': favourite_by,
            'guacamole': guacamole,
            'superset': superset,
            'jupyterhub': jupyterhub,
            'state': state,
        }
        # remove blank items
        data = {k: v for k, v in data.items() if v not in [None, False]}

        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url + '/v1/projects/', params=data)
        if response.status_code == 404:
            raise ProjectNotFoundException
        elif response.status_code != 200:
            raise ProjectException(status_code=response.status_code, error_msg=response.json())
        result = response.json()
        result['result'] = [self.project_object(item, self) for item in response.json()['result']]
        return result

    async def get(self, id='', code=''):  # noqa: A002
        await self.connect_redis()
        project_id = ''
        if id:
            project_id = id
        else:
            project_id = code

        project_key = CACHE_PREFIX + project_id
        try:
            if self.enable_cache and await self.redis.exists(project_key):
                return self.project_object(json.loads(await self.redis.get(project_key)), self)
        except ConnectionError:
            logger.error(f"Couldn't connect to redis, skipping cache: {self.redis}")

        async with httpx.AsyncClient() as client:
            response = await client.get(self.base_url + f'/v1/projects/{project_id}')
        if response.status_code == 404:
            raise ProjectNotFoundException
        elif response.status_code != 200:
            raise ProjectException(status_code=response.status_code, error_msg=response.json())

        try:
            if self.enable_cache and self.redis:
                await self.redis.setex(project_key, CACHE_EXPIRY, json.dumps(response.json()))
        except ConnectionError:
            logger.error(f"Couldn't connect to redis, skipping cache: {self.redis}")
        return self.project_object(response.json(), self)

    async def create(
        self,
        code: str,
        name: str,
        description: str,
        operator: str,
        created_by: str,
        image_url: Union[str, None] = None,
        tags: Union[list[str], None] = None,
        system_tags: Union[list[str], None] = None,
        is_discoverable: bool = True,
        version: int = 1,
    ) -> ProjectObject:
        if tags is None:
            tags = []
        if system_tags is None:
            system_tags = []
        data = {
            'code': code,
            'name': name,
            'description': description,
            'operator': operator,
            'image_url': image_url,
            'tags': tags,
            'system_tags': system_tags,
            'is_discoverable': is_discoverable,
            'created_by': created_by,
        }
        # remove blank items
        data = {k: v for k, v in data.items() if v is not None}

        async with httpx.AsyncClient() as client:
            response = await client.post(self.base_url + f'/v{version}/projects/', json=data)
        if response.status_code != 200:
            raise ProjectException(status_code=response.status_code, error_msg=response.json())
        return self.project_object(response.json(), self)

    async def clear_cache(self, code: str):
        self.redis.delete(CACHE_PREFIX + code)


class ProjectObjectSync(ProjectObject):
    def __init__(self, *args, **kwargs):
        self.project_object = ProjectObject(*args, **kwargs)
        super().__init__(*args, **kwargs)

    def json(self, *args, **kwargs):
        return asyncio.run(self.project_object.json(*args, **kwargs))

    def update(self, *args, **kwargs):
        asyncio.run(self.project_object.update(*args, **kwargs))
        for attr in self.attributes:
            setattr(self, attr, getattr(self.project_object, attr))
        return self

    def upload_logo(self, *args, **kwargs):
        asyncio.run(self.project_object.upload_logo(*args, **kwargs))
        for attr in self.attributes:
            setattr(self, attr, getattr(self.project_object, attr))
        return self


class ProjectClientSync:
    def __init__(self, project_url, redis_url, enable_cache=True):
        self.project_client = ProjectClient(project_url, redis_url, enable_cache=enable_cache, is_async=False)
        asyncio.run(self.project_client.connect_redis())

    def get(self, *args, **kwargs):
        return asyncio.run(self.project_client.get(*args, **kwargs))

    def search(self, *args, **kwargs):
        return asyncio.run(self.project_client.search(*args, **kwargs))

    def create(self, *args, **kwargs):
        return asyncio.run(self.project_client.create(*args, **kwargs))
