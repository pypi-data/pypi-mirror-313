# flake8: noqa
# type: ignore
import logging

from fastapi import Header

from secure_logs.config import SensitiveValueFilter, TraceIDAdapter

from .utils import trace_id_var


def get_trace_id(x_trace_id: str = Header(None)):
    return trace_id_var.get()


_LOGGING_CONFIGURED = False


def configure_logging(level: str, sensitive_patterns: list[str] = None):
    """
    Configures the logging level for the library and applies sensitive value redaction.

    Args:
        level (str): The logging level (e.g., DEBUG, INFO, WARNING, ERROR, CRITICAL).
        sensitive_patterns (list[str]): List of regex patterns for sensitive values.
    """
    global _LOGGING_CONFIGURED
    if not _LOGGING_CONFIGURED:
        logging.basicConfig(
            level=getattr(logging, level.upper(), logging.INFO),
            format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
        )
        if sensitive_patterns:
            sensitive_filter = SensitiveValueFilter(sensitive_patterns)
            logging.getLogger().addFilter(sensitive_filter)

        _LOGGING_CONFIGURED = True


def get_logger(
    name: str = __name__, sensitive_patterns: list[str] = None, show_last: int = 0
) -> TraceIDAdapter:
    """
    Returns a TraceIDAdapter logger with the given name. Optionally hides sensitive values.

    Args:
        name (str): The name of the logger.
        sensitive_patterns (list[str]): List of regex patterns for sensitive values.

    Returns:
        TraceIDAdapter: The logger instance.
    """
    logger = logging.getLogger(name)
    if not logging.getLogger().hasHandlers():
        configure_logging(
            level="DEBUG", sensitive_patterns=sensitive_patterns, show_last=show_last
        )
        logger.warning(
            "No logging configuration detected. Consider calling "
            "configure_logging()."
        )

    if sensitive_patterns:
        sensitive_filter = SensitiveValueFilter(sensitive_patterns, show_last)
        logger.addFilter(sensitive_filter)

    return TraceIDAdapter(logger, {})
