"""Azure Speech Translation Service with Live Interpreter support"""

import logging
from typing import Callable, Dict, List, Optional
from dataclasses import dataclass
from datetime import datetime
import azure.cognitiveservices.speech as speechsdk
from pydantic import BaseModel
from .config import Settings

logger = logging.getLogger(__name__)


class TranslationResult(BaseModel):
    """Translation result data structure"""
    original_text: str
    detected_language: Optional[str]
    translations: Dict[str, str]
    timestamp: datetime
    audio_data: Optional[bytes] = None
    duration_ms: int = 0

@dataclass
class AzureSpeechTranslator:
    """Azure Speech Translation service with Live Interpreter support"""
    
    def __init__(self, settings: Settings):
        """
        Initialize the translator with Azure credentials
        
        Args:
            settings: Application settings containing Azure credentials
        """
        self.settings = settings
        self.translation_config: Optional[speechsdk.translation.SpeechTranslationConfig] = None
        self.recognizer: Optional[speechsdk.translation.TranslationRecognizer] = None
        self._setup_translation_config()
        
    def _setup_translation_config(self):
        """Set up Azure Speech Translation configuration"""
        try:
            # Create translation config
            if self.settings.speech_endpoint:
                self.translation_config = speechsdk.translation.SpeechTranslationConfig(
                    endpoint=self.settings.speech_endpoint,
                    subscription=self.settings.speech_key
                )
            else:
                self.translation_config = speechsdk.translation.SpeechTranslationConfig(
                    subscription=self.settings.speech_key,
                    region=self.settings.speech_region
                )
            
            # Set source language (can be overridden by auto-detect)
            self.translation_config.speech_recognition_language = self.settings.source_language
            
            # Add target languages
            for lang in self.settings.target_languages:
                self.translation_config.add_target_language(lang)
                logger.info(f"Added target language: {lang}")
            
            # Set voice for synthesis
            if self.settings.voice_name:
                self.translation_config.voice_name = self.settings.voice_name
                logger.info(f"Using voice: {self.settings.voice_name}")
            
            logger.info("Translation configuration initialized successfully")
            
        except Exception as e:
            logger.error(f"Failed to initialize translation config: {e}")
            raise
    
    def synthesize_translation(
        self,
        text: str,
        target_language: str
    ) -> Optional[bytes]:
        """
        Synthesize translated text to speech audio
        
        Args:
            text: Translated text to synthesize
            target_language: Target language code (e.g., 'es-ES')
            
        Returns:
            Audio bytes or None if synthesis fails
        """
        try:
            # Create speech config for synthesis
            if self.settings.speech_endpoint:
                speech_config = speechsdk.SpeechConfig(
                    endpoint=self.settings.speech_endpoint,
                    subscription=self.settings.speech_key
                )
            else:
                speech_config = speechsdk.SpeechConfig(
                    subscription=self.settings.speech_key,
                    region=self.settings.speech_region
                )
            
            # Get appropriate voice for target language
            voice_name = self.settings.get_voice_for_language(target_language)
            logger.info(f"Using voice {voice_name} for language {target_language}")
            speech_config.speech_synthesis_voice_name = voice_name
            
            # Create synthesizer with null output (we'll get the audio data directly)
            synthesizer = speechsdk.SpeechSynthesizer(
                speech_config=speech_config,
                audio_config=None
            )
            
            # Synthesize
            result = synthesizer.speak_text(text)
            
            if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
                logger.info(f"Synthesized {len(result.audio_data)} bytes for '{text[:50]}...' using {voice_name}")
                return result.audio_data
            elif result.reason == speechsdk.ResultReason.Canceled:
                cancellation = result.cancellation_details
                logger.error(f"Synthesis canceled: {cancellation.reason}")
                if cancellation.reason == speechsdk.CancellationReason.Error:
                    logger.error(f"Error: {cancellation.error_details}")
                return None
            else:
                logger.warning(f"Synthesis result: {result.reason}")
                return None
                
        except Exception as e:
            logger.error(f"Synthesis error: {e}")
            return None
    
    def create_recognizer_from_microphone(
        self,
        auto_detect_languages: Optional[List[str]] = None
    ) -> speechsdk.translation.TranslationRecognizer:
        """
        Create a translation recognizer from default microphone
        
        Args:
            auto_detect_languages: List of languages to detect automatically
            
        Returns:
            Translation recognizer configured for microphone input
        """
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        
        if auto_detect_languages and self.settings.enable_auto_detect:
            # Enable automatic language detection
            auto_detect_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
                languages=auto_detect_languages
            )
            recognizer = speechsdk.translation.TranslationRecognizer(
                translation_config=self.translation_config,
                audio_config=audio_config,
                auto_detect_source_language_config=auto_detect_config
            )
            logger.info(f"Created recognizer with auto-detection for: {auto_detect_languages}")
        else:
            recognizer = speechsdk.translation.TranslationRecognizer(
                translation_config=self.translation_config,
                audio_config=audio_config
            )
            logger.info("Created recognizer with fixed source language")
        
        return recognizer
    
    def create_recognizer_from_file(
        self,
        audio_file_path: str,
        auto_detect_languages: Optional[List[str]] = None
    ) -> speechsdk.translation.TranslationRecognizer:
        """
        Create a translation recognizer from audio file
        
        Args:
            audio_file_path: Path to audio file
            auto_detect_languages: List of languages to detect automatically
            
        Returns:
            Translation recognizer configured for file input
        """
        audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)
        
        if auto_detect_languages and self.settings.enable_auto_detect:
            auto_detect_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
                languages=auto_detect_languages
            )
            recognizer = speechsdk.translation.TranslationRecognizer(
                translation_config=self.translation_config,
                audio_config=audio_config,
                auto_detect_source_language_config=auto_detect_config
            )
        else:
            recognizer = speechsdk.translation.TranslationRecognizer(
                translation_config=self.translation_config,
                audio_config=audio_config
            )
        
        logger.info(f"Created recognizer for file: {audio_file_path}")
        return recognizer
    
    async def translate_once(
        self,
        recognizer: Optional[speechsdk.translation.TranslationRecognizer] = None
    ) -> TranslationResult:
        """
        Perform single-shot translation
        
        Args:
            recognizer: Optional recognizer to use, creates microphone recognizer if None
            
        Returns:
            TranslationResult with recognized and translated text
        """
        if recognizer is None:
            recognizer = self.create_recognizer_from_microphone()
        
        logger.info("Starting single-shot recognition...")
        result = recognizer.recognize_once()
        
        return self._process_result(result)
    
    def start_continuous_translation(
        self,
        recognizer: speechsdk.translation.TranslationRecognizer,
        recognizing_callback: Optional[Callable[[TranslationResult], None]] = None,
        recognized_callback: Optional[Callable[[TranslationResult], None]] = None,
        synthesizing_callback: Optional[Callable[[bytes], None]] = None,
        canceled_callback: Optional[Callable[[str], None]] = None,
        session_stopped_callback: Optional[Callable[[], None]] = None
    ):
        """
        Start continuous translation with callbacks
        
        Args:
            recognizer: Translation recognizer to use
            recognizing_callback: Called for interim results
            recognized_callback: Called for final results
            synthesizing_callback: Called when audio is synthesized
            canceled_callback: Called on cancellation
            session_stopped_callback: Called when session stops
        """
        # Connect event handlers
        if recognizing_callback:
            recognizer.recognizing.connect(
                lambda evt: recognizing_callback(self._process_result(evt.result))
            )
        
        if recognized_callback:
            recognizer.recognized.connect(
                lambda evt: recognized_callback(self._process_result(evt.result))
            )
        
        if synthesizing_callback:
            recognizer.synthesizing.connect(
                lambda evt: synthesizing_callback(evt.result.audio)
            )
        
        if canceled_callback:
            recognizer.canceled.connect(
                lambda evt: canceled_callback(str(evt.cancellation_details))
            )
        
        if session_stopped_callback:
            recognizer.session_stopped.connect(
                lambda evt: session_stopped_callback()
            )
        
        # Start continuous recognition
        recognizer.start_continuous_recognition()
        logger.info("Started continuous translation")
    
    def stop_continuous_translation(
        self,
        recognizer: speechsdk.translation.TranslationRecognizer
    ):
        """
        Stop continuous translation
        
        Args:
            recognizer: Translation recognizer to stop
        """
        recognizer.stop_continuous_recognition()
        logger.info("Stopped continuous translation")
    
    def _process_result(
        self,
        result: speechsdk.translation.TranslationRecognitionResult
    ) -> TranslationResult:
        """
        Process Speech SDK result into TranslationResult
        
        Args:
            result: Speech SDK translation result
            
        Returns:
            Processed TranslationResult
        """
        detected_language = None
        original_text = ""
        translations = {}
        audio_data = None
        
        if result.reason == speechsdk.ResultReason.TranslatedSpeech:
            original_text = result.text
            translations = dict(result.translations.items())
            
            # Try to get detected language
            try:
                detected_language = result.properties.get(
                    speechsdk.PropertyId.SpeechServiceConnection_AutoDetectSourceLanguageResult
                )
            except Exception:
                detected_language = self.settings.source_language
            
            # Get audio if available
            try:
                audio_data = result.audio
            except Exception:
                pass
            
            logger.info(f"Translated: '{original_text}' -> {list(translations.keys())}")
            
        elif result.reason == speechsdk.ResultReason.RecognizedSpeech:
            original_text = result.text
            logger.info(f"Recognized without translation: '{original_text}'")
            
        elif result.reason == speechsdk.ResultReason.NoMatch:
            logger.warning("No speech could be recognized")
            
        elif result.reason == speechsdk.ResultReason.Canceled:
            details = result.cancellation_details
            logger.error(f"Translation canceled: {details.reason}")
            if details.reason == speechsdk.CancellationReason.Error:
                logger.error(f"Error details: {details.error_details}")
        
        return TranslationResult(
            original_text=original_text,
            detected_language=detected_language,
            translations=translations,
            timestamp=datetime.now(),
            audio_data=audio_data,
            duration_ms=int(result.duration / 10000) if result.duration else 0  # duration is in 100-nanosecond units
        )


