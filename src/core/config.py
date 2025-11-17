"""Configuration management for the application"""

from typing import List, Optional
from pathlib import Path
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings from environment variables"""
    
    model_config = SettingsConfigDict(
        env_file=str(Path(__file__).parent.parent.parent / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore"
    )
    
    # Azure Speech Service
    speech_key: str
    speech_region: str
    speech_endpoint: Optional[str] = None
    
    # Translation settings
    source_language: str = "en-US"
    target_language: str = "es-ES"
    target_language_2: Optional[str] = "en-US"
    target_language_3: Optional[str] = None
    
    # Voice settings
    voice_name: str = "en-US-JennyNeural"  # Default to prebuilt neural voice
    
    # Voice preferences per language (optional overrides)
    voice_en_us: Optional[str] = None
    voice_en_gb: Optional[str] = None
    voice_es_es: Optional[str] = None
    voice_es_mx: Optional[str] = None
    voice_fr_fr: Optional[str] = None
    voice_de_de: Optional[str] = None
    voice_it_it: Optional[str] = None
    voice_pt_br: Optional[str] = None
    voice_zh_cn: Optional[str] = None
    voice_ja_jp: Optional[str] = None
    voice_ko_kr: Optional[str] = None
    
    # Application settings
    log_level: str = "INFO"
    audio_buffer_ms: int = 100
    save_audio_files: bool = False
    
    # FastAPI backend
    backend_host: str = "0.0.0.0"
    backend_port: int = 8000
    cors_origins: str = "http://localhost:5173,http://localhost:3000"
    
    # Streamlit
    streamlit_server_port: int = 8501
    streamlit_server_address: str = "localhost"
    
    # Feature flags
    enable_live_interpreter: bool = True
    enable_auto_detect: bool = True
    enable_captions: bool = True
    enable_audio_playback: bool = True
    
    @property
    def target_languages(self) -> List[str]:
        """Get list of all configured target languages"""
        languages = [self.target_language]
        if self.target_language_2:
            languages.append(self.target_language_2)
        if self.target_language_3:
            languages.append(self.target_language_3)
        return languages
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Parse CORS origins string into list"""
        return [origin.strip() for origin in self.cors_origins.split(",")]
    
    @property
    def use_personal_voice(self) -> bool:
        """Check if personal voice is configured"""
        return self.voice_name == "personal-voice"
    
    def get_voice_for_language(self, language_code: str) -> str:
        """
        Get the configured voice for a specific language
        
        Args:
            language_code: Language code (e.g., 'es-ES')
            
        Returns:
            Voice name to use for this language
        """
        # Check for language-specific voice preference
        voice_attr = f"voice_{language_code.lower().replace('-', '_')}"
        preferred_voice = getattr(self, voice_attr, None)
        
        if preferred_voice:
            return preferred_voice
        
        # Use helper function from module
        return get_voice_for_language(language_code, None)


def get_settings() -> Settings:
    """Get application settings singleton"""
    return Settings()


# Language codes for common translations
SUPPORTED_LANGUAGES = {
    "en-US": "English (United States)",
    "en-GB": "English (United Kingdom)",
    "es-ES": "Spanish (Spain)",
    "es-MX": "Spanish (Mexico)",
    "fr-FR": "French (France)",
    "fr-CA": "French (Canada)",
    "de-DE": "German (Germany)",
    "it-IT": "Italian (Italy)",
    "pt-BR": "Portuguese (Brazil)",
    "pt-PT": "Portuguese (Portugal)",
    "zh-CN": "Chinese (Mandarin, Simplified)",
    "zh-TW": "Chinese (Mandarin, Traditional)",
    "ja-JP": "Japanese (Japan)",
    "ko-KR": "Korean (Korea)",
    "ar-SA": "Arabic (Saudi Arabia)",
    "hi-IN": "Hindi (India)",
    "ru-RU": "Russian (Russia)",
    "nl-NL": "Dutch (Netherlands)",
    "pl-PL": "Polish (Poland)",
    "sv-SE": "Swedish (Sweden)",
}

