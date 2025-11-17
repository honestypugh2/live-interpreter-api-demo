#!/usr/bin/env python3
"""
Test script for continuous language ID mode with continuous recognition

This script tests the Live Interpreter's ability to detect and translate
multiple languages in real-time during continuous speech recognition.
"""

import sys
import time
import logging
from pathlib import Path
from typing import List
from dataclasses import dataclass

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.config import Settings
from src.core.translator import LiveInterpreterTranslator, TranslationResult
from src.core.audio_handler import AudioPlayer

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

@dataclass
class ContinuousTranslationTester:
    """Test continuous translation with language detection"""
    
    def __init__(self, settings: Settings, enable_audio_playback: bool = True):
        """Initialize the tester
        
        Args:
            settings: Configuration settings
            enable_audio_playback: Whether to play audio for translations
        """
        self.settings = settings
        self.translator = LiveInterpreterTranslator(settings)
        self.audio_player = AudioPlayer() if enable_audio_playback else None
        self.enable_audio_playback = enable_audio_playback
        self.results: List[TranslationResult] = []
        self.is_running = False
        
    def on_recognizing(self, result: TranslationResult):
        """Handle interim recognition results"""
        if result.original_text:
            detected = result.detected_language or "Unknown"
            print(f"\n[Recognizing - {detected}] {result.original_text}")
            if result.translations:
                for lang, text in result.translations.items():
                    print(f"  → {lang}: {text}")
    
    def on_recognized(self, result: TranslationResult):
        """Handle final recognition results"""
        if result.original_text:
            detected = result.detected_language or "Unknown"
            print(f"\n[RECOGNIZED - {detected}] {result.original_text}")
            
            if result.translations:
                for lang, text in result.translations.items():
                    print(f"  → {lang}: {text}")
                
                # Synthesize and play audio for translations
                if self.enable_audio_playback and self.audio_player:
                    print(f"  [Synthesizing audio for {len(result.translations)} translation(s)...]")
                    for lang, text in result.translations.items():
                        try:
                            audio_bytes = self.translator.synthesize_translation(text, lang)
                            if audio_bytes:
                                print(f"  [▶️  Playing {lang}...]")
                                self.audio_player.play_bytes(audio_bytes)
                                time.sleep(0.5)  # Brief pause between languages
                        except Exception as e:
                            logger.error(f"Failed to play audio for {lang}: {e}")
                            print(f"  [❌ Playback error for {lang}]")
            
            # Store result
            self.results.append(result)
            
            # Show statistics
            print(f"  Duration: {result.duration_ms}ms")
            print(f"  Timestamp: {result.timestamp.strftime('%H:%M:%S.%f')[:-3]}")
    
    def on_synthesizing(self, audio_data: bytes):
        """Handle audio synthesis"""
        if audio_data:
            print(f"  [Audio synthesized: {len(audio_data)} bytes]")
    
    def on_canceled(self, details: str):
        """Handle cancellation"""
        print(f"\n[CANCELED] {details}")
        logger.error(f"Translation canceled: {details}")
    
    def on_session_stopped(self):
        """Handle session stop"""
        print("\n[SESSION STOPPED]")
        self.is_running = False
    
    def test_microphone_continuous(self, duration_seconds: int = 30, languages: List[str] = None):
        """
        Test continuous translation from microphone
        
        Args:
            duration_seconds: How long to run the test
            languages: List of languages to detect, or None for common languages
        """
        # Use common languages if not specified
        if languages is None:
            languages = ["en-US", "es-ES", "fr-FR", "de-DE", "it-IT", "pt-BR", "zh-CN", "ja-JP", "ko-KR"]
        
        print("\n" + "="*80)
        print("TEST: Continuous Translation from Microphone")
        print("="*80)
        print("\nConfiguration:")
        print(f"  - Duration: {duration_seconds} seconds")
        print(f"  - Detection languages: {', '.join(languages)}")
        print(f"  - Target languages: {self.settings.target_languages}")
        print(f"  - Voice mode: {'Personal' if self.translator.use_personal_voice else 'Prebuilt Neural'}")
        print(f"  - Voice name: {self.settings.voice_name}")
        print(f"  - Audio playback: {'Enabled' if self.enable_audio_playback else 'Disabled'}")
        
        # Create recognizer with continuous language detection
        print("\n[INFO] Creating recognizer with continuous language ID...")
        recognizer = self.translator.create_recognizer_from_microphone(
            auto_detect_languages=languages,
            use_continuous_mode=True
        )
        
        print("\n[INFO] Starting continuous translation...")
        print("=" * 80)
        print("🎤 SPEAK IN DIFFERENT LANGUAGES - TRANSLATION IN PROGRESS")
        print("=" * 80)
        print("\nTips:")
        print("  • Speak clearly in any language")
        print("  • The system will automatically detect language changes")
        print("  • Switch between languages naturally")
        print("  • Try multiple sentences in each language")
        print("\n" + "-"*80 + "\n")
        
        # Start continuous recognition with callbacks
        self.is_running = True
        self.translator.start_continuous_translation(
            recognizer=recognizer,
            recognizing_callback=self.on_recognizing,
            recognized_callback=self.on_recognized,
            synthesizing_callback=self.on_synthesizing,
            canceled_callback=self.on_canceled,
            session_stopped_callback=self.on_session_stopped
        )
        
        # Run for specified duration
        try:
            start_time = time.time()
            while self.is_running and (time.time() - start_time) < duration_seconds:
                remaining = duration_seconds - int(time.time() - start_time)
                if remaining % 10 == 0 and remaining > 0:
                    print(f"\n[INFO] {remaining} seconds remaining...")
                time.sleep(1)
        except KeyboardInterrupt:
            print("\n\n[INFO] Test interrupted by user")
        finally:
            # Stop recognition
            print("\n[INFO] Stopping continuous translation...")
            self.translator.stop_continuous_translation(recognizer)
            time.sleep(1)  # Give it time to clean up
        
        # Show summary
        self._show_summary()
    
    def test_file_continuous(self, audio_file: str, languages: List[str] = None):
        """
        Test continuous translation from audio file
        
        Args:
            audio_file: Path to audio file
            languages: List of languages to detect, or None for common languages
        """
        # Use common languages if not specified
        if languages is None:
            languages = ["en-US", "es-ES", "fr-FR", "de-DE", "it-IT", "pt-BR", "zh-CN", "ja-JP", "ko-KR"]
        
        print("\n" + "="*80)
        print("TEST: Continuous Translation from Audio File")
        print("="*80)
        print(f"\nFile: {audio_file}")
        print(f"Detection languages: {', '.join(languages)}")
        print(f"Target languages: {self.settings.target_languages}")
        
        # Create recognizer from file
        print("\n[INFO] Creating recognizer from file...")
        recognizer = self.translator.create_recognizer_from_file(
            audio_file_path=audio_file,
            auto_detect_languages=languages
        )
        
        print("[INFO] Starting continuous translation...")
        print("-"*80 + "\n")
        
        # Start continuous recognition
        self.is_running = True
        self.translator.start_continuous_translation(
            recognizer=recognizer,
            recognizing_callback=self.on_recognizing,
            recognized_callback=self.on_recognized,
            synthesizing_callback=self.on_synthesizing,
            canceled_callback=self.on_canceled,
            session_stopped_callback=self.on_session_stopped
        )
        
        # Wait for completion
        try:
            while self.is_running:
                time.sleep(0.5)
        except KeyboardInterrupt:
            print("\n\n[INFO] Test interrupted by user")
            self.translator.stop_continuous_translation(recognizer)
        
        # Show summary
        self._show_summary()
    
    def _show_summary(self):
        """Show test summary"""
        print("\n" + "="*80)
        print("TEST SUMMARY")
        print("="*80)
        
        if not self.results:
            print("\n⚠ No results captured")
            return
        
        print(f"\n✓ Total utterances recognized: {len(self.results)}")
        
        # Count languages detected
        languages = {}
        for result in self.results:
            lang = result.detected_language or "Unknown"
            languages[lang] = languages.get(lang, 0) + 1
        
        print("\n✓ Languages detected:")
        for lang, count in sorted(languages.items(), key=lambda x: x[1], reverse=True):
            print(f"  - {lang}: {count} utterance(s)")
        
        # Show translation coverage
        translation_langs = set()
        for result in self.results:
            translation_langs.update(result.translations.keys())
        
        print(f"\n✓ Translations generated for: {', '.join(sorted(translation_langs))}")
        
        # Show average duration
        avg_duration = sum(r.duration_ms for r in self.results) / len(self.results)
        print(f"\n✓ Average utterance duration: {avg_duration:.0f}ms")
        
        # Show sample results
        print("\n✓ Sample results:")
        for i, result in enumerate(self.results[:3], 1):
            lang = result.detected_language or "Unknown"
            print(f"\n  {i}. [{lang}] {result.original_text}")
            for tlang, ttext in result.translations.items():
                print(f"     → {tlang}: {ttext}")


