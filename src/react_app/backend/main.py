"""
FastAPI Backend for Azure Live Interpreter React App
Provides WebSocket support for real-time audio streaming and translation
"""

from fastapi import FastAPI, WebSocket, WebSocketDisconnect, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from typing import List, Optional, Dict
import logging
import sys
from pathlib import Path
import asyncio

# Add parent directories to path
sys.path.insert(0, str(Path(__file__).parent.parent.parent.parent))

from src.core.config import get_settings, SUPPORTED_LANGUAGES, NEURAL_VOICES
from src.core.translator import AzureSpeechTranslator, LiveInterpreterTranslator, TranslationResult
import azure.cognitiveservices.speech as speechsdk

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Azure Live Interpreter API",
    description="Real-time speech translation WebSocket API",
    version="1.0.0"
)

# Load settings
try:
    settings = get_settings()
    logger.info(f"Settings loaded. Region: {settings.speech_region}")
except Exception as e:
    logger.error(f"Failed to load settings: {e}")
    raise

# CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.cors_origins_list,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Pydantic models
class LanguageConfig(BaseModel):
    """Language configuration"""
    source_language: Optional[str] = None
    target_languages: List[str]
    use_live_interpreter: bool = False
    use_continuous_mode: bool = True
    voice_preferences: Optional[Dict[str, str]] = None

class TranslationResponse(BaseModel):
    """Translation result response"""
    original_text: str
    detected_language: Optional[str]
    translations: Dict[str, str]
    timestamp: str
    duration_ms: int
    synthesized_audio: Optional[Dict[str, str]] = None  # Base64 encoded audio per language

class HealthResponse(BaseModel):
    """Health check response"""
    status: str
    version: str
    azure_region: str
    live_interpreter_enabled: bool

# In-memory connection manager
class ConnectionManager:
    """Manage WebSocket connections"""
    
    def __init__(self):
        self.active_connections: List[WebSocket] = []
        self.translators: Dict[WebSocket, AzureSpeechTranslator] = {}
    
    async def connect(self, websocket: WebSocket):
        """Accept new WebSocket connection"""
        await websocket.accept()
        self.active_connections.append(websocket)
        logger.info(f"New connection. Total connections: {len(self.active_connections)}")
    
    def disconnect(self, websocket: WebSocket):
        """Remove WebSocket connection"""
        if websocket in self.active_connections:
            self.active_connections.remove(websocket)
        if websocket in self.translators:
            del self.translators[websocket]
        logger.info(f"Connection closed. Total connections: {len(self.active_connections)}")
    
    async def send_message(self, websocket: WebSocket, message: dict):
        """Send message to specific websocket"""
        try:
            await websocket.send_json(message)
        except Exception as e:
            logger.error(f"Error sending message: {e}")

manager = ConnectionManager()

