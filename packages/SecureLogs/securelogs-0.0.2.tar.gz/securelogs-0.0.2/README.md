# SecureLogs Library with Sensitive Value Masking

The **SecureLogs Library** provides logging functionality with **Trace ID** support and the ability to **mask sensitive values** in logs (such as credit card numbers, SSNs, tokens, etc.). It is designed for easy integration with **FastAPI** applications.

This guide will walk you through how to install, configure, and use the library to log trace information while hiding sensitive values.

## Table of Contents

1. [Installation](#1-installationinstallation)
2. [Basic Setup](#2-basic-setupbasic-setup)
3. [Configuring Logger](#3-configuring-logger)
4. [Using Sensitive Value Masking](#4-using-sensitive-value-masking)
5. [FastAPI Integration](#5-fastapi-integration)
6. [Example Output](#6-example-output)
7. [Configuration Options](#7-configuration-options)
8. [Conclusion](#8-conclusion)
9. [Example Implementation](#9-example-implementation)

## 1. Installation

To install the SecureLogs Library, use `pip`:

```bash
pip install SecureLogs
```

## 2. Basic Setup
Once installed, you need to configure the logger and integrate it into your FastAPI project.

### a. Import Required Components
In your FastAPI application, import the necessary components from the library.
```python
from uuid import UUID
from fastapi import Depends, FastAPI
from secure_logs import configure_logging, get_logger
from secure_logs import get_trace_id
from secure_logs.middleware import TraceIDMiddleware
```

### b. Configure Logging
You need to explicitly configure logging by calling configure_logging() with your preferred logging level (e.g., debug, info, etc.).

```python
# Set up logging with the desired level
configure_logging(level="debug")

app = FastAPI()
app.add_middleware(TraceIDMiddleware)

```
## 3. Configuring Logger
The logger can be configured to mask sensitive values such as credit card numbers, tokens, and other confidential data. You can also define how many characters of the sensitive data should be shown after masking.

### a. Define Patterns for Sensitive Values
You can provide a list of regular expression patterns or strings that match sensitive data (e.g., credit card numbers, tokens).

Example patterns to mask:

    Credit card numbers (\d{16})
    SSNs ((?:\d{3}-\d{2}-\d{4}))
    User-specific text (User)
    Tokens ((?<=Bearer\s)[a-zA-Z0-9]+)

### b. Initialize Logger with Masking
Use the `get_logger()` function to initialize the logger and provide sensitive value patterns and the number of visible characters.

```python
# Define patterns for sensitive data
sensitive_patterns = [
    r"\d{16}",  # Example: credit card numbers
    r"(?:\d{3}-\d{2}-\d{4})",  # Example: SSNs
    "User",  # Example: any text like 'User'
    r"(?<=Bearer\s)[a-zA-Z0-9]+"  # Example: token pattern
]

# Get the logger instance with sensitive patterns and show the last 2 characters
logger = get_logger(__name__, sensitive_patterns=sensitive_patterns, show_last=2)
```

### c. Example Logger Usage
```python
logger.debug("Debug message with sensitive data: 1234567812345678.")
logger.info("User information: SSN 123-45-6789.")
logger.warning("Token authorization: Bearer abc123DEF456")
```

## 4. Using Sensitive Value Masking
The library allows you to redact sensitive values in log messages based on user-defined patterns.

### Example of Redacting Sensitive Values

When logging a message, the logger will automatically mask sensitive data in accordance with the defined patterns.

Example Input:

```python
logger.info("User credit card: 1234567812345678.")
logger.info("User SSN: 123-45-6789.")
logger.info("Token authorization: Bearer abc123DEF456")
```

Example Output:

```bash
2024-12-01 10:00:00 - __main__ - INFO - [trace_id: c0095715-d5bb-4991-9176-c5335368e481] [function: get_user_info] User credit card: **************78
2024-12-01 10:00:01 - __main__ - INFO - [trace_id: c0095715-d5bb-4991-9176-c5335368e481] [function: get_user_info] User SSN: ***-**-**89
2024-12-01 10:00:02 - __main__ - INFO - [trace_id: c0095715-d5bb-4991-9176-c5335368e481] [function: get_user_info] Token authorization: Bearer ********56
```

### Customizing the Masking Behavior
You can control how many characters should remain visible after masking the sensitive data by using the show_last option. By default, it will mask the entire sensitive value, but you can customize it like this:

```python
# Mask with 2 visible characters after the mask
logger = get_logger(__name__, sensitive_patterns=sensitive_patterns, show_last=2)
```

## 5. FastAPI Integration
The library works seamlessly with FastAPI. You can use TraceIDMiddleware to add trace IDs to every request and pass them along with the logs.

### a. FastAPI Middleware
The middleware captures the trace ID from the request headers or generates a new one and passes it to the logger.

```python
# Add TraceIDMiddleware to FastAPI
app.add_middleware(TraceIDMiddleware)
```

### b. Using Trace ID in FastAPI Endpoints
When defining your FastAPI endpoints, you can easily include the trace ID by using Depends(get_trace_id).

```python
@app.get("/")
def say_hello(name: str = "Dev", trace_id: UUID = Depends(get_trace_id)):
    logger.debug("This is debug level log.")
    logger.info("This is info level log.")
    logger.error("This is error level log.")
    logger.warning("This is warning level log.")
    return {"Message": f"Hello {name}"}
```

## 6. Example Output

### Example Log Messages
When logging messages with sensitive data, the library will mask sensitive parts of the values based on the configured patterns.

```bash
2024-12-01 10:00:00 - __main__ - INFO - User credit card: ****************
2024-12-01 10:00:01 - __main__ - INFO - User SSN: ***-**-6789
2024-12-01 10:00:02 - __main__ - INFO - Token authorization: Bearer **********
```

## 7. Configuration Options
### a. Logging Level Configuration
The logging level can be configured using the configure_logging function.

```python
configure_logging(level="debug")
```

The available logging levels are:

* `DEBUG`
* `INFO`
* `WARNING`
* `ERROR`
* `CRITICAL`

### b. Sensitive Data Masking Patterns
You can provide a list of regular expressions or exact strings for sensitive data. Here are some examples:

* `r"\d{16}"`: Match credit card numbers.
* `r"(?:\d{3}-\d{2}-\d{4})"`: Match SSNs.
* `"User"`: Match the text "User".
* `r"(?<=Bearer\s)[a-zA-Z0-9]+"`: Match tokens (e.g., Bearer tokens).

### c. `show_last` Option
This option determines how many characters should remain visible after masking. The default is 0, which means the entire value is masked.

```python
logger = get_logger(__name__, sensitive_patterns=sensitive_patterns, show_last=2)
```

## 8. Conclusion
The SecureLogs Library simplifies logging with trace ID support and provides powerful features to mask sensitive data in logs. With easy integration into FastAPI, this library ensures that sensitive data like credit card numbers, SSNs, and tokens are securely hidden while providing useful trace information.

By using this library, you can ensure your application’s logs are secure, readable, and traceable.

## 9. Example Implementation
```python
from uuid import UUID

from fastapi import Depends, FastAPI

from secure_logs import configure_logging, get_logger
from secure_logs import get_trace_id
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
```
