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

## 📺 PEG Channel & Cable Broadcast Integration

### Overview: Public, Educational, and Government (PEG) Access

This section addresses the specific challenges of integrating Azure Live Interpreter API with **PEG cable channels** for government meetings, including:
- Closed captioning for cable broadcast (CEA-608/708)
- Multi-language translation for social media streams
- Round-trip data flow between cloud services and on-premises encoders
- Maintaining broadcast-quality latency (3-5 seconds)

### Key Challenges & Solutions

#### Challenge 1: Cloud-to-On-Prem Captioning Latency

**Problem:** Ensuring cloud-based translation can feed closed captioning back to on-prem encoders for PEG channel broadcast without excessive latency.

**Current State:**
- Typical on-prem closed captioning: 3-5 seconds latency
- Cloud round-trip adds: 1-3 seconds
- **Target:** Maintain total latency under 6 seconds

**Solution Architecture:**
```
┌────────────────────────────────────────────────────────────────────────┐
│                    On-Premises Broadcast Center                         │
│                                                                          │
│  ┌──────────┐     ┌──────────┐     ┌──────────────┐                   │
│  │Conference│────▶│  Audio   │────▶│    Video     │                    │
│  │   Mics   │     │  Mixer   │     │   Encoder    │                    │
│  │          │     │          │     │  (Hardware)  │                    │
│  └──────────┘     └────┬─────┘     └──────┬───────┘                   │
│                        │                   │                            │
│                        │ Audio Tap         │ SDI/HDMI Video             │
│                        ▼                   │                            │
│                   ┌─────────┐              │                            │
│                   │  Azure  │              │                            │
│                   │  APIM   │              │                            │
│                   │ Self-   │              ▼                            │
│                   │ Hosted  │         ┌──────────┐                     │
│                   │ Gateway │◀───────▶│ Caption  │                     │
│                   └────┬────┘         │ Encoder  │                     │
│                        │              │(CEA-708) │                     │
└────────────────────────┼──────────────┴────┬─────┘                     │
                         │                   │                            │
                         │ HTTPS (Secure)    │ Embedded Captions          │
                         ▼                   ▼                            │
┌────────────────────────────────────────────────────────────────────────┐
│                         Azure Cloud                                     │
│                                                                          │
│  ┌──────────────────┐    ┌──────────────────┐    ┌─────────────────┐ │
│  │  Azure API       │    │  Speech          │    │  Text           │ │
│  │  Management      │───▶│  Translation     │───▶│  Translation    │ │
│  │  (Gateway)       │    │  (Live           │    │  (Optional)     │ │
│  │                  │    │   Interpreter)   │    │                 │ │
│  └────────┬─────────┘    └──────────────────┘    └─────────────────┘ │
│           │                                                             │
│           │ Low-Latency WebSocket/HTTPS                                │
│           ▼                                                             │
│  ┌─────────────────────────────────────────────────────────────────┐  │
│  │            Caption Formatting Service                            │  │
│  │  • Converts Azure Speech output to CEA-608/708 format          │  │
│  │  • Handles line breaks and character limits (32 chars/line)    │  │
│  │  • Manages roll-up, pop-on, or paint-on modes                  │  │
│  │  • Returns formatted caption data stream                        │  │
│  └─────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────┘
                         │
                         │ Caption Data Return
                         ▼
                   [Back to Caption Encoder]
                         │
                         ▼
                   ┌──────────┐
                   │   PEG    │
                   │  Cable   │───▶ Cable Subscribers
                   │ Channel  │
                   └──────────┘
```

**Key Components:**

1. **Azure API Management (APIM) with Self-Hosted Gateway**
   - Deployed on-premises or edge location
   - Provides secure, low-latency connection to Azure
   - Caches responses for faster performance
   - Handles authentication and rate limiting
   - **Latency improvement:** Reduces round-trip by 30-50%

2. **Caption Formatting Service**
   - Converts Azure Speech Recognition output to CEA-608/708 standard
   - Handles timing and synchronization
   - Manages caption positioning and styling
   - **Available options:**
     - Azure Function with custom formatting logic
     - On-prem Python service (included in this demo)
     - Third-party caption encoder software

