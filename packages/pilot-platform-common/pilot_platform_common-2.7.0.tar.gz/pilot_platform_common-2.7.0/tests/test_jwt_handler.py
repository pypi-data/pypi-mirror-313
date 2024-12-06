# Copyright (C) 2022-2024 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.

import pytest

from common.jwt_handler import JWTHandler
from common.jwt_handler.jwt_handler_exception import JWTHandlerException
from common.jwt_handler.models import User


class TestJWTHandler:
    AUTH_SERVICE = 'http://AUTH_SERVICE'

    def test_get_token_from_authorization(self, mock_rsa_keys, mock_request_authorization):
        client = JWTHandler(mock_rsa_keys['public_key'])
        token = client.get_token(mock_request_authorization)
        assert token == 'test_token'

    def test_get_token_from_cookie_with_spaces(self, mock_rsa_keys, mock_request_cookie_with_spaces):
        client = JWTHandler(mock_rsa_keys['public_key'])
        token = client.get_token(mock_request_cookie_with_spaces)
        assert token == 'test_token'

    def test_get_token_from_cookie_no_spaces(self, mock_rsa_keys, mock_request_cookie_no_spaces):
        client = JWTHandler(mock_rsa_keys['public_key'])
        token = client.get_token(mock_request_cookie_no_spaces)
        assert token == 'test_token'

    def test_get_token_no_headers(self, mock_rsa_keys, mock_request_no_headers):
        with pytest.raises(JWTHandlerException, match='Failed to get token'):
            client = JWTHandler(mock_rsa_keys['public_key'])
            client.get_token(mock_request_no_headers)

    async def test_get_current_identity_admin(self, mock_jwt_admin, mock_get_user_from_auth):
        client = JWTHandler(mock_jwt_admin['public_key'])
        decoded_token = client.decode_validate_token(mock_jwt_admin['token'])
        current_identity = await client.get_current_identity(
            auth_service=self.AUTH_SERVICE, decoded_token=decoded_token
        )
        assert current_identity.id
        assert current_identity.username == 'test'
        assert current_identity.role
        assert current_identity.email == 'test@test.com'
        assert current_identity.first_name == 'test'
        assert current_identity.last_name == 'test'
        assert current_identity.realm_roles == ['platform-admin']

    async def test_get_current_identity_contributor(self, mock_jwt_contributor, mock_get_user_from_auth_contrib):
        client = JWTHandler(mock_jwt_contributor['public_key'])
        decoded_token = client.decode_validate_token(mock_jwt_contributor['token'])
        current_identity = await client.get_current_identity(
            auth_service=self.AUTH_SERVICE, decoded_token=decoded_token
        )
        assert current_identity.id
        assert current_identity.username == 'test'
        assert current_identity.role
        assert current_identity.email == 'test@test.com'
        assert current_identity.first_name == 'test'
        assert current_identity.last_name == 'test'
        assert current_identity.realm_roles == ['testproject-contributor']

    async def test_get_current_identity_collaborator(self, mock_jwt_collaborator, mock_get_user_from_auth_collab):
        client = JWTHandler(mock_jwt_collaborator['public_key'])
        decoded_token = client.decode_validate_token(mock_jwt_collaborator['token'])
        current_identity = await client.get_current_identity(
            auth_service=self.AUTH_SERVICE, decoded_token=decoded_token
        )
        assert current_identity.id
        assert current_identity.username == 'test'
        assert current_identity.role
        assert current_identity.email == 'test@test.com'
        assert current_identity.first_name == 'test'
        assert current_identity.last_name == 'test'
        assert current_identity.realm_roles == ['testproject-collaborator']

    async def test_get_current_identity_stateless_admin(self, mock_jwt_admin):
        client = JWTHandler(mock_jwt_admin['public_key'])
        decoded_token = client.decode_validate_token(mock_jwt_admin['token'])
        current_identity = await client.get_current_identity_stateless(decoded_token=decoded_token)
        assert current_identity.id
        assert current_identity.username == 'test'
        assert current_identity.role
        assert current_identity.email == 'test@test.com'
        assert current_identity.first_name == 'test'
        assert current_identity.last_name == 'test'
        assert current_identity.realm_roles == ['platform-admin']

    async def test_get_current_identity_stateless_contributor(self, mock_jwt_contributor):
        client = JWTHandler(mock_jwt_contributor['public_key'])
        decoded_token = client.decode_validate_token(mock_jwt_contributor['token'])
        current_identity = await client.get_current_identity_stateless(decoded_token=decoded_token)
        assert current_identity.id
        assert current_identity.username == 'test'
        assert current_identity.role
        assert current_identity.email == 'test@test.com'
        assert current_identity.first_name == 'test'
        assert current_identity.last_name == 'test'
        assert current_identity.realm_roles == ['testproject-contributor']

    async def test_get_current_identity_stateless_collaborator(self, mock_jwt_collaborator):
        client = JWTHandler(mock_jwt_collaborator['public_key'])
        decoded_token = client.decode_validate_token(mock_jwt_collaborator['token'])
        current_identity = await client.get_current_identity_stateless(decoded_token=decoded_token)
        assert current_identity.id
        assert current_identity.username == 'test'
        assert current_identity.role
        assert current_identity.email == 'test@test.com'
        assert current_identity.first_name == 'test'
        assert current_identity.last_name == 'test'
        assert current_identity.realm_roles == ['testproject-collaborator']

    async def test_user_model_to_dict(self):
        user = User(
            user_id='test',
            username='test',
            role='admin',
            email='test@test.com',
            first_name='test',
            last_name='test',
            realm_roles=['testproject-collaborator'],
        )
        data = user.to_dict()
        assert data['id'] == 'test'
        assert data['username'] == 'test'
        assert data['role'] == 'admin'
        assert data['email'] == 'test@test.com'
        assert data['first_name'] == 'test'
        assert data['last_name'] == 'test'
        assert data['realm_roles'] == ['testproject-collaborator']

    async def test_user_model_str(self):
        user = User(
            user_id='test',
            username='test',
            role='admin',
            email='test@test.com',
            first_name='test',
            last_name='test',
            realm_roles=['testproject-collaborator'],
        )
        assert str(user) == '<User test>'

    def test_get_current_identity_admin_expired_token(self, mock_jwt_admin_expired):
        with pytest.raises(JWTHandlerException, match='Failed to validate token'):
            client = JWTHandler(mock_jwt_admin_expired['public_key'])
            client.decode_validate_token(mock_jwt_admin_expired['token'])
