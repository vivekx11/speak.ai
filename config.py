"""Configuration Module for Speak.AI"""
import os
from dotenv import load_dotenv
from pathlib import Path

# Load environment variables
load_dotenv()

class Config:
    """Base configuration class"""
    # API Configuration
    GEMINI_API_KEY = os.getenv('GEMINI_API_KEY', '')
    MODEL_NAME = os.getenv('MODEL_NAME', 'gemini-pro')
    
    # Vosk Configuration
    VOSK_MODEL_PATH = os.getenv('VOSK_MODEL_PATH', './models/vosk-model-en-us-0.42-gigaspeech')
    SAMPLE_RATE = int(os.getenv('SAMPLE_RATE', 16000))
    AUDIO_DEVICE_INDEX = int(os.getenv('AUDIO_DEVICE_INDEX', 0))
    
    # TTS Configuration
    TTS_ENGINE = os.getenv('TTS_ENGINE', 'gtts')  # gtts or pyttsx3
    TTS_LANGUAGE = os.getenv('TTS_LANGUAGE', 'en-US')
    TTS_VOICE_ID = os.getenv('TTS_VOICE_ID', 'en')
    
    # Language Support
    SUPPORTED_LANGUAGES = os.getenv('SUPPORTED_LANGUAGES', 'en,hi,es,fr,de,ja').split(',')
    DEFAULT_LANGUAGE = os.getenv('DEFAULT_LANGUAGE', 'en')
    
    # Application
    DEBUG = os.getenv('DEBUG', 'False').lower() == 'true'
    LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO')
    APP_NAME = os.getenv('APP_NAME', 'Speak.AI')
    VERSION = os.getenv('VERSION', '1.0.0')
    
    # Web API
    FLASK_HOST = os.getenv('FLASK_HOST', '127.0.0.1')
    FLASK_PORT = int(os.getenv('FLASK_PORT', 5000))
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    
    # Database
    DB_TYPE = os.getenv('DB_TYPE', 'sqlite')
    DB_PATH = os.getenv('DB_PATH', './data/speak_ai.db')
    
    # Feature Flags
    ENABLE_CONVERSATION_MEMORY = os.getenv('ENABLE_CONVERSATION_MEMORY', 'True').lower() == 'true'
    MAX_CONVERSATION_LENGTH = int(os.getenv('MAX_CONVERSATION_LENGTH', 50))
    ENABLE_WEB_API = os.getenv('ENABLE_WEB_API', 'True').lower() == 'true'
    ENABLE_AUTO_SAVE = os.getenv('ENABLE_AUTO_SAVE', 'True').lower() == 'true'
    
    @staticmethod
    def validate():
        """Validate required configuration"""
        if not Config.GEMINI_API_KEY:
            raise ValueError('GEMINI_API_KEY not set in environment')
        return True
    
    @staticmethod
    def get_config_dict():
        """Get all configuration as dictionary"""
        return {
            'api_key': Config.GEMINI_API_KEY,
            'model': Config.MODEL_NAME,
            'language': Config.DEFAULT_LANGUAGE,
            'tts_engine': Config.TTS_ENGINE,
        }

if __name__ == '__main__':
    print(f'{Config.APP_NAME} v{Config.VERSION}')
    print(f'Configuration loaded successfully')
