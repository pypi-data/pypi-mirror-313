from __future__ import annotations

import logging
import logging.config

import structlog
from structlog import contextvars
from structlog.typing import EventDict
from structlog_sentry import SentryProcessor

from payla_utils.logging.default_configuration import get_default_logging_conf
from payla_utils.logging.sentry_logger import ignore_logger


class LoggerSetupError(Exception):
    pass


class LoggingConfigurator:
    def __init__(
        self,
        service_name: str,
        log_level: str,
        own_apps: list | None = None,
        config: dict | None = None,
        setup_logging_dict: bool = False,
    ):
        self.service_name = service_name
        self.log_level = log_level.upper()
        self.config = config
        self.own_apps = own_apps or []
        self.setup_logging_dict = setup_logging_dict

    @staticmethod
    def add_logger_name(logger: logging.Logger, method_name: str, event_dict: EventDict) -> EventDict:
        """
        Add the logger name to the event dict.
        """
        record = event_dict.get("_record")
        if record is None:
            event_dict["name"] = logger.name
        else:
            event_dict["name"] = record.name
        return event_dict

    def add_open_telemetry_spans(self, _, __, event_dict):
        from opentelemetry import trace
        from opentelemetry.trace import format_span_id, format_trace_id

        span = trace.get_current_span()
        if not span.is_recording():
            return event_dict

        ctx = span.get_span_context()
        parent = getattr(span, "parent", None)

        event_dict.update(
            {
                "span_id": format_span_id(ctx.span_id),
                "trace_id": format_trace_id(ctx.trace_id),
                "parent_span_id": None if not parent else format_span_id(parent.span_id),
            }
        )

        return event_dict

    def get_processors(self, tracing_enabled: bool) -> list:
        processors = [
            contextvars.merge_contextvars,
            self.add_logger_name,
            structlog.stdlib.add_log_level,
            structlog.stdlib.filter_by_level,
            structlog.processors.TimeStamper(fmt="iso"),
            structlog.stdlib.PositionalArgumentsFormatter(),
            structlog.processors.StackInfoRenderer(),
            structlog.dev.set_exc_info,
            structlog.processors.format_exc_info,
            structlog.processors.UnicodeDecoder(),
            structlog.processors.ExceptionPrettyPrinter(),
            structlog.stdlib.ExtraAdder(),
            SentryProcessor(event_level=logging.ERROR),
            structlog.processors.EventRenamer(to="message"),
            structlog.stdlib.ProcessorFormatter.wrap_for_formatter,
        ]
        if tracing_enabled:
            processors.insert(3, self.add_open_telemetry_spans)
        return processors

    def _fix_sentry_logging(self, extra_loggers_names: list[str] | None = None):
        """
        Ignore loggers using struct log to avoid duplicated events sent to sentry
        """
        for logger_name in [app.split('.', maxsplit=1)[0] for app in self.own_apps] + (extra_loggers_names or []):
            ignore_logger(logger_name)

    def configure_structlog(
        self,
        custom_processors=None,
        formatter='json_formatter',
        formatter_std_lib='json_formatter',
        tracing_enabled=False,
        extra_loggers_names: list[str] | None = None,
    ):
        if self.setup_logging_dict:
            logger_init_config = self.config or get_default_logging_conf(
                log_level=self.log_level,
                own_apps=self.own_apps,
                formatter=formatter,
                formatter_std_lib=formatter_std_lib,
            )
            for extra_logger_name in extra_loggers_names or []:
                logger_init_config['loggers'][extra_logger_name] = {
                    "handlers": ["console"],
                    "level": self.log_level,
                    "propagate": False,
                }

            logging.config.dictConfig(logger_init_config)

        self._fix_sentry_logging(extra_loggers_names=extra_loggers_names)

        processors = custom_processors or self.get_processors(tracing_enabled=tracing_enabled)

        structlog.configure(
            processors=processors,
            logger_factory=structlog.stdlib.LoggerFactory(),
            wrapper_class=structlog.stdlib.BoundLogger,
            cache_logger_on_first_use=True,
        )
