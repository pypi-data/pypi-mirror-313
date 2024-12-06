# Copyright (C) 2023-2024 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.

import pytest

from common.permissions.exceptions import PermissionsException
from common.permissions.exceptions import PermissionValidationError
from common.permissions.permissions_manager import PermissionsManager
from common.permissions.schemas import PermissionsRequestSchema
from common.permissions.schemas import PermissionsSchema


@pytest.fixture
def permission_manager():
    return PermissionsManager('test_project')


class TestPermissionManager:
    permission_request = [
        {'role': 'admin', 'zone': 'greenroom', 'resource': 'file_any', 'operation': 'copy'},
        {'role': 'admin', 'zone': 'greenroom', 'resource': 'file_any', 'operation': 'view'},
    ]

    async def test_assertion_mapper_return_granted_permission_without_denied_assertions(self, permission_manager):
        mapped_value = {'greenroom_file_any_copy': True}
        permission_assertions = {'has_permission': True}
        request = PermissionsSchema(**self.permission_request[0])
        mapped = permission_manager._assertion_mapper(request, permission_assertions)

        assert mapped.assertion == mapped_value

    async def test_assertion_mapper_return_denied_permission_with_denied_assertions(self, permission_manager):
        mapped_value = {'greenroom_file_any_copy': False}
        permission_assertions = {'has_permission': False, 'denied': [self.permission_request[0]]}

        request = PermissionsSchema(**self.permission_request[0])
        mapped = permission_manager._assertion_mapper(request, permission_assertions)

        assert mapped.assertion == mapped_value

    async def test_retrieve_project_role_return_valid_project_role(self, permission_manager):
        role = 'collaborator'
        project_role = permission_manager.retrieve_project_role(
            {'role': role, 'realm_roles': ['test_project-collaborator']}
        )
        assert project_role == role

    async def test_retrieve_project_role_return_platform_admin_for_admin_role(self, permission_manager):
        role = 'admin'
        project_role = permission_manager.retrieve_project_role({'role': role, 'realm_roles': ['test_project-admin']})

        assert project_role == 'platform_admin'

    async def test_retrieve_project_role_return_none_for_invalid_project_realm_role(self, permission_manager):
        role = permission_manager.retrieve_project_role(
            {'role': 'collaborator', 'realm_roles': ['invalid_project-invalid']}
        )

        assert not role

    async def test_retrieve_project_role_raise_permissions_exception_for_invalid_parameter_structure(
        self, permission_manager
    ):
        with pytest.raises(PermissionsException):
            permission_manager.retrieve_project_role({'role': 'collaborator', 'realmroles': ['test_project-invalid']})

    async def test_map_assertions_return_granted_permission_without_denied_assertions(self, permission_manager):
        mapped_values = {'greenroom_file_any_copy': True, 'greenroom_file_any_view': True}
        permission_assertions = {'has_permission': True}

        request = PermissionsRequestSchema(permissions=self.permission_request)
        mapped = permission_manager.map_assertions(request, permission_assertions)

        assert mapped.assertion == mapped_values

    async def test_map_assertions_return_return_denied_permissions_with_denied_assertions(self, permission_manager):
        mapped_values = {'greenroom_file_any_copy': False, 'greenroom_file_any_view': True}
        permission_assertions = {'has_permission': False, 'denied': [self.permission_request[0]]}

        request = PermissionsRequestSchema(permissions=self.permission_request)
        mapped = permission_manager.map_assertions(request, permission_assertions)

        assert mapped.assertion == mapped_values

    async def test_build_request_return_validated_request(self, permission_manager):
        request = permission_manager.build_request(self.permission_request, 'admin')
        assert request == PermissionsRequestSchema(permissions=self.permission_request)

    async def test_build_request_with_incorrect_request_raise_permission_validation_error(self, permission_manager):
        permission = [{'role': 'admin', 'operation': 'copy'}]
        with pytest.raises(PermissionValidationError):
            permission_manager.build_request(permission, 'admin')
