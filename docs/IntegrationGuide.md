# Integration Guide: On-Premises Encoder & Live Streaming Setup

## Overview

This guide helps you integrate the Azure Live Interpreter API with your existing on-premises video encoder and live streaming infrastructure for multilingual council meetings, conferences, or broadcast events.

## 🎯 Integration Goals

- Capture audio from existing AV system
- Translate speech in real-time using Azure Live Interpreter
- Route translated audio back to:
  - Live stream encoders (OBS, vMix, Wirecast)
  - On-premises broadcasting systems
  - Individual listening devices
  - Recording systems

## 🏗️ Integration Architecture Options

### Option 1: Audio Tap Integration (Recommended for Most Setups)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Existing On-Premises Setup                            │
│                                                                           │
│  ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐      │
│  │Conference│────▶│  Audio   │────▶│  Video   │────▶│   Live   │       │
│  │   Mics   │     │  Mixer   │     │ Encoder  │     │ Stream   │       │
│  │          │     │          │     │(OBS/vMix)│     │          │       │
│  └──────────┘     └────┬─────┘     └──────────┘     └──────────┘       │
│                        │                                                 │
│                        │ Audio Tap (Copy)                                │
│                        ▼                                                 │
│                   ┌─────────┐                                           │
│                   │ Audio   │                                           │
│                   │Interface│                                           │
│                   │(USB/XLR)│                                           │
│                   └────┬────┘                                           │
└────────────────────────┼──────────────────────────────────────────────┘
                         │
                         ▼
┌─────────────────────────────────────────────────────────────────────────┐
│              Live Interpreter Demo Application                           │
│                                                                           │
│  ┌──────────────┐     ┌──────────────┐     ┌──────────────┐           │
│  │   Audio      │────▶│    Azure     │────▶│  Translated  │           │
│  │   Capture    │     │Live Interpreter    │    Audio     │           │
│  │              │     │              │     │    Output    │           │
│  └──────────────┘     └──────────────┘     └──────┬───────┘           │
└──────────────────────────────────────────────────┼─────────────────────┘
                                                     │
                         ┌───────────────────────────┼───────────────────┐
                         │                           │                   │
                         ▼                           ▼                   ▼
                  ┌──────────┐              ┌──────────┐         ┌──────────┐
                  │Individual│              │ Virtual  │         │Broadcast │
                  │Headphones│              │  Audio   │         │ System   │
                  │          │              │  Cable   │         │          │
                  └──────────┘              └────┬─────┘         └──────────┘
                                                 │
                                                 ▼
                                          ┌──────────┐
                                          │  Video   │
                                          │ Encoder  │
                                          │(2nd Audio│
                                          │ Track)   │
                                          └──────────┘
```

**Pros:**
- ✅ Non-invasive to existing setup
- ✅ No changes to current workflow
- ✅ Easy to test and deploy
- ✅ Original audio stream unchanged

**Cons:**
- ⚠️ Requires additional audio interface
- ⚠️ Translation output is separate from main stream

### Option 2: Pre-Encoder Integration (Advanced)

```
┌─────────────────────────────────────────────────────────────────────────┐
│                    Enhanced On-Premises Setup                            │
│                                                                           │
│  ┌──────────┐     ┌──────────┐                                          │
│  │Conference│────▶│  Audio   │                                          │
│  │   Mics   │     │  Mixer   │                                          │
│  │          │     │          │                                          │
│  └──────────┘     └────┬─────┘                                          │
│                        │                                                 │
│                        ├───────────────────────────────┐                │
│                        │                               │                │
│                        ▼                               ▼                │
│                  ┌──────────┐                    ┌──────────┐          │
│                  │ Original │                    │   Audio  │          │
│                  │  Audio   │                    │Interface │          │
│                  │ to Video │                    │   USB    │          │
│                  │ Encoder  │                    └────┬─────┘          │
│                  │(Track 1) │                         │                │
│                  └────┬─────┘                         │                │
│                       │              ┌────────────────┘                │
│                       │              │                                 │
└───────────────────────┼──────────────┼─────────────────────────────────┘
                        │              │
                        │              ▼
                        │    ┌─────────────────┐
                        │    │Live Interpreter │
                        │    │  Demo App       │
                        │    └────────┬────────┘
                        │             │
                        │             ▼
                        │    ┌─────────────────┐
                        │    │Virtual Audio Out│
                        │    └────────┬────────┘
                        │             │
                        │             ▼
                        │    ┌─────────────────┐
                        │    │  Audio Return   │
                        │    │   Interface     │
                        │    └────────┬────────┘
                        │             │
                        ▼             ▼
                  ┌──────────────────────┐
                  │    Video Encoder     │
                  │  ┌────────────────┐  │
                  │  │Track 1: Original│ │
                  │  │Track 2: Spanish │ │
                  │  │Track 3: French  │ │
                  │  └────────────────┘  │
                  └──────────┬───────────┘
                             │
                             ▼
                      ┌─────────────┐
                      │ Live Stream │
                      │(Multi-audio)│
                      └─────────────┘
