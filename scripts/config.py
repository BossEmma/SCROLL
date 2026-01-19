import os

# Base Directory
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.dirname(BASE_DIR)

# Directories
OUTPUT_DIR = os.path.join(PROJECT_ROOT, "output")
MUSIC_DIR = os.path.join(PROJECT_ROOT, "background_music")

# Piper TTS Settings
PIPER_MODEL_PATH = os.path.join(PROJECT_ROOT, "voices/en_US-hfc_male-medium.onnx")

# Whisper.cpp Settings
WHISPER_BINARY = os.path.join(PROJECT_ROOT, "whisper.cpp/build/bin/whisper-cli")
WHISPER_MODEL = os.path.join(PROJECT_ROOT, "whisper.cpp/models/ggml-large-v3-turbo.bin")

# Check if files exist to prevent runtime errors
required_files = [PIPER_MODEL_PATH, WHISPER_BINARY, WHISPER_MODEL]
for f in required_files:
    if not os.path.exists(f):
        print(f"WARNING: Configuration file not found: {f}")