import requests
import json
from typing import Dict, List
import time
from datetime import timedelta
import os

class LocalLLM:
    def __init__(self, model_name: str = "llama2", host_type: str = "ollama"):
        """Initialize the local LLM with the specified model and host type."""
        self.model_name = model_name
        self.host_type = host_type.lower()
        
        # Configure API endpoints based on host type
        if self.host_type == "ollama":
            self.api_base = "http://localhost:11434/api"
        elif self.host_type == "lmstudio":
            self.api_base = "http://localhost:1234/v1"
        else:
            raise ValueError("host_type must be either 'ollama' or 'lmstudio'")
            
        self.timing_metrics = {
            "total_time": 0,
            "initial_generation": 0,
            "section_generation": 0,
            "api_calls": 0
        }

    def generate_response(self, prompt: str) -> str:
        """Generate a response using the local LLM API."""
        if self.host_type == "ollama":
            response = requests.post(
                f"{self.api_base}/generate",
                json={
                    "model": self.model_name,
                    "prompt": prompt,
                    "stream": False,
                    "options": {
                        "temperature": 0.7,
                        "top_p": 0.9,
                        "max_tokens": 2048
                    }
                }
            )
            return response.json()["response"]
        else:  # LM Studio
            response = requests.post(
                f"{self.api_base}/chat/completions",
                json={
                    "model": self.model_name,
                    "messages": [{"role": "user", "content": prompt}],
                    "temperature": 0.7,
                    "max_tokens": 2048
                }
            )
            return response.json()["choices"][0]["message"]["content"]

    def generate_course_content(self, segments: List[Dict]) -> Dict:
        """Generate course content from transcription segments."""
        start_time = time.time()
        self.timing_metrics["api_calls"] = 0
        
        course_content = {
            "title": "",
            "description": "",
            "objectives": [],
            "sections": []
        }

        # Generate course title, description, and objectives
        initial_start = time.time()
        initial_prompt = f"""Based on this content: {segments[0]['text'][:500]}
        Generate:
        1. A concise, engaging title
        2. A brief description
        3. 3-5 learning objectives
        
        Format the response as JSON:
        {{
            "title": "Course Title",
            "description": "Course Description",
            "objectives": ["Objective 1", "Objective 2", "Objective 3"]
        }}"""
        
        initial_response = self.generate_response(initial_prompt)
        self.timing_metrics["api_calls"] += 1
        self.timing_metrics["initial_generation"] = time.time() - initial_start
        
        try:
            # Extract JSON from response
            json_start = initial_response.find('{')
            json_end = initial_response.rfind('}') + 1
            initial_content = json.loads(initial_response[json_start:json_end])
            course_content["title"] = initial_content["title"]
            course_content["description"] = initial_content["description"]
            course_content["objectives"] = initial_content["objectives"]
        except:
            # Fallback if JSON parsing fails
            course_content["title"] = "Course Generated from Video"
            course_content["description"] = "A comprehensive course generated from video content"
            course_content["objectives"] = ["Understand the main concepts", "Apply the knowledge", "Master the skills"]

        # Process sections in batches
        section_start = time.time()
        batch_size = 2  # Process 2 sections at a time to manage memory
        for i in range(0, len(segments), batch_size):
            batch_segments = segments[i:i + batch_size]
            
            batch_prompt = f"""Generate course content for {len(batch_segments)} sections.
            For each section, provide:
            1. Structured learning content
            2. A concise summary
            3. 3 multiple choice questions
            
            Format the response as JSON:
            {{
                "sections": [
                    {{
                        "content": "Structured content here",
                        "summary": "Summary here",
                        "quiz": [
                            {{
                                "question": "Question text",
                                "options": ["Option 1", "Option 2", "Option 3", "Option 4"],
                                "correct_answer": "Option 1"
                            }}
                        ]
                    }}
                ]
            }}
            
            Section contents:
            {json.dumps([{"title": s["title"], "text": s["text"]} for s in batch_segments])}"""
            
            batch_response = self.generate_response(batch_prompt)
            self.timing_metrics["api_calls"] += 1
            
            try:
                # Extract JSON from response
                json_start = batch_response.find('{')
                json_end = batch_response.rfind('}') + 1
                batch_content = json.loads(batch_response[json_start:json_end])
                for j, section_content in enumerate(batch_content["sections"]):
                    section = {
                        "title": batch_segments[j]["title"],
                        "content": section_content["content"],
                        "summary": section_content["summary"],
                        "quiz": section_content["quiz"]
                    }
                    course_content["sections"].append(section)
            except:
                # Fallback if JSON parsing fails
                for segment in batch_segments:
                    section = {
                        "title": segment["title"],
                        "content": segment["text"],
                        "summary": "Summary not available",
                        "quiz": [{
                            "question": "Error generating quiz questions",
                            "options": ["Please try again", "Contact support", "Check the content", "Review the section"],
                            "correct_answer": "Please try again"
                        }]
                    }
                    course_content["sections"].append(section)
        
        self.timing_metrics["section_generation"] = time.time() - section_start
        self.timing_metrics["total_time"] = time.time() - start_time
        
        # Add timing information to course content
        course_content["generation_metrics"] = {
            "total_time": str(timedelta(seconds=int(self.timing_metrics["total_time"]))),
            "initial_generation": str(timedelta(seconds=int(self.timing_metrics["initial_generation"]))),
            "section_generation": str(timedelta(seconds=int(self.timing_metrics["section_generation"]))),
            "total_api_calls": self.timing_metrics["api_calls"],
            "sections_processed": len(segments),
            "average_time_per_section": str(timedelta(seconds=int(self.timing_metrics["section_generation"] / len(segments))))
        }

        return course_content 