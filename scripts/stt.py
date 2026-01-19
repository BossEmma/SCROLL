import os
import subprocess
import config

def stt(audio_path):
    """
    Local Speech-to-Text using whisper.cpp.
    """
    if not os.path.exists(audio_path):
        return ""

    abs_audio_path = os.path.abspath(audio_path)
    expected_output_file = abs_audio_path + ".txt"

    command = [
        config.WHISPER_BINARY,
        "-m", config.WHISPER_MODEL,
        "-f", abs_audio_path,
        "-otxt",             
        "--no-timestamps"    
    ]

    try:
        subprocess.run(command, check=True, capture_output=True)

        if os.path.exists(expected_output_file):
            with open(expected_output_file, "r", encoding="utf-8") as f:
                transcription = f.read().strip()
            os.remove(expected_output_file)
            return transcription
        return ""

    except Exception as e:
        print(f"Error running STT: {e}")
        return ""

# Compatibility function
def speech_to_text_func(audio_file):
    return stt(audio_file)