```

**Pros:**
- ✅ Integrated multi-audio live stream
- ✅ Viewer selects language in player
- ✅ Professional production quality
- ✅ Single unified workflow

**Cons:**
- ⚠️ More complex setup
- ⚠️ Requires virtual audio routing
- ⚠️ May need encoder configuration changes

### Option 3: Post-Encoder Integration (Hybrid Streaming)

```
┌─────────────────────────────────────────────────────────────────────────┐
│              Existing Production (Unchanged)                             │
│                                                                           │
│  Conference Mics → Mixer → Encoder → Main Live Stream (Original Audio)  │
│                                                                           │
└─────────────────────────────────────────────────────────────────────────┘
                             ↓ (Audio copy)
┌─────────────────────────────────────────────────────────────────────────┐
│              Parallel Translation System                                 │
│                                                                           │
│  Audio Input → Live Interpreter → Translated Audio → Web Interface      │
│                                                                           │
│  ┌──────────────────────────────────────────────────────────┐          │
│  │            React App WebSocket Server                     │          │
│  │  • Serves translated audio via WebSocket                 │          │
│  │  • Web UI at: https://yourdomain.com/translate           │          │
│  │  • Mobile-friendly interface                             │          │
│  └──────────────────────────────────────────────────────────┘          │
└─────────────────────────────────────────────────────────────────────────┘
                             ↓
                    Viewers access both:
                    • Main stream (original)
                    • Translation web app (translated)
