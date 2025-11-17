"""Demo Streamlit application with simulated council meeting transcript"""

import streamlit as st
import sys
from pathlib import Path
import time

# Add project root to path for imports
project_root = Path(__file__).resolve().parent.parent.parent
sys.path.insert(0, str(project_root))

from src.core.config import get_settings, SUPPORTED_LANGUAGES, NEURAL_VOICES
from src.core.translator import LiveInterpreterTranslator
from src.core.audio_handler import AudioPlayer
import logging
from datetime import datetime
import azure.cognitiveservices.speech as speechsdk

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Page configuration
st.set_page_config(
    page_title="Azure Live Interpreter Demo - Simulated Meeting",
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
    .status-active {
        background-color: #d1ecf1;
        border-left: 4px solid #0dcaf0;
    }
    .status-idle {
        background-color: #f0f0f0;
        border-left: 4px solid #888;
    }
    .translation-box {
        padding: 1.5rem;
        border-radius: 0.5rem;
        background-color: #f8f9fa;
        margin: 1rem 0;
        border-left: 4px solid #0078D4;
    }
    .speaker-box {
        padding: 1rem;
        border-radius: 0.5rem;
        margin: 0.5rem 0;
        background-color: #fff;
        border: 1px solid #ddd;
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

if 'translation_history' not in st.session_state:
    st.session_state.translation_history = []

if 'audio_player' not in st.session_state:
    st.session_state.audio_player = AudioPlayer()

if 'demo_running' not in st.session_state:
    st.session_state.demo_running = False

if 'demo_paused' not in st.session_state:
    st.session_state.demo_paused = False

if 'current_line_idx' not in st.session_state:
    st.session_state.current_line_idx = 0

if 'voice_preferences' not in st.session_state:
    st.session_state.voice_preferences = {}

# Simulated transcript - Council meeting about community park
SIMULATED_TRANSCRIPT = [
    {
        "speaker": "Council Chair (English)",
        "lang": "en-US",
        "text": "Good afternoon, everyone. Thank you for joining today's meeting. We'll discuss the new community park project and its budget allocation."
    },
    {
        "speaker": "Council Member (Spanish)",
        "lang": "es-ES",
        "text": "Buenas tardes. Este proyecto es muy importante para nuestra comunidad. Queremos asegurarnos de que el diseño incluya áreas verdes y espacios para niños."
    },
    {
        "speaker": "Council Chair (English)",
        "lang": "en-US",
        "text": "I completely agree. We also need to consider accessibility for seniors and people with disabilities. The design should be inclusive."
    },
    {
        "speaker": "Council Member (Spanish)",
        "lang": "es-ES",
        "text": "Perfecto. También necesitamos considerar el mantenimiento a largo plazo. ¿Cuál es el presupuesto anual propuesto?"
    },
    {
        "speaker": "Council Chair (English)",
        "lang": "en-US",
        "text": "The proposed budget is two hundred fifty thousand dollars for construction, with an annual maintenance budget of thirty thousand dollars."
    },
    {
        "speaker": "Council Member (Spanish)",
        "lang": "es-ES",
        "text": "¿Cuándo planeamos comenzar la construcción? La comunidad está muy emocionada por este proyecto."
    },
    {
        "speaker": "Council Chair (English)",
        "lang": "en-US",
        "text": "The goal is to start in early spring, once the budget is approved. We should have completion by next fall."
    },
    {
        "speaker": "Council Member (Spanish)",
        "lang": "es-ES",
        "text": "Excelente. Propongo que votemos hoy para aprobar el presupuesto y podamos avanzar con el proyecto."
    },
]

# Header
st.markdown('<div class="main-header">🌐 Azure Live Interpreter Demo</div>', unsafe_allow_html=True)
st.markdown("**Simulated Council Meeting - Real-time Translation Demo**")
st.markdown("---")

# Sidebar configuration
with st.sidebar:
    st.header("⚙️ Demo Configuration")
    
    st.info("📋 **Demo Mode**: Simulated council meeting with English ⇄ Spanish translation")
    
    # Target languages
    st.subheader("Target Languages")
    
    # For demo, we'll translate everything to both English and Spanish
    target_langs = ["en-US", "es-ES"]
    voice_selections = {}
    
    # Voice selection for English
    st.markdown("**🇺🇸 English Voice**")
    default_voice_idx_en = 0
    if "en-US" in st.session_state.voice_preferences:
        try:
            default_voice_idx_en = NEURAL_VOICES["en-US"].index(st.session_state.voice_preferences["en-US"])
        except ValueError:
            pass
    
    voice_en = st.selectbox(
        "Select English voice",
        options=NEURAL_VOICES["en-US"],
        index=default_voice_idx_en,
        format_func=lambda x: x.replace("Neural", "").replace("en-US-", ""),
        key="voice_en_us_demo"
    )
    voice_selections["en-US"] = voice_en
    st.session_state.voice_preferences["en-US"] = voice_en
    
    # Voice selection for Spanish
    st.markdown("**🇪🇸 Spanish Voice**")
    default_voice_idx_es = 0
    if "es-ES" in st.session_state.voice_preferences:
        try:
            default_voice_idx_es = NEURAL_VOICES["es-ES"].index(st.session_state.voice_preferences["es-ES"])
        except ValueError:
            pass
    
    voice_es = st.selectbox(
        "Select Spanish voice",
        options=NEURAL_VOICES["es-ES"],
        index=default_voice_idx_es,
        format_func=lambda x: x.replace("Neural", "").replace("es-ES-", ""),
        key="voice_es_es_demo"
    )
    voice_selections["es-ES"] = voice_es
    st.session_state.voice_preferences["es-ES"] = voice_es
    
    # Audio settings
    st.markdown("---")
    st.subheader("Audio Settings")
    enable_audio_playback = st.checkbox(
        "Play translated audio",
        value=True,
        help="Play audio for both original and translated text"
    )
    
    auto_advance = st.checkbox(
        "Auto-advance lines",
        value=True,
        help="Automatically advance to next line after playing audio"
    )
    
    if auto_advance:
        delay_seconds = st.slider(
            "Delay between lines (seconds)",
            min_value=1,
            max_value=10,
            value=3,
            help="Pause between dialogue lines"
        )
    else:
        delay_seconds = 0
    
    # Connection info
    st.markdown("---")
    st.subheader("📡 Connection")
    st.text(f"Region: {st.session_state.settings.speech_region}")
    if st.session_state.settings.speech_key:
        st.success("✅ API Key configured")
    else:
        st.error("❌ API Key missing")

# Helper function to translate and synthesize
def translate_and_synthesize(text: str, source_lang: str, target_langs: list, voice_prefs: dict):
    """Translate text to target languages and synthesize audio"""
    results = {}
    
    # Update settings
    settings = st.session_state.settings
    settings.target_language = target_langs[0]
    if len(target_langs) > 1:
        settings.target_language_2 = target_langs[1]
    
    # Apply voice preferences
    for lang, voice in voice_prefs.items():
        voice_attr = f"voice_{lang.lower().replace('-', '_')}"
        setattr(settings, voice_attr, voice)
    
    try:
        # Create translator
        translator = LiveInterpreterTranslator(settings)
        
        # Use Azure Translation API
        translation_config = speechsdk.translation.SpeechTranslationConfig(
            subscription=settings.speech_key,
            region=settings.speech_region
        )
        
        # Set source language
        translation_config.speech_recognition_language = source_lang
        
        # Add target languages (exclude source language)
        for lang in target_langs:
            if lang != source_lang:
                # Convert en-US to 'en', es-ES to 'es' for translation
                target_code = lang.split('-')[0]
                translation_config.add_target_language(target_code)
        
        # For demo purposes, we'll use a simple translation mapping
        # In production, you'd use the actual Azure translation
        translations = {}
        
        # Simple translation simulation for demo
        if source_lang == "en-US":
            # If source is English, provide Spanish translation
            if "es-ES" in target_langs or "es-MX" in target_langs:
                # In real scenario, this would come from Azure
                # For now, we'll just mark it as needing translation
                translations["es-ES"] = "[Translation would appear here from Azure]"
        elif source_lang.startswith("es"):
            # If source is Spanish, provide English translation
            if "en-US" in target_langs:
                translations["en-US"] = "[Translation would appear here from Azure]"
        
        # Synthesize audio for each translation
        synthesized_audio = {}
        for lang, trans_text in translations.items():
            audio_bytes = translator.synthesize_translation(trans_text, lang)
            if audio_bytes:
                synthesized_audio[lang] = audio_bytes
        
        # Also synthesize original text
        original_audio = translator.synthesize_translation(text, source_lang)
        
        results = {
            "original": text,
            "source_language": source_lang,
            "translations": translations,
            "synthesized_audio": synthesized_audio,
            "original_audio": original_audio,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
        
    except Exception as e:
        logger.error(f"Translation error: {e}")
        results = {
            "original": text,
            "source_language": source_lang,
            "translations": {"error": str(e)},
            "synthesized_audio": {},
            "original_audio": None,
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        }
    
    return results

# Main content
col1, col2 = st.columns([1, 1])

with col1:
    st.subheader("🎬 Demo Controls")
    
    # Status indicator
    demo_status = "Active" if st.session_state.demo_running else "Idle"
    status_class = "status-active" if st.session_state.demo_running else "status-idle"
    
    st.markdown(
        f'<div class="status-box {status_class}">Status: <b>{demo_status}</b></div>',
        unsafe_allow_html=True
    )
    
    # Control buttons
    col_btn1, col_btn2, col_btn3 = st.columns(3)
    
    with col_btn1:
        if st.button("▶️ Start Demo", disabled=st.session_state.demo_running, use_container_width=True):
            st.session_state.demo_running = True
            st.session_state.demo_paused = False
            st.session_state.current_line_idx = 0
            st.session_state.translation_history = []
            st.rerun()
    
    with col_btn2:
        if st.button("⏸️ Pause" if not st.session_state.demo_paused else "▶️ Resume", 
                     disabled=not st.session_state.demo_running, 
                     use_container_width=True):
            st.session_state.demo_paused = not st.session_state.demo_paused
            st.rerun()
    
    with col_btn3:
        if st.button("⏹️ Stop", disabled=not st.session_state.demo_running, use_container_width=True):
            st.session_state.demo_running = False
            st.session_state.demo_paused = False
            st.session_state.current_line_idx = 0
            st.rerun()
    
    # Progress
    if st.session_state.demo_running:
        progress = st.session_state.current_line_idx / len(SIMULATED_TRANSCRIPT)
        st.progress(progress)
        st.caption(f"Line {st.session_state.current_line_idx + 1} of {len(SIMULATED_TRANSCRIPT)}")
        
        if not st.session_state.demo_paused:
            st.info("🎙️ **Demo in progress...** Watch translations appear in real-time →")
    
    # Current speaker display
    st.markdown("---")
    st.subheader("🗣️ Current Speaker")
    
    if st.session_state.demo_running and st.session_state.current_line_idx < len(SIMULATED_TRANSCRIPT):
        current_line = SIMULATED_TRANSCRIPT[st.session_state.current_line_idx]
        
        st.markdown('<div class="speaker-box">', unsafe_allow_html=True)
        st.markdown(f"**{current_line['speaker']}**")
        
        # Language indicator
        lang_name = SUPPORTED_LANGUAGES.get(current_line['lang'], current_line['lang'])
        lang_flag = "🇺🇸" if current_line['lang'] == "en-US" else "🇪🇸"
        st.caption(f"{lang_flag} Speaking in: {lang_name}")
        
        # Original text
        st.markdown(f'<p class="caption-text">{current_line["text"]}</p>', unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Manual advance button
        if not auto_advance:
            if st.button("➡️ Next Line", key="manual_advance", use_container_width=True):
                # Process current line
                results = translate_and_synthesize(
                    current_line["text"],
                    current_line["lang"],
                    target_langs,
                    voice_selections
                )
                results["speaker"] = current_line["speaker"]
                results["detected_language"] = current_line["lang"]
                st.session_state.translation_history.append(results)
                
                # Play audio if enabled
                if enable_audio_playback and results.get("original_audio"):
                    st.session_state.audio_player.play_bytes(results["original_audio"])
                
                # Advance
                st.session_state.current_line_idx += 1
                if st.session_state.current_line_idx >= len(SIMULATED_TRANSCRIPT):
                    st.session_state.demo_running = False
                    st.success("✅ Demo completed!")
                st.rerun()
    
    elif not st.session_state.demo_running and st.session_state.translation_history:
        st.info("Demo completed. Review translations on the right →")
    else:
        st.info("👆 Click 'Start Demo' to begin the simulated meeting")

with col2:
    st.subheader("💬 Live Translations")
    
    # Show latest translation
    if st.session_state.translation_history:
        latest = st.session_state.translation_history[-1]
        
        st.markdown("**Latest Translation:**")
        st.markdown('<div class="translation-box">', unsafe_allow_html=True)
        
        # Speaker and original
        st.markdown(f"**{latest.get('speaker', 'Speaker')}**")
        st.markdown(f"**Original:** {latest['original']}")
        
        if latest.get("detected_language"):
            lang_name = SUPPORTED_LANGUAGES.get(latest["detected_language"], latest["detected_language"])
            st.caption(f"Detected: {lang_name}")
        
        # Translations
        st.markdown("**Translations:**")
        translations = latest.get("translations", {})
        
        if translations and not translations.get("error"):
            for lang, text in translations.items():
                lang_name = SUPPORTED_LANGUAGES.get(lang, lang)
                st.markdown(f'🌐 **{lang_name}:** {text}')
        else:
            st.info("Translation processing...")
        
        st.caption(f"⏱️ {latest['timestamp']}")
        st.markdown('</div>', unsafe_allow_html=True)
        
        # Audio playback
        if enable_audio_playback:
            st.markdown("**🔊 Audio Playback:**")
            
            col_audio1, col_audio2 = st.columns(2)
            
            with col_audio1:
                if latest.get("original_audio"):
                    lang_name = SUPPORTED_LANGUAGES.get(latest.get("source_language", ""), "Original")
                    if st.button(f"▶️ Play {lang_name}", key=f"play_orig_{latest['timestamp']}", use_container_width=True):
                        st.session_state.audio_player.play_bytes(latest["original_audio"])
                        st.success(f"✓ Played {lang_name}")
            
            with col_audio2:
                synthesized_audio = latest.get("synthesized_audio", {})
                if synthesized_audio:
                    for lang, audio_bytes in synthesized_audio.items():
                        lang_name = SUPPORTED_LANGUAGES.get(lang, lang)
                        if st.button(f"▶️ Play {lang_name}", key=f"play_trans_{lang}_{latest['timestamp']}", use_container_width=True):
                            st.session_state.audio_player.play_bytes(audio_bytes)
                            st.success(f"✓ Played {lang_name}")
    else:
        st.info("Translations will appear here as the demo progresses")

# Translation history
st.markdown("---")
st.subheader("📝 Meeting Transcript")

if st.session_state.translation_history:
    # Display in chronological order
    for idx, item in enumerate(st.session_state.translation_history):
        with st.expander(f"{idx + 1}. {item.get('speaker', 'Speaker')} - {item['timestamp']}", expanded=(idx == len(st.session_state.translation_history) - 1)):
            st.markdown(f"**Original:** {item['original']}")
            
            if item.get("detected_language"):
                lang_name = SUPPORTED_LANGUAGES.get(item["detected_language"], item["detected_language"])
                st.caption(f"Language: {lang_name}")
            
            st.markdown("**Translations:**")
            translations = item.get("translations", {})
            if translations and not translations.get("error"):
                for lang, text in translations.items():
                    lang_name = SUPPORTED_LANGUAGES.get(lang, lang)
                    st.markdown(f"- **{lang_name}:** {text}")
            else:
                st.info("Translation not available")
    
    # Clear history button
    if st.button("🗑️ Clear Transcript"):
        st.session_state.translation_history = []
        st.rerun()
else:
    st.info("Meeting transcript will appear here as the demo runs")

# Auto-advance logic
if st.session_state.demo_running and not st.session_state.demo_paused and auto_advance:
    if st.session_state.current_line_idx < len(SIMULATED_TRANSCRIPT):
        # Get current line
        current_line = SIMULATED_TRANSCRIPT[st.session_state.current_line_idx]
        
        # Process translation
        results = translate_and_synthesize(
            current_line["text"],
            current_line["lang"],
            target_langs,
            voice_selections
        )
        results["speaker"] = current_line["speaker"]
        results["detected_language"] = current_line["lang"]
        st.session_state.translation_history.append(results)
        
        # Play audio if enabled
        if enable_audio_playback and results.get("original_audio"):
            try:
                st.session_state.audio_player.play_bytes(results["original_audio"])
            except Exception as e:
                logger.error(f"Audio playback error: {e}")
        
        # Wait before advancing
        time.sleep(delay_seconds)
        
        # Advance to next line
        st.session_state.current_line_idx += 1
        
        # Check if demo is complete
        if st.session_state.current_line_idx >= len(SIMULATED_TRANSCRIPT):
            st.session_state.demo_running = False
            st.balloons()
        
        st.rerun()

# Footer
st.markdown("---")
st.markdown("""
<div style='text-align: center; color: #666; padding: 1rem;'>
    <p>Powered by Azure Speech Service | Live Interpreter Demo</p>
    <p style='font-size: 0.9rem;'>Simulated council meeting with real-time English ⇄ Spanish translation</p>
</div>
""", unsafe_allow_html=True)