class LiveInterpreterTranslator(AzureSpeechTranslator):
    """
    Azure Live Interpreter for real-time speech translation
    
    Supports two voice modes:
    1. Personal Voice (requires Azure approval): Preserves speaker's voice characteristics
       Apply at: https://aka.ms/customneural
    2. Prebuilt Neural Voice (no approval needed): High-quality neural text-to-speech voices
    
    Voice mode is determined by the `voice_name` setting:
    - If voice_name == "personal-voice", uses personal voice mode
    - Otherwise, uses the specified prebuilt neural voice
    """
    
    def __init__(self, settings: Settings, use_personal_voice: Optional[bool] = None):
        """
        Initialize Live Interpreter translator
        
        Args:
            settings: Application settings
            use_personal_voice: Override voice mode. If None, determined from settings.voice_name.
                              If True, use personal voice (requires approval).
                              If False, use prebuilt neural voice specified in settings.
        """
        if not settings.enable_live_interpreter:
            raise ValueError("Live Interpreter is not enabled in settings")
        
        super().__init__(settings)
        # Determine voice mode from settings or override
        self.use_personal_voice = use_personal_voice if use_personal_voice is not None else settings.use_personal_voice
        self._configure_live_interpreter()
    
    def _configure_live_interpreter(self):
        """Configure Live Interpreter specific settings"""
        # Note: Continuous language ID mode is only for continuous recognition scenarios
        # For single-shot (file-based) recognition, we'll use at-start detection
        # This will be set per-recognizer in create_recognizer methods
        
        # Choose voice mode
        if self.use_personal_voice:
            # Use personal voice for natural speaker style preservation
            # Note: Requires approval from Azure
            self.translation_config.voice_name = "personal-voice"
            logger.info("Live Interpreter mode configured with personal voice (requires Azure approval)")
        else:
            # Use prebuilt neural voice specified in settings
            # This works immediately without special approval
            if self.settings.voice_name and self.settings.voice_name != "personal-voice":
                self.translation_config.voice_name = self.settings.voice_name
                logger.info(f"Live Interpreter mode configured with prebuilt neural voice: {self.settings.voice_name}")
            else:
                logger.warning("No prebuilt voice specified, using default voice")
        
        logger.info(f"Voice mode: {'Personal' if self.use_personal_voice else 'Prebuilt Neural'}")
    
    def create_recognizer_from_file(
        self,
        audio_file_path: str,
        auto_detect_languages: Optional[List[str]] = None
    ) -> speechsdk.translation.TranslationRecognizer:
        """
        Create Live Interpreter recognizer from audio file
        
        For file-based recognition, uses at-start language detection
        """
        audio_config = speechsdk.audio.AudioConfig(filename=audio_file_path)
        
        # For file-based single-shot recognition, use at-start detection
        # If no languages specified, use a reasonable set of common languages
        if auto_detect_languages is None or len(auto_detect_languages) == 0:
            auto_detect_languages = ["en-US", "es-ES", "fr-FR", "de-DE", "it-IT", "pt-BR", "zh-CN", "ja-JP", "ko-KR"]
        
        auto_detect_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
            languages=auto_detect_languages
        )
        
        recognizer = speechsdk.translation.TranslationRecognizer(
            translation_config=self.translation_config,
            audio_config=audio_config,
            auto_detect_source_language_config=auto_detect_config
        )
        
        logger.info(f"Created Live Interpreter recognizer for file: {audio_file_path}")
        return recognizer
    
    def create_recognizer_from_microphone(
        self,
        auto_detect_languages: Optional[List[str]] = None,
        use_continuous_mode: bool = True
    ) -> speechsdk.translation.TranslationRecognizer:
        """
        Create Live Interpreter recognizer from microphone
        
        For Live Interpreter, auto-detection is recommended
        
        Args:
            auto_detect_languages: List of languages to detect, or None for common languages
            use_continuous_mode: If True, enables continuous language ID (for continuous recognition)
                                If False, uses at-start detection (for single-shot)
        """
        # If no languages specified, use a reasonable set of common languages
        if auto_detect_languages is None or len(auto_detect_languages) == 0:
            auto_detect_languages = ["en-US", "es-ES", "fr-FR", "de-DE", "it-IT", "pt-BR", "zh-CN", "ja-JP", "ko-KR"]
        
        auto_detect_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
            languages=auto_detect_languages
        )
        
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        
        recognizer = speechsdk.translation.TranslationRecognizer(
            translation_config=self.translation_config,
            audio_config=audio_config,
            auto_detect_source_language_config=auto_detect_config
        )
        
        # Set continuous language ID mode only for continuous recognition
        if use_continuous_mode:
            recognizer.properties.set_property(
                property_id=speechsdk.PropertyId.SpeechServiceConnection_LanguageIdMode,
                value='Continuous'
            )
            logger.info(f"Created Live Interpreter recognizer with continuous language detection for: {auto_detect_languages}")
        else:
            logger.info(f"Created Live Interpreter recognizer with at-start language detection for: {auto_detect_languages}")
        
        return recognizer
