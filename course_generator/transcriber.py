import whisper
import os
from typing import Dict, List
from .config import Config

class Transcriber:
    def __init__(self, model_size: str = None):
        """Initialize the transcriber with specified model size."""
        self.model = whisper.load_model(model_size or Config.DEFAULT_WHISPER_MODEL)

    def transcribe(self, audio_path: str) -> Dict:
        """Transcribe audio file and return the transcription result."""
        result = self.model.transcribe(audio_path)
        return result

    def segment_transcription(self, transcription: Dict) -> List[Dict]:
        """Segment the transcription into logical sections."""
        segments = []
        current_section = {
            "start": 0,
            "end": 0,
            "text": "",
            "title": ""
        }
        
        for segment in transcription["segments"]:
            # If there's a significant pause (more than 2 seconds) or
            # the segment is longer than 30 seconds, create a new section
            if (segment["start"] - current_section["end"] > 2 or
                segment["end"] - current_section["start"] > 30):
                if current_section["text"]:
                    segments.append(current_section)
                current_section = {
                    "start": segment["start"],
                    "end": segment["end"],
                    "text": segment["text"],
                    "title": f"Section {len(segments) + 1}"
                }
            else:
                current_section["end"] = segment["end"]
                current_section["text"] += " " + segment["text"]
        
        if current_section["text"]:
            segments.append(current_section)
            
        return segments 