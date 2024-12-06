# flake8: noqa
# type: ignore
# Example file

from uuid import UUID

from fastapi import Depends, FastAPI

from secure_logs import configure_logging, get_logger, get_trace_id
from secure_logs.middleware import TraceIDMiddleware

# You can explicitly configure logging
configure_logging(level="debug")  # Optional

app = FastAPI()
app.add_middleware(TraceIDMiddleware)

# Keep this in a common file from where you can access through out the project
# logger = get_logger(__name__,) # General implementation
# logger = get_logger(__name__, sensitive_patterns=['This', 'log']) # Hide sensitive values with *
# logger = get_logger(__name__, sensitive_patterns=['This', 'log'],show_last=1) # Hide sensitive values with * by showing only last 1 item


# Configure sensitive value filter
sensitive_patterns = [
    r"\d{16}",  # Example: credit card numbers
    r"(?:\d{3}-\d{2}-\d{4})",  # Example: SSNs
    "User",  # Example: any text
    "level",
    "log",
    r"(?<=Bearer\s)[a-zA-Z0-9]+",  # Example: token
]
logger = get_logger(__name__, sensitive_patterns=sensitive_patterns, show_last=2)


@app.get("/")
def say_hello(name: str = "Dev", trace_id: UUID = Depends(get_trace_id)):
    logger.debug("This is debug level log.")
    logger.info("This is info level log.")
    logger.error("This is error level log.")
    logger.warning("This is warning level log.")
    return {"Message": f"Hello {name}"}


@app.get("/userinfo")
def get_user_info(trace_id: UUID = Depends(get_trace_id)):
    logger.info("User credit card: 1234567812345678.")
    logger.info("User SSN: 123-45-6789.")
    logger.info("Token authorization: Bearer abc123DEF456")
    return {"user": "Dev"}
