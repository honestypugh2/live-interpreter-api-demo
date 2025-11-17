"""Main Streamlit application for Azure Live Interpreter Demo"""

import streamlit as st
import sys
from pathlib import Path
import queue
import threading
import logging
from datetime import datetime
import asyncio
import tempfile
import os as os_module

# Add project root to path for imports
# app.py is in src/streamlit_app/, so go up 2 levels to project root
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

# Import after path setup
from src.core.config import get_settings, SUPPORTED_LANGUAGES, NEURAL_VOICES  # noqa: E402
from src.core.translator import AzureSpeechTranslator, LiveInterpreterTranslator  # noqa: E402
from src.core.audio_handler import AudioRecorder, AudioPlayer  # noqa: E402

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Azure Live Interpreter Demo",
    page_icon="🌐",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS
st.markdown("""
<style>
    .main-header {
        font-size: 2.5rem;
        font-weight: bold;
        color: #0078D4;
        text-align: center;
        margin-bottom: 2rem;
    }
    .status-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 1rem 0;
    }
    .status-idle {
        background-color: #f0f0f0;
        border-left: 4px solid #888;
    }
    .status-recording {
        background-color: #fff3cd;
        border-left: 4px solid #ffc107;
    }
    .status-translating {
        background-color: #d1ecf1;
        border-left: 4px solid #0dcaf0;
    }
    .status-success {
        background-color: #d1e7dd;
        border-left: 4px solid #198754;
    }
    .translation-box {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        margin: 1rem 0;
    }
    .caption-text {
        font-size: 1.2rem;
        line-height: 1.6;
        margin: 0.5rem 0;
    }
</style>
""", unsafe_allow_html=True)

# Initialize session state
if 'settings' not in st.session_state:
    try:
        st.session_state.settings = get_settings()
    except Exception as e:
        st.error(f"Failed to load settings. Please check your .env file: {e}")
        st.stop()

if 'translator' not in st.session_state:
    st.session_state.translator = None

if 'translation_history' not in st.session_state:
    st.session_state.translation_history = []

if 'is_recording' not in st.session_state:
    st.session_state.is_recording = False

if 'current_status' not in st.session_state:
    st.session_state.current_status = "Idle"

if 'audio_recorder' not in st.session_state:
    st.session_state.audio_recorder = None

if 'audio_player' not in st.session_state:
    st.session_state.audio_player = AudioPlayer()

if 'recorded_audio' not in st.session_state:
    st.session_state.recorded_audio = None

if 'last_error' not in st.session_state:
    st.session_state.last_error = None

# Continuous translation state
if 'use_continuous_mode' not in st.session_state:
    st.session_state.use_continuous_mode = True  # Default to continuous mode

if 'continuous_recognizer' not in st.session_state:
    st.session_state.continuous_recognizer = None

if 'continuous_active' not in st.session_state:
    st.session_state.continuous_active = False

if 'interim_text' not in st.session_state:
    st.session_state.interim_text = ""

if 'interim_translations' not in st.session_state:
    st.session_state.interim_translations = {}

if 'needs_refresh' not in st.session_state:
    st.session_state.needs_refresh = False

if 'last_translation_count' not in st.session_state:
    st.session_state.last_translation_count = 0

if 'auto_refresh_enabled' not in st.session_state:
    st.session_state.auto_refresh_enabled = False

# Thread-safe queue for background callbacks
if 'translation_queue' not in st.session_state:
    st.session_state.translation_queue = queue.Queue()

if 'queue_lock' not in st.session_state:
    st.session_state.queue_lock = threading.Lock()

# Log buffer for displaying callback logs in UI
if 'log_buffer' not in st.session_state:
    st.session_state.log_buffer = []

if 'max_log_lines' not in st.session_state:
    st.session_state.max_log_lines = 20

# Voice preferences per language
if 'voice_preferences' not in st.session_state:
    st.session_state.voice_preferences = {}

