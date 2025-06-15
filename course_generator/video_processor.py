import os
import yt_dlp
from moviepy.editor import VideoFileClip
import tempfile
from .config import Config
import random
import logging

class VideoProcessor:
    def __init__(self):
        self.temp_dir = os.path.join(Config.TEMP_DIR, tempfile.mkdtemp())
        self.user_agents = [
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36',
            'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/92.0.4515.107 Safari/537.36',
            'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.124 Safari/537.36'
        ]
        self.logger = logging.getLogger(__name__)

    def download_youtube_video(self, url: str) -> str:
        """Download a YouTube video and return the local file path."""
        ydl_opts = {
            'format': 'best',  # Simple format selection
            'outtmpl': os.path.join(self.temp_dir, '%(title)s.%(ext)s'),
            'nocheckcertificate': True,
            'ignoreerrors': True,
            'no_warnings': True,
            'quiet': True,
            'http_headers': {
                'User-Agent': random.choice(self.user_agents),
                'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8',
                'Accept-Language': 'en-us,en;q=0.5',
                'Sec-Fetch-Mode': 'navigate',
            }
        }
        
        try:
            self.logger.info(f"Attempting to download video from: {url}")
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                info = ydl.extract_info(url, download=True)
                if not info:
                    raise Exception("Failed to extract video information")
                
                self.logger.info(f"Video title: {info.get('title', 'Unknown')}")
                self.logger.info("Starting download...")
                
                # Get the actual downloaded file path
                downloaded_files = [f for f in os.listdir(self.temp_dir) if f.endswith(('.mp4', '.webm', '.mkv'))]
                if not downloaded_files:
                    raise Exception("No video file was downloaded")
                
                video_path = os.path.join(self.temp_dir, downloaded_files[0])
                if not os.path.exists(video_path):
                    raise Exception(f"Downloaded file not found at {video_path}")
                
                self.logger.info(f"Successfully downloaded video to: {video_path}")
                return video_path
        except Exception as e:
            self.logger.error(f"Error downloading YouTube video: {str(e)}")
            raise Exception(f"Error downloading YouTube video: {str(e)}")

    def extract_audio(self, video_path: str) -> str:
        """Extract audio from video file."""
        try:
            video = VideoFileClip(video_path)
            audio_path = os.path.join(self.temp_dir, 'audio.wav')
            video.audio.write_audiofile(audio_path, codec='pcm_s16le')
            video.close()
            return audio_path
        except Exception as e:
            raise Exception(f"Error extracting audio: {str(e)}")

    def process_video(self, source: str) -> tuple[str, str]:
        """Process video from either YouTube URL or local file."""
        try:
            if source.startswith(('http://', 'https://')):
                video_path = self.download_youtube_video(source)
            else:
                if not os.path.exists(source):
                    raise FileNotFoundError(f"Video file not found at {source}")
                video_path = source
            
            audio_path = self.extract_audio(video_path)
            return video_path, audio_path
        except Exception as e:
            raise Exception(f"Error processing video: {str(e)}")

    def cleanup(self):
        """Clean up temporary files."""
        import shutil
        try:
            shutil.rmtree(self.temp_dir)
        except Exception as e:
            print(f"Warning: Error during cleanup: {str(e)}") 