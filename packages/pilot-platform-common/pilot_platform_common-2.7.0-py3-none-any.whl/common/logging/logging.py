# Copyright (C) 2023-2024 Indoc Systems
#
# Contact Indoc Systems for any questions regarding the use of this source code.

import datetime as dt
import json
import logging
import logging.config
from collections.abc import Mapping
from typing import Any
from typing import Union

from opentelemetry import trace

AUDIT = logging.INFO + 5


class Logger(logging.Logger):
    def audit(self, message: str, **kwds: Any) -> None:
        ...


class JsonFormatter(logging.Formatter):
    """Convert LogRecord to JSON string with trace and span IDs."""

    def format(self, record: logging.LogRecord) -> str:
        # Get the current span
        span = trace.get_current_span()

        # Extract trace ID and span ID
        span_context = span.get_span_context()
        trace_id = format(span_context.trace_id, '032x') if span_context.is_valid else None
        span_id = format(span_context.span_id, '016x') if span_context.is_valid else None
        trace_enabled = span_context.trace_flags.sampled if span_context.trace_flags is not None else False

        asctime = dt.datetime.fromtimestamp(record.created, tz=dt.timezone.utc).isoformat()
        level = record.levelname
        logger = record.name
        location = f'{record.filename}:{record.lineno}'
        message = record.getMessage()
        exc_info = None
        if record.exc_info:
            exc_info = self.formatException(record.exc_info)
        details = None
        if isinstance(record.args, Mapping):
            details = record.args

        return json.dumps(
            {
                'asctime': asctime,
                'level': level,
                'logger': logger,
                'location': location,
                'message': message,
                'exc_info': exc_info,
                'details': details,
                'trace_id': trace_id,
                'span_id': span_id,
                'trace_enabled': trace_enabled,
            }
        )


def extend_logger_class() -> None:
    """Register a new level and extend the default logging.Logger class with an additional method.

    Using setLoggerClass() is not feasible in this case, since logging.Logger instances could potentially be already
    created before the invocation of this function.
    """

    def audit(self: Logger, message: str, **kwds: Any) -> None:
        """Log message and **kwds with severity 'AUDIT'."""

        if self.isEnabledFor(AUDIT):
            args = (kwds,) if kwds else None
            self._log(AUDIT, message, args=args)

    logging.addLevelName(AUDIT, 'AUDIT')

    logger_class = logging.getLoggerClass()
    logger_class.audit = audit


def configure_logging(level: int, formatter: str = 'json', namespaces: Union[list[str], None] = None) -> None:
    """Configure python logging system using a config dictionary."""

    formatters = {
        'default': {
            'format': '%(asctime)s\t%(levelname)s\t[%(name)s]\t%(message)s',
        },
        'json': {
            '()': JsonFormatter,
        },
    }
    if formatter not in formatters:
        formatter = next(iter(formatters))

    if namespaces is None:
        namespaces = ['pilot', 'asyncio', 'uvicorn']

    config = {
        'handlers': ['stdout'],
        'level': level,
    }
    loggers = dict.fromkeys(namespaces, config)

    logging_config = {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': formatters,
        'handlers': {
            'stdout': {
                'formatter': formatter,
                'class': 'logging.StreamHandler',
                'stream': 'ext://sys.stdout',
            },
        },
        'loggers': loggers,
    }

    extend_logger_class()

    logging.config.dictConfig(logging_config)
