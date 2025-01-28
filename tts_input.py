class TTSInput:
    """Data class for TTS input parameters."""
    def __init__(self, model_id, voice_id, text):
        self.model_id = model_id
        self.voice_id = voice_id
        self.text = text