# Header
st.markdown('<div class="main-header">🌐 Azure Live Interpreter Demo</div>', unsafe_allow_html=True)
st.markdown("**Real-time speech translation powered by Azure Speech Service**")
st.markdown("---")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Configuration")
    
    # Mode selection
    use_live_interpreter = st.checkbox(
        "Use Live Interpreter",
        value=st.session_state.settings.enable_live_interpreter,
        help="Live Interpreter mode with automatic language detection and personal voice"
    )
    
    # Translation mode selection (only for Live Interpreter)
    if use_live_interpreter:
        st.session_state.use_continuous_mode = st.radio(
            "Translation Mode",
            options=[True, False],
            format_func=lambda x: "🔄 Continuous (Real-time)" if x else "🎯 Single-shot",
            index=0 if st.session_state.use_continuous_mode else 1,
            help="Continuous mode provides real-time translation as you speak. Single-shot mode translates after recording stops."
        )
        
        if st.session_state.use_continuous_mode:
            st.info("💡 Continuous mode will translate in real-time with automatic language detection")
    
    # Source language
    st.markdown("---")
    st.subheader("🎙️ Source Language")
    if not use_live_interpreter:
        source_lang = st.selectbox(
            "Source Language",
            options=list(SUPPORTED_LANGUAGES.keys()),
            index=list(SUPPORTED_LANGUAGES.keys()).index(st.session_state.settings.source_language),
            format_func=lambda x: f"{SUPPORTED_LANGUAGES[x]} ({x})"
        )
    else:
        st.info("✨ **Automatic Detection**\n\nLive Interpreter automatically detects the source language from speech. Supports 100+ languages including English, Spanish, French, German, Italian, Portuguese, Chinese, Japanese, Korean, Arabic, and more.")
        source_lang = None
    
    # Target languages
    st.subheader("🌐 Target Languages")
    st.caption("Select languages to translate into (up to 3)")
    
    target_langs = []
    voice_selections = {}
    
    # Multi-select for target languages
    available_langs = list(SUPPORTED_LANGUAGES.keys())
    default_langs = [st.session_state.settings.target_language]
    if st.session_state.settings.target_language_2:
        default_langs.append(st.session_state.settings.target_language_2)
    if st.session_state.settings.target_language_3:
        default_langs.append(st.session_state.settings.target_language_3)
    
    selected_languages = st.multiselect(
        "Target Languages",
        options=available_langs,
        default=default_langs[:3],  # Limit to 3
        format_func=lambda x: f"{SUPPORTED_LANGUAGES[x]}",
        max_selections=3,
        help="Azure Live Interpreter supports up to 3 simultaneous target languages"
    )
    
    target_langs = selected_languages[:3]  # Ensure max 3
    
    # Voice selection for each selected language
    if target_langs:
        st.markdown("---")
        st.subheader("🎤 Voice Selection")
        
        for idx, lang in enumerate(target_langs):
            if lang in NEURAL_VOICES:
                # Get default voice index
                default_voice_idx = 0
                if lang in st.session_state.voice_preferences:
                    try:
                        default_voice_idx = NEURAL_VOICES[lang].index(st.session_state.voice_preferences[lang])
                    except ValueError:
                        pass
                
                # Create a clean voice name formatter
                def format_voice_name(voice_name, lang_code):
                    # Remove "Neural" and language code prefix
                    clean_name = voice_name.replace("Neural", "").replace(f"{lang_code}-", "")
                    return clean_name
                
                selected_voice = st.selectbox(
                    f"{SUPPORTED_LANGUAGES[lang]}",
                    options=NEURAL_VOICES[lang],
                    index=default_voice_idx,
                    format_func=lambda x, language=lang: format_voice_name(x, language),
                    key=f"voice_select_{lang}_{idx}"
                )
                
                voice_selections[lang] = selected_voice
                st.session_state.voice_preferences[lang] = selected_voice
    else:
        st.warning("⚠️ Please select at least one target language")
    
    # Audio settings
    st.markdown("---")
    st.subheader("🔊 Audio Settings")
    enable_audio_playback = st.checkbox(
        "Enable audio playback",
        value=st.session_state.settings.enable_audio_playback,
        help="Play synthesized audio for translations using selected voices"
    )
    
    if enable_audio_playback:
        st.caption("✓ Translations will include audio playback buttons")
    
    save_audio = st.checkbox(
        "Save audio files",
        value=st.session_state.settings.save_audio_files,
        help="Save recorded and translated audio to disk"
    )
    
    # Connection info
    st.markdown("---")
    st.subheader("📡 Connection")
    st.text(f"Region: {st.session_state.settings.speech_region}")
    if st.session_state.settings.speech_key:
        st.success("✅ API Key configured")
    else:
        st.error("❌ API Key missing")
    
    # Voice mode info
    if use_live_interpreter:
        if st.session_state.settings.use_personal_voice:
            st.info("🎤 Voice: Personal Voice (requires approval)")
        else:
            st.info(f"🔊 Voice: {st.session_state.settings.voice_name}")

