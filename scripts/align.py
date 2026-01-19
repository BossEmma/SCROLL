import os
import subprocess
import json
import config

class AlignmentWord:
    def __init__(self, text, start, end):
        self.text = text
        self.start = start
        self.end = end

class AlignmentResult:
    def __init__(self, words_list):
        self.words = words_list

def parse_timestamp(time_val):
    try:
        if isinstance(time_val, (int, float)):
            return float(time_val)
        # Handle "00:00:01,500" format
        h, m, s = time_val.replace(',', '.').split(':')
        return int(h) * 3600 + int(m) * 60 + float(s)
    except:
        return 0.0

def align(audio_path, text_hint=""):
    if not os.path.exists(audio_path):
        print(f"Audio not found: {audio_path}")
        return AlignmentResult([])

    abs_audio_path = os.path.abspath(audio_path)
    expected_output_file = abs_audio_path + ".json"

    command = [
        config.WHISPER_BINARY,
        "-m", config.WHISPER_MODEL,
        "-f", abs_audio_path,
        "-oj",       
        "-ml", "1"   
    ]

    try:
        subprocess.run(command, check=True, capture_output=True)

        words_list = []
        
        if os.path.exists(expected_output_file):
            with open(expected_output_file, "r", encoding="utf-8") as f:
                data = json.load(f)

            # Support different whisper.cpp JSON formats
            segments = data.get("transcription", [])
            if not segments and isinstance(data, list):
                segments = data

            for segment in segments:
                text = segment.get("text", "").strip()
                
                # Handle timestamps
                t_from = segment.get("from") or segment.get("timestamps", {}).get("from")
                t_to = segment.get("to") or segment.get("timestamps", {}).get("to")

                start = parse_timestamp(t_from)
                end = parse_timestamp(t_to)

                if text:
                    words_list.append(AlignmentWord(text, start, end))

            os.remove(expected_output_file)
            
        return AlignmentResult(words_list)

    except Exception as e:
        print(f"Error in alignment: {e}")
        return AlignmentResult([])