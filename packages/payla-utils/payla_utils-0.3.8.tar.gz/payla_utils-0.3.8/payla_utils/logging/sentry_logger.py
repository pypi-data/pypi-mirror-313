from logging import LogRecord

from sentry_sdk.integrations.logging import LoggingIntegration

_IGNORED_LOGGERS = set()


def ignore_logger(logger_name: str) -> None:
    _IGNORED_LOGGERS.add(logger_name)


class PaylaLoggingIntegration(LoggingIntegration):
    def _handle_record(self, record: LogRecord) -> None:
        # This match upper logger names, e.g. "celery" will match "celery.worker"
        # or "celery.worker.job"
        if record.name in _IGNORED_LOGGERS or record.name.split(".")[0] in _IGNORED_LOGGERS:
            return
        super()._handle_record(record)
