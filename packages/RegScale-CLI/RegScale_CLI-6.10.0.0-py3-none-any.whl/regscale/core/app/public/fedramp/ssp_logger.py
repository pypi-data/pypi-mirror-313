from regscale.core.app.public.fedramp.reporting import (
    write_events,
    log_error,
    log_event,
)

import logging
from regscale.core.app.logz import create_logger


class CaptureEventsHandler:
    def __init__(self, events, errors, infos):
        self.handler = logging.Handler()
        self.events = events
        self.errors = errors
        self.infos = infos

    def emit(self, record):
        self.handler.emit(record)
        try:
            log_entry = self.handler.format(record)
            if record.levelname == "INFO":
                self.events.append(log_entry)
            elif record.levelname == "ERROR":
                self.errors.append(log_entry)
        except Exception:
            self.handler.handleError(record)


class SSPLogger:
    def __init__(self):
        self.events = []
        self.errors = []
        self.infos = []
        self.capture_handler = CaptureEventsHandler(self.events, self.errors, self.infos)
        self.logger = create_logger(custom_handler=self.capture_handler)

    def create_logger(self):
        return self.logger

    def info(self, event_msg: str, record_type: str = "", model_layer: str = ""):
        self.logger.info(event_msg)
        info = {
            "event_msg": event_msg,
            "record_type": record_type,
            "model_layer": model_layer,
        }
        self.infos.append(log_event(**info, level="Info"))

    def debug(self, msg, *args, **kwargs):
        self.logger.debug(msg, *args, **kwargs)

    def error(
        self,
        event_msg: str,
        record_type: str = "",
        model_layer: str = "",
        missing_element: str = "",
    ):
        self.logger.error(event_msg)
        error = {
            "event_msg": event_msg,
            "missing_element": missing_element,
            "record_type": record_type,
            "model_layer": model_layer,
        }
        self.errors.append(log_error(**error, level="Error"))

    def warning(self, event_msg: str, record_type: str = "", model_layer: str = ""):
        self.logger.warning(event_msg)
        warning = {
            "event_msg": event_msg,
            "record_type": record_type,
            "model_layer": model_layer,
        }
        self.infos.append(log_event(**warning, level="Warning"))

    def get_events(self):
        return self.events

    def get_errors(self):
        return self.errors

    def write_events(self):
        # Write the events.
        final_list = [*self.events, *self.errors, *self.infos]
        write_events(final_list)
