# Copyright (C) 2023-2024 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.

import re

import pytest
from httpx import RequestError

from common.permissions.exceptions import AuthServiceNotAvailable
from common.permissions.exceptions import AuthUnhandledException
from common.permissions.schemas import PermissionsRequestSchema
from common.services.auth_client import AuthClient


@pytest.fixture
def auth_client():
    return AuthClient('http://auth_service:5050/v1/')


class TestAuthClient:
    permission_request = PermissionsRequestSchema(
        permissions=[{'role': 'admin', 'zone': 'greenroom', 'resource': 'file_any', 'operation': 'copy'}]
    )

    async def test_get_assertions_return_granted_permission(self, auth_client, httpx_mock):
        project_code = 'test_project'
        granted = {'has_permission': True}
        httpx_mock.add_response(
            method='POST',
            url=re.compile(f'^{auth_client.service_url}authorize.*'),
            status_code=200,
            json=granted,
        )
        permission_assertion = await auth_client.get_assertions(project_code, self.permission_request)
        assert permission_assertion == granted

    async def test_get_assertions_raise_auth_unhandled_exception(self, auth_client, httpx_mock):
        project_code = 'test_project'
        httpx_mock.add_response(
            method='POST',
            url=re.compile(f'^{auth_client.service_url}authorize.*'),
            status_code=500,
            json={},
        )
        with pytest.raises(AuthUnhandledException):
            await auth_client.get_assertions(project_code, self.permission_request)

    async def test_get_assertions_raise_auth_service_unavailable_exception(self, auth_client, mocker):
        project_code = 'test_project'
        mocker.patch('httpx.AsyncClient.post', side_effect=RequestError('Connection Error'))
        with pytest.raises(AuthServiceNotAvailable):
            await auth_client.get_assertions(project_code, self.permission_request)
