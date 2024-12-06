# Copyright (C) 2023-2024 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.

from typing import Any
from typing import Optional
from typing import Union

from pydantic import ValidationError

from common.logging import logger
from common.permissions.exceptions import PermissionMappingError
from common.permissions.exceptions import PermissionsException
from common.permissions.exceptions import PermissionValidationError
from common.permissions.schemas import PermissionsMappedAssertionSchema
from common.permissions.schemas import PermissionsRequestSchema
from common.permissions.schemas import PermissionsSchema


class PermissionsManager:
    """Manages rbac permission assertions."""

    def __init__(self, project_code: str) -> None:
        self.project_code = project_code

    def _assertion_mapper(
        self, permission_request: PermissionsSchema, assertions: dict[str, Union[bool, list]]
    ) -> PermissionsMappedAssertionSchema:
        """Map assertions against single requested permission."""

        permission = True
        if not assertions['has_permission']:
            if permission_request.model_dump() in assertions['denied']:
                permission = False
        mapped = {
            f'{permission_request.zone}_{permission_request.resource}_' f'{permission_request.operation}': permission
        }

        return PermissionsMappedAssertionSchema(assertion=mapped)

    def build_request(self, permissions: list[dict[str, str]], role: str) -> PermissionsRequestSchema:
        """Build permission assertion request for auth service."""
        try:
            for permission in permissions:
                permission['role'] = role
            permission_request = PermissionsRequestSchema(permissions=permissions)

            return permission_request
        except ValidationError:
            logger.exception('Failed to parse and validate permissions.')
            raise PermissionValidationError('Permission request validation failed')
        except Exception:
            logger.exception('Error occurred when building permission request.')
            raise PermissionsException()

    def retrieve_project_role(self, current_identity: dict[str, Any]) -> Optional[str]:
        """Retrieve permissible project role based on user realm roles."""

        try:
            role = None
            if current_identity['role'] == 'admin':
                role = 'platform_admin'
            else:
                for realm_role in current_identity['realm_roles']:
                    if realm_role.startswith(self.project_code + '-'):
                        role = realm_role.replace(self.project_code + '-', '')

            return role
        except Exception:
            logger.exception(f'Cannot obtain role for project: {self.project_code}')
            raise PermissionsException(f'Failed to retrieve role for project: {self.project_code}')

    def map_assertions(
        self, permissions_requested: PermissionsRequestSchema, assertions: dict[str, Union[bool, list]]
    ) -> PermissionsMappedAssertionSchema:
        """Map rbac assertions from auth service against requested permissions."""

        mapped_assertions = {}
        try:
            for mapped in (
                self._assertion_mapper(permission, assertions) for permission in permissions_requested.permissions
            ):
                mapped_assertions.update(mapped.model_dump()['assertion'])

            return PermissionsMappedAssertionSchema(assertion=mapped_assertions)

        except ValidationError:
            logger.exception('Failed to parse and validate mapped asserted permissions.')
            raise PermissionValidationError('Permission mapped assertion validation failed')

        except Exception:
            logger.exception('Failed to map assertions')
            raise PermissionMappingError('Failed to map auth assertions to permissions')
