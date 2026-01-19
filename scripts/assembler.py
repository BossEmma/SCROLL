import PIL.Image
import subprocess
from youtube_ripper import get_video_resolution
import PIL 
from PIL import Image
import json


class editor:
    def __init__(self):
        pass
    
    def add_subtitles(self, subtitle_file, video, audio_file, duration, output_path="trimmed_video.mp4"):
        
        # Mix the original video audio with TTS audio
        mix_command = [
        'ffmpeg',
        '-y',
        '-i', video,
        '-i', audio_file,
        '-filter_complex', '[0:a][1:a]amix=inputs=2:duration=first:dropout_transition=3',
        '-c:v', 'copy',
        '-c:a', 'aac',
        '-f', 'mp4',
        'temp_video.mp4'
        ]

        subprocess.run(mix_command, check=True)

        # Add subtitles and trim
        subtitle_command = [
            'ffmpeg',
            '-y',
            '-i', 'temp_video.mp4',
            '-t', str(duration),
            '-vf', f"subtitles={subtitle_file}:force_style='Alignment=10,Fontsize=24,PrimaryColour=&HFFFFFF&,OutlineColour=&H000000&'",
            '-c:v', 'libx264',
            '-preset', 'fast',
            '-crf', '23',
            '-c:a', 'copy',
            '-f', 'mp4',
            output_path
        ]

        subprocess.run(subtitle_command, check=True)

    def create_thumbnail(self):

        width, height = get_video_resolution('subtitled_video.mp4')

    
        img = PIL.Image.open('post_pic.png')
        image_width, image_height = img.size

        x = 0
        y = 960 - (image_height/2)

        print(f'Height is {height} and width is {width}')
        thumbnail_command = [
            "ffmpeg",
            '-y',
            "-i", 'subtitled_video.mp4',
            "-i", 'post_pic.png',
            "-filter_complex", f"[1:v]scale=1080:800[scaled];[0:v][scaled]overlay={x}:{y}:enable='between(t,0,0.01)'",
            "-c:v", "libx264",
            "-c:a", "copy",
            'thumbnailed_video.mp4'
        ]
        subprocess.run(thumbnail_command)


    def add_background_music(self, video_path, music_path, output_path="video_with_music.mp4", volume=0.25):
        try:
            command = [
                'ffmpeg',
                '-y',
                '-i', video_path,
                '-i', music_path,
                '-filter_complex', f"[1:a]volume={volume}[bg];[0:a][bg]amix=inputs=2:duration=first:dropout_transition=3[a]",
                '-map', '0:v',
                '-map', '[a]',
                '-c:v', 'copy',
                '-c:a', 'aac',
                '-strict', 'experimental',
                output_path
            ]
            
            result = subprocess.run(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, encoding="utf-8", errors="replace", universal_newlines=True)
            
            if result.returncode != 0:
                raise RuntimeError(f"ffmpeg failed: {result.stderr}")
            
            print(f"Background music added successfully: {output_path}")
        
        except Exception as e:
            print(f"Error: {e}")
