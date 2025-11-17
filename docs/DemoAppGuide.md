# Demo Apps - Simulated Council Meeting

## Overview

This project includes **two demo versions** that simulate a bilingual council meeting without requiring live audio input:

1. **Streamlit Demo** (`app_demo.py`) - Python-based with real Azure TTS
2. **React Demo** (`AppDemo.tsx`) - Browser-only, no backend required

Both are perfect for:

- **Demonstrations** to stakeholders and at trade shows
- **Testing** translation and voice features
- **Training** sessions for users
- **Showcasing** capabilities without microphone setup

## Streamlit Demo App

### Features

### 🎭 Simulated Meeting
- Pre-scripted English/Spanish council meeting dialogue
- 8 lines of realistic conversation about a community park project
- Automatic speaker alternation between English and Spanish

### 🎤 Voice Customization
- Select from 9+ English neural voices
- Select from 10+ Spanish neural voices
- Real-time audio synthesis for all dialogue

### ⚙️ Playback Controls
- **Manual Mode**: Click through dialogue line-by-line
- **Auto Mode**: Automatic progression with configurable delays
- Pause/Resume functionality
- Progress tracking

### 🌐 Real-time Translation
- Live translation display as dialogue progresses
- Shows original text and speaker
- Displays translations in target languages
- Audio playback for both original and translated speech

## Running the Streamlit Demo

### Quick Start

```bash
cd src/streamlit_app
streamlit run app_demo.py
```

### Using the Demo

1. **Configure Voices** (Left Sidebar)
   - Choose your preferred English voice (e.g., Jenny, Guy, Aria)
   - Choose your preferred Spanish voice (e.g., Elvira, Alvaro)
   - Enable/disable audio playback
   - Set auto-advance mode and delay

2. **Start Demo**
   - Click "▶️ Start Demo" button
   - Watch as dialogue appears line-by-line
   - Translations appear in real-time on the right

3. **Control Playback**
   - **Auto Mode**: Demo advances automatically with delays
   - **Manual Mode**: Click "➡️ Next Line" to advance
   - **Pause**: Pause the demo at any time
   - **Stop**: End demo and review transcript

4. **Review Transcript**
   - Full meeting transcript appears at the bottom
   - Expand any line to see original and translations
   - Clear transcript to start fresh

## Simulated Meeting Content

The demo includes a realistic council meeting discussing:
- Community park project proposal
- Budget allocation ($250,000 construction + $30,000/year maintenance)
- Accessibility considerations
- Construction timeline
- Budget approval vote

### Sample Dialogue

**English Speaker:**
> "Good afternoon, everyone. Thank you for joining today's meeting. We'll discuss the new community park project and its budget allocation."

**Spanish Speaker:**
> "Buenas tardes. Este proyecto es muy importante para nuestra comunidad. Queremos asegurarnos de que el diseño incluya áreas verdes y espacios para niños."

## Customization

### Adding Your Own Transcript

Edit the `SIMULATED_TRANSCRIPT` list in `app_demo.py`:

```python
SIMULATED_TRANSCRIPT = [
    {
        "speaker": "Speaker Name",
        "lang": "en-US",  # or "es-ES", "fr-FR", etc.
        "text": "Your dialogue here"
    },
    # Add more lines...
]
```

### Supported Languages

- `en-US` - English (United States)
- `en-GB` - English (United Kingdom)
- `es-ES` - Spanish (Spain)
- `es-MX` - Spanish (Mexico)
- `fr-FR` - French (France)
- And many more (see `config.py`)

### Adjusting Timing

Modify the delay slider in the sidebar (1-10 seconds) to control:
- Pause between dialogue lines
- Time for audio playback
- Reading time for translations

## Use Cases

### 1. Sales Demonstrations
Show potential clients how the system works without needing:
- Live speakers
- Microphone setup
- Network connectivity issues

### 2. Training Sessions
Train users on:
- How translations appear
- Voice selection options
- Reviewing meeting transcripts
- Audio playback features

### 3. Testing Voice Options
Quickly test all available voices:
- Hear different voice personalities
- Compare male vs. female voices
- Test accent variations (Spain vs. Mexico Spanish)