3. **Integration Methods:**

   **Option A: Direct Encoder Integration (Lowest Latency)**
   ```python
   # Python service running on-prem
   # Receives Azure captions via APIM Gateway
   # Outputs to hardware caption encoder
   
   from azure.cognitiveservices.speech import SpeechConfig
   from caption_encoder import CEA708Encoder
   
   class CaptionBridge:
       def __init__(self):
           self.encoder = CEA708Encoder('/dev/ttyUSB0')  # Serial to caption encoder
           self.speech_config = SpeechConfig(subscription=key, region=region)
       
       def on_recognized(self, evt):
           # Format for CEA-708
           caption_text = self.format_caption(evt.result.text)
           # Send to hardware encoder
           self.encoder.send_caption(caption_text)
           
       def format_caption(self, text):
           # Split into 32-char lines, handle line breaks
           lines = [text[i:i+32] for i in range(0, len(text), 32)]
           return '\n'.join(lines[:4])  # Max 4 lines for CEA-708
   ```

   **Option B: WebVTT/SRT for IP Streaming**
   ```python
   # Generate WebVTT captions for IP-based distribution
   # Compatible with most streaming platforms
   
   def generate_webvtt(translations, start_time):
       vtt = "WEBVTT\n\n"
       for i, (text, timestamp) in enumerate(translations):
           vtt += f"{i+1}\n"
           vtt += f"{format_timestamp(timestamp)} --> {format_timestamp(timestamp + 3000)}\n"
           vtt += f"{text}\n\n"
       return vtt
   ```

#### Challenge 2: Social Media Platform Limitations

**Problem:** Most social media platforms (Facebook Live, YouTube Live, LinkedIn Live) only support a single closed captioning channel, limiting multi-language output.

**Platform Capabilities:**

| Platform | Caption Tracks | Multi-Audio | API Access | Latency |
|----------|---------------|-------------|------------|---------|
| YouTube Live | 1 (selectable) | Yes (future) | Yes | 5-10s |
| Facebook Live | 1 only | No | Limited | 10-15s |
| LinkedIn Live | 1 only | No | No | 10-20s |
| Twitter/X | 1 only | No | Limited | 5-10s |
| Twitch | 1 only | No | Yes | 2-5s |

**Solutions:**

**Solution 1: Multi-Platform Streaming Strategy**
```
┌────────────────────────────────────────────────────────────────────┐
│              Source: Council Meeting                                │
│              Audio: English + Spanish speakers                      │
└───────────────────────────┬────────────────────────────────────────┘
                            │
                            ▼
┌────────────────────────────────────────────────────────────────────┐
│                  Azure Live Interpreter                             │
│  • Detects language automatically                                  │
│  • Generates real-time transcription (English)                     │
│  • Generates real-time translation (Spanish)                       │
└─────────────┬─────────────────────────┬────────────────────────────┘
              │                         │
              ▼                         ▼
    ┌──────────────────┐      ┌──────────────────┐
    │  Stream 1        │      │  Stream 2        │
    │  YouTube Live    │      │  Facebook Live   │
    │  • English CC    │      │  • Spanish CC    │
    │  • Original Audio│      │  • Original Audio│
    └──────────────────┘      └──────────────────┘
              │                         │
              └────────┬────────────────┘
                       ▼
              ┌──────────────────┐
              │  PEG Cable       │
              │  • English CC    │
              │  (CEA-708)       │
              └──────────────────┘
```

**Solution 2: Custom Web Player with Language Selection**
```
┌────────────────────────────────────────────────────────────────────┐
│                    Custom Web Interface                             │
│              (Hosted on city/organization website)                  │
│                                                                      │
│  ┌──────────────────────────────────────────────────────────────┐  │
│  │                  Video Player                                 │  │
│  │  ┌────────────────────────────────────────────────────────┐  │  │
│  │  │           [  Meeting Video Stream  ]                   │  │  │
│  │  │                                                         │  │  │
│  │  │  [Original Audio from Cable/Stream]                    │  │  │
│  │  └────────────────────────────────────────────────────────┘  │  │
│  │                                                               │  │
│  │  Caption Language Selection:                                 │  │
│  │  ┌─────────┐  ┌─────────┐  ┌─────────┐                     │  │
│  │  │ English │  │ Spanish │  │ French  │                      │  │
│  │  └────┬────┘  └────┬────┘  └────┬────┘                     │  │
│  │       │            │            │                            │  │
│  │       └────────────┴────────────┘                            │  │
│  │                    │                                          │  │
│  │                    ▼                                          │  │
│  │         ┌─────────────────────────┐                          │  │
│  │         │ [Caption Display Area]  │                          │  │
│  │         │ Real-time captions in   │                          │  │
│  │         │ selected language       │                          │  │
│  │         └─────────────────────────┘                          │  │
│  └──────────────────────────────────────────────────────────────┘  │
│                                                                      │
│  WebSocket Connection to Azure Live Interpreter                     │
│  • Receives all language tracks simultaneously                      │
│  • Client-side switching (no server load)                           │
│  • Can be embedded in social media posts as link                    │
└──────────────────────────────────────────────────────────────────────┘

Distribution Options:
├── Embed on city website
├── Share link on Facebook/Twitter posts
├── QR code displayed during cable broadcast
└── Email to registered attendees
```

