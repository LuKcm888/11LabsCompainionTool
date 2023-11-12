import logging
import yaml

from text_to_speech_api import generate_tts
from tts_input import TTSInput

# Logging to a file with a specific format
logging.basicConfig(filename='app.log', filemode='w', level=logging.DEBUG,
                    format='%(asctime)s - %(levelname)s - %(message)s')

with open('config.yaml', 'r') as f:
    config = yaml.safe_load(f)

audio_map = {}
voice_version = ""
voice_id = ""
file_extension = ".wav"
CHUNK_SIZE = 1024

for audio in audio_map:
    dto_input = TTSInput(voice_version, voice_id, audio_map[audio])
    name = audio

    output = generate_tts(dto_input)
    with open(name + '.wav', file_extension) as f:
        for chunk in output.iter_content(chunk_size=CHUNK_SIZE):
            if chunk:
                f.write(chunk)
