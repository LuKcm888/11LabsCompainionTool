from abstract_dtooutput import AbstractDTOOutput


class TTSOutput(AbstractDTOOutput):
    def __init__(self, response, return_code, return_message, response_time):
        super().__init__(return_code, return_message, response_time)
        self.response = response
