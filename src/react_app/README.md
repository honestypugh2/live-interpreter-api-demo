# Azure Live Interpreter - React App

A modern, real-time speech translation web application built with **React**, **TypeScript**, **Tailwind CSS**, and **Azure Speech Service**. This application provides live interpretation capabilities with support for multiple languages, automatic language detection, and neural voice synthesis.

## 🌟 Features

### Core Translation Features
- **🎙️ Real-time Speech Translation** - Continuous mode for live translation as you speak
- **🌐 Multi-Language Support** - Translate into up to 3 languages simultaneously
- **🔍 Automatic Language Detection** - Live Interpreter mode with 100+ language support
- **🎤 Neural Voice Synthesis** - High-quality text-to-speech for translated content
- **🎵 Audio Playback** - Play synthesized audio for each translation
- **📊 Translation History** - Review all past translations with timestamps

### User Experience
- **⚡ WebSocket Communication** - Real-time bidirectional communication
- **🎨 Modern UI** - Responsive design with dark mode support
- **🔄 Continuous & Single-shot Modes** - Choose between real-time or on-demand translation
- **📱 Responsive Design** - Works on desktop, tablet, and mobile devices
- **🎯 Interim Results** - See translations forming in real-time

### Technical Features
- **TypeScript** - Type-safe development
- **Tailwind CSS** - Utility-first styling
- **Vite** - Fast build tool and dev server
- **FastAPI Backend** - High-performance Python backend
- **Azure Speech Service** - Enterprise-grade speech recognition and synthesis

---

## 📋 Table of Contents

