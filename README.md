# SCROLL

SCROLL is an automated content creation tool designed to generate viral-style vertical videos (TikToks, Shorts, Reels) from text stories. It streamlines the entire production process by handling text-to-speech, video sourcing, subtitle generation, and editing.

## 🚀 Features

- **Text-to-Speech (TTS)**: Uses Piper TTS to generate high-quality voiceovers from your text.
- **Automatic Subtitles**: Leverages high-precision alignment (via Whisper) to generate perfectly timed subtitles.
- **Background Video**: Automatically downloads satisfying background footage (e.g., Minecraft parkour) from YouTube.
- **Smart Editing**: Crops videos to vertical (9:16) format, aligns video length with audio, and mixes everything together.
- **Background Music**: Supports adding random background tracks from a music directory.

## 🛠️ Installation

### Prerequisites

- Python 3.8+
- [FFmpeg](https://ffmpeg.org/download.html) (Added to system PATH)
- [Whisper.cpp](https://github.com/ggerganov/whisper.cpp)
- [Piper TTS](https://github.com/rhasspy/piper)

### Setup

1. **Clone the repository**:

    ```bash
    git clone https://github.com/yourusername/SCROLL.git
    cd SCROLL
    ```

2. **Install Python Dependencies**:

    ```bash
    pip install -r requirements.txt
    ```

## 🐳 Docker Usage (Recommended)

The project includes a Dockerfile to handle all dependencies automatically.

1. **Build the image**:

    ```bash
    docker build -t scroll .
    ```

2. **Run the container**:

    ```bash
    docker run -v $(pwd)/output:/output scroll
    ```

## 📖 Usage

1. **Prepare your story**:
    Currently, the story text is configured within `scripts/main.py` (see the `create_tiktok_video` function).

2. **Add Background Music**:
    Place `.mp3` or `.wav` files in the `background_music/` directory (create it if it doesn't exist).

3. **Run the generator**:

    ```bash
    python scripts/main.py
    ```

4. **Find your video**:
    The final video will be saved in the `output/` directory.

## 📂 Project Structure

- `scripts/main.py`: Main entry point and orchestration.
- `scripts/tts.py`: Handles Text-to-Speech generation.
- `scripts/align.py`: Aligns audio with text for subtitles.
- `scripts/get_youtube.py`: Downloads and processes background videos.
- `scripts/assembler.py`: Combines audio, video, and subtitles.
