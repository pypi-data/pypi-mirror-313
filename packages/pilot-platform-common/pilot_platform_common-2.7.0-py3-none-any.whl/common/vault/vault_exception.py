# Copyright (C) 2022-2024 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.

from enum import Enum


class VaultClientError(Enum):
    CONNECT_ERROR = 'Failed to connect to Vault'
    RESPONSE_ERROR = 'Received invalid response from Vault'


class VaultClientException(Exception):
    def __init__(self, error: VaultClientError):
        self.error = error

    def __str__(self):
        return self.error.value
