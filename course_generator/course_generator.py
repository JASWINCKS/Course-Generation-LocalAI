from typing import List, Dict
import json
import time
from datetime import timedelta
from .config import Config
from .local_llm import LocalLLM

class CourseGenerator:
    def __init__(self, model_name: str = "llama2", host_type: str = "ollama"):
        """Initialize the course generator with local LLM."""
        self.llm = LocalLLM(model_name=model_name, host_type=host_type)
        self.timing_metrics = {
            "total_time": 0,
            "initial_generation": 0,
            "section_generation": 0,
            "api_calls": 0
        }

    def generate_course_content(self, segments: List[Dict]) -> Dict:
        """Generate course content from transcription segments."""
        return self.llm.generate_course_content(segments) 