1. [Quick Start](#-quick-start)
2. [Prerequisites](#-prerequisites)
3. [Installation](#-installation)
4. [Configuration](#-configuration)
5. [Running the Application](#-running-the-application)
6. [Usage Guide](#-usage-guide)
7. [Architecture](#-architecture)
8. [API Reference](#-api-reference)
9. [Troubleshooting](#-troubleshooting)
10. [Deployment](#-deployment)

---

## 🚀 Quick Start

Get up and running in 5 minutes!

### Option 1: One-Command Startup (Recommended)

**Linux/Mac:**
```bash
cd live-interpreter-api-demo/src/react_app
./start.sh
```

**Windows:**
```cmd
cd live-interpreter-api-demo\src\react_app
start.bat
```

**Or using npm:**
```bash
cd live-interpreter-api-demo/src/react_app
npm start
```

The startup script will:
- ✅ Check all prerequisites
- ✅ Install missing dependencies
- ✅ Start backend server (http://localhost:8000)
- ✅ Start frontend server (http://localhost:5173)
- ✅ Open the app in your browser

Press `Ctrl+C` to stop all servers.

---

### Option 2: Manual Setup

If you prefer to start servers manually, follow these steps:

### 1. Prerequisites Check

```bash
# Check Node.js (v16+ required)
node --version

# Check Python (3.9+ required)
python --version

# Check npm
npm --version
```

### 2. Clone and Navigate

```bash
cd live-interpreter-api-demo/src/react_app
```

### 3. Configure Environment

Create a `.env` file in the **project root** (not in `react_app/`):

```bash
# Navigate to project root
cd ../..

# Create .env file
cat > .env << 'EOF'
# Azure Speech Service Configuration
SPEECH_KEY=your_azure_speech_key_here
SPEECH_REGION=eastus

# Translation Settings
SOURCE_LANGUAGE=en-US
TARGET_LANGUAGE=es-ES
TARGET_LANGUAGE_2=fr-FR
TARGET_LANGUAGE_3=de-DE

# Voice Settings (Neural Voices)
VOICE_NAME=en-US-JennyNeural
VOICE_EN_US=en-US-JennyNeural
VOICE_ES_ES=es-ES-ElviraNeural
VOICE_FR_FR=fr-FR-DeniseNeural
VOICE_DE_DE=de-DE-KatjaNeural

# Application Settings
ENABLE_LIVE_INTERPRETER=true
ENABLE_AUTO_DETECT=true
ENABLE_AUDIO_PLAYBACK=true
SAVE_AUDIO_FILES=false
LOG_LEVEL=INFO

# Backend Server Settings
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
CORS_ORIGINS=http://localhost:5173,http://localhost:3000
EOF
```

### 4. Install Dependencies

```bash
# Backend dependencies (from project root)
pip install -r requirements.txt

# Frontend dependencies
cd src/react_app/frontend
npm install
```

### 5. Start the Application

**Terminal 1 - Backend:**
```bash
cd src/react_app/backend
python main.py
```

**Terminal 2 - Frontend:**
```bash
cd src/react_app/frontend
npm run dev
```

### 6. Access the App

Open your browser to: **http://localhost:5173**

---

## 📦 Prerequisites

### Required Software

| Software | Version | Purpose |
|----------|---------|---------|
| **Node.js** | 16.x or higher | JavaScript runtime for frontend |
| **npm** | 8.x or higher | Package manager |
| **Python** | 3.9 or higher | Backend runtime |
| **pip** | Latest | Python package manager |

### Azure Services

- **Azure Speech Service** subscription
- Speech Service API key and region

### Get Azure Speech Service Credentials

1. Go to [Azure Portal](https://portal.azure.com)
2. Create a **Speech Service** resource
3. Navigate to **Keys and Endpoint**
4. Copy **Key 1** (or Key 2) and **Region**

---

## 🔧 Installation

### Step 1: Install Python Dependencies

From the **project root**:

```bash
pip install -r requirements.txt
```

**Key dependencies:**
- `azure-cognitiveservices-speech` - Azure Speech SDK
- `fastapi` - Web framework
- `uvicorn` - ASGI server
- `websockets` - WebSocket support
- `pydantic` - Data validation
- `python-dotenv` - Environment configuration

### Step 2: Install Frontend Dependencies

```bash
cd src/react_app/frontend
npm install
```

**Key dependencies:**
- `react` - UI framework
- `typescript` - Type safety
- `vite` - Build tool
- `tailwindcss` - Styling
- WebSocket support (built into browsers)

---

## ⚙️ Configuration

### Environment Variables

All configuration is managed through the `.env` file in the **project root**.

#### Azure Speech Service Configuration

```env
SPEECH_KEY=your_azure_speech_key
SPEECH_REGION=eastus
SPEECH_ENDPOINT=optional_custom_endpoint
```

#### Translation Settings

```env
# Default source language (ignored in Live Interpreter mode)
SOURCE_LANGUAGE=en-US

# Target languages (up to 3)
TARGET_LANGUAGE=es-ES
TARGET_LANGUAGE_2=fr-FR
TARGET_LANGUAGE_3=de-DE
```

#### Voice Settings

Configure neural voices for each language:

```env
VOICE_NAME=en-US-JennyNeural
VOICE_EN_US=en-US-JennyNeural
VOICE_EN_GB=en-GB-SoniaNeural
VOICE_ES_ES=es-ES-ElviraNeural
VOICE_ES_MX=es-MX-DaliaNeural
VOICE_FR_FR=fr-FR-DeniseNeural
VOICE_DE_DE=de-DE-KatjaNeural
VOICE_IT_IT=it-IT-ElsaNeural
VOICE_PT_BR=pt-BR-FranciscaNeural
VOICE_ZH_CN=zh-CN-XiaoxiaoNeural
VOICE_JA_JP=ja-JP-NanamiNeural
VOICE_KO_KR=ko-KR-SunHiNeural
```

#### Application Settings

```env
# Enable Live Interpreter mode (automatic language detection)
ENABLE_LIVE_INTERPRETER=true

# Enable automatic language detection
ENABLE_AUTO_DETECT=true

# Enable audio playback of translations
ENABLE_AUDIO_PLAYBACK=true

# Save audio files to disk (development only)
SAVE_AUDIO_FILES=false

# Logging level (DEBUG, INFO, WARNING, ERROR)
LOG_LEVEL=INFO
```

#### Server Settings

```env
# Backend server configuration
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000

# CORS origins (comma-separated)
CORS_ORIGINS=http://localhost:5173,http://localhost:3000,http://127.0.0.1:5173
```

### Supported Languages

#### Popular Languages

| Code | Language | Neural Voices Available |
|------|----------|------------------------|
| `en-US` | English (US) | Jenny, Guy, Aria, Davis |
| `en-GB` | English (UK) | Sonia, Ryan |
| `es-ES` | Spanish (Spain) | Elvira, Alvaro |
| `es-MX` | Spanish (Mexico) | Dalia, Jorge |
| `fr-FR` | French (France) | Denise, Henri |
| `de-DE` | German | Katja, Conrad |
| `it-IT` | Italian | Elsa, Diego |
| `pt-BR` | Portuguese (Brazil) | Francisca, Antonio |
| `zh-CN` | Chinese (Mandarin) | Xiaoxiao, Yunxi |
| `ja-JP` | Japanese | Nanami, Keita |
| `ko-KR` | Korean | SunHi, InJoon |

**100+ additional languages** supported in Live Interpreter mode with automatic detection.

---

## 🏃 Running the Application

### Development Mode

#### Option 1: Run Both Servers Manually

**Terminal 1 - Backend:**
```bash
cd src/react_app/backend
python main.py
```
Output:
```
INFO:     Started server process
INFO:     Uvicorn running on http://0.0.0.0:8000
```

**Terminal 2 - Frontend:**
```bash
cd src/react_app/frontend
npm run dev
```
Output:
```
VITE v4.x.x  ready in 500 ms

➜  Local:   http://localhost:5173/
➜  Network: http://192.168.1.x:5173/
```

#### Option 2: Use a Process Manager (tmux/screen)

```bash
# Using tmux
tmux new -s interpreter
# Window 1: Backend
cd src/react_app/backend && python main.py
# Ctrl+B, C (new window)
# Window 2: Frontend
cd src/react_app/frontend && npm run dev
```

### Production Mode

#### Backend (Production)

```bash
cd src/react_app/backend
uvicorn main:app --host 0.0.0.0 --port 8000 --workers 4
```

#### Frontend (Build & Serve)

```bash
cd src/react_app/frontend

# Build for production
npm run build

# Preview production build
npm run preview

# Or serve with a static server
npx serve -s dist -p 5173
```

---

## 📖 Usage Guide

### Basic Workflow

1. **Open the Application**
   - Navigate to `http://localhost:5173`
   - Verify "Connected" status in the UI

2. **Configure Languages**
   - Toggle **Live Interpreter** for automatic language detection
   - Select **Continuous Mode** for real-time translation
   - Choose up to 3 target languages
   - Select voice preferences for each language

3. **Start Translation**
   - Click **Start Recording** 🔴
   - Speak clearly into your microphone
   - Watch translations appear in real-time

4. **Review Results**
   - See interim results during speaking
   - View final translations with detected language
   - Play audio for each translation
   - Review translation history

5. **Stop Translation**
   - Click **Stop & Translate** ⏹️
   - Review captured translations

### Translation Modes

#### Continuous Mode (Recommended)
- **Best for:** Meetings, conferences, live events
- **Behavior:** Translations stream in real-time as you speak
- **Features:** Interim results, automatic sentence detection
- **To Enable:** Check "Continuous Mode (Real-time)"

#### Single-shot Mode
- **Best for:** Short phrases, testing, specific utterances
- **Behavior:** Records audio, then translates after stopping
- **Features:** Single complete translation per recording
- **To Enable:** Uncheck "Continuous Mode"

### Live Interpreter Mode

**What is it?**
- Automatic language detection from 100+ languages
- No need to specify source language
- Higher quality neural voices
- Personal voice support (requires Azure approval)

**When to use:**
- Multi-language environments
- Unknown source languages
- Professional interpretation scenarios

**To Enable:**
- Check "Use Live Interpreter" in configuration
- "Continuous Mode" is recommended with Live Interpreter

### Voice Selection

Each target language has multiple neural voice options:

1. **Navigate to Language Configuration**
2. **Select Target Language** from dropdown
3. **Choose Voice** from voice dropdown below language
4. Voices are labeled by gender/style (e.g., Jenny, Guy, Aria)

### Audio Playback

- Audio synthesis happens automatically for each translation
- Click **▶️ Play** button next to any translation
- Playback uses browser's native audio capabilities
- Audio quality: 16kHz PCM, converted to WAV

---

## 🏗️ Architecture

### System Overview

```
┌─────────────────┐         WebSocket          ┌──────────────────┐
│                 │  ◄─────────────────────►   │                  │
│  React Frontend │                             │  FastAPI Backend │
│   (Port 5173)   │         HTTP/REST           │   (Port 8000)    │
│                 │  ◄─────────────────────►   │                  │
└─────────────────┘                             └──────────────────┘
                                                         │
                                                         │ Azure SDK
                                                         ▼
                                                ┌──────────────────┐
                                                │   Azure Speech   │
                                                │     Service      │
                                                └──────────────────┘
```

### Directory Structure

```
react_app/
├── backend/
│   ├── __init__.py
│   └── main.py                    # FastAPI server with WebSocket
│
├── frontend/
│   ├── public/                    # Static assets
│   ├── src/
│   │   ├── components/
│   │   │   ├── AudioRecorder.tsx  # Recording controls
│   │   │   ├── ConnectionStatus.tsx
│   │   │   ├── LanguageSelector.tsx  # Multi-language config
│   │   │   └── TranslationDisplay.tsx  # Results with audio
│   │   ├── hooks/
│   │   │   └── useWebSocket.ts    # WebSocket management
│   │   ├── types/
│   │   │   └── translation.ts     # TypeScript interfaces
│   │   ├── App.tsx                # Main application
│   │   ├── App.css
│   │   ├── index.css
│   │   └── main.tsx
│   ├── index.html
│   ├── package.json
│   ├── vite.config.ts
│   ├── tailwind.config.js
│   └── tsconfig.json
│
└── README.md                      # This file
```

### Technology Stack

#### Frontend
- **React 18** - UI framework
- **TypeScript** - Type safety
- **Vite** - Build tool & dev server
- **Tailwind CSS** - Utility-first styling
- **WebSocket API** - Real-time communication

#### Backend
- **FastAPI** - Modern Python web framework
- **Uvicorn** - ASGI server
- **Azure Speech SDK** - Speech recognition & synthesis
- **WebSockets** - Bidirectional communication
- **Pydantic** - Data validation

### Communication Flow

#### WebSocket Protocol

**Client → Server Messages:**

```typescript
// Configuration
{
  type: "config",
  data: {
    use_live_interpreter: boolean,
    use_continuous_mode: boolean,
    source_language?: string,
    target_languages: string[],
    voice_preferences: Record<string, string>
  }
}

// Start recording
{
  type: "start_recording",
  data: {}
}

// Stop recording
{
  type: "stop_recording",
  data: {}
}

// Ping
{
  type: "ping",
  data: { timestamp: number }
}
```

**Server → Client Messages:**

```typescript
// Connection established
{
  type: "connected",
  data: { message: string, server_version: string }
}

// Configuration confirmed
{
  type: "config_confirmed",
  data: {
    use_live_interpreter: boolean,
    use_continuous_mode: boolean,
    source_language: string,
    target_languages: string[]
  }
}

// Interim results (continuous mode)
{
  type: "recognizing",
  data: {
    original_text: string,
    translations: Record<string, string>,
    detected_language?: string
  }
}

// Final translation result
{
  type: "recognized",
  data: {
    original_text: string,
    translations: Record<string, string>,
    detected_language: string,
    timestamp: string,
    duration_ms: number,
    synthesized_audio: Record<string, string>  // Base64 encoded
  }
}

// Recording started
{
  type: "started",
  data: { message: string }
}

// Recording stopped
{
  type: "stopped",
  data: { message: string }
}

// Error
{
  type: "error",
  data: { message: string }
}
```

---

## 📚 API Reference

### REST Endpoints

#### Health Check
```http
GET /
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "version": "1.0.0",
  "azure_region": "eastus",
  "live_interpreter_enabled": true
}
```

#### Get Supported Languages
```http
GET /languages
```

**Response:**
```json
{
  "languages": {
    "en-US": "English (United States)",
    "es-ES": "Spanish (Spain)",
    ...
  },
  "voices": {
    "en-US": ["en-US-JennyNeural", "en-US-GuyNeural", ...],
    "es-ES": ["es-ES-ElviraNeural", "es-ES-AlvaroNeural", ...],
    ...
  }
}
```

#### Get Configuration
```http
GET /config
```

**Response:**
```json
{
  "source_language": "en-US",
  "target_languages": ["es-ES", "fr-FR", "de-DE"],
  "voice_name": "en-US-JennyNeural",
  "region": "eastus",
  "live_interpreter_enabled": true,
  "auto_detect_enabled": true
}
```

### WebSocket Endpoint

```
ws://localhost:8000/ws/translate
```

See [Communication Flow](#communication-flow) for message protocol.

---

## 🐛 Troubleshooting

### Common Issues

#### 1. WebSocket Connection Failed

**Symptoms:**
- "Disconnected" status in UI
- Console error: `WebSocket connection failed`

**Solutions:**
```bash
# Check backend is running
curl http://localhost:8000/health

# Check firewall
sudo ufw allow 8000

# Check CORS settings in .env
CORS_ORIGINS=http://localhost:5173
```

#### 2. No Audio Playback

**Symptoms:**
- Audio buttons not appearing
- Playback button doesn't work

**Solutions:**
```bash
# Check environment variable
ENABLE_AUDIO_PLAYBACK=true

# Check browser console for errors
# Enable microphone permissions
# Try different browser (Chrome recommended)
```

#### 3. Microphone Access Denied

**Symptoms:**
- "Microphone access denied" error
- Recording doesn't start

**Solutions:**
- **Chrome:** Settings → Privacy → Site Settings → Microphone → Allow
- **Firefox:** Preferences → Privacy & Security → Permissions → Microphone
- Reload page after granting permissions

#### 4. Azure Speech Service Errors

**Symptoms:**
- "Authentication failed" error
- "Invalid region" error

**Solutions:**
```bash
# Verify credentials
echo $SPEECH_KEY
echo $SPEECH_REGION

# Test connection
curl "https://$SPEECH_REGION.api.cognitive.microsoft.com/sts/v1.0/issuetoken" \
  -H "Ocp-Apim-Subscription-Key: $SPEECH_KEY"

# Check quota
# Azure Portal → Speech Service → Usage and Quotas
```

#### 5. Translation Not Appearing

**Symptoms:**
- Recording works but no translation shows
- Interim results work but final results don't

**Solutions:**
- Check backend logs for errors
- Verify target languages are valid
- Ensure voice preferences match available voices
- Check network tab in browser DevTools

#### 6. Build Errors

**Frontend build fails:**
```bash
# Clear cache and reinstall
cd frontend
rm -rf node_modules package-lock.json
npm install

# Update dependencies
npm update
```

**Backend errors:**
```bash
# Reinstall dependencies
pip install --upgrade -r requirements.txt

# Check Python version
python --version  # Should be 3.9+
```

### Debug Mode

Enable detailed logging:

```env
LOG_LEVEL=DEBUG
```

**Backend logs:**
```bash
cd src/react_app/backend
python main.py 2>&1 | tee app.log
```

**Frontend logs:**
- Open browser DevTools (F12)
- Check Console tab for client-side errors
- Check Network tab → WS for WebSocket messages

---

## 🚢 Deployment

### Docker Deployment (Recommended)

#### Create Dockerfile for Backend

```dockerfile
# backend.Dockerfile
FROM python:3.11-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy backend code
COPY src/react_app/backend/ ./backend/
COPY src/core/ ./core/
COPY .env .

WORKDIR /app/backend

CMD ["uvicorn", "main:app", "--host", "0.0.0.0", "--port", "8000"]
```

#### Create Dockerfile for Frontend

```dockerfile
# frontend.Dockerfile
FROM node:18-alpine as build

WORKDIR /app

# Install dependencies
COPY src/react_app/frontend/package*.json ./
RUN npm ci

# Build app
COPY src/react_app/frontend/ .
RUN npm run build

# Serve with nginx
FROM nginx:alpine
COPY --from=build /app/dist /usr/share/nginx/html
COPY nginx.conf /etc/nginx/conf.d/default.conf

EXPOSE 80
CMD ["nginx", "-g", "daemon off;"]
```

#### Docker Compose

```yaml
# docker-compose.yml
version: '3.8'

services:
  backend:
    build:
      context: .
      dockerfile: backend.Dockerfile
    ports:
      - "8000:8000"
    env_file:
      - .env
    restart: unless-stopped

  frontend:
    build:
      context: .
      dockerfile: frontend.Dockerfile
    ports:
      - "80:80"
    depends_on:
      - backend
    restart: unless-stopped
```

**Deploy:**
```bash
docker-compose up -d
```

### Azure App Service Deployment

#### Backend

```bash
# Create App Service
az webapp up --name my-interpreter-api \
  --runtime PYTHON:3.11 \
  --sku B1

# Configure environment variables
az webapp config appsettings set \
  --name my-interpreter-api \
  --settings SPEECH_KEY=$SPEECH_KEY SPEECH_REGION=$SPEECH_REGION
```

#### Frontend

```bash
# Build
cd src/react_app/frontend
npm run build

# Deploy to Azure Static Web Apps
az staticwebapp create \
  --name my-interpreter-app \
  --source dist/
```

### Environment-Specific Configuration

#### Production `.env`

```env
# Use production values
SPEECH_KEY=production_key
SPEECH_REGION=eastus

# Production CORS
CORS_ORIGINS=https://yourdomain.com,https://www.yourdomain.com

# Disable debug features
SAVE_AUDIO_FILES=false
LOG_LEVEL=WARNING

# Production server
BACKEND_HOST=0.0.0.0
BACKEND_PORT=8000
```

---

## 📄 License

This project is part of the Azure Live Interpreter API Demo. See the main project repository for license information.

---

## 🤝 Contributing

We welcome contributions! Please see the main project repository for contribution guidelines.

---

## 📞 Support

### Documentation
- [Azure Speech Service Documentation](https://docs.microsoft.com/azure/cognitive-services/speech-service/)
- [FastAPI Documentation](https://fastapi.tiangolo.com/)
- [React Documentation](https://react.dev/)
- [Tailwind CSS Documentation](https://tailwindcss.com/)

### Issues
Report issues in the main project repository.

---

## 🎯 Use Cases

### Council Meetings
- Real-time bilingual translation for city council meetings
- Instant Spanish translation for public hearings
- Audio playback for attendees with hearing devices

### Conferences & Events
- Multi-language support for international conferences
- Live interpretation for breakout sessions
- Recorded translations for later review

### Business Meetings
- Multilingual team collaboration
- Client presentations in multiple languages
- Remote interpretation services

### Education & Training
- Language learning and pronunciation practice
- Multilingual classroom support
- Accessibility for international students

---

## 🔮 Roadmap

- [ ] Mobile app support (iOS/Android)
- [ ] Recording playback and download
- [ ] Custom vocabulary support
- [ ] Speaker diarization
- [ ] Translation quality metrics
- [ ] Multi-user collaboration
- [ ] Integration with video conferencing platforms

---

## 🙏 Acknowledgments

Built with:
- [Azure Speech Service](https://azure.microsoft.com/services/cognitive-services/speech-services/)
- [React](https://react.dev/)
- [FastAPI](https://fastapi.tiangolo.com/)
- [Tailwind CSS](https://tailwindcss.com/)
- [Vite](https://vitejs.dev/)

---

**Made with ❤️ for multilingual communication**
