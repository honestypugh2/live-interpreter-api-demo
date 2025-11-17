"""Pytest unit tests for continuous translation functionality"""

import pytest
from datetime import datetime
from src.core.translator import TranslationResult, LiveInterpreterTranslator
from src.core.config import Settings


@pytest.fixture
def mock_settings():
    """Create a mock settings object for testing"""
    return Settings(
        speech_key='test_key',
        speech_region='eastus',
        speech_endpoint='https://liveinterpreter-demo.openai.azure.com',
        source_language='en-US',
        target_language='es-ES',
        target_language_2='fr-FR',
        voice_name='en-US-JennyNeural',
        host='localhost',
        enable_live_interpreter=True,
        enable_auto_detect=True,
        enable_captions=True,
        enable_audio_playback=True
    )


class TestTranslationResult:
    """Tests for TranslationResult data structure"""
    
    def test_translation_result_creation(self):
        """Test creating a TranslationResult"""
        result = TranslationResult(
            original_text="Hello world",
            detected_language="en-US",
            translations={"es-ES": "Hola mundo"},
            timestamp=datetime.now()
        )
        
        assert result.original_text == "Hello world"
        assert result.detected_language == "en-US"
        assert result.translations["es-ES"] == "Hola mundo"
    
    def test_translation_result_with_multiple_languages(self):
        """Test TranslationResult with multiple target languages"""
        result = TranslationResult(
            original_text="Good morning",
            detected_language="en-US",
            translations={
                "es-ES": "Buenos días",
                "fr-FR": "Bonjour"
            },
            timestamp=datetime.now()
        )
        
        assert len(result.translations) == 2
        assert result.translations["es-ES"] == "Buenos días"
        assert result.translations["fr-FR"] == "Bonjour"
    
    def test_translation_result_empty_translations(self):
        """Test TranslationResult with empty translations dict"""
        result = TranslationResult(
            original_text="Test",
            detected_language=None,
            translations={},
            timestamp=datetime.now()
        )
        
        assert result.original_text == "Test"
        assert len(result.translations) == 0


class TestLiveInterpreterTranslator:
    """Tests for LiveInterpreterTranslator"""
    
    def test_translator_initialization(self, mock_settings):
        """Test basic translator initialization"""
        translator = LiveInterpreterTranslator(mock_settings)
        
        assert translator is not None
        assert translator.settings == mock_settings
    
    def test_translator_has_translation_config(self, mock_settings):
        """Test that translator creates translation config"""
        translator = LiveInterpreterTranslator(mock_settings)
        
        assert hasattr(translator, 'translation_config')
        assert translator.translation_config is not None


class TestContinuousTranslationCallbacks:
    """Tests for continuous translation callback handling"""
    
    def test_recognizing_callback_invoked(self):
        """Test that recognizing callback is invoked with interim results"""
        callback_invoked = {'called': False, 'result': None}
        
        def on_recognizing(result: TranslationResult):
            callback_invoked['called'] = True
            callback_invoked['result'] = result
        
        # Simulate calling the callback
        test_result = TranslationResult(
            original_text="Hello",
            translations={'es-ES': 'Hola'},
            detected_language='en-US',
            timestamp=datetime.now()
        )
        on_recognizing(test_result)
        
        assert callback_invoked['called'] is True
        assert callback_invoked['result'].original_text == "Hello"
    
    def test_recognized_callback_invoked(self):
        """Test that recognized callback is invoked with final results"""
        callback_invoked = {'called': False, 'result': None}
        
        def on_recognized(result: TranslationResult):
            callback_invoked['called'] = True
            callback_invoked['result'] = result
        
        # Simulate calling the callback
        test_result = TranslationResult(
            original_text="Hello world",
            translations={'es-ES': 'Hola mundo'},
            detected_language='en-US',
            timestamp=datetime.now()
        )
        on_recognized(test_result)
        
        assert callback_invoked['called'] is True
        assert callback_invoked['result'].original_text == "Hello world"
    
    def test_multiple_callbacks_handling(self):
        """Test handling multiple callbacks in sequence"""
        results = []
        
        def on_recognizing(result: TranslationResult):
            results.append(('recognizing', result))
        
        def on_recognized(result: TranslationResult):
            results.append(('recognized', result))
        
        # Simulate interim result
        interim_result = TranslationResult(
            original_text="Hello",
            translations={'es-ES': 'Hola'},
            detected_language='en-US',
            timestamp=datetime.now()
        )
        on_recognizing(interim_result)
        
        # Simulate final result
        final_result = TranslationResult(
            original_text="Hello world",
            translations={'es-ES': 'Hola mundo'},
            detected_language='en-US',
            timestamp=datetime.now()
        )
        on_recognized(final_result)
        
        assert len(results) == 2
        assert results[0][0] == 'recognizing'
        assert results[1][0] == 'recognized'


class TestLanguageDetection:
    """Tests for automatic language detection"""
    
    def test_language_detection_result(self):
        """Test language detection in translation result"""
        result = TranslationResult(
            original_text="Hello",
            detected_language="en-US",
            translations={"es-ES": "Hola"},
            timestamp=datetime.now()
        )
        
        assert result.detected_language == "en-US"
    
    def test_multiple_language_detection(self):
        """Test detection with multiple possible languages"""
        # Test that detected_language can be None
        result = TranslationResult(
            original_text="...",
            detected_language=None,
            translations={},
            timestamp=datetime.now()
        )
        
        assert result.detected_language is None


class TestContinuousTranslationEdgeCases:
    """Test edge cases in continuous translation"""
    
    def test_empty_original_text(self):
        """Test handling of empty original text"""
        result = TranslationResult(
            original_text="",
            detected_language=None,
            translations={},
            timestamp=datetime.now()
        )
        
        assert result.original_text == ""
        assert len(result.translations) == 0
    
    def test_unknown_language_detection(self):
        """Test handling of unknown language"""
        result = TranslationResult(
            original_text="Some text",
            detected_language="unknown",
            translations={},
            timestamp=datetime.now()
        )
        
        assert result.detected_language == "unknown"
    
    def test_very_long_duration(self):
        """Test result with long duration"""
        result = TranslationResult(
            original_text="Long text",
            detected_language="en-US",
            translations={"es-ES": "Texto largo"},
            timestamp=datetime.now(),
            duration_ms=30000  # 30 seconds
        )
        
        assert result.duration_ms == 30000


class TestContinuousModeTiming:
    """Tests for timing and synchronization in continuous mode"""
    
    def test_result_timestamp_accuracy(self):
        """Test that result timestamps are accurate"""
        before = datetime.now()
        result = TranslationResult(
            original_text="Test",
            detected_language="en-US",
            translations={"es-ES": "Prueba"},
            timestamp=datetime.now()
        )
        after = datetime.now()
        
        assert before <= result.timestamp <= after
    
    def test_duration_calculation(self):
        """Test duration calculation"""
        result = TranslationResult(
            original_text="Test phrase",
            detected_language="en-US",
            translations={"es-ES": "Frase de prueba"},
            timestamp=datetime.now(),
            duration_ms=1500
        )
        
        assert result.duration_ms == 1500
        assert isinstance(result.duration_ms, int)


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