**Implementation Code:**
```html
<!-- Custom web player with multi-language captions -->
<!DOCTYPE html>
<html>
<head>
    <title>Council Meeting - Multi-Language Captions</title>
</head>
<body>
    <video id="player" controls>
        <source src="https://stream.city.gov/live/council.m3u8" type="application/x-mpegURL">
    </video>
    
    <div id="language-selector">
        <button onclick="selectLanguage('en')">English</button>
        <button onclick="selectLanguage('es')">Spanish</button>
        <button onclick="selectLanguage('fr')">French</button>
    </div>
    
    <div id="captions"></div>
    
    <script>
        const ws = new WebSocket('wss://captions.city.gov/live');
        let currentLanguage = 'en';
        
        ws.onmessage = (event) => {
            const data = JSON.parse(event.data);
            if (data.translations[currentLanguage]) {
                document.getElementById('captions').textContent = 
                    data.translations[currentLanguage];
            }
        };
        
        function selectLanguage(lang) {
            currentLanguage = lang;
        }
    </script>
</body>
</html>
```

#### Challenge 3: Avoiding Custom Development

**Problem:** Desire to avoid custom development; preference for off-the-shelf or template-based solutions.

**Off-the-Shelf Solutions:**

**Option 1: Azure Speech Translation Accelerator**
- **What it is:** Pre-built solution template from Microsoft
- **Includes:**
  - Azure Speech Service integration
  - Caption formatting logic
  - Web player with language selection
  - WebSocket server for real-time streaming
- **Deployment:** Azure ARM template or Terraform
- **Customization:** Configuration-based (no code changes needed)
- **Cost:** Azure services only (~$50-200/month depending on usage)

**Deployment:**
```bash
# Clone the accelerator repository
git clone https://github.com/Azure-Samples/cognitive-services-speech-translation-accelerator

# Configure settings
cp config.example.json config.json
# Edit config.json with your Azure credentials and settings

# Deploy to Azure
az deployment group create \
  --resource-group rg-council-translation \
  --template-file azuredeploy.json \
  --parameters @config.json

# Result: Fully functional translation system with:
# - Web UI for viewing translations
# - REST API for integration
# - Caption export (CEA-608/708, WebVTT, SRT)
```

**Option 2: This Demo Project (Template-Based)**
- **Advantages:**
  - Open source and customizable
  - Two UI options (Streamlit for simple, React for production)
  - Built-in Azure Live Interpreter integration
  - Ready for Docker containerization
- **Setup time:** 1-2 hours
- **Customization:** Configuration file (.env) only
- **Deployment options:**
  - On-premises Windows/Linux server
  - Azure VM or App Service
  - Docker container

**Quick Deployment for PEG Integration:**
```bash
# 1. Clone and configure
git clone https://github.com/your-org/live-interpreter-api-demo
cd live-interpreter-api-demo
cp .env.example .env

# 2. Configure for cable broadcast
cat >> .env << EOF
# PEG Channel Integration
ENABLE_LIVE_INTERPRETER=true
ENABLE_CAPTIONS=true
OUTPUT_CAPTION_FORMAT=CEA708  # or WebVTT, SRT
CAPTION_OUTPUT_PORT=/dev/ttyUSB0  # Serial port to caption encoder
ENABLE_AUDIO_PLAYBACK=false  # Audio handled by encoder
TARGET_LANGUAGE=es-ES
SECONDARY_TARGET_LANGUAGE=fr-FR
EOF

# 3. Deploy with Docker
docker build -t council-translator .
docker run -d \
  --name council-translator \
  --device=/dev/ttyUSB0 \
  -p 8000:8000 \
  council-translator

# 4. Verify connectivity to caption encoder
curl http://localhost:8000/health
```