# Helper function to add logs to UI buffer
def add_log_to_ui(translation_queue, message):
    """Add a log message to the UI buffer (thread-safe via queue)"""
    timestamp = datetime.now().strftime("%H:%M:%S")
    log_entry = f"[{timestamp}] {message}"
    # Put log in queue for thread-safe processing
    try:
        translation_queue.put({
            'type': 'log',
            'message': log_entry
        }, block=False)
    except queue.Full:
        logger.warning(f"Queue full, log dropped: {message}")

# Continuous translation callback factory functions
def create_callbacks(translation_queue, translator):
    """Create callback functions that don't access st.session_state"""
    
    def on_recognizing(result):
        """Handle interim recognition results"""
        if result.original_text:
            logger.info(f"[CALLBACK] Recognizing: {result.original_text[:50]}...")
            add_log_to_ui(translation_queue, f"[CALLBACK] Recognizing: {result.original_text[:50]}...")
            # Put interim result in queue
            try:
                translation_queue.put({
                    'type': 'interim',
                    'text': result.original_text,
                    'translations': dict(result.translations) if result.translations else {}
                }, block=False)
                logger.info("[CALLBACK] Queued interim result")
                add_log_to_ui(translation_queue, "[CALLBACK] Queued interim result")
            except queue.Full:
                logger.warning("[CALLBACK] Queue full, skipping interim result")
                add_log_to_ui(translation_queue, "[CALLBACK] ⚠️ Queue full, skipping interim result")

    def on_recognized(result):
        """Handle final recognition results"""
        logger.info("[CALLBACK] on_recognized triggered")
        add_log_to_ui(translation_queue, "[CALLBACK] on_recognized triggered")
        logger.info(f"[CALLBACK] Result has text: {bool(result.original_text)}")
        
        if result.original_text:
            detected = result.detected_language or "Unknown"
            logger.info(f"[CALLBACK] Recognized [{detected}]: {result.original_text}")
            add_log_to_ui(translation_queue, f"[CALLBACK] ✓ Recognized [{detected}]: {result.original_text[:50]}...")
            logger.info(f"[CALLBACK] Translations received: {dict(result.translations)}")
            
            # Synthesize audio for translations if translator is available
            synthesized_audio = {}
            if translator and result.translations:
                logger.info(f"[CALLBACK] Translator available, synthesizing for {len(result.translations)} translations")
                add_log_to_ui(translation_queue, f"[CALLBACK] Synthesizing audio for {len(result.translations)} language(s)...")
                for lang, text in result.translations.items():
                    try:
                        logger.info(f"[CALLBACK] Synthesizing audio for {lang}: {text[:50]}...")
                        audio_bytes = translator.synthesize_translation(text, lang)
                        if audio_bytes:
                            synthesized_audio[lang] = audio_bytes
                            logger.info(f"[CALLBACK] ✓ Synthesized {len(audio_bytes)} bytes for {lang}")
                            add_log_to_ui(translation_queue, f"[CALLBACK] ✓ Synthesized audio for {lang}")
                        else:
                            logger.warning(f"[CALLBACK] ✗ No audio synthesized for {lang}")
                            add_log_to_ui(translation_queue, f"[CALLBACK] ✗ No audio for {lang}")
                    except Exception as e:
                        logger.error(f"[CALLBACK] ✗ Error synthesizing audio for {lang}: {e}")
                        add_log_to_ui(translation_queue, f"[CALLBACK] ✗ Error synthesizing {lang}")
                        import traceback
                        traceback.print_exc()
            else:
                logger.warning(f"[CALLBACK] Translator available: {translator is not None}, Translations: {len(result.translations) if result.translations else 0}")
            
            # Create translation entry
            translation_entry = {
                "original": result.original_text,
                "detected_language": result.detected_language,
                "translations": dict(result.translations),  # Ensure it's a dict, not Azure object
                "timestamp": result.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                "audio_data": result.audio_data,
                "synthesized_audio": synthesized_audio
            }
            
            # Put final result in queue instead of directly modifying session state
            try:
                translation_queue.put({
                    'type': 'final',
                    'entry': translation_entry
                }, block=False)
                logger.info(f"[CALLBACK] Queued final translation with {len(result.translations)} translation(s)")
                add_log_to_ui(translation_queue, f"[CALLBACK] ✓ Queued translation ({len(result.translations)} lang, {len(synthesized_audio)} audio)")
            except queue.Full:
                logger.error("[CALLBACK] Queue full, could not add translation!")
                add_log_to_ui(translation_queue, "[CALLBACK] ✗ Queue full!")
        else:
            logger.warning("[CALLBACK] No original text in result")
            add_log_to_ui(translation_queue, "[CALLBACK] ⚠️ No text recognized")

    def on_synthesizing(audio_data: bytes):
        """Handle audio synthesis"""
        if audio_data:
            logger.info(f"[CALLBACK] Audio synthesized: {len(audio_data)} bytes")
            add_log_to_ui(translation_queue, f"[CALLBACK] Audio synthesized: {len(audio_data)} bytes")

    def on_session_stopped():
        """Handle session stop"""
        logger.info("Continuous translation session stopped")
        # Send session stopped event to queue
        try:
            translation_queue.put({
                'type': 'session_stopped'
            }, block=False)
        except queue.Full:
            logger.error("Queue full, could not queue session_stopped event")

    def on_canceled(details):
        """Handle cancellation"""
        logger.error(f"Translation canceled: {details}")
        # Put error in queue for UI to handle
        try:
            translation_queue.put({
                'type': 'error',
                'message': f"Translation canceled: {details}"
            }, block=False)
        except queue.Full:
            logger.error("Queue full, could not queue error")
    
    return on_recognizing, on_recognized, on_synthesizing, on_session_stopped, on_canceled

