# flake8: noqa
# type: ignore
import logging

from secure_logs.config import SensitiveValueFilter, TraceIDAdapter

from secure_logs import configure_logging, get_logger  # isort: skip


def test_configure_logging_once(mocker):
    mock_basic_config = mocker.patch("logging.basicConfig")
    configure_logging(level="DEBUG")
    configure_logging(level="INFO")
    mock_basic_config.assert_called_once()


def test_trace_id_adapter(mocker):
    mock_trace_id = mocker.patch(
        "secure_logs.config.get_trace_id", return_value="12345"
    )
    logger = logging.getLogger("test")
    adapter = TraceIDAdapter(logger, {})
    result = adapter.process("Test log message", {})
    assert "[trace_id: 12345]" in result[0]
    assert (
        "[function: _multicall]" in result[0]
    )  # Expected function name during pytest execution


def test_sensitive_value_filter_full_redaction():
    patterns = [r"\d{16}"]
    filter_instance = SensitiveValueFilter(sensitive_patterns=patterns)
    record = logging.LogRecord(
        "test", logging.INFO, "", 0, "Card: 1234567812345678", None, None
    )
    filter_instance.filter(record)
    assert record.msg == "Card: ****************"


def test_sensitive_value_filter_partial_redaction():
    patterns = [r"\d{16}"]
    filter_instance = SensitiveValueFilter(sensitive_patterns=patterns, show_last=4)
    record = logging.LogRecord(
        "test", logging.INFO, "", 0, "Card: 1234567812345678", None, None
    )
    filter_instance.filter(record)
    assert record.msg == "Card: ************5678"


def test_sensitive_value_filter_multiple_patterns():
    patterns = [r"\d{16}", r"User: \w+"]
    filter_instance = SensitiveValueFilter(sensitive_patterns=patterns)
    record = logging.LogRecord(
        "test", logging.INFO, "", 0, "Card: 1234567812345678, User: John", None, None
    )
    filter_instance.filter(record)
    assert record.msg == "Card: ****************, **********"


def test_get_logger_adapter(mocker):
    logger = get_logger("test_logger")
    assert isinstance(logger, logging.LoggerAdapter)


def test_get_logger_sensitive_filter(mocker):
    mock_add_filter = mocker.patch("logging.Logger.addFilter")
    patterns = [r"\d{16}"]
    get_logger("test_logger", sensitive_patterns=patterns)
    mock_add_filter.assert_called_once_with(mocker.ANY)
    assert isinstance(mock_add_filter.call_args[0][0], SensitiveValueFilter)
