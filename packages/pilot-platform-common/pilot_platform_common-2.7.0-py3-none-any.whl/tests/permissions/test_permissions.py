# Copyright (C) 2022-2024 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.

import re
from uuid import uuid4

import pytest

from common import get_project_role
from common import has_file_permission
from common import has_permission
from common import has_permissions
from common.permissions.exceptions import ProjectRoleNotFound


class TestPermissions:
    @pytest.mark.asyncio
    async def test_has_permission_true(self, httpx_mock, redis, project_mock):
        project_code = str(uuid4())
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': [f'{project_code}-admin'],
        }
        url = f'http://auth/authorize?role=admin&resource=project&zone=core&operation=view&project_code={project_code}'
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': True}}, url=url)

        result = await has_permission(
            'http://auth/', 'http://project', redis.url, project_code, 'project', 'core', 'view', current_identity
        )
        assert result is True

    @pytest.mark.asyncio
    async def test_has_permission_false(self, httpx_mock, redis, project_mock):
        project_code = str(uuid4())
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': [f'{project_code}-admin'],
        }
        url = f'http://auth/authorize?role=admin&resource=project&zone=core&operation=view&project_code={project_code}'
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': False}}, url=url)
        result = await has_permission(
            'http://auth/', 'http://project', redis.url, project_code, 'project', 'core', 'view', current_identity
        )
        assert result is False

    @pytest.mark.asyncio
    async def test_has_permission_platform_admin_true(self, httpx_mock, redis, project_mock):
        project_code = str(uuid4())
        current_identity = {
            'username': 'test',
            'role': 'admin',
        }
        url = (
            'http://auth/authorize?role=platform_admin&resource=project&zone=core&operation=view'
            f'&project_code={project_code}'
        )
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': True}}, url=url)
        result = await has_permission(
            'http://auth/', 'http://project', redis.url, project_code, 'project', 'core', 'view', current_identity
        )
        assert result is True

    @pytest.mark.asyncio
    async def test_has_permission_no_project_code(self, httpx_mock, redis):
        project_code = str(uuid4())
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': [f'{project_code}-admin'],
        }
        result = await has_permission(
            'http://auth/', 'http://project', redis.url, '', 'project', 'core', 'view', current_identity
        )
        assert result is False

    @pytest.mark.asyncio
    async def test_has_permission_service_error(self, httpx_mock, redis, project_mock):
        project_code = str(uuid4())
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': [f'{project_code}-admin'],
        }
        url = f'http://auth/authorize?role=admin&resource=project&zone=core&operation=view&project_code={project_code}'
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': True}}, url=url, status_code=500)
        with pytest.raises(Exception):  # noqa: B017
            await has_permission(
                'http://auth/', 'http://project', redis.url, project_code, 'project', 'core', 'view', current_identity
            )


