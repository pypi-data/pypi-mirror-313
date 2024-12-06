# flake8: noqa
# type: ignore
import inspect
import logging
import re

from .utils import get_trace_id


class TraceIDAdapter(logging.LoggerAdapter):
    def process(self, msg, kwargs):
        trace_id = get_trace_id()
        frame = inspect.currentframe()
        calling_frame = frame.f_back.f_back.f_back
        function_name = calling_frame.f_code.co_name
        return (
            f"[trace_id: {trace_id}] [function: {function_name}] {msg}",
            kwargs,
        )  # noqa


class SensitiveValueFilter(logging.Filter):
    """
    A logging filter to hide sensitive values while optionally showing
    a specified number of trailing characters.
    """

    def __init__(self, sensitive_patterns: list[str] = None, show_last: int = 0):
        """
        Initializes the filter with a list of sensitive patterns to hide.

        Args:
            sensitive_patterns (list[str]): List of regex patterns for sensitive values.
            show_last (int): Number of trailing characters to show after redaction.
        """
        super().__init__()
        self.sensitive_patterns = [
            re.compile(pattern) for pattern in sensitive_patterns
        ]
        self.show_last = show_last

    def _redact(self, match: re.Match) -> str:
        """
        Redacts a matched sensitive value, leaving only the specified number
        of trailing characters visible.

        Args:
            match (re.Match): The regex match object.

        Returns:
            str: The redacted string.
        """
        full_value = match.group(0)
        if self.show_last > 0 and len(full_value) > self.show_last:
            redacted_part = "*" * (len(full_value) - self.show_last)
            visible_part = full_value[-self.show_last :]
            return f"{redacted_part}{visible_part}"
        return "*" * len(full_value)

    def filter(self, record: logging.LogRecord) -> bool:
        """
        Filters the log message to redact sensitive values.

        Args:
            record (logging.LogRecord): The log record.

        Returns:
            bool: Always True, as we modify the record in place.
        """
        for pattern in self.sensitive_patterns:
            record.msg = pattern.sub(self._redact, record.msg)
        return True
