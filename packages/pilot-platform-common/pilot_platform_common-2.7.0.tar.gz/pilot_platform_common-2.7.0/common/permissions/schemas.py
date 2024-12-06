# Copyright (C) 2023-2024 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.

from pydantic import BaseModel


class PermissionsSchema(BaseModel):
    """Schema for permission to be asserted."""

    role: str
    zone: str
    resource: str
    operation: str


class PermissionsRequestSchema(BaseModel):
    """Schema for permissions requested to be asserted."""

    permissions: list[PermissionsSchema]


class PermissionsMappedAssertionSchema(BaseModel):
    """Schema for mapped asserted permissions."""

    assertion: dict[str, bool]
