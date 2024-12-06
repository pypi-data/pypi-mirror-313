# Copyright (C) 2022-2024 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.

from logging import DEBUG
from logging import ERROR

from common.logging import logger


class BaseClient:
    """
    Summary:
        The base client for all object storage class that will
        include some basic functions:
            - set logger level to DEBUG
            - set logger level to ERROR
    """

    def __init__(self, client_name: str) -> None:
        self.client_name = client_name

        # the flag to turn on class-wide logs
        self.logger = logger
        # initially only print out error info
        self.logger.setLevel(ERROR)

    async def debug_on(self):
        """
        Summary:
            The funtion will switch the log level to DEBUG
        """
        self.logger.setLevel(DEBUG)

        return

    async def debug_off(self):
        """
        Summary:
            The funtion will switch the log level to ERROR
        """
        self.logger.setLevel(ERROR)

        return