**Option 3: Azure Communication Services (ACS) + AI Foundry**
- **For:** Organizations planning future scalability
- **Capabilities:**
  - Multi-party video calling with transcription
  - Built-in recording and storage
  - Direct social media integration
  - Advanced AI features (sentiment analysis, summarization)
- **Deployment:** Azure portal configuration
- **Development:** Low-code/no-code options available
- **Cost:** Pay-per-use (starts at $0.004/minute)

**When to use:**
- Need to scale to multiple simultaneous meetings
- Want advanced analytics (speaker identification, keyword extraction)
- Require integration with Microsoft Teams
- Planning to add interactive features (Q&A, polls)

#### Challenge 4: Maintaining Latency Requirements

**Problem:** Need to maintain or improve current latency (3-5 seconds) for closed captioning.

**Latency Breakdown Analysis:**

| Stage | Typical Latency | Optimized Latency | Optimization Method |
|-------|----------------|-------------------|---------------------|
| Audio capture | 50-100ms | 20-50ms | Lower buffer size, direct tap |
| Network to Azure | 50-150ms | 30-80ms | Use closest Azure region, wired connection |
| Speech recognition | 200-500ms | 150-300ms | Enable low-latency mode |
| Translation | 100-300ms | 50-150ms | Pre-load language models |
| Caption formatting | 50-100ms | 20-50ms | Local processing (APIM gateway) |
| Network return | 50-150ms | 30-80ms | APIM gateway edge caching |
| Encoder processing | 100-200ms | 50-100ms | Hardware encoder, optimized settings |
| **Total** | **600-1500ms** | **350-810ms** | **Combined optimizations** |
| **Current target** | **3000-5000ms** | | **We can beat this!** |

**Optimization Strategies:**

1. **Use Azure API Management Self-Hosted Gateway**
   ```bash
   # Deploy APIM gateway on-premises
   docker run -d \
     --name azure-apim-gateway \
     -e config.service.endpoint='<gateway-url>' \
     -e config.service.auth='<gateway-key>' \
     -p 8080:8080 \
     mcr.microsoft.com/azure-api-management/gateway:latest
   ```
   **Benefit:** Reduces round-trip latency by 100-300ms

2. **Enable Low-Latency Mode in Azure Speech**
   ```python
   # In your configuration
   speech_config = speechsdk.SpeechConfig(subscription=key, region=region)
   speech_config.set_property(
       speechsdk.PropertyId.SpeechServiceConnection_InitialSilenceTimeoutMs, 
       "3000"  # Reduced from default 5000ms
   )
   speech_config.set_property(
       speechsdk.PropertyId.SpeechServiceConnection_EndSilenceTimeoutMs,
       "500"  # Reduced from default 1000ms
   )
   ```
   **Benefit:** Reduces recognition delay by 200-500ms

3. **Use Closest Azure Region**
   - **East Coast:** Use `eastus` or `eastus2`
   - **West Coast:** Use `westus2`
   - **Europe:** Use `westeurope`
   - **Asia:** Use `japaneast` or `southeastasia`
   
   **Latency comparison:**
   - Same region: 30-50ms
   - Cross-country: 60-100ms
   - Cross-ocean: 150-250ms

4. **Hardware Acceleration**
   - Use GPU-enabled Azure VM for faster processing
   - Deploy caption formatting service on edge server
   - Use SSD storage for caching

#### Challenge 5: Workflow Integration

**Problem:** Uncertainty about the workflow for integrating Azure services with existing hardware and broadcast infrastructure.

**Complete Workflow Diagram:**

