"""Audio handling utilities for capture and playback"""

import logging
import os
from typing import Optional, Callable
import numpy as np
import sounddevice as sd
import soundfile as sf
from datetime import datetime

logger = logging.getLogger(__name__)


class AudioRecorder:
    """Record audio from microphone"""
    
    def __init__(
        self,
        sample_rate: int = 16000,
        channels: int = 1,
        chunk_duration_ms: int = 100
    ):
        """
        Initialize audio recorder
        
        Args:
            sample_rate: Audio sample rate in Hz
            channels: Number of audio channels (1=mono, 2=stereo)
            chunk_duration_ms: Duration of each audio chunk in milliseconds
        """
        self.sample_rate = sample_rate
        self.channels = channels
        self.chunk_duration_ms = chunk_duration_ms
        self.chunk_size = int(sample_rate * chunk_duration_ms / 1000)
        self.is_recording = False
        self.audio_data = []
        
    def start_recording(self, callback: Optional[Callable[[np.ndarray], None]] = None):
        """
        Start recording audio
        
        Args:
            callback: Optional callback function called for each audio chunk
        """
        self.is_recording = True
        self.audio_data = []
        
        def audio_callback(indata, frames, time_info, status):
            if status:
                logger.warning(f"Audio callback status: {status}")
            
            if self.is_recording:
                self.audio_data.append(indata.copy())
                if callback:
                    callback(indata.copy())
        
        self.stream = sd.InputStream(
            samplerate=self.sample_rate,
            channels=self.channels,
            callback=audio_callback,
            blocksize=self.chunk_size
        )
        self.stream.start()
        logger.info("Started audio recording")
    
    def stop_recording(self) -> np.ndarray:
        """
        Stop recording and return recorded audio
        
        Returns:
            NumPy array of recorded audio data
        """
        self.is_recording = False
        if hasattr(self, 'stream'):
            self.stream.stop()
            self.stream.close()
        
        if self.audio_data:
            audio_array = np.concatenate(self.audio_data, axis=0)
            logger.info(f"Stopped recording. Duration: {len(audio_array)/self.sample_rate:.2f}s")
            return audio_array
        else:
            logger.warning("No audio data recorded")
            return np.array([])
    
    def save_to_file(self, audio_data: np.ndarray, filename: Optional[str] = None) -> str:
        """
        Save audio data to WAV file
        
        Args:
            audio_data: NumPy array of audio data
            filename: Output filename (auto-generated if None)
            
        Returns:
            Path to saved file
        """
        if filename is None:
            timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
            filename = f"recording_{timestamp}.wav"
        
        # Ensure directory exists
        os.makedirs(os.path.dirname(filename) if os.path.dirname(filename) else ".", exist_ok=True)
        
        sf.write(filename, audio_data, self.sample_rate)
        logger.info(f"Saved audio to: {filename}")
        return filename


