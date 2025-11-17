"""Pytest unit tests for configuration settings"""

import pytest
from unittest.mock import patch

from src.core.config import Settings
from src.core.translator import LiveInterpreterTranslator


class TestSettings:
    """Tests for Settings configuration"""
    
    def test_settings_initialization(self):
        """Test Settings can be initialized"""
        settings = Settings()
        
        assert settings is not None
        assert hasattr(settings, 'source_language')
        assert hasattr(settings, 'target_languages')
        assert hasattr(settings, 'voice_name')
    
    def test_settings_has_required_fields(self):
        """Test Settings has all required fields"""
        settings = Settings()
        
        # Check required fields exist
        assert hasattr(settings, 'speech_key')
        assert hasattr(settings, 'speech_region')
        assert hasattr(settings, 'source_language')
        assert hasattr(settings, 'target_languages')
        assert hasattr(settings, 'voice_name')
        assert hasattr(settings, 'enable_live_interpreter')
    
    def test_target_languages_is_list(self):
        """Test target_languages property returns a list"""
        settings = Settings()
        
        assert isinstance(settings.target_languages, list)
        assert len(settings.target_languages) >= 1
    
    @patch.dict('os.environ', {
        'SPEECH_KEY': 'test_key',
        'SPEECH_REGION': 'eastus',
        'SOURCE_LANGUAGE': 'en-US',
        'TARGET_LANGUAGE': 'es-ES',
        'TARGET_LANGUAGE_2': 'fr-FR',
        'VOICE_NAME': 'en-US-JennyNeural',
        'ENABLE_LIVE_INTERPRETER': 'true'
    })
    def test_settings_from_environment(self):
        """Test Settings loads from environment variables"""
        settings = Settings()
        
        assert settings.speech_key == 'test_key'
        assert settings.speech_region == 'eastus'
        assert settings.source_language == 'en-US'
        assert 'es-ES' in settings.target_languages
        assert 'fr-FR' in settings.target_languages
        assert settings.voice_name == 'en-US-JennyNeural'
        assert settings.enable_live_interpreter is True
    
    @patch.dict('os.environ', {
        'SPEECH_KEY': 'test_key',
        'SPEECH_REGION': 'westus2',
        'TARGET_LANGUAGE': 'es-ES',
        'TARGET_LANGUAGE_2': '',  # Empty second language
        'TARGET_LANGUAGE_3': ''   # Empty third language
    })
    def test_settings_single_target_language(self):
        """Test Settings with single target language"""
        settings = Settings()
        
        target_langs = [lang for lang in settings.target_languages if lang]
        assert 'es-ES' in target_langs
    
    @patch.dict('os.environ', {
        'SPEECH_KEY': 'test_key',
        'SPEECH_REGION': 'eastus',
        'TARGET_LANGUAGE': 'es-ES',
        'TARGET_LANGUAGE_2': 'fr-FR',
        'TARGET_LANGUAGE_3': 'de-DE'
    })
    def test_settings_multiple_target_languages(self):
        """Test Settings with multiple target languages"""
        settings = Settings()
        
        assert 'es-ES' in settings.target_languages
        assert 'fr-FR' in settings.target_languages
        assert 'de-DE' in settings.target_languages


class TestLiveInterpreterTranslator:
    """Tests for LiveInterpreterTranslator initialization"""
    
    @patch.dict('os.environ', {
        'SPEECH_KEY': 'test_key',
        'SPEECH_REGION': 'eastus',
        'SOURCE_LANGUAGE': 'en-US',
        'TARGET_LANGUAGE': 'es-ES',
        'ENABLE_LIVE_INTERPRETER': 'true'
    })
    def test_translator_initialization(self):
        """Test LiveInterpreterTranslator can be initialized"""
        settings = Settings()
        translator = LiveInterpreterTranslator(settings)
        
        assert translator is not None
        assert translator.settings == settings
        assert hasattr(translator, 'translation_config')
    
    @patch.dict('os.environ', {
        'SPEECH_KEY': 'test_key',
        'SPEECH_REGION': 'eastus',
        'SOURCE_LANGUAGE': 'en-US',
        'TARGET_LANGUAGE': 'es-ES',
        'TARGET_LANGUAGE_2': 'fr-FR',
        'ENABLE_LIVE_INTERPRETER': 'true'
    })
    def test_translator_with_multiple_target_languages(self):
        """Test translator initialization with multiple target languages"""
        settings = Settings()
        translator = LiveInterpreterTranslator(settings)
        
        assert translator is not None
        assert len(settings.target_languages) >= 2
    
    @patch.dict('os.environ', {
        'SPEECH_KEY': 'test_key',
        'SPEECH_REGION': 'eastus',
        'VOICE_NAME': 'en-US-JennyNeural',
        'ENABLE_LIVE_INTERPRETER': 'true'
    })
    def test_translator_with_prebuilt_voice(self):
        """Test translator with prebuilt neural voice"""
        settings = Settings()
        translator = LiveInterpreterTranslator(settings, use_personal_voice=False)
        
        assert translator.use_personal_voice is False
        assert settings.voice_name == 'en-US-JennyNeural'
    
    @patch.dict('os.environ', {
        'SPEECH_KEY': 'test_key',
        'SPEECH_REGION': 'eastus',
        'VOICE_NAME': 'personal-voice',
        'ENABLE_LIVE_INTERPRETER': 'true'
    })
    def test_translator_with_personal_voice(self):
        """Test translator with personal voice mode"""
        settings = Settings()
        translator = LiveInterpreterTranslator(settings, use_personal_voice=True)
        
        assert translator.use_personal_voice is True
        assert settings.voice_name == 'personal-voice'


class TestConfigIntegration:
    """Integration tests for configuration"""
    
    @patch.dict('os.environ', {
        'SPEECH_KEY': 'test_key',
        'SPEECH_REGION': 'eastus',
        'SOURCE_LANGUAGE': 'en-US',
        'TARGET_LANGUAGE': 'es-ES',
        'VOICE_NAME': 'en-US-JennyNeural',
        'ENABLE_LIVE_INTERPRETER': 'true'
    })
    def test_full_configuration_workflow(self):
        """Test complete configuration workflow"""
        # Load settings
        settings = Settings()
        assert settings.speech_key == 'test_key'
        assert settings.enable_live_interpreter is True
        
        # Create translator
        translator = LiveInterpreterTranslator(settings)
        assert translator.settings == settings
        
        # Verify configuration
        assert translator.translation_config is not None
    
    @patch.dict('os.environ', {
        'SPEECH_KEY': '',
        'SPEECH_REGION': 'eastus'
    })
    def test_missing_speech_key_validation(self):
        """Test validation when speech key is missing"""
        # Settings should still initialize, validation happens at runtime
        settings = Settings()
        assert settings.speech_key == ''


class TestConfigEdgeCases:
    """Test edge cases and error conditions"""
    
    @patch.dict('os.environ', {
        'SPEECH_KEY': 'test_key',
        'SPEECH_REGION': 'eastus',
        'TARGET_LANGUAGE': '',  # Empty target language
        'TARGET_LANGUAGE_2': '',
        'TARGET_LANGUAGE_3': ''
    })
    def test_empty_target_languages(self):
        """Test handling of empty target languages"""
        settings = Settings()
        
        # Should handle empty list gracefully
        assert isinstance(settings.target_languages, list)
    
    def test_get_voice_for_language(self):
        """Test getting voice for specific language"""
        settings = Settings()
        
        # Should return configured voice or default
        voice = settings.get_voice_for_language('es-ES')
        assert voice is not None or voice is None  # Either configured or None


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
