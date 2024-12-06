# Copyright (C) 2022-2024 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.

import os
from typing import Any
from typing import Optional

from httpx import AsyncClient

from common.logging import logger
from common.permissions.exceptions import ProjectRoleNotFound
from common.permissions.permissions_manager import PermissionsManager
from common.project.project_client import ProjectClient
from common.services.auth_client import AuthClient


async def has_permission(
    auth_url: str,
    project_url: str,
    redis_url: str,
    project_code: str,
    resource: str,
    zone: str,
    operation: str,
    current_identity: dict[str, Any],
) -> bool:
    if current_identity['role'] == 'admin':
        role = 'platform_admin'
    else:
        if not project_code:
            logger.info('No project code and not a platform admin, permission denied')
            return False
        role = await get_project_role(project_code, current_identity)
        if not role:
            logger.info('Unable to get project role in permissions check, user might not belong to project')
            return False

    enable_state_check = os.environ.get('ENABLE_PROJECT_STATE_CHECK', 'true') == 'true'
    if enable_state_check:
        project_client = ProjectClient(project_url, redis_url)
        project = await project_client.get(project_code)
        if project.state == 'trashed':
            return False

    try:
        payload = {
            'role': role,
            'resource': resource,
            'zone': zone,
            'operation': operation,
            'project_code': project_code,
        }
        async with AsyncClient(timeout=15) as client:
            response = await client.get(auth_url + 'authorize', params=payload)
        if response.status_code != 200:
            error_msg = f'Error calling authorize API - {response.json()}'
            logger.info(error_msg)
            raise Exception(error_msg)
        if response.json()['result'].get('has_permission'):
            return True
        return False
    except Exception as e:
        error_msg = str(e)
        logger.info(f'Exception on authorize call: {error_msg}')
        raise Exception(f'Error calling authorize API - {error_msg}')


async def get_project_role(project_code: str, current_identity: dict[str, Any]) -> Optional[str]:
    role = None
    if current_identity['role'] == 'admin':
        role = 'platform_admin'
    else:
        for realm_role in current_identity['realm_roles']:
            # if this is a role for the correct project
            if realm_role.startswith(project_code + '-'):
                role = realm_role.replace(project_code + '-', '')
    return role


async def get_project_folder_entity(metadata_url: str, name: str, _type: str, zone: str, project_code: str):
    payload = {
        'name': name,
        'container_code': project_code,
        'container_type': 'project',
        'zone': 0 if zone == 'greenroom' else 1,
        'status': 'ACTIVE',
        'type': 'project_folder',
    }
    async with AsyncClient(timeout=15) as client:
        response = await client.get(metadata_url + 'item/', params=payload)
        if response.status_code == 404:
            # We can't know whether the project folder has been deleted or not, so try both
            payload['status'] = 'TRASHED'
            response = await client.get(metadata_url + 'item/', params=payload)
        response.raise_for_status()
    return response.json()['result']


async def has_file_permission(
    auth_url: str,
    metadata_url: str,
    project_url: str,
    redis_url: str,
    file_entity: dict,
    operation: str,
    current_identity: dict,
) -> bool:
    if file_entity['container_type'] != 'project':
        logger.info('Unsupport container type, permission denied')
        return False
    project_code = file_entity['container_code']
    username = current_identity['username']
    zone = 'greenroom' if file_entity['zone'] == 0 else 'core'

    folder_path_split = get_folder_path(file_entity)
    root_folder = folder_path_split[0] if folder_path_split else None

    if root_folder == 'shared':
        if len(folder_path_split) == 1:
            # We're checking the permission of the project folder itself
            project_folder_name = file_entity['name']
        else:
            project_folder_name = folder_path_split[1]
        project_folder_name = get_name_or_path(file_entity, folder_path_split)
        project_folder = await get_project_folder_entity(
            metadata_url,
            name=project_folder_name,
            _type='project_folder',
            project_code=project_code,
            zone=zone,
        )
        project_folder_id = project_folder['id']

        if not await has_permission(
            auth_url,
            project_url,
            redis_url,
            project_code,
            f'file_shared_{project_folder_id}',
            zone,
            operation,
            current_identity,
        ):
            return False
    elif root_folder == 'users':
        name_folder_name = get_name_or_path(file_entity, folder_path_split)
        # If the user has file_any permission return True, if the file is in the users namefolder and the
        # user has file own permissions return True else False
        if not await has_permission(
            auth_url, project_url, redis_url, project_code, 'file_any', zone, operation, current_identity
        ):
            if name_folder_name != username:
                return False
            if not await has_permission(
                auth_url,
                project_url,
                redis_url,
                project_code,
                'file_in_own_namefolder',
                zone,
                operation,
                current_identity,
            ):
                return False
    else:
        # Root level permissions
        if operation != 'view':
            return False
    return True


def get_folder_path(file_entity: dict[str, str]) -> list[str]:
    if file_entity.get('status') in ['TRASHED', 'DELETED']:
        path_for_permissions = 'restore_path'
    else:
        path_for_permissions = 'parent_path'
    path = file_entity.get(path_for_permissions, '')
    if path:
        return path.split('/')
    else:
        return []


def get_name_or_path(file_entity: dict[str, str], folder_path_split: list[str]) -> str:
    if len(folder_path_split) == 1:
        # We're checking the permission of the project folder itself
        folder_name = file_entity['name']
    else:
        folder_name = folder_path_split[1]
    return folder_name


async def has_permissions(
    auth_url: str,
    project_url: str,
    redis_url: str,
    project_code: str,
    permissions: list[dict[str, str]],
    current_identity: dict[str, Any],
) -> dict[str, bool]:
    """Performs bulk permission assertions for a project."""
    enable_state_check = os.environ.get('ENABLE_PROJECT_STATE_CHECK', 'true') == 'true'
    if enable_state_check:
        project_client = ProjectClient(project_url, redis_url)
        project = await project_client.get(project_code)
        if project.state == 'trashed':
            return False

    permission_manager = PermissionsManager(project_code)
    role = permission_manager.retrieve_project_role(current_identity)
    if not role:
        logger.error(
            f'Unable to get project role in permissions check, user might not belong to project: ' f'{project_code}'
        )
        raise ProjectRoleNotFound('User role does not exist for project')

    permission_request = permission_manager.build_request(permissions, role)

    auth_client = AuthClient(auth_url)
    assertions = await auth_client.get_assertions(project_code, permission_request)

    mapped_assertions = permission_manager.map_assertions(permission_request, assertions)

    return mapped_assertions.model_dump()['assertion']
