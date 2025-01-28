from abstract_dtooutput import AbstractDTOOutput


class TTSOutput(AbstractDTOOutput):
    """Data class for TTS output (extends AbstractDTOOutput)."""

    def __init__(self, response, return_code, return_message, response_time):
        super().__init__(return_code, return_message, response_time)
        self.response = response