```

**Pros:**
- ✅ Zero impact on existing production
- ✅ Easy to deploy and test
- ✅ Scalable to any number of viewers
- ✅ Works with any encoder/streaming platform

**Cons:**
- ⚠️ Two separate interfaces for viewers
- ⚠️ Requires additional hosting
- ⚠️ Synchronization challenges

## 🔌 Hardware Integration Points

### Critical Questions to Ask Your Customer

#### 1. Current Audio Infrastructure
- **Q:** What audio mixer/console are you using?
  - *Examples: Behringer X32, Yamaha TF series, Allen & Heath SQ*
- **Q:** How many audio channels are in use?
- **Q:** Is there an available auxiliary output or matrix output?
- **Q:** What connector types are available? (XLR, TRS, RCA)

#### 2. Current Video Encoder Setup
- **Q:** What encoder software/hardware are you using?
  - *OBS Studio, vMix, Wirecast, TriCaster, hardware encoders*
- **Q:** How many audio tracks does your stream currently have?
- **Q:** Can your encoder accept additional audio inputs?
- **Q:** What audio input format? (USB, HDMI, NDI, SDI, analog)

#### 3. Network Infrastructure
- **Q:** Where will the translation computer be located?
  - *Control room, server room, cloud VM*
- **Q:** What's the available bandwidth?
  - *Minimum: 5 Mbps upload for Azure API*
- **Q:** Is there a wired network connection available?
- **Q:** Are there firewall restrictions for outbound HTTPS/WebSocket?

#### 4. Output Distribution Requirements
- **Q:** Who needs access to translated audio?
  - In-room attendees via PA system
  - Individual listeners via headphones
  - Live stream viewers
  - Recording system
  - Remote participants
- **Q:** How many simultaneous language outputs needed?
  - *Example: Original + Spanish + French = 3 tracks*

## 🛠️ Required Hardware Components

### Minimum Setup (Audio Tap Method)

| Component | Purpose | Example Products | Est. Cost |
|-----------|---------|------------------|-----------|
| **Audio Interface** | Capture audio from mixer | Focusrite Scarlett 2i2, Behringer UMC202HD | $100-180 |
| **Cables** | Connect mixer to interface | XLR cables, 1/4" TRS cables | $20-50 |
| **Computer** | Run Live Interpreter app | Intel i5/Ryzen 5, 8GB RAM, Windows/Linux | $500-800 |
| **Headphone Amp** (optional) | Distribute to listeners | Behringer HA400, ART HeadAmp | $25-100 |

### Professional Setup (Multi-track Encoder Integration)

| Component | Purpose | Example Products | Est. Cost |
|-----------|---------|------------------|-----------|
| **Audio Interface** | Multi-channel I/O | Focusrite Clarett+, MOTU M4 | $300-500 |
| **Virtual Audio Router** | Software audio routing | VB-Audio VoiceMeeter, JACK Audio | Free-$50 |
| **Network Audio Device** (optional) | Dante/AES67 integration | Audinate AVIO adapters | $200-400 |
| **Dedicated PC** | Translation processing | Same as above | $500-800 |

## 📋 Integration Checklist

### Phase 1: Discovery & Planning
- [ ] Document current audio signal flow
- [ ] Identify available audio tap points
- [ ] Verify encoder audio input capabilities
- [ ] Test network connectivity to Azure
- [ ] Confirm Azure Speech Service region availability
- [ ] Determine required output languages
- [ ] Map audio distribution requirements

### Phase 2: Hardware Preparation
- [ ] Purchase/obtain audio interface
- [ ] Acquire necessary cables and adapters
- [ ] Set up dedicated computer for translation
- [ ] Install audio drivers and test capture
- [ ] Configure audio routing (if using virtual cables)

### Phase 3: Software Installation
- [ ] Install Python 3.12+ and dependencies
- [ ] Clone Live Interpreter demo repository
- [ ] Configure `.env` with Azure credentials
- [ ] Test basic audio capture functionality
- [ ] Verify Azure API connectivity

### Phase 4: Integration Testing
- [ ] Connect audio tap to interface
- [ ] Test audio levels and quality
- [ ] Run translation with test audio
- [ ] Verify output audio quality
- [ ] Test encoder integration (if applicable)
- [ ] Validate end-to-end latency

### Phase 5: Production Deployment
- [ ] Document final configuration
- [ ] Train staff on system operation
- [ ] Create troubleshooting guide
- [ ] Set up monitoring and alerts
- [ ] Plan for failover/backup scenarios

## 🎚️ Audio Routing Configurations

### Configuration A: OBS Studio Integration

**Scenario:** Add translated audio as second track in OBS stream

**Setup Steps:**

1. **Install Virtual Audio Cable**
   ```bash
   # Windows: Download VB-Audio Virtual Cable
   # Linux: Install PulseAudio or JACK
   # macOS: Install BlackHole
   ```

2. **Configure Live Interpreter Output**
   - Set output device to "Virtual Cable Input"
   - This will route translated audio to virtual device

3. **Configure OBS Audio Sources**
   ```
   OBS Sources:
   ├── Audio Input Capture (Original)
   │   └── Device: Physical mixer output
   └── Audio Input Capture (Translation)
       └── Device: Virtual Cable Output
   ```

4. **OBS Advanced Audio Properties**
   ```
   Source: Original Audio
   ├── Track 1: ✓
   └── Track 2: ✗
   
   Source: Translated Audio
   ├── Track 1: ✗
   └── Track 2: ✓
   ```

5. **OBS Output Settings**
   ```
   Settings > Output > Streaming
   └── Audio Track: 1 and 2
   
   Settings > Output > Recording
   └── Audio Track: 1 and 2
   ```

**Result:** Stream contains both original (track 1) and translated (track 2) audio

### Configuration B: vMix Integration

**Scenario:** Multi-language streaming with vMix

**Setup Steps:**

1. **Add Audio Inputs to vMix**
   ```
   Add Input > Audio > Audio Input
   ├── Input 1: Mixer Output (Original)
   └── Input 2: Virtual Cable (Translation)
   ```

2. **Configure Audio Mixer**
   ```
   vMix Audio Mixer:
   ├── Master: Original audio
   ├── Bus A: Translated Spanish
   ├── Bus B: Translated French
   └── Bus C: Translated Mandarin
   ```

3. **Streaming Configuration**
   ```
   Settings > Outputs
   ├── Stream 1: Master (Original)
   ├── Stream 2: Bus A (Spanish)
   └── Stream 3: Bus B (French)
   ```

**Result:** Multiple simultaneous streams, one per language

### Configuration C: Hardware Encoder (Tricaster, Pearl, etc.)

**Scenario:** Integration with dedicated hardware encoder

**Setup Steps:**

1. **Physical Audio Connections**
   ```
   Audio Mixer AUX OUT → Computer Audio Interface IN
   Computer Audio Interface OUT → Encoder Audio IN (Ch 3-4)
   ```

2. **Audio Channel Mapping**
   ```
   Encoder Input Configuration:
   ├── Ch 1-2: Room microphones (Original)
   └── Ch 3-4: Translated audio from computer
   ```

3. **Encoder Output Configuration**
   ```
   Stream Profile:
   ├── Video: H.264 1080p
   └── Audio:
       ├── Track 1: Stereo (Ch 1-2) - Original
       └── Track 2: Stereo (Ch 3-4) - Translation
   ```

## 🔧 Software Configuration Details

### Environment Variables for Integration

```env
# Azure Configuration
SPEECH_KEY=your_azure_speech_key
SPEECH_REGION=eastus
ENABLE_LIVE_INTERPRETER=true

