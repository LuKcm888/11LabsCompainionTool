import logging
from abstract_request import execute, BackendRequestPayload
from return_code import ReturnCode
from return_message import ReturnMessage
from tts_output import TTSOutput

logger = logging.getLogger(__name__)

url = "https://api.elevenlabs.io/v1/text-to-speech/"
read_timeout = 1000
request_timeout = 3000

headers = {
    "Accept": "audio/mpeg",
    "Content-Type": "application/json",
    "xi-api-key": "07048e3ee0156f7a2d520827ece9fcf9"
}

data = {
    "voice_settings": {
        "stability": 0.5,
        "similarity_boost": 0.5
    }
}


def generate_tts(dto_input):
    logger.info("generate_tts: Entering Method")
    output = TTSOutput(None, ReturnCode.FAILURE, "fail", "0")

    if validate_generate_tts_input(dto_input):
        api_url = url + dto_input.voice_id
        data["text"] = dto_input.text
        data["model_id"] = "eleven_multilingual_v2"

        output = execute(output, BackendRequestPayload(api_url, "POST", data, headers, read_timeout, request_timeout))

    else:
        output.return_code = ReturnCode.MISSING_INPUTS
        output.return_message = ReturnMessage.MISSING_INPUTS

    return output


def validate_generate_tts_output():
    return


def validate_generate_tts_input(input):
    valid = False
    if input is not None:
        if input.model_id is not None and input.voice_id is not None:
            valid = True
    return valid
