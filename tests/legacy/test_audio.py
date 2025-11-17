#!/usr/bin/env python3
"""Test script for audio_handler.py"""

import sys
import time
from pathlib import Path

# Add src to path
sys.path.insert(0, str(Path(__file__).parent))

from src.core.audio_handler import (
    AudioRecorder,
    AudioPlayer,
    AudioConverter,
    get_audio_devices,
    get_default_input_device,
    get_default_output_device
)

def test_device_detection():
    """Test audio device detection"""
    print("\n" + "="*60)
    print("TEST 1: Audio Device Detection")
    print("="*60)
    
    try:
        # Get all devices
        devices = get_audio_devices()
        print(f"\n✓ Found {len(devices)} audio devices")
        
        # Get default input
        input_device = get_default_input_device()
        print(f"✓ Default input device: {input_device['name']}")
        print(f"  - Channels: {input_device['max_input_channels']}")
        print(f"  - Sample rate: {input_device['default_samplerate']} Hz")
        
        # Get default output
        output_device = get_default_output_device()
        print(f"✓ Default output device: {output_device['name']}")
        print(f"  - Channels: {output_device['max_output_channels']}")
        print(f"  - Sample rate: {output_device['default_samplerate']} Hz")
        
        return True
    except Exception as e:
        print(f"✗ Device detection failed: {e}")
        return False


def test_audio_recorder():
    """Test audio recording"""
    print("\n" + "="*60)
    print("TEST 2: Audio Recording")
    print("="*60)
    
    try:
        recorder = AudioRecorder(sample_rate=16000, channels=1)
        print("✓ AudioRecorder initialized")
        
        # Test recording for 3 seconds
        print("\n🎤 Recording for 3 seconds... Please speak!")
        recorder.start_recording()
        time.sleep(3)
        audio_data = recorder.stop_recording()
        
        print("✓ Recording stopped")
        print(f"  - Duration: {len(audio_data)/16000:.2f} seconds")
        print(f"  - Samples: {len(audio_data)}")
        print(f"  - Shape: {audio_data.shape}")
        
        # Test saving to file
        filename = recorder.save_to_file(audio_data, "test_recording.wav")
        print(f"✓ Saved recording to: {filename}")
        
        return True, audio_data
    except Exception as e:
        print(f"✗ Recording failed: {e}")
        import traceback
        traceback.print_exc()
        return False, None


def test_audio_player(audio_data=None):
    """Test audio playback"""
    print("\n" + "="*60)
    print("TEST 3: Audio Playback")
    print("="*60)
    
    try:
        player = AudioPlayer(sample_rate=16000)
        print("✓ AudioPlayer initialized")
        
        if audio_data is not None:
            print("\n🔊 Playing back recorded audio...")
            player.play_audio(audio_data)
            print("✓ Playback completed")
        
        # Test playing from file
        try:
            print("\n🔊 Playing back from file...")
            player.play_file("test_recording.wav")
            print("✓ File playback completed")
        except FileNotFoundError:
            print("⚠ Skipping file playback (no test file)")
        
        return True
    except Exception as e:
        print(f"✗ Playback failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def test_audio_converter():
    """Test audio conversion utilities"""
    print("\n" + "="*60)
    print("TEST 4: Audio Conversion")
    print("="*60)
    
    try:
        import numpy as np
        
        # Test bytes to numpy conversion
        test_bytes = b'\x00\x01' * 100
        array = AudioConverter.bytes_to_numpy(test_bytes, dtype=np.int16)
        print(f"✓ Converted {len(test_bytes)} bytes to array of shape {array.shape}")
        
        # Test WAV loading if test file exists
        try:
            audio_data, sample_rate = AudioConverter.wav_to_numpy("test_recording.wav")
            print(f"✓ Loaded WAV file: {len(audio_data)} samples at {sample_rate} Hz")
        except FileNotFoundError:
            print("⚠ Skipping WAV loading test (no test file)")
        
        return True
    except Exception as e:
        print(f"✗ Conversion test failed: {e}")
        import traceback
        traceback.print_exc()
        return False


def main():
    """Run all tests"""
    print("\n" + "="*60)
    print("AUDIO HANDLER TEST SUITE")
    print("="*60)
    
    results = {}
    
    # Test 1: Device detection
    results['device_detection'] = test_device_detection()
    
    # Test 2: Audio recording
    recording_success, audio_data = test_audio_recorder()
    results['recording'] = recording_success
    
    # Test 3: Audio playback
    if recording_success and audio_data is not None:
        results['playback'] = test_audio_player(audio_data)
    else:
        print("\n⚠ Skipping playback test (recording failed)")
        results['playback'] = False
    
    # Test 4: Audio conversion
    results['conversion'] = test_audio_converter()
    
    # Summary
    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    
    for test_name, success in results.items():
        status = "✓ PASS" if success else "✗ FAIL"
        print(f"{status}: {test_name.replace('_', ' ').title()}")
    
    total_tests = len(results)
    passed_tests = sum(results.values())
    
    print(f"\nTotal: {passed_tests}/{total_tests} tests passed")
    
    if passed_tests == total_tests:
        print("\n🎉 All tests passed!")
        return 0
    else:
        print(f"\n⚠ {total_tests - passed_tests} test(s) failed")
        return 1


if __name__ == "__main__":
    try:
        exit_code = main()
        sys.exit(exit_code)
    except KeyboardInterrupt:
        print("\n\n⚠ Tests interrupted by user")
        sys.exit(130)
    except Exception as e:
        print(f"\n\n✗ Unexpected error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)
