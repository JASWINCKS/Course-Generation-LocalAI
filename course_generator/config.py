import os
from dotenv import load_dotenv
from typing import Optional

# Load environment variables from .env file
load_dotenv()

class Config:
    """Configuration class to handle environment variables."""
    
    # LLM Host Configuration
    DEFAULT_LLM_HOST: str = os.getenv("DEFAULT_LLM_HOST", "ollama")
    DEFAULT_LLM_MODEL: str = os.getenv("DEFAULT_LLM_MODEL", "mistral")
    
    # AssemblyAI Configuration (Optional)
    ASSEMBLYAI_API_KEY: Optional[str] = os.getenv("ASSEMBLYAI_API_KEY")
    
    # YouTube API Configuration (Optional)
    YOUTUBE_API_KEY: Optional[str] = os.getenv("YOUTUBE_API_KEY")
    
    # Application Settings
    DEBUG: bool = os.getenv("DEBUG", "False").lower() == "true"
    LOG_LEVEL: str = os.getenv("LOG_LEVEL", "INFO")
    
    # Output Settings
    OUTPUT_DIR: str = os.getenv("OUTPUT_DIR", "output")
    TEMP_DIR: str = os.getenv("TEMP_DIR", "temp")
    
    # Model Settings
    DEFAULT_WHISPER_MODEL: str = os.getenv("DEFAULT_WHISPER_MODEL", "base")
    
    # Export Settings
    DEFAULT_EXPORT_FORMAT: str = os.getenv("DEFAULT_EXPORT_FORMAT", "PDF")
    
    @classmethod
    def validate(cls) -> bool:
        """Validate that all required environment variables are set."""
        # No required API keys for local operation
        return True
    
    @classmethod
    def setup(cls):
        """Set up the configuration and create necessary directories."""
        # Create output and temp directories if they don't exist
        os.makedirs(cls.OUTPUT_DIR, exist_ok=True)
        os.makedirs(cls.TEMP_DIR, exist_ok=True)
        
        # Validate configuration
        cls.validate()
        
        return cls 