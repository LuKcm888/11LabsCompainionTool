import logging
import time
import requests
import sys

from return_code import ReturnCode
from return_message import ReturnMessage

logger = logging.getLogger(__name__)

def execute(output, payload):
    logger.info("execute: Entering method")

    response = None
    method = payload.http_method
    url = payload.base_url
    data = payload.data
    headers = payload.headers

    attempts = 3
    backoff_seconds = 1

    for attempt in range(1, attempts + 1):
        logger.debug(f"Attempt {attempt} of {attempts} for URL: {url}")
        try:
            start_time = time.time()
            if method == "GET":
                response = requests.request(method, url, headers=headers, timeout=payload.read_timeout)
            else:
                response = requests.request(method, url, json=data, headers=headers, timeout=payload.read_timeout)
            end_time = time.time()

            elapsed_time_ms = (end_time - start_time) * 1000
            response_code = response.status_code
            logger.info("execute: received response: %s", response_code)

            if response_code == 401:
                logger.error("execute: Received 401 unauthorized. Exiting program.")
                output.return_code = ReturnCode.UNABLE_TO_AUTHENTICATE
                output.return_message = ReturnMessage.UNABLE_TO_AUTHENTICATE
                output.response_time = elapsed_time_ms
                # Terminate the entire program.
                sys.exit(1)
            else:
                if response is not None:
                    output.return_code = ReturnCode.SUCCESS
                    output.return_message = ReturnMessage.SUCCESS
                    output.response_time = elapsed_time_ms
                    logger.debug("execute: got response: %s, time: %.2fms", output.return_code, elapsed_time_ms)
            break
        except requests.exceptions.RequestException as e:
            logger.error("execute: Caught RequestException on attempt %d: %s", attempt, str(e))
            if attempt == attempts:
                output.return_code = ReturnCode.EXCEPTION_THROWN
                output.return_message = ReturnMessage.EXCEPTION_THROWN
                logger.error("execute: All retries exhausted.")
            else:
                logger.info("execute: Retrying after %s seconds...", backoff_seconds)
                time.sleep(backoff_seconds)

    logger.info("execute: Exiting method")
    return response


class BackendRequestPayload:
    """Data structure for describing an HTTP request's parameters."""
    def __init__(self, base_url: str, http_method: str, data: dict, headers: dict, read_timeout: int, request_timeout: int):
        self.base_url = base_url
        self.http_method = http_method
        self.data = data
        self.headers = headers
        self.read_timeout = read_timeout
        self.request_timeout = request_timeout