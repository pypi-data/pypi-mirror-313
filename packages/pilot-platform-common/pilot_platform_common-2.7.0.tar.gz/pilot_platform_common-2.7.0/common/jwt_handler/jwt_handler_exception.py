# Copyright (C) 2022-2024 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.

from enum import Enum


class JWTHandlerError(Enum):
    GET_TOKEN_ERROR = 'Failed to get token'
    VALIDATE_TOKEN_ERROR = 'Failed to validate token'


class JWTHandlerException(Exception):
    def __init__(self, error: JWTHandlerError):
        self.error = error

    def __str__(self):
        return self.error.value