# Audio Settings
AUDIO_INPUT_DEVICE=USB Audio CODEC  # Your audio interface name
AUDIO_SAMPLE_RATE=16000
AUDIO_CHANNELS=1  # Mono for translation

# Translation Settings
SOURCE_LANGUAGE=en-US
TARGET_LANGUAGES=es-ES,fr-FR  # Comma-separated
AUTO_DETECT_LANGUAGES=en-US,es-ES,fr-FR  # For bidirectional

# Voice Settings (use prebuilt neural voices)
VOICE_NAME_ES=es-ES-ElviraNeural
VOICE_NAME_FR=fr-FR-DeniseNeural

# Output Settings
AUDIO_OUTPUT_DEVICE=Virtual Cable Input  # For routing to encoder
ENABLE_AUDIO_PLAYBACK=true
AUDIO_OUTPUT_FORMAT=wav  # wav, mp3, or raw

# Continuous Mode (for live streaming)
USE_CONTINUOUS_MODE=true
CONTINUOUS_MODE_TIMEOUT=0  # 0 = unlimited

# Latency Optimization
ENABLE_LOW_LATENCY_MODE=true
SPEECH_RECOGNITION_MODE=continuous
```

### Testing Audio Routing

Run this test script to verify your audio chain:

```bash
# Test 1: List available audio devices
python -c "
from src.core.audio_handler import list_audio_devices
list_audio_devices()
"

# Test 2: Capture and playback test
python test_audio.py

# Test 3: Test translation with file
python -c "
from src.core.translator import LiveInterpreterTranslator
from src.core.config import get_settings
translator = LiveInterpreterTranslator(get_settings())
translator.translate_audio_file('test_audio.wav')
"
```

## 🎯 Common Integration Scenarios

### Scenario 1: City Council Meetings

**Requirements:**
- Main stream with original English audio
- Separate stream with Spanish translation
- Individual headphones for in-person attendees

**Recommended Setup:**
- Option 3 (Post-Encoder Integration)
- React app hosted on city web server
- Original stream via YouTube/traditional CDN
- Translation available at: `council.city.gov/translate`

**Equipment Needed:**
- 1x Audio interface (USB): $150
- 1x Computer (existing server): $0
- Virtual hosting for React app: $10/month

### Scenario 2: Corporate Conference

**Requirements:**
- Professional multi-language broadcast
- 3 languages (EN, ES, FR)
- Integrated into video production

**Recommended Setup:**
- Option 2 (Pre-Encoder Integration)
- vMix or OBS with multi-track audio
- 3 separate stream outputs or multi-track single stream

**Equipment Needed:**
- 1x Multi-channel audio interface: $400
- 1x Dedicated translation PC: $800
- Virtual audio routing software: Free

### Scenario 3: Hybrid Event

**Requirements:**
- In-person with PA system
- Live stream to YouTube
- Remote attendees need translation

**Recommended Setup:**
- Option 1 (Audio Tap Integration)
- PA system unchanged
- Translation available via:
  - Headphones for in-person
  - Web app for remote viewers

**Equipment Needed:**
- 1x Audio interface: $150
- 1x Headphone distribution amp: $100
- 10x Headphones: $200

## 🚨 Troubleshooting Integration Issues

### Issue: Audio not reaching translation app

**Checklist:**
1. Verify audio interface is recognized
   ```bash
   python -c "import sounddevice; print(sounddevice.query_devices())"
   ```
2. Check audio levels in system mixer
3. Test with different input device in settings
4. Verify cable connections and mixer routing

### Issue: Translation output not reaching encoder

**Checklist:**
1. Verify virtual audio cable is installed and active
2. Check encoder input device selection
3. Test virtual cable with audio playback
4. Verify audio format compatibility (sample rate, channels)

### Issue: High latency between original and translation

**Optimization Steps:**
1. Enable low-latency mode in config
2. Use wired network connection
3. Close unnecessary applications
4. Consider Azure region closer to location
5. Optimize audio buffer settings:
   ```python
   # In audio_handler.py
   BUFFER_SIZE = 512  # Smaller = lower latency, higher CPU
   ```

### Issue: Audio quality degradation

**Troubleshooting:**
1. Verify sample rate matches throughout chain (16kHz recommended)
2. Check for audio clipping in mixer or interface
3. Ensure sufficient network bandwidth (5+ Mbps)
4. Test with different neural voice options
5. Verify audio interface drivers are updated

## 📊 Performance Metrics & Monitoring

### Key Metrics to Monitor

| Metric | Target | Critical Threshold |
|--------|--------|-------------------|
| **API Latency** | < 500ms | > 2000ms |
| **End-to-End Latency** | < 2s | > 5s |
| **Audio Capture Dropouts** | 0% | > 0.1% |
| **Translation Accuracy** | > 95% | < 85% |
| **Network Bandwidth** | < 2 Mbps | > 10 Mbps |
| **CPU Usage** | < 50% | > 80% |
| **Azure API Errors** | 0/hour | > 5/hour |

### Monitoring Commands

```bash
# Monitor network bandwidth
iftop -i eth0

