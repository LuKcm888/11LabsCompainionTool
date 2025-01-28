import logging
from abstract_request import execute, BackendRequestPayload
from oldstuff.http_method import HttpMethod
from return_code import ReturnCode
from return_message import ReturnMessage
from tts_output import TTSOutput
from config import load_config

logger = logging.getLogger(__name__)

try:
    CONFIG = load_config()
    API_URL = CONFIG['api'].get('base_url', 'https://api.elevenlabs.io/v1/text-to-speech/')
    READ_TIMEOUT = CONFIG['api'].get('read_timeout', 1000)
    REQUEST_TIMEOUT = CONFIG['api'].get('request_timeout', 3000)
    HEADERS = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": CONFIG['api'].get('xi_api_key', '')
    }
except Exception as e:
    logger.exception("Failed to load config in text_to_speech_api.py: %s", e)
    # Provide defaults
    API_URL = "https://api.elevenlabs.io/v1/text-to-speech/"
    READ_TIMEOUT = 1000
    REQUEST_TIMEOUT = 3000
    HEADERS = {
        "Accept": "audio/mpeg",
        "Content-Type": "application/json",
        "xi-api-key": ""
    }

def generate_tts(tts_input):
    """Generate text-to-speech audio using the ElevenLabs API."""
    logger.info("generate_tts: Entering method")

    output = TTSOutput(None, ReturnCode.FAILURE, "fail", "0")

    if not validate_tts_input(tts_input):
        output.return_code = ReturnCode.MISSING_INPUTS
        output.return_message = ReturnMessage.MISSING_INPUTS
        return output

    api_url = f"{API_URL}{tts_input.voice_id}"

    request_data = {
        "voice_settings": CONFIG.get('voice_settings', {}),
        "text": tts_input.text,
        "model_id": tts_input.model_id
    }

    payload = BackendRequestPayload(
        base_url=api_url,
        http_method=HttpMethod.POST.value,
        data=request_data,
        headers=HEADERS,
        read_timeout=READ_TIMEOUT,
        request_timeout=REQUEST_TIMEOUT,
    )

    try:
        response = execute(output, payload)
        if response:
            output.response = response
    except Exception as ex:
        logger.exception("Error while executing TTS request: %s", ex)
        output.return_code = ReturnCode.EXCEPTION_THROWN
        output.return_message = ReturnMessage.EXCEPTION_THROWN

    logger.info("generate_tts: Exiting method")
    return output


def validate_tts_input(tts_input):
    if tts_input is None:
        return False
    if not tts_input.model_id or not tts_input.voice_id:
        return False
    return True