class AudioPlayer:
    """Play audio through speakers"""
    
    def __init__(self, sample_rate: int = 16000):
        """
        Initialize audio player
        
        Args:
            sample_rate: Audio sample rate in Hz
        """
        self.sample_rate = sample_rate
    
    def play_audio(self, audio_data: np.ndarray):
        """
        Play audio data
        
        Args:
            audio_data: NumPy array of audio data to play
        """
        try:
            sd.play(audio_data, self.sample_rate)
            sd.wait()
            logger.info(f"Played audio: {len(audio_data)/self.sample_rate:.2f}s")
        except Exception as e:
            logger.error(f"Error playing audio: {e}")
    
    def play_file(self, filename: str):
        """
        Play audio from file
        
        Args:
            filename: Path to audio file
        """
        try:
            audio_data, sample_rate = sf.read(filename)
            sd.play(audio_data, sample_rate)
            sd.wait()
            logger.info(f"Played file: {filename}")
        except Exception as e:
            logger.error(f"Error playing file: {e}")
    
    def play_bytes(self, audio_bytes: bytes, sample_rate: Optional[int] = None):
        """
        Play audio from bytes
        
        Args:
            audio_bytes: Audio data as bytes (supports WAV, raw PCM)
            sample_rate: Sample rate (uses instance default if None)
        """
        if sample_rate is None:
            sample_rate = self.sample_rate
        
        try:
            # Check if it's a WAV file (has RIFF header)
            if audio_bytes[:4] == b'RIFF':
                # It's a WAV file with headers, use wave module to parse
                import wave
                import io
                
                wav_buffer = io.BytesIO(audio_bytes)
                with wave.open(wav_buffer, 'rb') as wav_file:
                    sample_rate = wav_file.getframerate()
                    n_channels = wav_file.getnchannels()
                    audio_data = wav_file.readframes(wav_file.getnframes())
                    
                    # Convert to numpy array
                    if wav_file.getsampwidth() == 2:  # 16-bit
                        audio_array = np.frombuffer(audio_data, dtype=np.int16).astype(np.float32) / 32768.0
                    elif wav_file.getsampwidth() == 1:  # 8-bit
                        audio_array = np.frombuffer(audio_data, dtype=np.uint8).astype(np.float32) / 128.0 - 1.0
                    else:
                        raise ValueError(f"Unsupported sample width: {wav_file.getsampwidth()}")
                    
                    # Reshape for multi-channel audio
                    if n_channels > 1:
                        audio_array = audio_array.reshape(-1, n_channels)
            else:
                # Assume raw 16-bit PCM audio
                audio_array = np.frombuffer(audio_bytes, dtype=np.int16).astype(np.float32) / 32768.0
            
            sd.play(audio_array, sample_rate)
            sd.wait()
            logger.info(f"Played audio: {len(audio_bytes)} bytes at {sample_rate}Hz")
        except Exception as e:
            logger.error(f"Error playing audio bytes: {e}")
            import traceback
            traceback.print_exc()
            raise


class AudioConverter:
    """Convert between audio formats"""
    
    @staticmethod
    def numpy_to_wav(audio_data: np.ndarray, sample_rate: int, output_file: str):
        """
        Convert NumPy array to WAV file
        
        Args:
            audio_data: NumPy array of audio data
            sample_rate: Audio sample rate
            output_file: Output WAV filename
        """
        sf.write(output_file, audio_data, sample_rate)
        logger.info(f"Converted NumPy array to WAV: {output_file}")
    
    @staticmethod
    def wav_to_numpy(input_file: str) -> tuple[np.ndarray, int]:
        """
        Load WAV file to NumPy array
        
        Args:
            input_file: Input WAV filename
            
        Returns:
            Tuple of (audio_data, sample_rate)
        """
        audio_data, sample_rate = sf.read(input_file)
        logger.info(f"Loaded WAV to NumPy array: {input_file}")
        return audio_data, sample_rate
    
    @staticmethod
    def bytes_to_numpy(audio_bytes: bytes, dtype=np.int16) -> np.ndarray:
        """
        Convert audio bytes to NumPy array
        
        Args:
            audio_bytes: Raw audio bytes
            dtype: Data type for conversion
            
        Returns:
            NumPy array of audio data
        """
        return np.frombuffer(audio_bytes, dtype=dtype)


def get_audio_devices():
    """
    Get list of available audio devices
    
    Returns:
        List of audio device information
    """
    devices = sd.query_devices()
    logger.info(f"Found {len(devices)} audio devices")
    return devices


def get_default_input_device():
    """
    Get default input device information
    
    Returns:
        Dictionary with device information
    """
    device = sd.query_devices(kind='input')
    logger.info(f"Default input device: {device['name']}")
    return device


def get_default_output_device():
    """
    Get default output device information
    
    Returns:
        Dictionary with device information
    """
    device = sd.query_devices(kind='output')
    logger.info(f"Default output device: {device['name']}")
    return device