# Monitor CPU usage
htop

# Check Azure API health
curl -I https://eastus.api.cognitive.microsoft.com

# Monitor application logs
tail -f logs/live-interpreter.log
```

## 💡 Best Practices

### Audio Quality
- ✅ Use wired audio connections whenever possible
- ✅ Set mixer levels to -12dB to -6dB (avoid clipping)
- ✅ Use balanced XLR connections for long cable runs
- ✅ Test audio quality before live event

### Network Reliability
- ✅ Use wired Ethernet (avoid WiFi for production)
- ✅ Configure QoS for Azure traffic if available
- ✅ Have backup cellular connection as failover
- ✅ Monitor network health during event

### System Redundancy
- ✅ Have backup computer ready to swap
- ✅ Keep backup Azure Speech Service key
- ✅ Document entire audio signal flow
- ✅ Train multiple staff members on operation

### Pre-Event Testing
- ✅ Full rehearsal with all equipment 48 hours before
- ✅ Test all language pairs
- ✅ Verify output to all destinations
- ✅ Test failover procedures

## 📞 Integration Support Contacts

### Before Starting Integration
**Recommended Approach:**
1. Fill out the integration questionnaire (below)
2. Schedule technical consultation call
3. Review documented current setup
4. Create integration plan
5. Execute phased rollout

### Integration Questionnaire

Please provide the following information:

**Audio System:**
- Mixer model: _________________
- Available outputs: _________________
- Current audio routing: _________________

**Video Encoder:**
- Encoder type: _________________
- Current audio inputs: _________________
- Streaming destination: _________________

**Network:**
- Connection type: _________________
- Available bandwidth: _________________
- Firewall restrictions: _________________

**Requirements:**
- Number of translation languages: _________________
- Output destinations: _________________
- Expected concurrent users: _________________
- Event duration: _________________

**Timeline:**
- Go-live date: _________________
- Testing availability: _________________

## 🔗 Related Documentation

- [Main README](README.md) - Project overview
- [Quick Start Guide](QUICKSTART.md) - Basic setup
- [Architecture Flow](ARCHITECTURE_FLOW.md) - System design
- [Testing Guide](TESTING_GUIDE.md) - Quality assurance
- [Council Meeting Setup](examples/council_meeting_setup.md) - Specific use case

---

**Need Help?** Open an issue on GitHub with the tag `integration-support` and include:
- Your current setup description
- Integration goals
- Completed questionnaire (above)
- Any relevant diagrams or photos

**Remember:** Start with Option 1 (Audio Tap) for the lowest risk initial deployment, then evolve to more integrated solutions as you gain confidence with the system.
