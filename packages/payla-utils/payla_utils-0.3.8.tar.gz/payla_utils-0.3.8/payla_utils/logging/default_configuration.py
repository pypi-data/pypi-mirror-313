import sys

import structlog
from django.utils.log import DEFAULT_LOGGING


def get_default_logging_conf(log_level: str, formatter: str, formatter_std_lib: str, own_apps: list[str]) -> dict:
    formatters = {
        'verbose': {
            'format': '%(asctime)s %(levelname)s %(name)s %(message)s',
        },
        'django.server': DEFAULT_LOGGING['formatters']['django.server'],
        'json_formatter': {
            '()': 'payla_utils.logging.logformatter.LogFormatter',
            'format': '%(timestamp)s %(level)s %(name)s %(message)s %(pathname)s:%(lineno)d',
        },
        "plain_console": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.dev.ConsoleRenderer(event_key='message'),
        },
        "plain_console_std_lib": {
            # std library + 3rd party loggers don't use structlog and therefore don't run through the processors
            "processor": structlog.dev.ConsoleRenderer(event_key='event'),
        },
        "key_value": {
            "()": structlog.stdlib.ProcessorFormatter,
            "processor": structlog.processors.KeyValueRenderer(
                key_order=['microservice', 'timestamp', 'level', 'event', 'logger']
            ),
        },
    }

    if formatter not in formatters or formatter_std_lib not in formatters:
        raise NotImplementedError("formatter not supported")

    return {
        'version': 1,
        'disable_existing_loggers': False,
        'formatters': formatters,
        'handlers': {
            'console': {
                'level': log_level,
                'class': 'logging.StreamHandler',
                'formatter': formatter,
                'stream': sys.stdout,
            },
            'console_std_lib': {
                'level': log_level,
                'class': 'logging.StreamHandler',
                'formatter': formatter_std_lib,
                'stream': sys.stdout,
            },
            'django.server': DEFAULT_LOGGING['handlers']['django.server'],
        },
        "root": {
            "level": log_level,
            "handlers": ["console_std_lib"],
            "propagate": False,
        },
        'loggers': {
            '': {
                'level': log_level,
                'handlers': ['console_std_lib'],
                "propagate": False,
            },
            'django.request': {
                'level': log_level,
                'handlers': ['console_std_lib'],
                "propagate": False,
            },
            "django.security.DisallowedHost": {
                'level': log_level,
                'handlers': ['console_std_lib'],
                "propagate": False,
            },
            'django.server': DEFAULT_LOGGING['loggers']['django.server'],
            "celery.task": {
                "handlers": ["console_std_lib"],
                "level": log_level,
                "propagate": False,
            },
            "celery": {
                "handlers": ["console_std_lib"],
                "level": log_level,
                "propagate": False,
            },
            # Setup loggers for each app
            **{
                app.split('.', maxsplit=1)[0]: {
                    "handlers": ["console"],
                    "level": log_level,
                    "propagate": False,
                }
                for app in own_apps
            },
        },
    }