class TestFilePermissions:
    @pytest.mark.asyncio
    async def test_has_file_permission_in_namefolder_true(self, httpx_mock, redis, project_mock):
        project_code = str(uuid4())
        file_data = {
            'parent_path': 'users/test',
            'zone': 'core',
            'container_code': project_code,
            'container_type': 'project',
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': [f'{project_code}-admin'],
        }
        url = f'http://auth/authorize?role=admin&resource=file_any&zone=core&operation=view&project_code={project_code}'
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': False}}, url=url)
        url = (
            'http://auth/authorize?role=admin&resource=file_in_own_namefolder&zone=core&operation=view'
            f'&project_code={project_code}'
        )
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': True}}, url=url)
        result = await has_file_permission(
            'http://auth/', 'http://metadata/v1/', 'http://project', redis.url, file_data, 'view', current_identity
        )
        assert result is True

    @pytest.mark.asyncio
    async def test_has_file_permission_in_other_namefolder_true(self, httpx_mock, redis, project_mock):
        project_code = str(uuid4())
        file_data = {
            'parent_path': 'users/another',
            'zone': 'core',
            'container_code': project_code,
            'container_type': 'project',
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': [f'{project_code}-admin'],
        }
        url = f'http://auth/authorize?role=admin&resource=file_any&zone=core&operation=view&project_code={project_code}'
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': False}}, url=url)
        result = await has_file_permission(
            'http://auth/', 'http://metadata/v1/', 'http://project', redis.url, file_data, 'view', current_identity
        )
        assert result is False

    @pytest.mark.asyncio
    async def test_has_file_permission_false(self, httpx_mock, redis, project_mock):
        project_code = str(uuid4())
        file_data = {
            'parent_path': 'users/test',
            'zone': 'core',
            'container_code': project_code,
            'container_type': 'project',
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': [f'{project_code}-admin'],
        }
        url = f'http://auth/authorize?role=admin&resource=file_any&zone=core&operation=view&project_code={project_code}'
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': False}}, url=url)
        url = (
            'http://auth/authorize?role=admin&resource=file_in_own_namefolder&zone=core&operation=view'
            f'&project_code={project_code}'
        )
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': False}}, url=url)
        result = await has_file_permission(
            'http://auth/', 'http://metadata/v1/', 'http://project', redis.url, file_data, 'view', current_identity
        )
        assert result is False

    @pytest.mark.asyncio
    async def test_has_file_permission_outside_of_namefolder_false(self, httpx_mock, redis, project_mock):
        project_code = str(uuid4())
        file_data = {
            'parent_path': 'users/test',
            'zone': 'core',
            'container_code': project_code,
            'container_type': 'project',
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': [f'{project_code}-admin'],
        }
        url = f'http://auth/authorize?role=admin&resource=file_any&zone=core&operation=view&project_code={project_code}'
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': False}}, url=url)
        url = (
            'http://auth/authorize?role=admin&resource=file_in_own_namefolder&zone=core&operation=view'
            f'&project_code={project_code}'
        )
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': False}}, url=url)
        result = await has_file_permission(
            'http://auth/', 'http://metadata/v1/', 'http://project', redis.url, file_data, 'view', current_identity
        )
        assert result is False

    @pytest.mark.asyncio
    async def test_has_file_permission_wrong_project(self, httpx_mock, redis):
        project_code = str(uuid4())
        file_data = {
            'parent_path': 'users/test',
            'zone': 'core',
            'container_code': project_code,
            'container_type': 'project',
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': ['wrongproject-admin'],
        }
        result = await has_file_permission(
            'http://auth/', 'http://metadata/v1/', 'http://project', redis.url, file_data, 'view', current_identity
        )
        assert result is False

    @pytest.mark.asyncio
    async def test_has_file_permission_wrong_container_type(self, httpx_mock, redis):
        project_code = str(uuid4())
        file_data = {
            'parent_path': 'users/test',
            'zone': 'core',
            'container_code': project_code,
            'container_type': 'dataset',
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': [f'{project_code}-admin'],
        }
        result = await has_file_permission(
            'http://auth/', 'http://metadata/v1/', 'http://project', redis.url, file_data, 'view', current_identity
        )
        assert result is False

    @pytest.mark.asyncio
    async def test_has_file_permission_trashed(self, httpx_mock, redis, project_mock):
        project_code = str(uuid4())
        file_data = {
            'status': 'TRASHED',
            'restore_path': 'users/test',
            'zone': 'core',
            'container_code': project_code,
            'container_type': 'project',
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': [f'{project_code}-admin'],
        }
        url = f'http://auth/authorize?role=admin&resource=file_any&zone=core&operation=view&project_code={project_code}'
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': False}}, url=url)
        url = (
            'http://auth/authorize?role=admin&resource=file_in_own_namefolder&zone=core&operation=view'
            f'&project_code={project_code}'
        )
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': True}}, url=url)
        result = await has_file_permission(
            'http://auth/', 'http://metadata/v1/', 'http://project', redis.url, file_data, 'view', current_identity
        )
        assert result is True

    @pytest.mark.asyncio
    async def test_has_file_permission_namefolder(self, httpx_mock, redis, project_mock):
        project_code = str(uuid4())
        file_data = {
            'parent_path': 'users',
            'type': 'name_folder',
            'name': 'test',
            'zone': 'core',
            'container_code': project_code,
            'container_type': 'project',
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': [f'{project_code}-admin'],
        }
        url = f'http://auth/authorize?role=admin&resource=file_any&zone=core&operation=view&project_code={project_code}'
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': False}}, url=url)
        url = (
            'http://auth/authorize?role=admin&resource=file_in_own_namefolder&zone=core&operation=view'
            f'&project_code={project_code}'
        )
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': True}}, url=url)
        result = await has_file_permission(
            'http://auth/', 'http://metadata/v1/', 'http://project', redis.url, file_data, 'view', current_identity
        )
        assert result is True

    @pytest.mark.asyncio
    @pytest.mark.parametrize('is_authorized', [True, False])
    async def test_has_file_permission_file_in_shared_folder(
        self, httpx_mock, get_project_folder, is_authorized, redis, project_mock
    ):
        project_code = str(uuid4())
        file_data = {
            'type': 'file',
            'name': 'test.txt',
            'zone': 'core',
            'container_code': project_code,
            'container_type': 'project',
            'parent_path': 'shared/user',
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': [f'{project_code}-admin'],
        }
        project_folder = get_project_folder
        resource = 'file_shared_' + project_folder['id']

        url = (
            f'http://auth/authorize?role=admin&resource={resource}&zone=core&operation=view&project_code={project_code}'
        )
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': is_authorized}}, url=url)

        result = await has_file_permission(
            'http://auth/', 'http://metadata/v1/', 'http://project', redis.url, file_data, 'view', current_identity
        )
        assert result is is_authorized

    @pytest.mark.asyncio
    @pytest.mark.parametrize('is_authorized', [True, False])
    async def test_has_file_permission_file_in_shared_folder_trashed_sourced(
        self, httpx_mock, is_authorized, redis, project_mock
    ):
        project_code = str(uuid4())
        file_data = {
            'type': 'file',
            'name': 'test.txt',
            'zone': 'core',
            'container_code': project_code,
            'container_type': 'project',
            'parent_path': 'shared/user',
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': [f'{project_code}-admin'],
        }
        PROJECT_FOLDER_DATA = {
            'type': 'project_folder',
            'name': 'user',
            'id': str(uuid4()),
        }

        url = (
            f'http://metadata/v1/item/?name=user&container_code={project_code}&container_type=project&zone=1'
            '&type=project_folder&status=ACTIVE'
        )
        httpx_mock.add_response(status_code=404, method='GET', json={}, url=url)

        url = (
            f'http://metadata/v1/item/?name=user&container_code={project_code}&container_type=project&zone=1'
            '&type=project_folder&status=TRASHED'
        )
        httpx_mock.add_response(method='GET', json={'result': PROJECT_FOLDER_DATA}, url=url)
        project_folder = PROJECT_FOLDER_DATA

        resource = 'file_shared_' + project_folder['id']
        url = (
            f'http://auth/authorize?role=admin&resource={resource}&zone=core&operation=view&project_code={project_code}'
        )
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': is_authorized}}, url=url)

        result = await has_file_permission(
            'http://auth/', 'http://metadata/v1/', 'http://project', redis.url, file_data, 'view', current_identity
        )
        assert result is is_authorized

    @pytest.mark.asyncio
    @pytest.mark.parametrize('is_authorized', [True, False])
    async def test_has_file_permission_file_in_shared_folder_trash(
        self, httpx_mock, is_authorized, redis, project_mock
    ):
        project_code = str(uuid4())
        file_data = {
            'type': 'file',
            'name': 'test.txt',
            'zone': 'core',
            'container_code': project_code,
            'container_type': 'project',
            'restore_path': 'shared',
            'status': 'TRASHED',
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': [f'{project_code}-admin'],
        }
        PROJECT_FOLDER_DATA = {
            'type': 'project_folder',
            'name': 'user',
            'id': str(uuid4()),
        }

        meta_url = re.compile('^http://metadata/v1/item/.*$')
        httpx_mock.add_response(method='GET', json={'result': PROJECT_FOLDER_DATA}, url=meta_url)

        resource = 'file_shared_' + PROJECT_FOLDER_DATA['id']

        url = (
            f'http://auth/authorize?role=admin&resource={resource}&zone=core&operation=view&project_code={project_code}'
        )
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': is_authorized}}, url=url)

        result = await has_file_permission(
            'http://auth/', 'http://metadata/v1/', 'http://project', redis.url, file_data, 'view', current_identity
        )
        assert result is is_authorized

    @pytest.mark.asyncio
    @pytest.mark.parametrize('is_authorized', [True, False])
    async def test_has_file_permission_shared_folder(
        self, httpx_mock, get_project_folder, is_authorized, redis, project_mock
    ):
        project_code = str(uuid4())
        file_data = {
            'type': 'project_folder',
            'name': 'user',
            'zone': 'core',
            'container_code': project_code,
            'container_type': 'project',
            'parent_path': 'shared',
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': [f'{project_code}-admin'],
        }
        project_folder = get_project_folder
        resource = 'file_shared_' + project_folder['id']

        url = (
            f'http://auth/authorize?role=admin&resource={resource}&zone=core&operation=view&project_code={project_code}'
        )
        httpx_mock.add_response(method='GET', json={'result': {'has_permission': is_authorized}}, url=url)

        result = await has_file_permission(
            'http://auth/', 'http://metadata/v1/', 'http://project', redis.url, file_data, 'view', current_identity
        )
        assert result is is_authorized

    @pytest.mark.asyncio
    async def test_has_file_permission_root_level_users(self, httpx_mock, redis):
        project_code = str(uuid4())
        file_data = {
            'type': 'root_folder',
            'name': 'users',
            'zone': 'core',
            'container_code': project_code,
            'container_type': 'project',
            'parent_path': None,
            'parent': None,
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': [f'{project_code}-admin'],
        }
        result = await has_file_permission(
            'http://auth/', 'http://metadata/v1/', 'http://project', redis.url, file_data, 'view', current_identity
        )
        assert result is True

    @pytest.mark.asyncio
    async def test_has_file_permission_root_level_shared(self, httpx_mock, redis):
        project_code = str(uuid4())
        file_data = {
            'type': 'root_folder',
            'name': 'shared',
            'zone': 'core',
            'container_code': project_code,
            'container_type': 'project',
            'parent_path': None,
            'parent': None,
        }
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': [f'{project_code}-admin'],
        }
        result = await has_file_permission(
            'http://auth/', 'http://metadata/v1/', 'http://project', redis.url, file_data, 'view', current_identity
        )
        assert result is True