# Main content area
# Show auto-refresh notice for continuous mode
if st.session_state.continuous_active:
    st.info("🔄 **Continuous Mode Active** - Click the 'Refresh' button in the Translation Output section to see new translations")

col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎤 Audio Input")
    
    # Status indicator
    current_display_status = st.session_state.current_status
    if st.session_state.continuous_active and st.session_state.is_recording:
        current_display_status = "Translating (Live)"
    
    status_class = {
        "Idle": "status-idle",
        "Recording": "status-recording",
        "Translating": "status-translating",
        "Translating (Live)": "status-translating",
        "Success": "status-success"
    }.get(current_display_status, "status-idle")
    
    st.markdown(
        f'<div class="status-box {status_class}">Status: <b>{current_display_status}</b></div>',
        unsafe_allow_html=True
    )
    
    # Recording controls
    col_rec1, col_rec2, col_rec3 = st.columns([1, 1, 1])
    
    with col_rec1:
        if st.button("🔴 Start Recording", disabled=st.session_state.is_recording, use_container_width=True):
            st.session_state.is_recording = True
            st.session_state.current_status = "Recording"
            st.session_state.last_error = None
            
            # Update settings with selected target languages
            settings = st.session_state.settings
            settings.target_language = target_langs[0]
            if len(target_langs) > 1:
                settings.target_language_2 = target_langs[1]
            else:
                settings.target_language_2 = None
            
            if len(target_langs) > 2:
                settings.target_language_3 = target_langs[2]
            else:
                settings.target_language_3 = None
            
            # Apply voice preferences to settings
            for lang, voice in voice_selections.items():
                voice_attr = f"voice_{lang.lower().replace('-', '_')}"
                setattr(settings, voice_attr, voice)
                logger.info(f"Set voice for {lang}: {voice}")
            
            logger.info(f"Target languages configured: {target_langs}")
            logger.info(f"Settings target languages: {settings.target_languages}")
            logger.info(f"Voice preferences: {voice_selections}")
            
            # Check if using continuous mode with Live Interpreter
            if use_live_interpreter and st.session_state.use_continuous_mode:
                # Continuous translation mode
                try:
                    # Create translator with updated settings
                    translator = LiveInterpreterTranslator(settings)
                    st.session_state.translator = translator
                    
                    logger.info(f"Translator initialized with target languages: {translator.settings.target_languages}")
                    
                    # Create recognizer with continuous language detection
                    recognizer = translator.create_recognizer_from_microphone(
                        auto_detect_languages=["en-US", "es-ES", "fr-FR", "de-DE", "it-IT", "pt-BR"],
                        use_continuous_mode=True
                    )
                    st.session_state.continuous_recognizer = recognizer
                    
                    # Create callbacks that close over queue and translator (no st.* calls)
                    on_recognizing, on_recognized, on_synthesizing, on_session_stopped, on_canceled = create_callbacks(
                        st.session_state.translation_queue,
                        translator
                    )
                    
                    # Start continuous translation
                    translator.start_continuous_translation(
                        recognizer=recognizer,
                        recognizing_callback=on_recognizing,
                        recognized_callback=on_recognized,
                        synthesizing_callback=on_synthesizing,
                        canceled_callback=on_canceled,
                        session_stopped_callback=on_session_stopped
                    )
                    
                    st.session_state.continuous_active = True
                    logger.info("Started continuous translation")
                    
                except Exception as e:
                    st.session_state.last_error = f"Failed to start continuous translation: {str(e)}"
                    st.session_state.is_recording = False
                    st.session_state.current_status = "Idle"
                    logger.error(f"Continuous translation error: {e}")
            else:
                # Single-shot mode - just start recording audio
                st.session_state.audio_recorder = AudioRecorder(sample_rate=16000, channels=1)
                st.session_state.audio_recorder.start_recording()
                logger.info("Started recording (single-shot mode)")
            
            st.rerun()
    
    with col_rec2:
        if st.button("⏹️ Stop & Translate", disabled=not st.session_state.is_recording, use_container_width=True):
            st.session_state.is_recording = False
            
            # Check if using continuous mode
            if st.session_state.continuous_active:
                # Stop continuous translation
                st.session_state.current_status = "Idle"
                
                if st.session_state.continuous_recognizer and st.session_state.translator:
                    try:
                        st.session_state.translator.stop_continuous_translation(
                            st.session_state.continuous_recognizer
                        )
                        logger.info("Stopped continuous translation")
                    except Exception as e:
                        logger.error(f"Error stopping continuous translation: {e}")
                
                st.session_state.continuous_active = False
                st.session_state.continuous_recognizer = None
                st.session_state.translator = None
                st.rerun()
                
            elif st.session_state.audio_recorder:
                # Single-shot mode - process recorded audio
                st.session_state.current_status = "Translating"
                
                # Stop recording and get audio data
                audio_data = st.session_state.audio_recorder.stop_recording()
                st.session_state.recorded_audio = audio_data
                logger.info(f"Stopped recording: {len(audio_data)} samples")
                
                # Update settings with selected target languages
                settings = st.session_state.settings
                settings.target_language = target_langs[0]
                if len(target_langs) > 1:
                    settings.target_language_2 = target_langs[1]
                else:
                    settings.target_language_2 = None
                
                if len(target_langs) > 2:
                    settings.target_language_3 = target_langs[2]
                else:
                    settings.target_language_3 = None
                
                # Apply voice preferences to settings
                for lang, voice in voice_selections.items():
                    voice_attr = f"voice_{lang.lower().replace('-', '_')}"
                    setattr(settings, voice_attr, voice)
                    logger.info(f"Set voice for {lang}: {voice}")
                
                # Perform translation
                try:
                    # Save audio to temporary file for Azure SDK
                    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tmp_file:
                        st.session_state.audio_recorder.save_to_file(audio_data, tmp_file.name)
                        temp_audio_path = tmp_file.name
                    
                    # Create translator with updated settings
                    if use_live_interpreter:
                        translator = LiveInterpreterTranslator(settings)
                    else:
                        translator = AzureSpeechTranslator(settings)
                    
                    # Create recognizer from audio file
                    recognizer = translator.create_recognizer_from_file(
                        temp_audio_path,
                        auto_detect_languages=["en-US", "es-ES", "fr-FR"] if use_live_interpreter else None
                    )
                    
                    # Perform translation
                    result = asyncio.run(translator.translate_once(recognizer))
                    
                    # Add to history
                    if result.original_text:
                        # Synthesize audio for each translation
                        synthesized_audio = {}
                        for lang, text in result.translations.items():
                            logger.info(f"Synthesizing audio for {lang}: {text}")
                            audio_bytes = translator.synthesize_translation(text, lang)
                            if audio_bytes:
                                synthesized_audio[lang] = audio_bytes
                                logger.info(f"Synthesized audio for {lang}: {len(audio_bytes)} bytes")
                            else:
                                logger.warning(f"No audio synthesized for {lang}")
                        
                        translation_entry = {
                            "original": result.original_text,
                            "detected_language": result.detected_language,
                            "translations": dict(result.translations),  # Ensure it's a dict, not Azure object
                            "timestamp": result.timestamp.strftime("%Y-%m-%d %H:%M:%S"),
                            "audio_data": result.audio_data,
                            "synthesized_audio": synthesized_audio
                        }
                        st.session_state.translation_history.append(translation_entry)
                        st.session_state.current_status = "Success"
                        st.session_state.last_error = None
                        logger.info(f"Translation successful: {result.original_text}")
                    else:
                        st.session_state.current_status = "Idle"
                        st.session_state.last_error = "No speech detected in the recording"
                        logger.warning("No speech detected")
                    
                    # Clean up temp file
                    os_module.unlink(temp_audio_path)
                    
                except Exception as e:
                    st.session_state.current_status = "Idle"
                    st.session_state.last_error = str(e)
                    logger.error(f"Translation error: {e}")
                    import traceback
                    traceback.print_exc()
                
                st.rerun()
            else:
                logger.warning("No audio recorder or continuous recognizer active")
                st.session_state.current_status = "Idle"
                st.rerun()
    
    with col_rec3:
        if st.button("🔄 Reset", use_container_width=True):
            st.session_state.is_recording = False
            st.session_state.current_status = "Idle"
            st.rerun()
    
    # Recording indicator
    if st.session_state.is_recording:
        if st.session_state.continuous_active:
            st.warning("🎙️ **Live translation in progress...** Speak naturally!")
            st.info("💡 **Click the 'Refresh Now' button on the right** to see translations as they arrive →")
            
            # Show translation count to encourage refresh
            if len(st.session_state.translation_history) > 0:
                st.success(f"✅ {len(st.session_state.translation_history)} translation(s) captured so far")
        else:
            st.warning("🎙️ **Recording in progress...** Speak now!")
            st.info("Click 'Stop & Translate' when finished speaking")
    
    # Error display
    if st.session_state.last_error:
        st.error(f"❌ Error: {st.session_state.last_error}")
        if st.button("Clear Error"):
            st.session_state.last_error = None
            st.rerun()

