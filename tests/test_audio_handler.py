"""Pytest unit tests for audio_handler.py"""

import pytest
import numpy as np
from pathlib import Path
from unittest.mock import patch, MagicMock
import tempfile

from src.core.audio_handler import (
    AudioRecorder,
    AudioPlayer,
    AudioConverter,
    get_audio_devices,
    get_default_input_device,
    get_default_output_device
)


@pytest.fixture
def sample_audio_data():
    """Generate sample audio data for testing"""
    sample_rate = 16000
    duration = 1.0  # 1 second
    frequency = 440  # A4 note
    samples = np.arange(int(sample_rate * duration))
    audio_data = np.sin(2 * np.pi * frequency * samples / sample_rate).astype(np.float32)
    return audio_data


@pytest.fixture
def temp_wav_file(sample_audio_data):
    """Create a temporary WAV file for testing"""
    with tempfile.NamedTemporaryFile(suffix='.wav', delete=False) as f:
        temp_path = f.name
    
    # Write audio data to WAV file
    import soundfile as sf
    sf.write(temp_path, sample_audio_data, 16000)
    
    yield temp_path
    
    # Cleanup
    Path(temp_path).unlink(missing_ok=True)


class TestAudioDevices:
    """Tests for audio device detection functions"""
    
    @patch('sounddevice.query_devices')
    def test_get_audio_devices(self, mock_query):
        """Test getting all audio devices"""
        mock_devices = [
            {'name': 'Device 1', 'max_input_channels': 2, 'max_output_channels': 0},
            {'name': 'Device 2', 'max_input_channels': 0, 'max_output_channels': 2},
        ]
        mock_query.return_value = mock_devices
        
        devices = get_audio_devices()
        
        assert len(devices) == 2
        assert devices[0]['name'] == 'Device 1'
        mock_query.assert_called_once()
    
    @patch('sounddevice.query_devices')
    def test_get_default_input_device(self, mock_query):
        """Test getting default input device"""
        mock_device = {
            'name': 'Default Input',
            'max_input_channels': 2,
            'default_samplerate': 44100
        }
        mock_query.return_value = mock_device
        
        device = get_default_input_device()
        
        assert device['name'] == 'Default Input'
        assert device['max_input_channels'] == 2
        mock_query.assert_called_once_with(kind='input')
    
    @patch('sounddevice.query_devices')
    def test_get_default_output_device(self, mock_query):
        """Test getting default output device"""
        mock_device = {
            'name': 'Default Output',
            'max_output_channels': 2,
            'default_samplerate': 44100
        }
        mock_query.return_value = mock_device
        
        device = get_default_output_device()
        
        assert device['name'] == 'Default Output'
        assert device['max_output_channels'] == 2
        mock_query.assert_called_once_with(kind='output')


class TestAudioRecorder:
    """Tests for AudioRecorder class"""
    
    def test_init_default_params(self):
        """Test AudioRecorder initialization with default parameters"""
        recorder = AudioRecorder()
        
        assert recorder.sample_rate == 16000
        assert recorder.channels == 1
        assert recorder.chunk_duration_ms == 100
        assert recorder.chunk_size == 1600  # 16000 * 100 / 1000
        assert recorder.is_recording is False
        assert recorder.audio_data == []
    
    def test_init_custom_params(self):
        """Test AudioRecorder initialization with custom parameters"""
        recorder = AudioRecorder(sample_rate=44100, channels=2, chunk_duration_ms=50)
        
        assert recorder.sample_rate == 44100
        assert recorder.channels == 2
        assert recorder.chunk_duration_ms == 50
        assert recorder.chunk_size == 2205  # 44100 * 50 / 1000
    
    @patch('sounddevice.InputStream')
    def test_start_recording(self, mock_stream_class):
        """Test starting audio recording"""
        mock_stream = MagicMock()
        mock_stream_class.return_value = mock_stream
        
        recorder = AudioRecorder()
        recorder.start_recording()
        
        assert recorder.is_recording is True
        assert recorder.audio_data == []
    
    def test_stop_recording_returns_numpy_array(self):
        """Test stopping recording returns numpy array"""
        recorder = AudioRecorder()
        recorder.is_recording = True
        recorder.audio_data = [np.array([1, 2, 3]), np.array([4, 5, 6])]
        
        result = recorder.stop_recording()
        
        assert isinstance(result, np.ndarray)
        assert len(result) == 6
        assert recorder.is_recording is False
    
    def test_stop_recording_empty_data(self):
        """Test stopping recording with no data"""
        recorder = AudioRecorder()
        recorder.is_recording = True
        recorder.audio_data = []
        
        result = recorder.stop_recording()
        
        assert isinstance(result, np.ndarray)
        assert len(result) == 0
    
    @patch('soundfile.write')
    def test_save_to_file(self, mock_write, sample_audio_data):
        """Test saving audio to file"""
        recorder = AudioRecorder()
        
        filename = recorder.save_to_file(sample_audio_data, "test.wav")
        
        assert filename == "test.wav"
        mock_write.assert_called_once()
        args = mock_write.call_args
        # sf.write(filename, audio_data, sample_rate) - positional args
        assert args[0][0] == "test.wav"
        np.testing.assert_array_equal(args[0][1], sample_audio_data)
        assert args[0][2] == 16000
    
    @patch('soundfile.write')
    def test_save_to_file_default_filename(self, mock_write, sample_audio_data):
        """Test saving audio with auto-generated filename"""
        recorder = AudioRecorder()
        
        filename = recorder.save_to_file(sample_audio_data)
        
        assert filename.startswith("recording_")
        assert filename.endswith(".wav")
        mock_write.assert_called_once()


