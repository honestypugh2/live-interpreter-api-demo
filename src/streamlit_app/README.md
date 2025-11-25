# Streamlit App - Azure Live Interpreter

This directory contains the Streamlit-based user interface for the Azure Live Interpreter demo.

## Features

- 🎤 **One-click Audio Recording**: Simple interface to capture audio from microphone
- 🌐 **Real-time Translation**: Instant translation to multiple target languages
- 🔍 **Auto Language Detection**: Live Interpreter mode automatically detects source language
- 💬 **Live Captions**: Display translations as text captions
- 🔊 **Audio Playback**: Play back synthesized translated audio
- 📝 **Translation History**: Review past translations with timestamps
- ⚙️ **Easy Configuration**: Sidebar settings for quick adjustments

## Running the App

### Prerequisites

1. Verify uv is installed:
   ```bash
   uv --version
   ```
   
   If not installed:
   ```bash
   # Unix/macOS/Linux
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows
   powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Or using pip
   pip install uv
   ```

2. Install dependencies:
   ```bash
   # From project root
   uv sync
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

2. Configure environment variables in `.env`:
   ```env
   SPEECH_KEY=your_azure_speech_key
   SPEECH_REGION=eastus
   SOURCE_LANGUAGE=en-US
   TARGET_LANGUAGE=es-ES
   ```

### Start the App

```bash
cd src/streamlit_app
streamlit run app.py
```

The app will open in your browser at `http://localhost:8501`

## Usage

1. **Configure Settings** (Sidebar)
   - Toggle "Use Live Interpreter" for automatic language detection
   - Select source and target languages
   - Enable/disable audio playback

2. **Record Audio**
   - Click "Start Recording" button
   - Speak into your microphone
   - Click "Stop & Translate" when finished

3. **View Results**
   - Original text displays in the top section
   - Translations appear for each configured target language
   - Click "Play Translated Audio" to hear the translation

4. **Review History**
   - Scroll down to see all previous translations
   - Expand any item to view details
   - Click "Clear History" to reset

## Configuration Options

### Translation Modes

**Standard Mode**
- Specify exact source language
- Translate to 1-2 target languages
- Uses neural voices for synthesis

**Live Interpreter Mode** (Recommended for meetings)
- Automatic source language detection
- Low-latency speech-to-speech translation
- Personal voice preservation
- Requires Azure approval

### Supported Languages

Common language pairs for council meetings:
- English (en-US) ↔ Spanish (es-ES, es-MX)
- English (en-US) ↔ French (fr-FR)
- English (en-US) ↔ Mandarin (zh-CN)
- English (en-US) ↔ Portuguese (pt-BR)

See full list in sidebar dropdown.

## Tips for Best Results

### Audio Quality
- Use a quality USB microphone or conference mic
- Minimize background noise
- Speak at normal conversational pace
- Position microphone 6-12 inches from speaker

### Network
- Stable internet connection (10+ Mbps recommended)
- Close bandwidth-intensive applications
- Consider wired connection for critical meetings

### Usage Patterns
- **Quick Tests**: Use single-shot mode with Start/Stop buttons
- **Meetings**: Enable Live Interpreter for continuous translation
- **Review**: Check translation history for accuracy

## Troubleshooting

### "Failed to load settings" error
- Check that `.env` file exists in project root
- Verify `SPEECH_KEY` and `SPEECH_REGION` are set
- Ensure region supports Live Interpreter if enabled

### "No microphone detected"
- Grant microphone permissions in browser/OS
- Check that microphone is plugged in and working
- Try selecting different audio device in system settings

### "Translation not working"
- Verify Azure credentials are correct
- Check internet connection
- Ensure Speech Service resource is active in Azure portal
- Review logs in terminal for error messages

### High latency or delays
- Check network speed (run speed test)
- Close other applications using bandwidth
- Consider using closer Azure region
- Disable audio playback if only text needed

## Customization

### Styling
Modify the CSS in `app.py` to change colors, fonts, and layout:
```python
st.markdown("""
<style>
    .main-header {
        color: #0078D4;  /* Change header color */
    }
</style>
""", unsafe_allow_html=True)
```

### Languages
Add more languages by editing `SUPPORTED_LANGUAGES` in `src/core/config.py`

### Audio Settings
Adjust sample rate, chunk size, and buffer settings in audio recorder initialization

## Architecture

```
streamlit_app/
├── app.py                    # Main application
├── components/               # Reusable UI components (future)
│   ├── audio_recorder.py    # Audio recording component
│   ├── language_selector.py # Language selection UI
│   ├── translation_display.py # Translation results display
│   └── audio_player.py      # Audio playback component
└── README.md                # This file
```

## Performance

- **Startup Time**: ~2-3 seconds
- **Translation Latency**: 200-500ms (network dependent)
- **Memory Usage**: ~150-250MB
- **CPU Usage**: Low (5-10% on modern processors)

## Deployment

### Local Network
Share with other computers on same network:
```bash
streamlit run app.py --server.address=0.0.0.0
```
Access from other devices using: `http://<your-ip>:8501`

### Cloud Hosting
Deploy to Streamlit Cloud for public access:
1. Push code to GitHub
2. Connect repository to Streamlit Cloud
3. Add secrets for `SPEECH_KEY` and `SPEECH_REGION`
4. Deploy

See main README for production deployment options.

## Support

For issues specific to the Streamlit app:
- Check Streamlit documentation: https://docs.streamlit.io
- Review session state management for any state issues
- Enable debug logging in `.env`: `LOG_LEVEL=DEBUG`

For Azure Speech Service issues:
- See main project README.md
- Check Azure Speech Service documentation
- Review Azure portal for service health
