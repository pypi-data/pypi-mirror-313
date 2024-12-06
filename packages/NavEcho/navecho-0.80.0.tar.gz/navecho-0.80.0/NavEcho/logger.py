import logging
import configparser
import httpx  # For asynchronous HTTP requests
import os
import traceback
from functools import wraps
from datetime import datetime

class NavEcho:
    def __init__(self, config_file='config.ini'):
        """Initialize the ErrorLogger by reading configuration settings from config.ini."""
        # Read the config file
        config = configparser.ConfigParser()
        if not os.path.exists(config_file):
            raise FileNotFoundError("Configuration file not found.")
        config.read(config_file)

        # Validate necessary configuration
        if 'DEFAULT' not in config or 'apm_baseurl' not in config['DEFAULT'] or 'api_endpoint' not in config['DEFAULT']:
            raise ValueError("Configuration file is missing required settings.")

        # Set the API base URL and endpoint for logging
        self.api_base_url = config['DEFAULT']['apm_baseurl']  # Base URL of your API
        self.api_endpoint = config['DEFAULT']['api_endpoint']  # Endpoint for logging
        self.app_name = config['DEFAULT'].get('apm_app_name', 'UnknownApp')  # Application Name
        self.app_type = config['DEFAULT'].get('apm_app_type', 'UnknownType')
        self.user_id = config['DEFAULT'].get('user_id', 0)

        # Form the full API URL once and store it
        self.api_url = self.form_api_url()  # Store the formatted API URL

        # Configure the logger
        self.logger = logging.getLogger('ErrorLogger')
        self.logger.setLevel(logging.DEBUG)  # Set the logging level to the lowest to capture all

        # Console handler for debugging purposes
        console_handler = logging.StreamHandler()
        console_handler.setLevel(logging.DEBUG)
        console_formatter = logging.Formatter('%(asctime)s %(levelname)s: %(message)s')
        console_handler.setFormatter(console_formatter)
        self.logger.addHandler(console_handler)

    async def log(self, message: str, log_level: str = 'INFO', exception: Exception = None, status_code: int = 200, response_time: float = None):
        """
        Log a message with the specified log level, status code, and send it to the API.
        If an exception is provided, the stack trace will be included in the log.
        """
        log_level = log_level.upper()
        if log_level not in ['DEBUG', 'INFO', 'WARN', 'ERROR', 'FATAL']:
            raise ValueError(f"Invalid log level: {log_level}")

        # Get stack trace if exception is provided
        stack_trace = self._get_stack_trace(exception) if exception else None

        # Format log data for sending to the API
        log_data = self._format_log_data({
            "log_level": log_level,    # Log level (DEBUG, INFO, WARN, ERROR, FATAL)
            "message": message,       # Custom message or exception message
            "stack_trace": stack_trace,  # Full stack trace if exception is provided
            "category": "General",
            "status_code": status_code,  # HTTP status code
            "response_time": response_time  # Response time of API call
        })

        log_func = getattr(self.logger, log_level.lower(), self.logger.info)
        log_func(f"{log_level}: {message} {f'- Exception: {exception}' if exception else ''} - Status Code: {status_code} - Response Time: {response_time}ms")

        await self._send_logs_to_api(log_data)

    async def log_debug(self, message: str, status_code: int = 200, response_time: float = None):
        """Log a DEBUG message."""
        await self.log(message, log_level='DEBUG', status_code=status_code, response_time=response_time)

    async def log_info(self, message: str, status_code: int = 200, response_time: float = None):
        """Log an INFO message."""
        await self.log(message, log_level='INFO', status_code=status_code, response_time=response_time)

    async def log_warn(self, message: str, status_code: int = 400, response_time: float = None):
        """Log a WARN message."""
        await self.log(message, log_level='WARN', status_code=status_code, response_time=response_time)

    async def log_error(self, message: str, exception: Exception = None, status_code: int = 500, response_time: float = None):
        """Log an ERROR message with an optional exception, status code, and response time."""
        await self.log(message, log_level='ERROR', exception=exception, status_code=status_code, response_time=response_time)

    async def log_fatal(self, message: str, exception: Exception = None, status_code: int = 500, response_time: float = None):
        """Log a FATAL message with an optional exception, status code, and response time."""
        await self.log(message, log_level='FATAL', exception=exception, status_code=status_code, response_time=response_time)

    def _format_log_data(self, log):
        """Format the log data to be sent to the API."""
        timestamp = datetime.now().isoformat()  # ISO 8601 formatted timestamp
        return {
            "app_name": self.app_name,
            "app_type": self.app_type,
            "user_id": self.user_id,
            "category": log.get('category', 'General'),
            "category_description": log.get('category_description', ''),
            "exception_details": log.get('exception_details', ''),
            "message": log.get('message', ''),
            "exp_object": log.get('exp_object', ''),
            "exp_process": log.get('exp_process', ''),
            "inner_exception": log.get('inner_exception', ''),
            "stack_trace": log.get('stack_trace', ''),  # Full stack trace
            "timestamp": timestamp,
            "log_level": log.get('log_level', 'INFO').upper(),
            "category_id": log.get('category_id', 1),
            "status_code": log.get('status_code', 200),
            "response_time": log.get('response_time')
        }

    def form_api_url(self):
        """Form the full API URL using the base URL and the endpoint."""
        base_url = self.api_base_url.rstrip('/')
        api_endpoint = self.api_endpoint.lstrip('/')
        return f"{base_url}/{api_endpoint}"

    async def _send_logs_to_api(self, log_data):
        """Send the logs to the specified API endpoint asynchronously."""
        async with httpx.AsyncClient() as client:
            try:
                response = await client.post(self.api_url, json=log_data, headers={"Content-Type": "application/json"})
                if response.status_code != 200:
                    self.logger.error(f"Error response from API: {response.text}")
                response.raise_for_status()
                self.logger.info("Logs successfully sent to API.")
            except httpx.RequestError as e:
                self.logger.error(f"Failed to send logs to API: {e}")

    def _get_stack_trace(self, exception):
        """Return the full stack trace without truncation."""
        return ''.join(traceback.format_exception(type(exception), exception, exception.__traceback__))

def capture_exception(logger_instance):
    """A decorator to automatically capture and log exceptions in functions asynchronously."""
    def decorator(func):
        @wraps(func)
        async def wrapper(*args, **kwargs):
            try:
                return await func(*args, **kwargs)
            except Exception as e:
                # Prepare exception details to log
                exception_details = str(e) if str(e) else "No details provided"

                # Log the exception using the provided logger instance with a default status code of 500
                await logger_instance.log_error(f"Exception occurred in {func.__name__}", exception=exception_details, status_code=500)

                # Re-raise the exception to ensure the original application can handle it
                raise
        return wrapper
    return decorator
