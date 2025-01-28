from abc import ABC


class AbstractDTOOutput(ABC):
    """Abstract base for data transfer object output classes."""

    def __init__(self, return_code, return_message, response_time):
        self.return_code = return_code
        self.return_message = return_message
        self.response_time = response_time