### 4. Feature Showcase
Demonstrate specific features:
- Real-time translation accuracy
- Audio synthesis quality
- Multi-language support
- Transcript generation

## Technical Details

### Translation Approach
The demo uses Azure Speech SDK for:
- Text-to-speech synthesis (original audio)
- Voice selection per language
- Audio playback

**Note:** For the demo, translations are simulated. The real `app.py` uses Azure's Live Interpreter API for actual translation. You can integrate real translation by:
1. Using Azure Translation API
2. Implementing the Live Interpreter recognizer
3. Processing actual audio streams

### Performance
- No audio recording required
- No microphone permissions needed
- Fast playback (only synthesis latency)
- Predictable demonstration flow

## Comparison with Full App

| Feature | app_demo.py | app.py |
|---------|-------------|--------|
| Audio Input | ❌ Simulated | ✅ Live Microphone |
| Translation | ⚠️ Demo/Simulated | ✅ Real Azure API |
| Voice Synthesis | ✅ Real Azure TTS | ✅ Real Azure TTS |
| Playback Control | ✅ Manual/Auto | ⏺️ Real-time only |
| Use Case | Demo/Training | Production Use |

## Troubleshooting

### No Audio Playing
- Check that "Play translated audio" is enabled
- Verify system audio is working
- Ensure Azure Speech key is valid

### Demo Not Starting
- Check Azure credentials in `.env` file
- Verify `SPEECH_KEY` and `SPEECH_REGION` are set
- Check terminal for error messages

### Slow Performance
- Reduce delay between lines
- Disable audio playback for faster demo
- Check internet connection speed

## React Demo App

### Features

- **No Backend Required**: Runs entirely in the browser
- **No Azure API Calls**: Pre-scripted translations for demos
- **Instant Startup**: No Python or backend dependencies
- **Modern UI**: Responsive React interface with Tailwind CSS
- **Perfect for Trade Shows**: No internet or Azure credentials needed after initial load

### Running the React Demo

```bash
cd src/react_app
./start-demo.sh  # Windows: start-demo.bat
```

Or manually:
```bash
cd src/react_app/frontend
npm run dev:demo
```

Open browser to `http://localhost:5173`

### Demo Features

1. **Simulated Council Meeting**
   - Same 8-line English/Spanish dialogue as Streamlit demo
   - Pre-defined translations display instantly

2. **Demo Controls**
   - Start/Pause/Resume/Stop buttons
   - Progress bar showing current line
   - Auto-advance with configurable delay (1-10 seconds)
   - Manual step-through mode

3. **Live Translation Display**
   - Shows current speaker and language
   - Displays original text
   - Shows translations in real-time
   - Simulated audio playback buttons

4. **Meeting Transcript**
   - Expandable history of all translations
   - Collapsible entries for easy navigation
   - Clear transcript button

### Deployment

Build for static hosting (GitHub Pages, Netlify, Vercel):

```bash
cd src/react_app/frontend
npm run build:demo
```

Deploy the `dist/` folder to any static hosting service - no server needed!

## Comparison

| Feature | Streamlit Demo | React Demo |
|---------|----------------|------------|
| **Backend** | Required (Python) | Not required |
| **Azure API** | Real calls | Simulated |
| **Audio** | Real Azure TTS | Simulated |
| **Internet** | Required | Optional (after load) |
| **Startup Time** | ~5-10 seconds | Instant |
| **Best For** | Testing real Azure | Trade shows, training |
| **Deployment** | Server required | Static hosting |

## Next Steps

After demoing with `app_demo.py`, try:

1. **Full Live App** (`app.py`)
   - Real microphone input
   - Live translation with Azure
   - Continuous or single-shot modes

2. **Custom Transcripts**
   - Create meeting-specific scripts
   - Add more languages
   - Extend dialogue scenarios

3. **Production Deployment**
   - Set up for actual meetings
   - Configure microphone hardware
   - Train users on live system

## Support

For issues or questions:
- Review main `README.md` for general setup
- Check `TROUBLESHOOTING.md` for common issues
- Refer to Azure Speech SDK documentation

---

**Tip:** The demo app is perfect for showing to council members, administrators, or stakeholders before deploying the live system!