def test_basic_continuous(enable_audio_playback: bool = True):
    """Run basic continuous translation test
    
    Args:
        enable_audio_playback: Whether to play translated audio
    """
    print("\n" + "="*80)
    print("BASIC CONTINUOUS TRANSLATION TEST")
    print("="*80)
    
    try:
        # Load settings
        settings = Settings()
        
        # Verify Live Interpreter is enabled
        if not settings.enable_live_interpreter:
            print("\n⚠ Live Interpreter is not enabled in settings")
            print("  Set ENABLE_LIVE_INTERPRETER=true in .env file")
            return False
        
        # Create tester with audio playback option
        tester = ContinuousTranslationTester(settings, enable_audio_playback=enable_audio_playback)
        
        # Run microphone test (30 seconds)
        tester.test_microphone_continuous(duration_seconds=30)
        
        return True
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_file_continuous(enable_audio_playback: bool = True):
    """Run continuous translation test on audio file
    
    Args:
        enable_audio_playback: Whether to play translated audio
    """
    print("\n" + "="*80)
    print("FILE-BASED CONTINUOUS TRANSLATION TEST")
    print("="*80)
    
    try:
        # Load settings
        settings = Settings()
        
        # Create tester with audio playback option
        tester = ContinuousTranslationTester(settings, enable_audio_playback=enable_audio_playback)
        
        # Check for test audio file
        audio_file = "test_recording.wav"
        if not Path(audio_file).exists():
            print(f"\n⚠ Audio file not found: {audio_file}")
            print("  Run test_audio.py first to create a test recording")
            return False
        
        # Run file test
        tester.test_file_continuous(audio_file)
        
        return True
        
    except Exception as e:
        logger.error(f"Test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Main test runner"""
    print("\n" + "="*80)
    print("CONTINUOUS LANGUAGE ID MODE TEST SUITE")
    print("="*80)
    print("\nThis test suite validates continuous translation with automatic")
    print("language detection for the Azure Live Interpreter service.")
    
    print("\n\nAvailable tests:")
    print("  1. Microphone - Continuous translation from microphone (30s)")
    print("  2. File - Continuous translation from audio file")
    print("  3. Both - Run both tests")
    print("  q. Quit")
    
    choice = input("\nSelect test (1-3, q): ").strip()
    
    if choice.lower() == 'q':
        print("\nExiting...")
        return
    
    # Ask about audio playback
    playback_choice = input("\nEnable audio playback? (y/n, default=y): ").strip().lower()
    enable_audio = playback_choice != 'n'
    
    if enable_audio:
        print("✓ Audio playback enabled - translations will be played as they arrive")
    else:
        print("✓ Audio playback disabled - only text output")
    
    if choice == '1':
        success = test_basic_continuous(enable_audio_playback=enable_audio)
    elif choice == '2':
        success = test_file_continuous(enable_audio_playback=enable_audio)
    elif choice == '3':
        success = test_basic_continuous(enable_audio_playback=enable_audio)
        if success:
            input("\nPress Enter to continue to file test...")
            success = test_file_continuous(enable_audio_playback=enable_audio)
    else:
        print("\n⚠ Invalid choice")
        return
    
    # Final result
    print("\n" + "="*80)
    if success:
        print("✓ TEST COMPLETED SUCCESSFULLY")
    else:
        print("✗ TEST FAILED")
    print("="*80 + "\n")


if __name__ == "__main__":
    main()
