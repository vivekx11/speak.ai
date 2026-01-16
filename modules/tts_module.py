"""Text-to-Speech Module"""
from gtts import gTTS
import pyttsx3
from config import Config
import os
import logging
from datetime import datetime
import hashlib

logger = logging.getLogger(__name__)

class TTSModule:
    """Handle Text-to-Speech conversion"""
    
    def __init__(self):
        """Initialize TTS Module"""
        self.engine = Config.TTS_ENGINE
        self.default_lang = Config.DEFAULT_LANGUAGE
        self.audio_dir = 'static/audio'
        
        # Create audio directory if it doesn't exist
        os.makedirs(self.audio_dir, exist_ok=True)
        
        # Initialize pyttsx3 if selected
        if self.engine == 'pyttsx3':
            self.tts_engine = pyttsx3.init()
            self.tts_engine.setProperty('rate', 150)
            logger.info('pyttsx3 engine initialized')
        
        logger.info('TTS Module initialized')
    
    def text_to_speech(self, text, language=None):
        """Convert text to speech
        
        Args:
            text (str): Text to convert
            language (str): Language code (en, hi, es, etc.)
            
        Returns:
            str: URL/path to audio file
        """
        try:
            if not text or len(text.strip()) == 0:
                logger.warning('Empty text provided for TTS')
                return None
            
            if language is None:
                language = self.default_lang
            
            # Generate filename based on text hash
            text_hash = hashlib.md5(text.encode()).hexdigest()[:8]
            filename = f'{self.audio_dir}/response_{text_hash}_{datetime.now().timestamp()}.mp3'
            
            if self.engine == 'gtts':
                return self._gtts_convert(text, language, filename)
            elif self.engine == 'pyttsx3':
                return self._pyttsx3_convert(text, filename)
            else:
                logger.error(f'Unknown TTS engine: {self.engine}')
                return None
        
        except Exception as e:
            logger.error(f'Error in TTS: {str(e)}')
            return None
    
    def _gtts_convert(self, text, language, filename):
        """Convert using Google Text-to-Speech"""
        try:
            # Map language codes
            lang_map = {
                'en': 'en',
                'hi': 'hi',
                'es': 'es',
                'fr': 'fr',
                'de': 'de',
                'ja': 'ja'
            }
            
            lang_code = lang_map.get(language[:2], 'en')
            tts = gTTS(text=text, lang=lang_code, slow=False)
            tts.save(filename)
            
            logger.info(f'Audio generated: {filename}')
            return f'/{filename}'
        
        except Exception as e:
            logger.error(f'gTTS error: {e}')
            return None
    
    def _pyttsx3_convert(self, text, filename):
        """Convert using pyttsx3"""
        try:
            self.tts_engine.save_to_file(text, filename)
            self.tts_engine.runAndWait()
            
            logger.info(f'Audio generated: {filename}')
            return f'/{filename}'
        
        except Exception as e:
            logger.error(f'pyttsx3 error: {e}')
            return None
    
    def get_supported_languages(self):
        """Get list of supported languages"""
        return Config.SUPPORTED_LANGUAGES
    
    def set_language(self, language):
        """Set default language"""
        if language in Config.SUPPORTED_LANGUAGES:
            self.default_lang = language
            return True
        return False

if __name__ == '__main__':
    tts = TTSModule()
    url = tts.text_to_speech('Hello, this is a test message', 'en')
    print(f'Audio saved at: {url}')