class TestGetCurrentRole:
    @pytest.mark.asyncio
    async def test_get_current_role_admin(self, httpx_mock):
        project_code = str(uuid4())
        current_identity = {
            'username': 'test',
            'role': 'admin',
            'realm_roles': [f'{project_code}-admin'],
        }
        result = await get_project_role(project_code, current_identity)
        assert result == 'platform_admin'

    @pytest.mark.asyncio
    async def test_get_current_role_member(self, httpx_mock):
        project_code = str(uuid4())
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': [f'{project_code}-admin'],
        }
        result = await get_project_role(project_code, current_identity)
        assert result == 'admin'

    async def test_get_current_role_non_default(self, httpx_mock):
        project_code = str(uuid4())
        current_identity = {
            'username': 'test',
            'role': 'member',
            'realm_roles': [f'{project_code}-customrole'],
        }
        result = await get_project_role(project_code, current_identity)
        assert result == 'customrole'


class TestBulkPermissions:
    auth_service_url = 'http://auth_service/v1/'
    permission_request = [
        {'role': 'admin', 'zone': 'greenroom', 'resource': 'file_any', 'operation': 'copy'},
        {'role': 'admin', 'zone': 'greenroom', 'resource': 'file_any', 'operation': 'view'},
    ]

    async def test_has_permissions_return_mapped_assertions(self, httpx_mock, redis, project_mock):
        project_code = str(uuid4())
        current_identity = {'role': 'collaborator', 'realm_roles': [f'{project_code}-collaborator']}
        granted = {'has_permission': True}
        mapped_result = {'greenroom_file_any_copy': True, 'greenroom_file_any_view': True}

        httpx_mock.add_response(
            method='POST',
            url=f'{self.auth_service_url}authorize?project_code={project_code}',
            status_code=200,
            json=granted,
        )
        mapped = await has_permissions(
            self.auth_service_url, 'http://project', redis.url, project_code, self.permission_request, current_identity
        )

        assert mapped == mapped_result

    async def test_has_permissions_raise_project_role_not_found_exception_for_invalid_role(
        self, httpx_mock, redis, project_mock
    ):
        project_code = str(uuid4())
        identity = {'role': 'collaborator', 'realm_roles': ['invalid-collaborator']}
        with pytest.raises(ProjectRoleNotFound):
            await has_permissions(
                self.auth_service_url, 'http://project', redis.url, project_code, self.permission_request, identity
            )
