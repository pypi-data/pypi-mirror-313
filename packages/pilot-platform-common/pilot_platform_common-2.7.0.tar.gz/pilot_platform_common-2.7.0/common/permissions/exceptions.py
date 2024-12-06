# Copyright (C) 2023-2024 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.


class AuthUnhandledException(Exception):
    """Raised when unhandled/unexpected internal error occurred."""

    pass


class AuthServiceNotAvailable(Exception):
    """Raised when auth service is not available."""

    pass


class PermissionsException(Exception):
    """Raised when permissions error is encountered."""

    pass


class ProjectRoleNotFound(Exception):
    """Raised when project role cannot be matched against realm roles."""

    pass


class PermissionMappingError(Exception):
    """Raised when asserted permissions fail to map to requested permissions."""

    pass


class PermissionValidationError(Exception):
    """Raised when permissions fail to adhere to schema."""

    pass
