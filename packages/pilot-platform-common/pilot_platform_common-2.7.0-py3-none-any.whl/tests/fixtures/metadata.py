# Copyright (C) 2023-2024 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.

import re
from uuid import uuid4

import pytest


@pytest.fixture()
def get_project_folder(httpx_mock):
    PROJECT_FOLDER_DATA = {
        'type': 'project_folder',
        'name': 'user',
        'id': str(uuid4()),
    }

    url = re.compile('^http://metadata/v1/item/.*$')
    httpx_mock.add_response(method='GET', json={'result': PROJECT_FOLDER_DATA}, url=url)
    return PROJECT_FOLDER_DATA