with col2:
    st.subheader("💬 Translation Output")
    
    # Process queue and update session state
    items_processed = 0
    logs_processed = 0
    try:
        while not st.session_state.translation_queue.empty():
            item = st.session_state.translation_queue.get_nowait()
            
            if item['type'] == 'log':
                # Process log entry
                st.session_state.log_buffer.append(item['message'])
                # Keep only the last N log lines
                if len(st.session_state.log_buffer) > st.session_state.max_log_lines:
                    st.session_state.log_buffer.pop(0)
                logs_processed += 1
            
            elif item['type'] == 'interim':
                st.session_state.interim_text = item['text']
                st.session_state.interim_translations = item['translations']
                logger.info(f"[UI] Processed interim result: {item['text'][:50]}...")
                items_processed += 1
            
            elif item['type'] == 'final':
                st.session_state.translation_history.append(item['entry'])
                st.session_state.interim_text = ""
                st.session_state.interim_translations = {}
                logger.info(f"[UI] Processed final translation. Total: {len(st.session_state.translation_history)}")
                items_processed += 1
                # Add UI log directly to buffer (we're in main thread)
                timestamp = datetime.now().strftime("%H:%M:%S")
                st.session_state.log_buffer.append(f"[{timestamp}] [UI] ✓ Processed translation #{len(st.session_state.translation_history)}")
                if len(st.session_state.log_buffer) > st.session_state.max_log_lines:
                    st.session_state.log_buffer.pop(0)
            
            elif item['type'] == 'error':
                # Handle error from callback
                st.session_state.last_error = item['message']
                st.session_state.continuous_active = False
                st.session_state.is_recording = False
                st.session_state.current_status = "Idle"
                logger.error(f"[UI] Processed error from callback: {item['message']}")
                items_processed += 1
            
            elif item['type'] == 'session_stopped':
                # Handle session stopped from callback
                st.session_state.continuous_active = False
                st.session_state.is_recording = False
                st.session_state.current_status = "Idle"
                logger.info("[UI] Session stopped by callback")
                items_processed += 1
                
    except queue.Empty:
        pass
    
    if items_processed > 0:
        logger.info(f"[UI] Processed {items_processed} items from queue")
        # Add summary log directly to buffer (we're in main thread)
        timestamp = datetime.now().strftime("%H:%M:%S")
        st.session_state.log_buffer.append(f"[{timestamp}] [UI] Processed {items_processed} items from queue")
        if len(st.session_state.log_buffer) > st.session_state.max_log_lines:
            st.session_state.log_buffer.pop(0)
    
    # Add prominent refresh button for continuous mode
    if st.session_state.continuous_active:
        # Check if there are new translations since last view
        current_count = len(st.session_state.translation_history)
        new_translations = current_count > st.session_state.last_translation_count
        
        col_info, col_btn = st.columns([2, 1])
        with col_info:
            st.caption(f"📊 Total translations: {current_count}")
            if new_translations:
                st.success(f"✨ {current_count - st.session_state.last_translation_count} new translation(s)!")
        with col_btn:
            if st.button("🔄 Refresh Now", key="refresh_translations", use_container_width=True, type="primary"):
                st.session_state.last_translation_count = current_count
                logger.info("[UI] Refresh button clicked, rerunning...")
                # Add log directly to buffer (we're in main thread)
                timestamp = datetime.now().strftime("%H:%M:%S")
                st.session_state.log_buffer.append(f"[{timestamp}] [UI] Refresh button clicked")
                if len(st.session_state.log_buffer) > st.session_state.max_log_lines:
                    st.session_state.log_buffer.pop(0)
                st.rerun()
        
        # Show live log output for continuous mode
        with st.expander("📋 Live Activity Log", expanded=True):
            if st.session_state.log_buffer:
                log_text = "\n".join(reversed(st.session_state.log_buffer[-10:]))  # Show last 10 entries
                st.code(log_text, language=None)
            else:
                st.info("No activity yet. Logs will appear here as you speak.")
    elif st.session_state.translation_history:
        st.caption(f"📊 Total translations: {len(st.session_state.translation_history)}")
    
    # Show interim results if in continuous mode
    if st.session_state.continuous_active and st.session_state.interim_text:
        st.markdown('<div class="translation-box" style="border: 2px dashed #0dcaf0;">', unsafe_allow_html=True)
        st.markdown("**🔄 Recognizing... (interim)**")
        st.markdown(f'<p class="caption-text" style="color: #666;">🗣️ {st.session_state.interim_text}</p>', unsafe_allow_html=True)
        
        if st.session_state.interim_translations:
            st.markdown("**Translating...**")
            for lang, text in st.session_state.interim_translations.items():
                lang_name = SUPPORTED_LANGUAGES.get(lang, lang)
                st.markdown(f'<p class="caption-text" style="color: #666;">🌐 {lang_name}: {text}</p>', unsafe_allow_html=True)
        
        st.markdown('</div>', unsafe_allow_html=True)
    
    # Show latest completed translation
    if st.session_state.translation_history:
        latest = st.session_state.translation_history[-1]
        
        st.markdown("**Latest Translation:**")
        
        st.markdown('<div class="translation-box">', unsafe_allow_html=True)
        
        # Original text
        st.markdown("**Original:**")
        st.markdown(f'<p class="caption-text">🗣️ {latest["original"]}</p>', unsafe_allow_html=True)
        
        if latest.get("detected_language"):
            st.caption(f"Detected: {latest['detected_language']}")
        
        # Translations
        st.markdown("**Translations:**")
        translations = latest.get("translations", {})
        logger.info(f"Displaying translations: {translations}")
        
        if translations and isinstance(translations, dict) and len(translations) > 0:
            for lang, text in translations.items():
                lang_name = SUPPORTED_LANGUAGES.get(lang, lang)
                st.markdown(f'<p class="caption-text">🌐 **{lang_name}:** {text}</p>', unsafe_allow_html=True)
        else:
            st.warning(f"⚠️ No translations available. Translations object: {type(translations)}, Length: {len(translations) if translations else 0}")
            logger.warning(f"No translations to display. Data: {translations}")
        
        # Timestamp
        st.caption(f"⏱️ {latest['timestamp']}")
        
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Audio playback for translated languages
        synthesized_audio = latest.get("synthesized_audio", {})
        logger.info(f"Audio playback check: enable_audio_playback={enable_audio_playback}, synthesized_audio keys={list(synthesized_audio.keys())}, count={len(synthesized_audio)}")
        
        if enable_audio_playback and synthesized_audio and len(synthesized_audio) > 0:
            st.markdown("**🔊 Play Translated Audio:**")
            
            # Create columns for each language
            num_langs = len(synthesized_audio)
            cols = st.columns(num_langs)
            for idx, (lang, audio_bytes) in enumerate(synthesized_audio.items()):
                lang_name = SUPPORTED_LANGUAGES.get(lang, lang)
                with cols[idx]:
                    if st.button(f"▶️ {lang_name}", key=f"play_{lang}_{latest['timestamp']}", use_container_width=True):
                        try:
                            with st.spinner(f"Playing {lang_name}..."):
                                st.session_state.audio_player.play_bytes(audio_bytes)
                            st.success(f"✓ Played {lang_name}")
                        except Exception as e:
                            st.error(f"Playback error: {str(e)}")
                            logger.error(f"Audio playback error: {e}")
                            import traceback
                            traceback.print_exc()
        elif enable_audio_playback:
            st.info(f"🔇 Audio synthesis in progress or not available... (Audio data available: {len(synthesized_audio)} language(s))")
        else:
            st.info("🔇 Audio playback disabled in settings")
    else:
        st.info("👆 Click 'Start Recording' to begin translation")

