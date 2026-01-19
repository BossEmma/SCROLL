import tts
import assembler
import get_youtube
import align
import os
import subprocess
import json
import config
import random

def cleanup_temp_files():

    temp_files = [
        'edited_video_1080x1920.mp4',
        'TTS.wav',
        'subtitles.srt',
        'temp_video.mp4',
    ]
    # `trimmed_video.mp4` is only temporary if background music is added
    music_found = False
    if os.path.isdir(config.MUSIC_DIR):
        if any(f.endswith(('.mp3', '.wav', '.aac')) for f in os.listdir(config.MUSIC_DIR)):
            music_found = True
            
    if music_found:
        temp_files.append('trimmed_video.mp4')

    for file in temp_files:
        if os.path.exists(file):
            os.remove(file)

def create_tiktok_video():
    story = """
"""

    youtube_link = 'https://youtu.be/2VpG0WS4uCo?si=XCfICart_k6PLDzQ'
    
    try:
        os.makedirs(config.OUTPUT_DIR, exist_ok=True)
        
        # Generate a safe filename from the story title
        title = story.strip().split('\n')[0]
        safe_title = "".join([c for c in title if c.isalnum() or c.isspace()]).rstrip()
        final_video_name = f"{safe_title}.mp4"
        final_video_path = os.path.join(config.OUTPUT_DIR, final_video_name)

        print("Processing story...")

        # Step 2: Generate TTS audio
        print("Generating TTS audio...")
        audio_file = tts.tts(text, "TTS.mp3")  
        print(f"TTS audio generated: {audio_file}")

        # Get audio duration
        print("Getting audio duration...")
        result = subprocess.run(
            ['ffprobe', '-v', 'error', '-show_format', '-of', 'json', audio_file],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            raise RuntimeError(f"ffprobe failed to get duration: {result.stderr}")
        probe = json.loads(result.stdout)
        duration = float(probe['format']['duration'])

        # Step 3: Align the generated audio with the text
        print("Aligning audio with text...")
        alignment_result = align.align("TTS.wav", text)
        
        # Step 4: Generate SRT file from alignment result
        print("Creating subtitles...")
        write_srt_from_alignment(alignment_result, "subtitles.srt")

        # Step 5: Download and prepare video
        print("Downloading and preparing video...")
        get_youtubeget_video_and_prepare(youtube_link)

        # Step 6: Edit the video
        print("Editing video...")
        video_editor = assembler.editor()
        
        # Add subtitles, mix audio, and trim to duration
        video_editor.add_subtitles('subtitles.srt', 'edited_video_1080x1920.mp4', 'TTS.wav', duration)
        
        # Trim video to audio length is now done in add_subtitles
        
        # Add background music if available
        music_file = None
        if os.path.isdir(config.MUSIC_DIR):
            music_files = [f for f in os.listdir(config.MUSIC_DIR) if f.endswith(('.mp3', '.wav', '.aac'))]
            if music_files:
                music_file = os.path.join(config.MUSIC_DIR, random.choice(music_files))

        if music_file:
            print(f"Adding background music: {os.path.basename(music_file)}")
            video_editor.add_background_music('trimmed_video.mp4', music_file, final_video_path)
            print(f"Final video created: {final_video_path}")
        else:
            os.rename('trimmed_video.mp4', final_video_path)
            print(f"No background music found. Final video: {final_video_path}")
            
        print("Video creation completed successfully!")
        
    except Exception as e:
        print(f"Error occurred: {e}")
        import traceback
        traceback.print_exc()
    finally:
        # Clean up temporary files
        cleanup_temp_files()

def write_srt_from_alignment(alignment_result, srt_filename="subtitles.srt"):
    """Generate SRT subtitle file from alignment result"""
    with open(srt_filename, "w", encoding="utf-8") as f:
        for idx, word in enumerate(alignment_result.words, 1):
            start = word.start
            end = word.end
            
            def fmt(t):
                h = int(t // 3600)
                m = int((t % 3600) // 60)
                s = int(t % 60)
                ms = int((t - int(t)) * 1000)
                return f"{h:02}:{m:02}:{s:02},{ms:03}"
            
            f.write(f"{idx}\n{fmt(start)} --> {fmt(end)}\n{word.text}\n\n")

if __name__ == "__main__":
    create_tiktok_video()

