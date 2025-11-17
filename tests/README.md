# Test Suite

This directory contains unit tests for the Live Interpreter API Demo project.

## Test Structure

The test suite is organized into the following files:

### Pytest Unit Tests (Modern)

- **`test_audio_handler.py`** (23 tests) - Unit tests for audio recording, playback, and conversion functionality
- **`test_config.py`** (14 tests) - Unit tests for configuration settings and translator initialization
- **`test_continuous_translation_unit.py`** (15 tests) - Unit tests for continuous translation features

### Legacy Test Scripts

Legacy interactive test scripts have been moved to `tests/legacy/`:

- **`legacy/test_audio.py`** - Interactive audio device testing script
- **`legacy/test_continuous_translation.py`** - Interactive continuous translation testing script

## Running Tests

### Run All Pytest Tests

```bash
# From the project root directory
python -m pytest tests/ -v
```

### Run Specific Test File

```bash
# Run audio handler tests
python -m pytest tests/test_audio_handler.py -v

# Run config tests
python -m pytest tests/test_config.py -v

# Run continuous translation tests
python -m pytest tests/test_continuous_translation_unit.py -v
```

### Run Specific Test Class

```bash
# Run only AudioRecorder tests
python -m pytest tests/test_audio_handler.py::TestAudioRecorder -v

# Run only Settings tests
python -m pytest tests/test_config.py::TestSettings -v
```

### Run Specific Test

```bash
# Run a single test
python -m pytest tests/test_audio_handler.py::TestAudioRecorder::test_start_recording -v
```

### Run Tests with Coverage

```bash
# Install coverage if needed
pip install pytest-cov

# Run with coverage report
python -m pytest tests/ --cov=src --cov-report=html
```

### Run Only Modern Pytest Tests

```bash
# Skip legacy test scripts
python -m pytest tests/test_audio_handler.py tests/test_config.py tests/test_continuous_translation_unit.py -v
```

## Test Options

### Verbose Output
```bash
python -m pytest tests/ -v
```

### Show Print Statements
```bash
python -m pytest tests/ -s
```

### Stop on First Failure
```bash
python -m pytest tests/ -x
```

### Run Tests Matching Pattern
```bash
# Run all tests with "audio" in the name
python -m pytest tests/ -k "audio" -v
```

### Show Slowest Tests
```bash
python -m pytest tests/ --durations=10
```

## Test Requirements

The test suite requires the following packages (already in `pyproject.toml`):

- `pytest>=9.0.1`
- `pytest-mock>=3.15.1`
- `pytest-cov` (optional, for coverage reports)

Install test dependencies:

```bash
pip install -e ".[test]"
```

## Test Coverage

Current test coverage:

- **Audio Handler**: Full coverage of device detection, recording, playback, and conversion
- **Configuration**: Full coverage of Settings class and translator initialization
- **Translation**: Coverage of TranslationResult data structure and continuous translation callbacks

## Writing New Tests

When adding new tests, follow these guidelines:

1. Use pytest fixtures for setup/teardown
2. Mock external dependencies (Azure SDK, sounddevice, etc.)
3. Organize tests into classes by functionality
4. Use descriptive test names following `test_<feature>_<scenario>` pattern
5. Add docstrings to test functions
6. Test both success and error cases

Example test structure:

```python
import pytest
from unittest.mock import patch, MagicMock

class TestFeature:
    """Tests for specific feature"""
    
    @pytest.fixture
    def mock_dependency(self):
        """Create mock dependency"""
        return MagicMock()
    
    def test_feature_success_case(self, mock_dependency):
        """Test successful operation"""
        # Arrange
        # Act
        # Assert
        pass
    
    def test_feature_error_case(self, mock_dependency):
        """Test error handling"""
        # Arrange
        # Act
        # Assert
        pass
```

## Continuous Integration

These tests are designed to run in CI/CD pipelines without requiring actual audio hardware or Azure credentials.

## Troubleshooting

### Import Errors

If you encounter import errors, ensure you're running tests from the project root:

```bash
cd /path/to/live-interpreter-api-demo
python -m pytest tests/
```

### Audio Device Errors

The pytest unit tests mock all audio devices. If you see audio device errors, you may be running legacy test scripts instead of pytest tests.

### Azure SDK Errors

Pytest tests do not require Azure credentials. If you see Azure SDK errors, ensure you're using the pytest unit tests, not legacy scripts.

## Results Summary

Current test results: **52 passing tests** ✅

```
tests/test_audio_handler.py - 23 passed
tests/test_config.py - 14 passed
tests/test_continuous_translation_unit.py - 15 passed
```