class TestAudioPlayer:
    """Tests for AudioPlayer class"""
    
    def test_init_default_params(self):
        """Test AudioPlayer initialization with default parameters"""
        player = AudioPlayer()
        
        assert player.sample_rate == 16000
    
    def test_init_custom_sample_rate(self):
        """Test AudioPlayer initialization with custom sample rate"""
        player = AudioPlayer(sample_rate=44100)
        
        assert player.sample_rate == 44100
    
    @patch('sounddevice.play')
    @patch('sounddevice.wait')
    def test_play_audio(self, mock_wait, mock_play, sample_audio_data):
        """Test playing audio data"""
        player = AudioPlayer()
        
        player.play_audio(sample_audio_data)
        
        mock_play.assert_called_once()
        mock_wait.assert_called_once()
        args = mock_play.call_args
        # sd.play(audio_data, sample_rate) - positional args
        np.testing.assert_array_equal(args[0][0], sample_audio_data)
        assert args[0][1] == 16000
    
    @patch('soundfile.read')
    @patch('sounddevice.play')
    @patch('sounddevice.wait')
    def test_play_file(self, mock_wait, mock_play, mock_read, sample_audio_data):
        """Test playing audio from file"""
        mock_read.return_value = (sample_audio_data, 16000)
        player = AudioPlayer()
        
        player.play_file("test.wav")
        
        mock_read.assert_called_once_with("test.wav")
        mock_play.assert_called_once()
        mock_wait.assert_called_once()
    
    @patch('soundfile.read')
    def test_play_file_not_found(self, mock_read):
        """Test playing non-existent file logs error but doesn't raise"""
        mock_read.side_effect = FileNotFoundError("File not found")
        player = AudioPlayer()
        
        # play_file catches exceptions and logs them, doesn't raise
        player.play_file("nonexistent.wav")
        mock_read.assert_called_once_with("nonexistent.wav")


class TestAudioConverter:
    """Tests for AudioConverter class"""
    
    def test_bytes_to_numpy_int16(self):
        """Test converting bytes to numpy array with int16 dtype"""
        test_bytes = b'\x00\x01\x02\x03\x04\x05\x06\x07'
        
        result = AudioConverter.bytes_to_numpy(test_bytes, dtype=np.int16)
        
        assert isinstance(result, np.ndarray)
        assert result.dtype == np.int16
        assert len(result) == 4  # 8 bytes / 2 bytes per int16
    
    def test_bytes_to_numpy_float32(self):
        """Test converting bytes to numpy array with float32 dtype"""
        test_bytes = b'\x00\x00\x00\x00\x00\x00\x80\x3f'
        
        result = AudioConverter.bytes_to_numpy(test_bytes, dtype=np.float32)
        
        assert isinstance(result, np.ndarray)
        assert result.dtype == np.float32
        assert len(result) == 2  # 8 bytes / 4 bytes per float32
    
    @patch('soundfile.read')
    def test_wav_to_numpy(self, mock_read, sample_audio_data):
        """Test loading WAV file to numpy array"""
        mock_read.return_value = (sample_audio_data, 16000)
        
        audio_data, sample_rate = AudioConverter.wav_to_numpy("test.wav")
        
        assert isinstance(audio_data, np.ndarray)
        assert sample_rate == 16000
        mock_read.assert_called_once_with("test.wav")
    
    @patch('soundfile.write')
    def test_numpy_to_wav(self, mock_write, sample_audio_data):
        """Test saving numpy array to WAV file"""
        AudioConverter.numpy_to_wav(sample_audio_data, 16000, "output.wav")
        
        mock_write.assert_called_once()
        args = mock_write.call_args
        assert args[0][0] == "output.wav"
        assert args[0][2] == 16000


class TestAudioIntegration:
    """Integration tests using actual file operations"""
    
    def test_record_save_and_load(self, temp_wav_file, sample_audio_data):
        """Test the full cycle: generate, save, load audio"""
        # Load the audio file
        audio_data, sample_rate = AudioConverter.wav_to_numpy(temp_wav_file)
        
        assert isinstance(audio_data, np.ndarray)
        assert sample_rate == 16000
        assert len(audio_data) > 0
    
    @patch('sounddevice.InputStream')
    @patch('soundfile.write')
    def test_record_and_save_workflow(self, mock_write, mock_stream_class):
        """Test complete recording workflow"""
        # Setup mocks
        mock_stream = MagicMock()
        mock_stream_class.return_value = mock_stream
        
        # Create recorder and record
        recorder = AudioRecorder(sample_rate=16000, channels=1)
        recorder.start_recording()
        
        # Simulate recorded data
        recorder.audio_data = [
            np.random.randn(1600).astype(np.float32),
            np.random.randn(1600).astype(np.float32)
        ]
        
        audio_data = recorder.stop_recording()
        filename = recorder.save_to_file(audio_data, "test_output.wav")
        
        assert len(audio_data) == 3200
        assert filename == "test_output.wav"
        mock_write.assert_called_once()


class TestEdgeCases:
    """Test edge cases and error conditions"""
    
    def test_empty_audio_data(self):
        """Test handling of empty audio data"""
        empty_data = np.array([], dtype=np.float32)
        
        # Empty data should not raise errors during conversion
        audio_bytes = empty_data.tobytes()
        assert len(audio_bytes) == 0
    
    @patch('soundfile.read')
    def test_corrupted_file_handling(self, mock_read):
        """Test handling of corrupted audio file"""
        mock_read.side_effect = RuntimeError("Corrupted file")
        
        with pytest.raises(RuntimeError):
            AudioConverter.wav_to_numpy("corrupted.wav")


if __name__ == "__main__":
    pytest.main([__file__, "-v", "--tb=short"])
