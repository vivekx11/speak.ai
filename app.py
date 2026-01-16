"""Main Flask Application for Speak.AI Web Interface"""
from flask import Flask, render_template, request, jsonify
from flask_cors import CORS
import logging
from config import Config
from datetime import datetime
import os
import json

# Initialize Flask app
app = Flask(__name__, 
            template_folder='templates',
            static_folder='static')
CORS(app)

# Configure logging
logging.basicConfig(level=Config.LOG_LEVEL)
logger = logging.getLogger(__name__)

# Conversation history
conversation_history = []
max_history = Config.MAX_CONVERSATION_LENGTH

# Initialize modules (lazy loading)
ai_module = None
tts_module = None

def init_modules():
    """Initialize AI and TTS modules"""
    global ai_module, tts_module
    try:
        from modules.ai_module import AIModule
        from modules.tts_module import TTSModule
        
        Config.validate()
        ai_module = AIModule()
        tts_module = TTSModule()
        logger.info(f'{Config.APP_NAME} v{Config.VERSION} started')
    except Exception as e:
        logger.error(f'Module initialization error: {e}')

@app.before_request
def before_request():
    """Initialize modules before first request"""
    if ai_module is None:
        init_modules()

@app.route('/')
def index():
    """Serve main page"""
    return render_template('index.html')

@app.route('/api/chat', methods=['POST'])
def chat():
    """Handle user chat messages"""
    try:
        data = request.json
        user_message = data.get('message', '').strip()
        language = data.get('language', Config.DEFAULT_LANGUAGE)
        
        if not user_message:
            return jsonify({'error': 'Empty message'}), 400
        
        if not ai_module:
            return jsonify({'error': 'AI module not initialized'}), 500
        
        # Get AI response
        ai_response = ai_module.generate_response(user_message)
        
        # Generate speech
        audio_url = None
        if tts_module:
            audio_url = tts_module.text_to_speech(ai_response, language)
        
        # Store conversation
        if Config.ENABLE_CONVERSATION_MEMORY:
            conversation_history.append({
                'timestamp': datetime.now().isoformat(),
                'user': user_message,
                'ai': ai_response,
                'language': language
            })
            # Keep history size manageable
            if len(conversation_history) > max_history:
                conversation_history.pop(0)
        
        return jsonify({
            'response': ai_response,
            'audio_url': audio_url,
            'language': language,
            'timestamp': datetime.now().isoformat()
        })
    
    except Exception as e:
        logger.error(f'Error in chat: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/speech-to-text', methods=['POST'])
def speech_to_text():
    """Convert speech to text using Vosk"""
    try:
        audio_data = request.files.get('audio')
        if not audio_data:
            return jsonify({'error': 'No audio provided'}), 400
        
        if not ai_module:
            return jsonify({'error': 'AI module not initialized'}), 500
        
        # Process audio (placeholder for actual STT)
        text = ai_module.vosk_stt(audio_data)
        
        if not text:
            return jsonify({'error': 'Could not process audio'}), 400
        
        return jsonify({'text': text})
    
    except Exception as e:
        logger.error(f'Error in STT: {str(e)}')
        return jsonify({'error': str(e)}), 500

@app.route('/api/config', methods=['GET'])
def get_config():
    """Get application configuration"""
    return jsonify({
        'app_name': Config.APP_NAME,
        'version': Config.VERSION,
        'languages': Config.SUPPORTED_LANGUAGES,
        'default_language': Config.DEFAULT_LANGUAGE,
        'tts_engine': Config.TTS_ENGINE,
        'enable_memory': Config.ENABLE_CONVERSATION_MEMORY
    })

@app.route('/api/history', methods=['GET'])
def get_history():
    """Get conversation history"""
    limit = request.args.get('limit', 50, type=int)
    return jsonify({
        'history': conversation_history[-limit:],
        'total': len(conversation_history)
    })

@app.route('/api/clear-history', methods=['POST'])
def clear_history():
    """Clear conversation history"""
    global conversation_history
    conversation_history = []
    return jsonify({'message': 'History cleared', 'status': 'success'})

@app.route('/api/health', methods=['GET'])
def health_check():
    """Health check endpoint"""
    return jsonify({
        'status': 'healthy',
        'app': Config.APP_NAME,
        'version': Config.VERSION,
        'timestamp': datetime.now().isoformat()
    })

@app.errorhandler(404)
def not_found(error):
    return jsonify({'error': 'Not found'}), 404

@app.errorhandler(500)
def server_error(error):
    logger.error(f'Server error: {error}')
    return jsonify({'error': 'Server error'}), 500

if __name__ == '__main__':
    init_modules()
    app.run(
        host=Config.FLASK_HOST,
        port=Config.FLASK_PORT,
        debug=Config.DEBUG
    )
