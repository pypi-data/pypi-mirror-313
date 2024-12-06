# Copyright (C) 2023-2024 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.

from typing import Union

from httpx import AsyncClient
from httpx import HTTPStatusError
from httpx import RequestError

from common.logging import logger
from common.permissions.exceptions import AuthServiceNotAvailable
from common.permissions.exceptions import AuthUnhandledException
from common.permissions.schemas import PermissionsRequestSchema


class AuthClient:
    """Client to connect with auth service."""

    def __init__(self, auth_service_url: str) -> None:
        self.service_url = auth_service_url

    async def get_assertions(
        self, project_code: str, permissions: PermissionsRequestSchema
    ) -> dict[str, Union[bool, list]]:
        """Retrieve bulk rbac permission assertions."""

        try:
            payload = permissions.model_dump()['permissions']
            async with AsyncClient(timeout=15) as client:
                response = await client.post(
                    self.service_url + 'authorize', json=payload, params={'project_code': project_code}
                )
                response.raise_for_status()

            return response.json()

        except HTTPStatusError:
            logger.exception(f'Auth service could not retrieve bulk permission assertions: {response.text}')
            raise AuthUnhandledException()

        except RequestError:
            logger.exception('Unable to connect to the auth service to retrieve bulk permission assertions')
            raise AuthServiceNotAvailable()

        except Exception:
            logger.exception('Unable to retrieve bulk permission assertions')
            raise AuthUnhandledException()
