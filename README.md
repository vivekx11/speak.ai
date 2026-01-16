# 🎙️ Speak.AI - Advanced Voice-Activated AI Assistant

[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Python 3.8+](https://img.shields.io/badge/Python-3.8%2B-blue.svg)](https://www.python.org/downloads/)

An advanced voice-activated AI assistant built with Flask, Vosk STT, Google Gemini API, and multi-language text-to-speech support. Interact with AI entirely through voice in your local language, featuring real-time speech recognition, intelligent conversation, and multilingual support.

## 🌟 Features

- **Voice Input**: Real-time speech recognition using Vosk STT
- **AI Responses**: Powered by Google Gemini API for intelligent conversations
- **Multi-language Support**: Interact in English, Hindi, Spanish, French, German, and Japanese
- **Text-to-Speech**: Multiple TTS engines (gTTS and pyttsx3)
- **Web Interface**: Modern, responsive UI with chat history
- **Conversation Memory**: Automatic conversation history tracking
- **REST API**: Complete API endpoints for integration
- **Zero Dependencies**: Runs completely offline (except API calls)

## 📋 Project Structure

```
speak.ai/
├── app.py                    # Flask backend application
├── config.py                 # Configuration management
├── requirements.txt          # Python dependencies
├── .env.example             # Environment variables template
│
├── modules/
│   ├── ai_module.py         # Gemini API integration
│   ├── tts_module.py        # Text-to-speech functionality
│   └── stt_module.py        # Speech-to-text (Vosk)
│
├── templates/
│   └── index.html           # Main web interface
│
└── static/
    ├── css/
    │   └── style.css        # Modern styling
    └── js/
        └── app.js           # Frontend logic
```

## 🚀 Quick Start

### Prerequisites

- Python 3.8 or higher
- Gemini API Key (get it from [Google AI Studio](https://makersuite.google.com))
- Vosk Model (auto-downloaded)

### Installation

1. **Clone the repository**
   ```bash
   git clone https://github.com/vivekx11/speak.ai.git
   cd speak.ai
   ```

2. **Create virtual environment**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

4. **Configure environment**
   ```bash
   cp .env.example .env
   # Edit .env and add your Gemini API key
   ```

5. **Run the application**
   ```bash
   python app.py
   ```
   
   Access at `http://localhost:5000`

## 🔧 Configuration

Edit `.env` file to customize:

```env
# Gemini API
GEMINI_API_KEY=your_api_key_here
MODEL_NAME=gemini-pro

# Speech Recognition
VOSK_MODEL_PATH=./models/vosk-model-en-us-0.42-gigaspeech
SAMPLE_RATE=16000

# Text-to-Speech
TTS_ENGINE=gtts  # gtts or pyttsx3
DEFAULT_LANGUAGE=en
SUPPORTED_LANGUAGES=en,hi,es,fr,de,ja

# Web Server
FLASK_HOST=127.0.0.1
FLASK_PORT=5000
FLASK_ENV=development
```

## 🎯 API Endpoints

### POST `/api/chat`
Send a message and get AI response
```json
{
  "message": "Hello, what's the weather like?",
  "language": "en"
}
```

### GET `/api/history`
Retrieve conversation history

### POST `/api/clear-history`
Clear all conversation history

### GET `/api/config`
Get application configuration

### GET `/api/health`
Health check endpoint

## 💡 Usage Examples

### Web Interface
1. Open browser to `http://localhost:5000`
2. Select your language
3. Type or click mic button to speak
4. Get instant AI responses
5. View conversation history anytime

### REST API
```bash
curl -X POST http://localhost:5000/api/chat \
  -H "Content-Type: application/json" \
  -d '{"message": "Hello", "language": "en"}'
```

## 🔑 Supported Languages

| Code | Language |
|------|----------|
| en   | English  |
| hi   | हिंदी (Hindi) |
| es   | Español  |
| fr   | Français |
| de   | Deutsch  |
| ja   | 日本語   |

## 🛠️ Advanced Features

- **Conversation Summarization**: Get summaries of conversations
- **Custom System Prompts**: Define AI behavior
- **Audio Recording**: Direct mic input with Vosk
- **Session Management**: Per-session conversation tracking
- **Error Handling**: Robust error management and recovery

## 📦 Dependencies

- **Flask** - Web framework
- **Vosk** - Offline speech recognition
- **google-generativeai** - Gemini API client
- **gTTS/pyttsx3** - Text-to-speech engines
- **python-dotenv** - Environment configuration

## 🤝 Contributing

Contributions are welcome! Please feel free to submit a Pull Request.

## 📄 License

MIT License - see LICENSE file for details

## ⭐ Acknowledgments

- Google Gemini API for intelligent responses
- Vosk for offline speech recognition
- Flask community for excellent documentation

## 📞 Support

For issues, questions, or suggestions, please open an GitHub issue.

---

**Built with ❤️ by [vivekx11](https://github.com/vivekx11)**
