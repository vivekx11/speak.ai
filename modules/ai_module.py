"""AI Module using Google Gemini API"""
import google.generativeai as genai
from config import Config
import logging

logger = logging.getLogger(__name__)

class AIModule:
    """Handle AI interactions using Gemini API"""
    
    def __init__(self):
        """Initialize Gemini API"""
        try:
            genai.configure(api_key=Config.GEMINI_API_KEY)
            self.model = genai.GenerativeModel(Config.MODEL_NAME)
            self.chat = self.model.start_chat(history=[])
            logger.info('AI Module initialized successfully')
        except Exception as e:
            logger.error(f'Failed to initialize AI Module: {e}')
            raise
    
    def generate_response(self, user_input, system_prompt=None):
        """Generate AI response using Gemini
        
        Args:
            user_input (str): User message
            system_prompt (str): Optional system prompt
            
        Returns:
            str: AI generated response
        """
        try:
            if not user_input or not isinstance(user_input, str):
                return "Please provide a valid message."
            
            # Create message with optional system prompt
            if system_prompt:
                full_input = f"{system_prompt}\n\nUser: {user_input}"
            else:
                full_input = user_input
            
            # Generate response
            response = self.chat.send_message(full_input)
            
            # Extract and clean response
            response_text = response.text.strip()
            logger.info(f'Generated response for: {user_input[:50]}...')
            
            return response_text
            
        except Exception as e:
            logger.error(f'Error generating response: {str(e)}')
            return "Sorry, I couldn't process that. Please try again."
    
    def vosk_stt(self, audio_data):
        """Convert speech to text using Vosk
        
        Args:
            audio_data: Audio file data
            
        Returns:
            str: Recognized text
        """
        try:
            # Placeholder for Vosk integration
            # In production, implement actual Vosk STT
            logger.info('Processing audio with Vosk')
            return "I'm listening"
        except Exception as e:
            logger.error(f'Error in STT: {str(e)}')
            return None
    
    def get_conversation_summary(self, conversation_history):
        """Get a summary of conversation
        
        Args:
            conversation_history (list): List of conversation messages
            
        Returns:
            str: Summary of conversation
        """
        try:
            messages = "\n".join([f"User: {msg['user']}\nAI: {msg['ai']}" 
                                  for msg in conversation_history[-5:]])
            
            summary_prompt = f"""Summarize this conversation briefly:
{messages}

Provide a concise 2-3 sentence summary."""
            
            response = self.model.generate_content(summary_prompt)
            return response.text
            
        except Exception as e:
            logger.error(f'Error generating summary: {e}')
            return "Unable to generate summary"

if __name__ == '__main__':
    try:
        ai = AIModule()
        response = ai.generate_response("Hello! What can you do?")
        print(response)
    except Exception as e:
        print(f'Error: {e}')
