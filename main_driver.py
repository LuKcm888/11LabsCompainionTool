import logging
import os
import pandas as pd

from text_to_speech_api import generate_tts
from tts_input import TTSInput
from config import load_config


################################
# Central logging setup function
################################
def setup_logging(log_level=logging.INFO):
    logger = logging.getLogger()
    logger.setLevel(log_level)

    # Clear existing handlers to avoid duplication
    if logger.hasHandlers():
        logger.handlers.clear()

    file_handler = logging.FileHandler('app.log', mode='w')
    file_handler.setLevel(logging.DEBUG)
    file_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    file_handler.setFormatter(file_formatter)

    console_handler = logging.StreamHandler()
    console_handler.setLevel(logging.DEBUG)
    console_formatter = logging.Formatter('%(asctime)s - %(levelname)s - %(message)s')
    console_handler.setFormatter(console_formatter)

    logger.addHandler(file_handler)
    logger.addHandler(console_handler)


# Get module-level logger after setup
logger = logging.getLogger(__name__)


def main():
    """Main entry point of the application."""
    setup_logging()

    try:
        config = load_config()
        if not config:
            logger.warning("Empty or invalid config. Aborting.")
            return

        csv_file_path = config.get('csv_file_path', 'sub_en.csv')
        if not os.path.exists(csv_file_path):
            logger.error("CSV file not found: %s", csv_file_path)
            return

        try:
            df = pd.read_csv(csv_file_path)
        except Exception as csv_err:
            logger.exception("Failed to read CSV: %s", csv_err)
            return

        folder_name = config['tts'].get('output_folder', 'Dude')
        chunk_size = config['tts'].get('chunk_size', 1024)

        os.makedirs(folder_name, exist_ok=True)

        for _, row in df.iterrows():
            model_id = config['tts'].get('model_id', 'eleven_multilingual_v2')
            voice_id = config['tts'].get('voice_id', 'BAD6xWTKPpgU6HnIIs1I')
            text = row.get('Dialogue', '')

            tts_input = TTSInput(
                model_id=model_id,
                voice_id=voice_id,
                text=text
            )

            file_name = f"{row.get('Key', 'unknown_key')}.wav"
            output_file_path = os.path.join(folder_name, file_name)

            logger.info("Generating TTS for: %s", output_file_path)
            try:
                tts_output = generate_tts(tts_input)
            except Exception as tts_err:
                logger.exception("Failed to generate TTS for %s: %s", output_file_path, tts_err)
                continue

            if tts_output and tts_output.response:
                with open(output_file_path, 'wb') as f:
                    for chunk in tts_output.response.iter_content(chunk_size=chunk_size):
                        if chunk:
                            f.write(chunk)
                logger.info("Successfully generated: %s", output_file_path)
            else:
                logger.error("Failed to generate TTS for: %s", output_file_path)
    except Exception as e:
        logger.exception("Unexpected error in main: %s", e)


if __name__ == "__main__":
    main()