```
┌──────────────────────────────────────────────────────────────────────────────┐
│                          STEP 1: AUDIO CAPTURE                                │
│                                                                                │
│  Council Chamber                                                               │
│  ┌──────────┐    ┌──────────┐    ┌──────────┐                               │
│  │ Podium   │───▶│  Ceiling │───▶│  Audio   │                               │
│  │   Mic    │    │   Mics   │    │  Mixer   │                               │
│  └──────────┘    └──────────┘    │(Existing)│                               │
│                                   └─────┬────┘                               │
│                                         │                                     │
│                              ┌──────────┴──────────┐                         │
│                              │  Main Mix Output     │                         │
│                              │  (To existing encoder)│                        │
│                              └──────────┬───────────┘                        │
│                                         │                                     │
│                              ┌──────────┴──────────┐                         │
│                              │  AUX Send 1 (Copy)  │                         │
│                              │  XLR Output          │                         │
│                              └──────────┬───────────┘                        │
└────────────────────────────────────────┼────────────────────────────────────┘
                                          │
┌────────────────────────────────────────┼────────────────────────────────────┐
│                    STEP 2: AUDIO INTERFACE                                    │
│                                                                                │
│                              ┌──────────┴───────────┐                        │
│                              │  Audio Interface     │                         │
│                              │  (USB/Thunderbolt)   │                         │
│                              │  - Focusrite         │                         │
│                              │  - MOTU              │                         │
│                              │  - RME               │                         │
│                              └──────────┬───────────┘                        │
│                                         │ USB                                 │
└────────────────────────────────────────┼────────────────────────────────────┘
                                          │
┌────────────────────────────────────────┼────────────────────────────────────┐
│                  STEP 3: TRANSLATION SERVER                                   │
│                  (On-Prem or Azure VM)                                        │
│                                         │                                     │
│                              ┌──────────▼───────────┐                        │
│                              │  This Demo App       │                         │
│                              │  (Python Backend)    │                         │
│                              └──────────┬───────────┘                        │
│                                         │                                     │
│                              ┌──────────▼───────────┐                        │
│                              │ Azure APIM Gateway   │                         │
│                              │ (Self-Hosted)        │                         │
│                              └──────────┬───────────┘                        │
│                                         │ HTTPS (Secure)                      │
└────────────────────────────────────────┼────────────────────────────────────┘
                                          │
┌────────────────────────────────────────┼────────────────────────────────────┐
│                      STEP 4: AZURE CLOUD                                      │
│                                         │                                     │
│                              ┌──────────▼───────────┐                        │
│                              │  Azure Speech        │                         │
│                              │  Translation         │                         │
│                              │  (Live Interpreter)  │                         │
│                              └──────────┬───────────┘                        │
│                                         │                                     │
│                    ┌────────────────────┴────────────────────┐              │
│                    │                                          │              │
│         ┌──────────▼───────────┐              ┌──────────────▼────────────┐│
│         │  English               │              │  Spanish                  ││
│         │  Transcription         │              │  Translation              ││
│         │  (Original Language)   │              │  (Target Language)        ││
│         └──────────┬───────────┘              └──────────────┬────────────┘│
│                    │                                          │              │
└────────────────────┼──────────────────────────────────────────┼──────────────┘
                     │                                          │
┌────────────────────┼──────────────────────────────────────────┼──────────────┐
│              STEP 5: CAPTION FORMATTING                       │              │
│                    │                                          │              │
│         ┌──────────▼───────────┐              ┌──────────────▼────────────┐│
│         │  Caption Formatter   │              │  Caption Formatter        ││
│         │  (CEA-708 English)   │              │  (CEA-708 Spanish)        ││
│         │  - Line breaks       │              │  - Line breaks            ││
│         │  - 32 char limit     │              │  - 32 char limit          ││
│         │  - Timing sync       │              │  - Timing sync            ││
│         └──────────┬───────────┘              └──────────────┬────────────┘│
└────────────────────┼──────────────────────────────────────────┼──────────────┘
                     │                                          │
┌────────────────────┼──────────────────────────────────────────┼──────────────┐
│              STEP 6: OUTPUT DISTRIBUTION                      │              │
│                    │                                          │              │
│      ┌─────────────┴─────────────┐              ┌────────────┴────────────┐│
│      │                            │              │                         ││
│   ┌──▼────────────┐    ┌──────────▼─────┐   ┌──▼─────────┐   ┌────────┐  ││
│   │  Hardware     │    │   YouTube       │   │  Facebook  │   │Custom  │  ││
│   │  Caption      │───▶│   Live          │   │  Live      │   │Web     │  ││
│   │  Encoder      │    │   (English CC)  │   │  (Spanish) │   │Player  │  ││
│   │  (CEA-708)    │    └─────────────────┘   └────────────┘   │(Both)  │  ││
│   └───────┬───────┘                                            └────────┘  ││
│           │                                                                 ││
│           ▼                                                                 ││
│   ┌───────────────┐                                                        ││
│   │  PEG Cable    │                                                        ││
│   │  Channel      │───▶ Cable TV Subscribers                              ││
│   │  (Broadcast)  │    (English captions embedded)                        ││
│   └───────────────┘                                                        ││
└──────────────────────────────────────────────────────────────────────────────┘
```