# Neural voice options for common languages
NEURAL_VOICES = {
    "en-US": [
        "en-US-JennyNeural",
        "en-US-GuyNeural", 
        "en-US-AriaNeural",
        "en-US-DavisNeural",
        "en-US-AmberNeural",
        "en-US-AnaNeural",
        "en-US-AndrewNeural",
        "en-US-EmmaNeural",
        "en-US-BrianNeural"
    ],
    "en-GB": [
        "en-GB-SoniaNeural",
        "en-GB-RyanNeural",
        "en-GB-LibbyNeural",
        "en-GB-AbbiNeural"
    ],
    "es-ES": [
        "es-ES-ElviraNeural",
        "es-ES-AlvaroNeural",
        "es-ES-AbrilNeural",
        "es-ES-ArnauNeural",
        "es-ES-DarioNeural",
        "es-ES-EliasNeural",
        "es-ES-EstrellaNeural",
        "es-ES-IreneNeural",
        "es-ES-LaiaNeural",
        "es-ES-LiaNeural"
    ],
    "es-MX": [
        "es-MX-DaliaNeural",
        "es-MX-JorgeNeural",
        "es-MX-BeatrizNeural",
        "es-MX-CandelaNeural",
        "es-MX-CarlotaNeural",
        "es-MX-CecilioNeural",
        "es-MX-GerardoNeural",
        "es-MX-LibertoNeural",
        "es-MX-LucianoNeural",
        "es-MX-MarinaNeural"
    ],
    "fr-FR": ["fr-FR-DeniseNeural", "fr-FR-HenriNeural", "fr-FR-BrigitteNeural", "fr-FR-AlainNeural"],
    "fr-CA": ["fr-CA-SylvieNeural", "fr-CA-JeanNeural", "fr-CA-AntoineNeural"],
    "de-DE": ["de-DE-KatjaNeural", "de-DE-ConradNeural", "de-DE-AmalaNeural", "de-DE-BerndNeural"],
    "it-IT": ["it-IT-ElsaNeural", "it-IT-DiegoNeural", "it-IT-IsabellaNeural", "it-IT-BenignoNeural"],
    "pt-BR": ["pt-BR-FranciscaNeural", "pt-BR-AntonioNeural", "pt-BR-BrendaNeural", "pt-BR-DonatoNeural"],
    "pt-PT": ["pt-PT-RaquelNeural", "pt-PT-DuarteNeural"],
    "zh-CN": ["zh-CN-XiaoxiaoNeural", "zh-CN-YunyangNeural", "zh-CN-XiaoyiNeural", "zh-CN-YunjianNeural"],
    "ja-JP": ["ja-JP-NanamiNeural", "ja-JP-KeitaNeural", "ja-JP-AoiNeural", "ja-JP-DaichiNeural"],
    "ko-KR": ["ko-KR-SunHiNeural", "ko-KR-InJoonNeural", "ko-KR-BongJinNeural", "ko-KR-GookMinNeural"],
    "ar-SA": ["ar-SA-ZariyahNeural", "ar-SA-HamedNeural"],
    "hi-IN": ["hi-IN-SwaraNeural", "hi-IN-MadhurNeural"],
    "ru-RU": ["ru-RU-SvetlanaNeural", "ru-RU-DmitryNeural"],
    "nl-NL": ["nl-NL-ColetteNeural", "nl-NL-MaartenNeural"],
    "pl-PL": ["pl-PL-AgnieszkaNeural", "pl-PL-MarekNeural"],
    "sv-SE": ["sv-SE-SofieNeural", "sv-SE-MattiasNeural"],
}

# Default voice selection per language (first choice from NEURAL_VOICES)
DEFAULT_VOICES = {
    lang: voices[0] for lang, voices in NEURAL_VOICES.items()
}

def get_voice_for_language(language_code: str, preferred_voice: Optional[str] = None) -> str:
    """
    Get appropriate voice for a language
    
    Args:
        language_code: Language code (e.g., 'es-ES')
        preferred_voice: Optional preferred voice name
        
    Returns:
        Voice name to use
    """
    # If preferred voice is specified and valid for this language, use it
    if preferred_voice and language_code in NEURAL_VOICES:
        if preferred_voice in NEURAL_VOICES[language_code]:
            return preferred_voice
    
    # Otherwise use default for this language
    if language_code in DEFAULT_VOICES:
        return DEFAULT_VOICES[language_code]
    
    # Fallback to Jenny if language not found
    return "en-US-JennyNeural"
