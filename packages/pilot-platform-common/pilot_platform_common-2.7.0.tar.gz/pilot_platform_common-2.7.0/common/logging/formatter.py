# Copyright (C) 2022-2024 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.

import os
from logging import LogRecord
from typing import Any

from pythonjsonlogger import jsonlogger


class CustomJsonFormatter(jsonlogger.JsonFormatter):
    """Custom formatter to format logging records as json strings."""

    def __init__(self, *args: Any, **kwds: Any) -> None:
        super().__init__(*args, **kwds)

        self.namespace = None

    def get_namespace(self) -> str:
        """Get namespace for current service."""

        if self.namespace is None:
            self.namespace = os.environ.get('namespace', 'unknown')

        return self.namespace

    def add_fields(self, log_record: dict[str, Any], record: LogRecord, message_dict: dict[str, Any]) -> None:
        """Add custom fields into the log record."""

        super().add_fields(log_record, record, message_dict)

        log_record['level'] = record.levelname
        log_record['namespace'] = self.get_namespace()
        log_record['sub_name'] = record.name


def get_formatter() -> CustomJsonFormatter:
    """Return instance of default formatter."""

    return CustomJsonFormatter(fmt='%(asctime)s %(namespace)s %(sub_name)s %(level)s %(message)s')