**Step-by-Step Setup Process:**

**Week 1: Planning & Prerequisites**
- [ ] Audit current AV setup (mixer model, available outputs)
- [ ] Create Azure Speech Service resource
- [ ] Set up Azure API Management (if using self-hosted gateway)
- [ ] Order audio interface hardware (if needed)
- [ ] Identify caption encoder model and connection method

**Week 2: Software Setup**
- [ ] Deploy this demo app on on-prem server or Azure VM
- [ ] Configure `.env` with Azure credentials
- [ ] Set up APIM self-hosted gateway (optional but recommended)
- [ ] Test Azure connectivity and latency
- [ ] Configure caption formatting service

**Week 3: Hardware Integration**
- [ ] Connect audio mixer AUX output to audio interface
- [ ] Install audio interface drivers
- [ ] Test audio capture quality
- [ ] Connect caption encoder (serial/IP)
- [ ] Test caption output to encoder

**Week 4: Testing & Validation**
- [ ] Test with recorded audio samples
- [ ] Measure end-to-end latency
- [ ] Test failover scenarios
- [ ] Validate caption quality on cable broadcast
- [ ] Train staff on operation

**Week 5: Live Deployment**
- [ ] Soft launch with one meeting
- [ ] Monitor performance metrics
- [ ] Gather feedback from viewers
- [ ] Adjust settings as needed
- [ ] Document final configuration

### Recommended Solution for PEG Channels

**For Most Organizations:**

1. **Start with Post-Encoder Integration (Option 3)**
   - Least disruptive to existing workflow
   - Can be tested in parallel with current setup
   - Easy to disable if issues arise

2. **Use This Demo Project as Foundation**
   - Open source, free to use
   - Proven integration patterns
   - Active community support

3. **Deploy APIM Self-Hosted Gateway**
   - Significant latency improvement
   - Enhanced security
   - Better reliability

4. **Multi-Platform Distribution Strategy**
   - PEG Cable: English captions via CEA-708
   - YouTube Live: English captions
   - Facebook Live: Spanish captions
   - Custom web player: Both languages selectable

5. **Cost Estimate (Annual)**
   - Azure Speech Service: $1,200-2,400 (based on 24 meetings/year)
   - Azure APIM: $600-1,200 (Developer tier)
   - Hardware (one-time): $300-500
   - **Total Year 1:** $2,100-4,100
   - **Subsequent Years:** $1,800-3,600

**Expected Latency:**
- **With optimizations:** 800ms - 1.5 seconds (better than current 3-5 seconds!)
- **Without optimizations:** 1.5 - 3 seconds (still meets requirements)

### Demo Plan for Council Meeting Simulation

**Objective:** Validate the complete workflow with English and Spanish audio feeds.

**Demo Scenario:**
- **Duration:** 20-minute simulated council meeting
- **Languages:** English primary, Spanish secondary
- **Speakers:** 3-4 participants alternating languages
- **Outputs:** 
  - Live captions on monitor (both languages)
  - Caption data stream to test encoder
  - WebSocket feed to custom web player

**Setup:**
```bash
# 1. Use included demo app
cd src/streamlit_app
streamlit run app_demo.py

# 2. Configure for demo
# Edit .env:
ENABLE_LIVE_INTERPRETER=true
SOURCE_LANGUAGE=en-US
TARGET_LANGUAGE=es-ES
ENABLE_CAPTIONS=true
OUTPUT_CAPTION_FORMAT=WebVTT  # Easier to validate

# 3. Run with pre-recorded audio or live microphone
# Demo app will:
# - Show real-time recognition
# - Display translations
# - Generate caption files
# - Measure latency at each stage
```

**Success Criteria:**
- [ ] Audio properly captured and sent to Azure
- [ ] Both languages recognized accurately (>90%)
- [ ] Translations display in under 2 seconds
- [ ] Caption format is correct (line breaks, timing)
- [ ] No dropped audio segments
- [ ] System handles speaker switches smoothly

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
