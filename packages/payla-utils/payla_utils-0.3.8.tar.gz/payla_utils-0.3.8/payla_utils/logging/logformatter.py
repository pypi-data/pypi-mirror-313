from datetime import datetime, timezone

from pythonjsonlogger import jsonlogger

from payla_utils.settings import payla_utils_settings


# This is straight from python-json-logger's documentation and will
# add a few useful default fields to each log message.
class LogFormatter(jsonlogger.JsonFormatter):
    def add_fields(self, log_record, record, message_dict):
        super().add_fields(log_record, record, message_dict)
        # add project name
        log_record['microservice'] = payla_utils_settings.MICROSERVICE_NAME
        if not log_record.get('timestamp'):
            now = datetime.now(tz=timezone.utc).strftime('%Y-%m-%dT%H:%M:%S.%fZ')
            log_record['timestamp'] = now
        if log_record.get('level'):
            log_record['level'] = log_record['level'].upper()
        else:
            log_record['level'] = record.levelname