# Translation history section
st.markdown("---")
st.subheader("📝 Translation History")

if st.session_state.translation_history:
    # Show all history items (not just when > 1)
    # Display in reverse chronological order (skip the last one since it's shown above in "Latest Translation")
    history_to_show = st.session_state.translation_history[:-1] if len(st.session_state.translation_history) > 1 else []
    
    if history_to_show:
        for idx, item in enumerate(reversed(history_to_show)):
            entry_num = len(st.session_state.translation_history) - idx - 1
            with st.expander(f"Translation {entry_num} - {item['timestamp']}"):
                st.markdown(f"**Original:** {item['original']}")
                if item.get("detected_language"):
                    st.caption(f"Language: {item['detected_language']}")
                st.markdown("**Translations:**")
                translations = item.get("translations", {})
                if translations and isinstance(translations, dict):
                    for lang, text in translations.items():
                        st.markdown(f"- **{SUPPORTED_LANGUAGES.get(lang, lang)}:** {text}")
                else:
                    st.info("No translations available")
                
                # Add audio playback buttons (always show if audio exists)
                synthesized_audio = item.get("synthesized_audio", {})
                if synthesized_audio and len(synthesized_audio) > 0:
                    st.markdown("**🔊 Audio Playback:**")
                    # Create columns for each language
                    num_langs = len(synthesized_audio)
                    cols = st.columns(num_langs)
                    for col_idx, (lang, audio_bytes) in enumerate(synthesized_audio.items()):
                        lang_name = SUPPORTED_LANGUAGES.get(lang, lang)
                        with cols[col_idx]:
                            if st.button(f"▶️ {lang_name}", key=f"play_hist_{entry_num}_{lang}", use_container_width=True):
                                try:
                                    with st.spinner(f"Playing {lang_name}..."):
                                        st.session_state.audio_player.play_bytes(audio_bytes)
                                    st.success("✓ Played")
                                except Exception as e:
                                    st.error(f"Error: {str(e)}")
    else:
        st.info("💡 Previous translations will appear here. The most recent translation is shown above.")
    
    # Clear history button
    if st.button("🗑️ Clear History"):
        st.session_state.translation_history = []
        st.session_state.log_buffer = []  # Also clear logs
        st.rerun()