# REST API Endpoints
@app.get("/", response_model=HealthResponse)
async def root():
    """Health check endpoint"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        azure_region=settings.speech_region,
        live_interpreter_enabled=settings.enable_live_interpreter
    )

@app.get("/health", response_model=HealthResponse)
async def health_check():
    """Detailed health check"""
    return HealthResponse(
        status="healthy",
        version="1.0.0",
        azure_region=settings.speech_region,
        live_interpreter_enabled=settings.enable_live_interpreter
    )

@app.get("/languages")
async def get_languages():
    """Get supported languages"""
    return {
        "languages": SUPPORTED_LANGUAGES,
        "voices": NEURAL_VOICES
    }

@app.get("/config")
async def get_config():
    """Get current configuration (without sensitive data)"""
    return {
        "source_language": settings.source_language,
        "target_languages": settings.target_languages,
        "voice_name": settings.voice_name,
        "region": settings.speech_region,
        "live_interpreter_enabled": settings.enable_live_interpreter,
        "auto_detect_enabled": settings.enable_auto_detect
    }

# WebSocket endpoint for real-time translation
@app.websocket("/ws/translate")
async def websocket_translate(websocket: WebSocket):
    """
    WebSocket endpoint for real-time translation
    
    Protocol:
    1. Client connects
    2. Client sends config: {"type": "config", "data": {...}}
    3. Client sends audio chunks: {"type": "audio", "data": <base64 audio>}
    4. Server sends translations: {"type": "translation", "data": {...}}
    5. Server sends audio: {"type": "audio", "data": <base64 audio>}
    """
    await manager.connect(websocket)
    
    translator: Optional[AzureSpeechTranslator] = None
    recognizer: Optional[speechsdk.translation.TranslationRecognizer] = None
    
    try:
        # Send welcome message
        await manager.send_message(websocket, {
            "type": "connected",
            "data": {
                "message": "Connected to Azure Live Interpreter API",
                "server_version": "1.0.0"
            }
        })
        
        while True:
            # Receive message from client
            data = await websocket.receive_json()
            message_type = data.get("type")
            message_data = data.get("data", {})
            
            if message_type == "config":
                # Initialize translator with client configuration
                logger.info(f"Received config: {message_data}")
                
                use_live_interpreter = message_data.get("use_live_interpreter", False)
                use_continuous_mode = message_data.get("use_continuous_mode", True)
                source_lang = message_data.get("source_language")
                target_langs = message_data.get("target_languages", [settings.target_language])[:3]  # Max 3 languages
                voice_preferences = message_data.get("voice_preferences", {})
                
                # Update settings temporarily for this connection
                settings.source_language = source_lang or settings.source_language
                settings.target_language = target_langs[0] if target_langs else settings.target_language
                settings.target_language_2 = target_langs[1] if len(target_langs) > 1 else None
                settings.target_language_3 = target_langs[2] if len(target_langs) > 2 else None
                
                # Apply voice preferences
                for lang, voice in voice_preferences.items():
                    voice_attr = f"voice_{lang.lower().replace('-', '_')}"
                    if hasattr(settings, voice_attr):
                        setattr(settings, voice_attr, voice)
                        logger.info(f"Set voice for {lang}: {voice}")
                
                # Create translator
                if use_live_interpreter and settings.enable_live_interpreter:
                    translator = LiveInterpreterTranslator(settings)
                    logger.info(f"Created Live Interpreter translator with {len(target_langs)} target languages")
                else:
                    translator = AzureSpeechTranslator(settings)
                    logger.info("Created standard translator")
                
                manager.translators[websocket] = translator
                
                await manager.send_message(websocket, {
                    "type": "config_confirmed",
                    "data": {
                        "use_live_interpreter": use_live_interpreter,
                        "use_continuous_mode": use_continuous_mode,
                        "source_language": settings.source_language,
                        "target_languages": target_langs
                    }
                })
            
            elif message_type == "start_recording":
                # Start continuous translation
                logger.info("Starting continuous translation")
                
                if translator is None:
                    await manager.send_message(websocket, {
                        "type": "error",
                        "data": {"message": "Translator not configured. Send config first."}
                    })
                    continue
                
                # Create recognizer
                recognizer = translator.create_recognizer_from_microphone()
                
                # Get the event loop for callbacks
                loop = asyncio.get_event_loop()
                
                # Set up callbacks
                def on_recognizing(result: TranslationResult):
                    """Send interim results"""
                    asyncio.run_coroutine_threadsafe(
                        manager.send_message(websocket, {
                            "type": "recognizing",
                            "data": {
                                "original_text": result.original_text,
                                "translations": result.translations,
                                "detected_language": result.detected_language
                            }
                        }),
                        loop
                    )
                
                def on_recognized(result: TranslationResult):
                    """Send final results"""
                    # Synthesize audio for translations
                    synthesized_audio = {}
                    if result.translations:
                        logger.info(f"Synthesizing audio for {len(result.translations)} translations")
                        for lang, text in result.translations.items():
                            try:
                                audio_bytes = translator.synthesize_translation(text, lang)
                                if audio_bytes:
                                    import base64
                                    synthesized_audio[lang] = base64.b64encode(audio_bytes).decode('utf-8')
                                    logger.info(f"Synthesized {len(audio_bytes)} bytes for {lang}")
                            except Exception as e:
                                logger.error(f"Error synthesizing audio for {lang}: {e}")
                    
                    asyncio.run_coroutine_threadsafe(
                        manager.send_message(websocket, {
                            "type": "recognized",
                            "data": {
                                "original_text": result.original_text,
                                "translations": result.translations,
                                "detected_language": result.detected_language,
                                "timestamp": result.timestamp.isoformat(),
                                "duration_ms": result.duration_ms,
                                "synthesized_audio": synthesized_audio
                            }
                        }),
                        loop
                    )
                
                def on_synthesizing(audio_data: bytes):
                    """Send synthesized audio"""
                    if audio_data and len(audio_data) > 0:
                        # Convert to base64 for JSON transmission
                        import base64
                        audio_base64 = base64.b64encode(audio_data).decode('utf-8')
                        asyncio.run_coroutine_threadsafe(
                            manager.send_message(websocket, {
                                "type": "audio",
                                "data": {
                                    "audio": audio_base64,
                                    "format": "pcm16",
                                    "sample_rate": 16000
                                }
                            }),
                            loop
                        )
                
                def on_canceled(error: str):
                    """Send error"""
                    asyncio.run_coroutine_threadsafe(
                        manager.send_message(websocket, {
                            "type": "error",
                            "data": {"message": f"Translation canceled: {error}"}
                        }),
                        loop
                    )
                
                def on_stopped():
                    """Send stopped notification"""
                    asyncio.run_coroutine_threadsafe(
                        manager.send_message(websocket, {
                            "type": "stopped",
                            "data": {"message": "Translation stopped"}
                        }),
                        loop
                    )
                
                # Start continuous recognition with callbacks
                translator.start_continuous_translation(
                    recognizer=recognizer,
                    recognizing_callback=on_recognizing,
                    recognized_callback=on_recognized,
                    synthesizing_callback=on_synthesizing,
                    canceled_callback=on_canceled,
                    session_stopped_callback=on_stopped
                )
                
                await manager.send_message(websocket, {
                    "type": "started",
                    "data": {"message": "Recording started"}
                })
            
            elif message_type == "stop_recording":
                # Stop continuous translation
                logger.info("Stopping continuous translation")
                
                if recognizer:
                    translator.stop_continuous_translation(recognizer)
                    recognizer = None
                
                await manager.send_message(websocket, {
                    "type": "stopped",
                    "data": {"message": "Recording stopped"}
                })
            
            elif message_type == "ping":
                # Respond to ping
                await manager.send_message(websocket, {
                    "type": "pong",
                    "data": {"timestamp": message_data.get("timestamp")}
                })
            
            else:
                logger.warning(f"Unknown message type: {message_type}")
                await manager.send_message(websocket, {
                    "type": "error",
                    "data": {"message": f"Unknown message type: {message_type}"}
                })
    
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
        manager.disconnect(websocket)
    
    except Exception as e:
        logger.error(f"WebSocket error: {e}", exc_info=True)
        try:
            await manager.send_message(websocket, {
                "type": "error",
                "data": {"message": f"Server error: {str(e)}"}
            })
        except Exception:
            pass
        manager.disconnect(websocket)
    
    finally:
        # Clean up
        if recognizer:
            try:
                translator.stop_continuous_translation(recognizer)
            except Exception:
                pass

# Error handlers
@app.exception_handler(HTTPException)
async def http_exception_handler(request, exc):
    """Handle HTTP exceptions"""
    return JSONResponse(
        status_code=exc.status_code,
        content={"error": exc.detail}
    )

@app.exception_handler(Exception)
async def general_exception_handler(request, exc):
    """Handle general exceptions"""
    logger.error(f"Unhandled exception: {exc}", exc_info=True)
    return JSONResponse(
        status_code=500,
        content={"error": "Internal server error"}
    )

# Startup event
@app.on_event("startup")
async def startup_event():
    """Run on application startup"""
    logger.info("=" * 50)
    logger.info("Azure Live Interpreter API Starting...")
    logger.info(f"Region: {settings.speech_region}")
    logger.info(f"Live Interpreter: {'Enabled' if settings.enable_live_interpreter else 'Disabled'}")
    logger.info(f"CORS Origins: {settings.cors_origins_list}")
    logger.info("=" * 50)

# Shutdown event
@app.on_event("shutdown")
async def shutdown_event():
    """Run on application shutdown"""
    logger.info("Azure Live Interpreter API Shutting down...")

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(
        app,
        host=settings.backend_host,
        port=settings.backend_port,
        log_level=settings.log_level.lower()
    )
