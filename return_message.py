from enum import Enum


class ReturnMessage(Enum):
    SUCCESS = "Service call was successful"
    FAILURE = "Service call failed"
    EXCEPTION_THROWN = "An exception was thrown."
    INVALID_BACKEND_RESPONSE = "Invalid response"
    UNABLE_PROCESS_RESULT = "Failed to process response"
    MISSING_INPUTS = "Missing INPUT parameters"
    MISSING_OUTPUTS = "Missing OUTPUT parameters"
    BACKEND_FAILURE_RESPONSE = "Backend is unavailable"
    UNABLE_TO_AUTHENTICATE = "Could not authenticate"
