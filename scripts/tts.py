import wave
import os
from piper import PiperVoice
import config

# Load the model strictly once
try:
    voice = PiperVoice.load(config.PIPER_MODEL_PATH)
    print(f"Loaded Voice Model: {config.PIPER_MODEL_PATH}")
except Exception as e:
    print(f"Failed to load Piper model: {e}")
    voice = None

def tts(text, filename="output.wav"):
    """
    Synthesizes text to speech using Piper.
    Forces .wav extension.
    """
    if voice is None:
        raise Exception("TTS Model not loaded.")

    # Force WAV extension
    base_name = os.path.splitext(filename)[0]
    wav_filename = base_name + ".wav"

    try:
        with wave.open(wav_filename, "wb") as wav_file:
            voice.synthesize_wav(text, wav_file)
        return wav_filename
    except Exception as e:
        print(f"Error in TTS: {e}")
        return None