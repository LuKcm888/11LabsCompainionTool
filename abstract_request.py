import requests
import time
import logging

from return_code import ReturnCode
from return_message import ReturnMessage

logger = logging.getLogger(__name__)


def execute(output, payload):
    response = None
    method = payload.http_method
    url = payload.base_url
    data = payload.data
    headers = payload.headers
    try:
        start_time = time.time()
        response = requests.request(method, url, json=data, headers=headers)
        end_time = time.time()
        elapsed_time_ms = (end_time - start_time) * 1000
        if response is not None:
            output.response = response
            output.return_code = ReturnCode.SUCCESS
            output.return_message = ReturnMessage.SUCCESS
            output.response_time = elapsed_time_ms
            logger.debug("execute: got response: " + str(output.return_code) + ", time:" + str(elapsed_time_ms))
    except Exception as e:
        logger.error("execute: Caught Exception: " + str(e))
        output.return_code = ReturnCode.EXCEPTION_THROWN
        output.return_message = ReturnMessage.EXCEPTION_THROWN

    return response


class BackendRequestPayload():

    def __init__(self, base_url: str, http_method, data, headers, read_timeout, request_timeout):
        self.base_url = base_url
        self.http_method = http_method
        self.data = data
        self.headers = headers
        self.read_timeout = read_timeout
        self.request_timeout = request_timeout
