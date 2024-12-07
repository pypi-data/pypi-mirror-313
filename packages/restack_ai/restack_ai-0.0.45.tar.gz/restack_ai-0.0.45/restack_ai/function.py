from temporalio import activity
from temporalio.exceptions import ApplicationError
from typing import Any
from .observability import logger, log_with_context

activity.logger.logger = logger

class ActivityLogger:
    """Wrapper for activity logger that ensures proper context and formatting"""
    
    def __init__(self):
        self._logger = activity.logger
    
    def _log(self, level: str, message: str, **kwargs: Any):
        try:
            activity.info()
            getattr(self._logger, level)(message, extra={'extra_fields': kwargs})
        except RuntimeError:
            log_with_context(level.upper(), message, **kwargs)

    def debug(self, message: str, **kwargs: Any): self._log('debug', message, **kwargs)
    def info(self, message: str, **kwargs: Any): self._log('info', message, **kwargs)
    def warning(self, message: str, **kwargs: Any): self._log('warning', message, **kwargs)
    def error(self, message: str, **kwargs: Any): self._log('error', message, **kwargs)
    def critical(self, message: str, **kwargs: Any): self._log('critical', message, **kwargs)

log = ActivityLogger()

FunctionFailure = ApplicationError
function_info = activity.info
heartbeat = activity.heartbeat
function = activity

__all__ = [
    'FunctionFailure',
    'log',
    'function_info',
    'heartbeat',
]

def current_workflow():
    return activity.Context.current().info