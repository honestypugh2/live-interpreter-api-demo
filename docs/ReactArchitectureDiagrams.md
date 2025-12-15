# React Architecture Diagrams

Visual architecture diagrams for the React-based Azure Live Interpreter application with FastAPI backend, generated using the [diagrams](https://diagrams.mingrammer.com/) Python library.

## Diagrams Overview

### 1. Client-Server Architecture Diagram

![React Client-Server Architecture](../images/react_client_server_architecture.png)

**File**: `../images/react_client_server_architecture.png`

This diagram illustrates the complete client-server architecture with clear separation between frontend and backend:

#### Architecture Layers

**React Frontend (Browser - TypeScript/Vite)**

*UI Components*
- **Language Selector**: Dropdown for source/target language configuration
- **Audio Recorder**: Recording controls with visual feedback
- **Translation Display**: Real-time translation results display
- **Connection Status**: WebSocket connection state indicator

*Custom Hooks*
- **useWebSocket**: WebSocket client management and message handling
- **useAudioRecorder**: Microphone capture and audio chunk streaming
- **useTranslation**: Translation state management and display logic

*Browser APIs*
- **getUserMedia()**: Native browser API for microphone access
- **Web Audio API**: Native browser API for audio playback

**FastAPI Backend Server (Python)**

*WebSocket Layer*
- **WebSocket Handler**: Main WebSocket endpoint and connection handler
- **Connection Manager**: Active WebSocket connection pool management
- **Message Router**: Routes incoming messages to appropriate handlers
- **Session Manager**: Manages user sessions and translator instances

*Core Services*
- **Config Manager**: Loads environment variables and settings
- **Translator (LiveInterpreter)**: Manages Azure Speech SDK translation
- **Audio Handler**: Processes audio streams and manages audio I/O

*Azure SDK*
- **SpeechTranslationConfig**: Azure Speech service configuration
- **TranslationRecognizer**: Main translation engine interface
- **Event Callbacks**: Handles asynchronous Azure events

**System Audio I/O**
- **Microphone**: Captures PCM audio input
- **Speaker**: Outputs translated audio

**Azure Cloud Services**
- **Live Interpreter Engine**: Azure Speech Translation Service
  - Language Detection (automatic source language identification)
  - Speech-to-Speech Translation (real-time translation)
  - Neural Voice Synthesis (high-quality TTS)

#### Key Characteristics

✅ **Client-Server Separation**: Frontend and backend are independent services  
✅ **Asynchronous Communication**: WebSocket for bi-directional real-time messaging  
✅ **Scalable Architecture**: Backend can handle multiple concurrent clients  
✅ **Type Safety**: TypeScript in frontend for type-safe development  
✅ **Modern Stack**: React + Vite (frontend), FastAPI + uvicorn (backend)

#### Communication Flow

**Connection Colors in Diagram:**
- 🔵 **Blue**: WebSocket messages (JSON) between client and backend
- 🔴 **Red**: Azure SDK calls and events
- 🟢 **Green**: Audio data streaming
- ⚫ **Black**: Standard data flow

**Data Flow Path:**
1. User interacts with React UI components
2. Custom hooks manage state and WebSocket communication
3. Browser APIs access microphone and speakers
4. WebSocket sends messages to FastAPI backend
5. Backend routes messages to core services
6. Core services use Azure SDK to communicate with Azure
7. Azure processes speech and returns events
8. Events flow back through callbacks → backend → WebSocket → frontend
9. React re-renders UI with updated translations

---

### 2. WebSocket Message Flow Diagram

![React WebSocket Message Flow](../images/react_websocket_flow.png)

**File**: `../images/react_websocket_flow.png`

This diagram shows the complete WebSocket message exchange sequence for a continuous translation session:

#### Message Flow Phases

**Phase 1: WebSocket Connection**
1. **WS Connect**: Client initiates WebSocket connection to backend
2. **Connection Accepted**: Backend accepts and registers the connection

**Phase 2: Configuration**
3. **Send Config**: Client sends configuration (source language, target languages, mode)
   ```json
   {
     "type": "config",
     "source_language": "en-US",
     "target_languages": ["es-ES", "fr-FR"],
     "use_continuous_mode": true
   }
   ```
4. **Initialize Translator**: Backend creates Azure Speech SDK translator
5. **Translator Ready**: Azure confirms translator is ready
6. **Config Confirmed**: Backend confirms configuration to client
   ```json
   {
     "type": "config_confirmed",
     "use_live_interpreter": true
   }
   ```

**Phase 3: Start Translation Session**
7. **Start Recording**: Client sends start recording message
   ```json
   {
     "type": "start_recording"
   }
   ```
8. **Create Recognizer**: Backend creates TranslationRecognizer
9. **Start Continuous Recognition**: Backend starts Azure recognition session

**Phase 4: Continuous Translation Loop** *(repeats for each utterance)*

10. **Audio Stream**: Backend streams PCM audio chunks to Azure
11. **Recognizing Event**: Azure sends interim results
12. **Interim Translation Message**: Backend forwards interim results to client
    ```json
    {
      "type": "recognizing",
      "original_text": "Hello world...",
      "translations": {
        "es-ES": "Hola mundo..."
      }
    }
    ```
13. *[User continues speaking...]*
14. **Recognized Event**: Azure sends final translation results
15. **Synthesize Audio**: Backend requests audio synthesis
16. **Audio Data**: Azure returns Base64-encoded audio
17. **Final Translation + Audio**: Backend sends complete result to client
    ```json
    {
      "type": "recognized",
      "original_text": "Hello world",
      "translations": {
        "es-ES": "Hola mundo"
      },
      "detected_language": "en-US",
      "synthesized_audio": {
        "es-ES": "base64encodedaudiodata..."
      },
      "timestamp": "2025-12-12T17:00:00Z"
    }
    ```
18. **Loop Continues**: Process repeats for next utterance

**Phase 5: Stop Translation**
18. **Stop Recording**: Client sends stop message
    ```json
    {
      "type": "stop_recording"
    }
    ```
19. **Stop Recognition**: Backend stops Azure recognition
20. **Session Stopped**: Azure confirms session ended
21. **Stopped Confirmation**: Backend confirms to client
    ```json
    {
      "type": "stopped"
    }
    ```

**Phase 6: Connection Cleanup**
22. **Close WebSocket**: Client closes WebSocket connection
23. **Cleanup Resources**: Backend releases Azure resources
24. **Connection Closed**: Backend confirms cleanup complete

#### Message Types

| Type | Direction | Purpose |
|------|-----------|---------|
| `config` | Client → Backend | Configure translation settings |
| `config_confirmed` | Backend → Client | Confirm configuration accepted |
| `start_recording` | Client → Backend | Begin translation session |
| `recognizing` | Backend → Client | Interim translation results |
| `recognized` | Backend → Client | Final translation + audio |
| `stop_recording` | Client → Backend | End translation session |
| `stopped` | Backend → Client | Confirm session ended |
| `error` | Backend → Client | Error notification |

---

## Technical Specifications

### WebSocket Communication
- **Protocol**: WebSocket (ws:// or wss://)
- **Message Format**: JSON
- **Encoding**: UTF-8
- **Connection**: Persistent bi-directional connection
- **Heartbeat**: Ping/pong for connection health

### Audio Streaming
- **Format**: PCM (Pulse Code Modulation)
- **Sample Rate**: 16kHz
- **Bit Depth**: 16-bit
- **Channels**: Mono (1 channel)
- **Chunk Size**: Configurable (typically 1024-4096 bytes)
- **Transport**: WebSocket binary frames or Base64-encoded JSON

### Backend Server
- **Framework**: FastAPI (Python)
- **ASGI Server**: uvicorn
- **WebSocket**: Native FastAPI WebSocket support
- **Concurrency**: Async/await (asyncio)
- **Session Storage**: In-memory dict (can use Redis for production)

### Frontend Application
- **Framework**: React 18+
- **Language**: TypeScript
- **Build Tool**: Vite
- **State Management**: React hooks (useState, useEffect, useContext)
- **WebSocket Client**: Native WebSocket API
- **Audio**: Web Audio API, MediaRecorder API

### Azure Service Details
- **Service**: Azure Speech Translation (Live Interpreter)
- **Regions**: eastus, westus2, westeurope, japaneast, southeastasia
- **Latency**: 
  - Interim results: ~100-300ms
  - Final results with audio: ~1-2 seconds
- **Languages**: 100+ supported languages

---

## File Structure

```
src/react_app/
├── frontend/                       # React Frontend (TypeScript)
│   ├── src/
│   │   ├── components/            # UI Components
│   │   │   ├── AudioRecorder.tsx
│   │   │   ├── LanguageSelector.tsx
│   │   │   ├── TranslationDisplay.tsx
│   │   │   └── ConnectionStatus.tsx
│   │   ├── hooks/                 # Custom Hooks
│   │   │   └── useWebSocket.ts
│   │   ├── types/                 # TypeScript Types
│   │   │   └── translation.ts
│   │   ├── App.tsx               # Main App Component
│   │   └── main.tsx              # Entry Point
│   ├── package.json
│   └── vite.config.ts
│
├── backend/                        # FastAPI Backend (Python)
│   └── main.py                    # WebSocket Server
│       ├── WebSocket Handler
│       ├── Connection Manager
│       ├── Message Router
│       └── Session Manager
│
src/core/                          # Shared Core Services
├── config.py                      # Configuration Manager
├── translator.py                  # Translation Core
└── audio_handler.py               # Audio I/O Handler
```

---

## Deployment Architecture

### Development Setup
```
┌─────────────────┐         ┌──────────────────┐
│  React Dev      │         │  FastAPI Dev     │
│  Server         │         │  Server          │
│  (Vite)         │         │  (uvicorn)       │
│  Port 5173      │────────>│  Port 8000       │
└─────────────────┘   CORS  └──────────────────┘
                                      │
                                      ▼
                              ┌──────────────────┐
                              │  Azure Speech    │
                              │  Translation     │
                              └──────────────────┘
```

### Production Setup
```
┌─────────────────┐
│  Nginx/CDN      │
│  (Static Files) │
│  Port 443       │
└────────┬────────┘
         │ HTTPS
         ▼
┌─────────────────┐         ┌──────────────────┐
│  React Build    │         │  FastAPI Server  │
│  (Static HTML/  │         │  (WebSocket)     │
│   JS/CSS)       │────────>│  Port 8000       │
└─────────────────┘   WSS   └──────────────────┘
                                      │
                                      ▼
                              ┌──────────────────┐
                              │  Azure Speech    │
                              │  Translation     │
                              └──────────────────┘
```

---

## Generating the Diagrams

### Prerequisites

1. **Python 3.10+** installed
2. **GraphViz** installed ([download](https://graphviz.org/download/))
3. **diagrams** package installed

### Installation

```bash
# Activate virtual environment
source .venv/bin/activate

# Install diagrams package (if not already installed)
uv add diagrams

# Or using pip
pip install diagrams
```

### Generate Diagrams

```bash
# Generate client-server architecture diagram
python scripts/generate_react_architecture.py

# Generate WebSocket message flow diagram
python scripts/generate_react_websocket_flow.py

# Generate all diagrams at once
python scripts/generate_all_diagrams.py

# Diagrams will be saved to images/ directory
```

### Customize Diagrams

Edit the generator scripts to customize:
- Layout direction (`direction="TB"` or `"LR"`)
- Colors for different communication types
- Add/remove components
- Modify labels and descriptions
- Change output format (`outformat="png"`, `"pdf"`, `"svg"`)

---

## Architecture Comparison

### React (Client-Server) vs Streamlit (Monolithic)

| Aspect | React | Streamlit |
|--------|-------|-----------|
| **Architecture** | Client-Server | Monolithic |
| **Frontend** | React (TypeScript) | Streamlit (Python) |
| **Backend** | FastAPI (separate) | Integrated |
| **Communication** | WebSocket | Direct SDK calls |
| **State** | React state + backend | st.session_state |
| **Execution** | Asynchronous | Synchronous |
| **Scalability** | High (horizontal) | Limited |
| **Deployment** | 2 services | 1 service |
| **Concurrency** | Multiple users | Limited |
| **Complexity** | Higher | Lower |
| **Best For** | Production | Demos/Prototypes |

### When to Use React Architecture

✅ **Good for:**
- Production applications
- Multiple concurrent users
- High-traffic scenarios
- Microservices architecture
- Mobile-responsive UI
- Advanced UI/UX requirements
- Horizontal scaling needs

⚠️ **Considerations:**
- More complex deployment
- Two services to maintain
- Requires frontend expertise
- More development time

---

## WebSocket Connection Management

### Connection Lifecycle

```python
# Backend (FastAPI)
class ConnectionManager:
    def __init__(self):
        self.active_connections: Dict[str, WebSocket] = {}
    
    async def connect(self, websocket: WebSocket, client_id: str):
        await websocket.accept()
        self.active_connections[client_id] = websocket
    
    async def disconnect(self, client_id: str):
        if client_id in self.active_connections:
            del self.active_connections[client_id]
    
    async def send_message(self, message: dict, client_id: str):
        if client_id in self.active_connections:
            await self.active_connections[client_id].send_json(message)
```

```typescript
// Frontend (React)
const useWebSocket = (url: string) => {
  const [ws, setWs] = useState<WebSocket | null>(null);
  const [status, setStatus] = useState<'connecting' | 'connected' | 'disconnected'>('disconnected');
  
  useEffect(() => {
    const websocket = new WebSocket(url);
    
    websocket.onopen = () => {
      setStatus('connected');
      setWs(websocket);
    };
    
    websocket.onmessage = (event) => {
      const message = JSON.parse(event.data);
      // Handle message
    };
    
    websocket.onclose = () => {
      setStatus('disconnected');
    };
    
    return () => websocket.close();
  }, [url]);
  
  return { ws, status };
};
```

---

## Error Handling

### Backend Error Messages

```json
{
  "type": "error",
  "error_code": "TRANSLATION_FAILED",
  "message": "Failed to translate audio",
  "details": "Azure Speech SDK error: Invalid audio format",
  "timestamp": "2025-12-12T17:00:00Z"
}
```

### Frontend Error Handling

```typescript
websocket.onerror = (error) => {
  console.error('WebSocket error:', error);
  setConnectionStatus('error');
  showNotification('Connection error. Please try again.');
};
```

---

## Related Documentation

- [README.md](../README.md) - Main project documentation
- [StreamlitArchitectureDiagrams.md](StreamlitArchitectureDiagrams.md) - Streamlit architecture
- [Quickstart.md](Quickstart.md) - Getting started guide
- [ProjectStructure.md](ProjectStructure.md) - Detailed project structure
- [ProductionDeploymentGuide.md](ProductionDeploymentGuide.md) - Production deployment
- [IntegrationGuide.md](IntegrationGuide.md) - Integration patterns

---

## License

These diagrams are part of the Live Interpreter API Demo project. See [LICENSE](../LICENSE) for details.

---

**Generated**: December 12, 2025  
**Tool**: Python diagrams library with Azure icons  
**Files**: 
- `../images/react_client_server_architecture.png` (Client-Server Architecture)
- `../images/react_websocket_flow.png` (WebSocket Message Flow)