else:
    st.info("No translation history yet. Start recording to see translations here.")

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>Powered by Azure Speech Service | Live Interpreter API Demo</p>
    <p style='font-size: 0.9rem;'>For council meetings, conference rooms, and multilingual events</p>
</div>
""", unsafe_allow_html=True)

# Instructions in expander
with st.expander("📖 How to Use"):
    st.markdown("""
    ### Getting Started
    
    1. **Configure Settings** (Sidebar)
       - Choose between standard translation or Live Interpreter mode
       - Select translation mode: **Continuous (Real-time)** or Single-shot
       - Choose target languages for translation
       
    2. **Continuous Mode (Default for Live Interpreter)**
       - Click "Start Recording" to begin real-time translation
       - Speak naturally - translations are captured in the background
       - **Click 'Refresh Now' button** in Translation Output section to see new translations
       - Translations appear with detected language and audio playback
       - Click "Stop & Translate" when finished
       
    3. **Single-shot Mode**
       - Click "Start Recording" and speak into your microphone
       - Click "Stop & Translate" to process the recording
       - Results appear automatically
       
    4. **View Results**
       - In continuous mode: Click 'Refresh Now' to update the display
       - View translations with detected language
       - Play back translated audio using the playback buttons (if enabled)
       - Review history of all translations below
       
    ### Tips
    - **Continuous mode** is recommended for meetings and live events
    - **Remember to click 'Refresh Now'** to see new translations in continuous mode
    - Ensure microphone permissions are granted
    - Speak clearly and at a moderate pace
    - Translations are captured continuously but displayed when you refresh
    - Switch between languages naturally - automatic detection is active
    
    ### Use Cases
    - **Council Meetings:** Real-time bilingual English-Spanish translation
    - **Conferences:** Multi-language support with instant translations
    - **Training Sessions:** Accessible content in multiple languages
    - **Customer Service:** Real-time translation for support calls
    """)
