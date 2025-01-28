# Text-to-Speech (TTS) Program

## Overview

This Python-based TTS (Text-to-Speech) application reads data from a CSV file, sends each row’s content to the ElevenLabs API, and saves the resulting audio files. The user can configure various settings (API key, voice settings, model, etc.) in config.yaml.

## Features

### Configurable via config.yaml:

API base URL, API key, timeouts.

Voice settings (stability, similarity boost, style).

TTS parameters (model_id, voice_id, chunk_size, output_folder).

CSV file path.

### Central Logging with setup_logging in main.py. The same log settings apply across all modules.

### Exception Handling in key areas:

CSV read errors.

API request/retry logic.

Unauthorized (401) responses terminate the program.


## Getting Started

Dependencies: Make sure you have Python 3.9+ (or a suitable version) and install:

pip install -r requirements.txt

(Adjust your environment as needed, e.g., venv or Conda.)

## Configuration:

Copy or edit config_example.yaml to match your settings.  Rename to config.yaml Notable keys:

api.base_url: The ElevenLabs text-to-speech endpoint.

api.xi_api_key: Your ElevenLabs API key.

tts.output_folder: Folder where .wav files are saved.

csv_file_path: CSV file location.

## Run the Program:

python main.py

The script processes each row in the CSV, calls ElevenLabs, and outputs .wav files.

## Project Layout

.
├── config.yaml
├── config.py
├── main.py
├── abstract_request.py
├── text_to_speech_api.py
├── tts_input.py
├── tts_output.py
├── user_output.py
├── return_message.py
├── return_code.py
├── abstract_dtooutput.py
├── utility.py
└── test_main.py

## How It Works

### main.py:

Configures logging.

Loads config.

Reads CSV rows.

Calls generate_tts from text_to_speech_api.py for each row.

Writes audio to .wav files.

### text_to_speech_api.py:

Loads voice settings from config.

Builds a request payload.

Executes request via abstract_request.execute.

Handles errors.

### abstract_request.py:

Sends HTTP request with retry.

Checks if the server responded 401 → calls sys.exit(1).

