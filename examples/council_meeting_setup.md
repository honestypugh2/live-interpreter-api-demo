# Council Meeting Setup Guide

> **⚠️ IMPORTANT NOTICE**  
> This setup guide references demo code intended for **development and learning purposes only**. It is **not designed for production use**. For production council meeting deployments, please consult with professional AV integrators and implement appropriate Azure best practices for security, reliability, error handling, and monitoring.

Complete guide for setting up Azure Live Interpreter for a bilingual council meeting or conference room with English and Spanish translation.

## Use Case Overview

**Scenario**: City Council Meeting
- **Languages**: English ↔ Spanish
- **Attendees**: 20-50 people (mixed language speakers)
- **Duration**: 2-4 hours
- **Requirements**:
  - Real-time translation for all attendees
  - Individual listening options (headphones or room speakers)
  - Caption display on screens
  - Recording for public access

## Architecture Options

### Option 1: Simple Setup (Small Meetings)

**Best for**: 5-10 people, informal meetings, quick setup

**Equipment Needed**:
- Laptop with demo app
- USB conference microphone ($100-$200)
- Wireless headphones for attendees ($50 each)
- Internet connection (10+ Mbps)

**Setup**:
```
Speaker Microphone → Laptop → Azure Translation → 
├── Bluetooth to Headphones (Spanish listeners)
└── Room Speakers (English listeners)
```

**Cost**: ~$500 initial + ~$5/meeting Azure costs

---

### Option 2: Professional AV Setup (Recommended)

**Best for**: Official council meetings, 20-50 people, permanent installation

**Equipment Needed**:
1. **Audio Input**:
   - 4-6 Ceiling/boundary microphones ($200 each)
   - Audio mixer (Behringer X32, ~$500)
   - XLR cables and stands

2. **Processing**:
   - Dedicated computer (Windows 10+, i5/8GB+)
   - Audio interface (Focusrite Scarlett 2i2, ~$180)
   - FastAPI backend server
   - React frontend on local network

3. **Audio Output**:
   - Infrared assistive listening system (~$1,000)
   - OR: FM transmitter + receivers ($500-800)
   - OR: Individual headphone amplifier ($200)
   - Room PA system for original audio

4. **Visual**:
   - Large display(s) for captions
   - HDMI capture or direct computer connection

**Setup Diagram**:
```
Room Mics → Mixer → Audio Interface → Computer → Azure →
                                                    ↓
├── Channel 1 (Original) → PA System → Room Speakers
├── Channel 2 (Spanish) → Transmitter → Headsets
└── Captions → Display Screens
```

**Cost**: $3,000-$5,000 initial + ~$10/meeting Azure costs

---

### Option 3: Hybrid Meeting (Remote + In-Person)

**Best for**: Hybrid meetings with remote attendees

**Additional Equipment**:
- Streaming encoder or OBS Studio
- NDI or RTMP output
- Zoom/Teams integration (optional)

**Setup**:
```
Room Audio → Mixer → Computer → Azure Translation →
├── Local outputs (as Option 2)
├── Streaming platform → Remote attendees
└── Recording → Cloud storage
```

**Cost**: $4,000-$6,000 initial + ~$15/meeting Azure costs

## Step-by-Step Setup

### Phase 1: Azure Configuration

1. **Create Azure Resources**:
   - Create a Speech Service resource in the Azure Portal: https://portal.azure.com/#create/Microsoft.CognitiveServicesSpeechServices
   - Select a region that supports Live Interpreter: `eastus`, `westus2`, `westeurope`, `japaneast`, or `southeastasia`
   - Choose pricing tier (S0 for production)
   - Copy the Speech Key and Region from the resource

2. **Configure Application**:
   
   Create `.env` file (copy from `.env.example`):
   ```env
   # Azure Speech Service
   SPEECH_KEY=your_speech_service_key_here
   SPEECH_REGION=eastus
   SPEECH_ENDPOINT=https://eastus.api.cognitive.microsoft.com
   
   # Translation Settings
   SOURCE_LANGUAGE=en-US
   TARGET_LANGUAGE=es-ES
   
   # Voice Settings
   VOICE_NAME=en-US-JennyNeural
   
   # Application Settings
   LOG_LEVEL=INFO
   ```

### Phase 2: Hardware Setup

**Microphone Placement**:
- Position mics 18-24" from speakers
- Use boundary mics on table or ceiling mics above
- Test coverage before meeting
- Minimize background noise sources

**Audio Mixer Configuration**:
1. Connect all mics to mixer inputs
2. Set gain levels (avoid clipping)
3. Apply gentle compression
4. Enable phantom power if needed (XLR mics)
5. Main output → Audio interface

**Computer Audio Interface**:
1. Connect mixer output → interface input
2. Interface USB → computer
3. Set as default input device
4. Test recording levels

**Output Distribution**:

*Option A: Assistive Listening System*
```
Computer audio out → Transmitter base station
Attendees receive individual receivers with headphones
```

*Option B: FM System*
```
Computer → FM transmitter (87-108 MHz)
Attendees tune portable FM radios
```

*Option C: Wired Headphone System*
```
Computer → Headphone amplifier → Multiple headphone jacks
Attendees use provided headphones at seats
```

### Phase 3: Software Deployment

**On Dedicated Computer**:

1. **Install dependencies**:
   ```bash
   # Clone project
   git clone https://github.com/honestypugh2/live-interpreter-api-demo.git
   cd live-interpreter-api-demo
   
   # Verify uv is installed
   uv --version
   
   # If uv is not installed, install it:
   # Unix/macOS/Linux:
   curl -LsSf https://astral.sh/uv/install.sh | sh
   
   # Windows:
   # powershell -c "irm https://astral.sh/uv/install.ps1 | iex"
   
   # Or using pip:
   # pip install uv
   
   # Set up Python environment (requires Python 3.12+)
   # Sync dependencies (creates .venv automatically)
   uv sync
   
   # Activate virtual environment
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   
   # Copy and configure .env file
   cp .env.example .env
   # Edit .env with your Azure credentials
   ```

2. **Quick Start (Recommended)**:
   ```bash
   cd src/react_app
   chmod +x start.sh  # Make executable (first time only)
   ./start.sh  # On Windows: start.bat
   ```
   This script automatically:
   - Checks prerequisites (Python, Node.js, .env file)
   - Installs dependencies if needed
   - Starts both backend (port 8000) and frontend (port 5173)
   - Displays health status and logs

3. **Manual Start** (Alternative):
   
   **Terminal 1 - Backend**:
   ```bash
   cd src/react_app/backend
   uvicorn main:app --reload --host 0.0.0.0 --port 8000
   ```
   
   **Terminal 2 - Frontend**:
   ```bash
   cd src/react_app/frontend
   npm install
   npm run dev -- --host 0.0.0.0 --port 5173
   ```

4. **Access from other devices**:
   - On meeting room network: `http://<computer-ip>:5173`
   - Display captions on large screen
   - Operators can control from tablets

5. **Demo Mode (No Microphone/Azure Required)**:
   ```bash
   # Streamlit demo
   cd src/streamlit_app
   streamlit run app_demo.py
   
   # React demo
   cd src/react_app
   ./start-demo.sh  # On Windows: start-demo.bat
   ```
   Demo modes provide simulated translations for testing the UI without live audio or Azure costs.

### Phase 4: Pre-Meeting Checklist

**1 Week Before**:
- [ ] Test complete audio chain
- [ ] Verify Azure credits/billing
- [ ] Check internet bandwidth
- [ ] Test backup internet connection
- [ ] Prepare contingency plans

**1 Day Before**:
- [ ] Charge all wireless equipment
- [ ] Test microphones and speakers
- [ ] Verify computer startup/auto-launch
- [ ] Test translation with sample audio
- [ ] Print quick-reference guides

**1 Hour Before**:
- [ ] Power on all equipment
- [ ] Start backend and frontend servers
- [ ] Test end-to-end translation
- [ ] Distribute headsets/receivers
- [ ] Brief attendees on usage

**During Meeting**:
- [ ] Monitor translation quality
- [ ] Watch for audio clipping/distortion
- [ ] Check internet connection status
- [ ] Have backup operator ready
- [ ] Save recordings if enabled

## Network Requirements

**Bandwidth Per Meeting**:
- Upload: 512 kbps (audio to Azure)
- Download: 256 kbps (translations from Azure)
- **Recommended**: 10 Mbps symmetrical
- **Minimum**: 2 Mbps upload, 1 Mbps download

**Network Setup**:
```
Council Network (Wired Ethernet)
    ↓
Computer running demo
    ↓
Azure Speech Service (Cloud)
    ↓
Returned translations
```

**Reliability**:
- Use wired Ethernet (not WiFi)
- Configure static IP for computer
- Set up failover 4G/5G hotspot
- Monitor connection with ping tests

## Audio Quality Settings

**Recording Settings** (in app):
- Sample Rate: 16 kHz (adequate) or 48 kHz (best)
- Channels: Mono (single mic) or Stereo (mixed room)
- Format: WAV or FLAC lossless

**Mixer Settings**:
- HPF (High Pass Filter): 80-100 Hz
- Compression Ratio: 3:1
- Gate Threshold: -40 dB
- Master Output: -6 dB peak

## Accessibility Considerations

**For Attendees**:
- Provide clear instructions in both languages
- Label headphone channels (English/Spanish)
- Offer volume control on each headset
- Display captions prominently
- Have backup interpreters on standby

**For Speakers**:
- Brief on speaking pace and clarity
- Provide feedback on audio levels
- Show real-time translation display
- Allow for translation lag (~2-3 seconds)

## Troubleshooting

### No Translation Output
1. Check Azure credentials
2. Verify internet connection
3. Test microphone input levels
4. Review backend logs
5. Restart services if needed

### Poor Translation Quality
1. Reduce background noise
2. Ask speakers to slow down
3. Check microphone positioning
4. Verify audio isn't clipping
5. Ensure clear pronunciation

### Audio Feedback/Echo
1. Reduce speaker volume
2. Reposition microphones away from speakers
3. Enable acoustic echo cancellation
4. Use directional microphones

### Latency Issues
1. Check internet speed
2. Close bandwidth-heavy applications
3. Use wired connection
4. Choose closer Azure region

## Cost Analysis

### How These Estimates Were Calculated

**Equipment Costs**: Based on retail prices from major vendors (B&H Photo, Sweetwater, Amazon) as of November 2025. Prices may vary by retailer, region, and current promotions.

**Where to Get Equipment Pricing**:
- **Audio Equipment**: [Sweetwater.com](https://www.sweetwater.com), [B&H Photo](https://www.bhphotovideo.com)
- **Conference Microphones**: Amazon, manufacturer websites (Jabra, Poly, Shure)
- **Assistive Listening Systems**: [Williams Sound](https://www.williamssound.com), [Listen Technologies](https://www.listentech.com)
- **Computers**: Dell, HP, Lenovo business sections

**Azure Service Costs**: Based on official Azure pricing as of November 2025. Actual costs depend on:
- Meeting duration (billed per hour)
- Number of target languages (2+ languages incur additional charges)
- Amount of synthesized speech (billed per character for TTS)
- Region (some regions have different pricing)

**Where to Get Azure Pricing**:
- **Official Pricing Page**: [Azure Speech Services Pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/speech-services/)
- **Pricing Calculator**: [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/) - Build custom estimates
- **Your Azure Portal**: View actual usage and costs in Cost Management + Billing

### One-Time Setup Costs

**Note**: These are approximate retail prices. Consider:
- Bulk purchase discounts
- Refurbished/used equipment savings (20-40% off)
- Professional installation may cost more in some regions
- Cables and accessories vary widely by brand

| Item | Cost | Where to Buy |
|------|------|-------------|
| Microphones (6x) | $1,200 | Shure MX418, Audio-Technica boundary mics (~$200 each) |
| Audio Mixer | $500 | Behringer X32 Compact, Mackie ProFX series |
| Audio Interface | $180 | Focusrite Scarlett 2i2 (3rd Gen) |
| Computer | $800 | Dell OptiPlex, HP EliteDesk (i5, 8GB RAM, SSD) |
| Assistive Listening System | $1,000 | Williams Sound, Listen Technologies IR systems |
| Cables & Accessories | $200 | XLR cables, stands, adapters (Amazon, Monoprice) |
| Installation | $500 | Local AV integrator (varies by region: $50-100/hr) |
| **Total** | **$4,380** | **Estimates as of Nov 2025** |

### Recurring Costs (Per Meeting)

**Calculation Methodology**:

**Azure Speech Translation Cost**:
- **Base Rate**: $2.50/hour for speech translation (up to 2 target languages)
- **Calculation**: 2-hour meeting × $2.50/hour = $5.00
- **Source**: [Azure Speech Translation Pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/speech-services/)
- **Note**: 3+ target languages add $0.50/hour per additional language

**Live Interpreter Pricing** (Alternative pricing model):
- If using Live Interpreter feature specifically:
  - Input audio: $1.00 per audio hour
  - Output text: $10.00 per 1M characters
  - Output audio (Standard voice): $1.50 per audio hour
  - Output audio (Custom voice): $2.00 per audio hour
- **Total for 2-hr meeting with Live Interpreter**: ~$7.00 (input + output audio)
- The estimates in this guide use standard Speech Translation rates for simplicity

**Azure Neural TTS Cost**:
- **Base Rate**: $15.00 per 1 million characters
- **Estimation**: ~5,000 words translated = ~30,000 characters
- **Calculation**: 30,000 chars × ($15.00 / 1,000,000) = $0.45
- **Used in table**: $0.08 (conservative estimate assuming less speech)
- **Source**: [Azure Text-to-Speech Pricing](https://azure.microsoft.com/en-us/pricing/details/cognitive-services/speech-services/)

**How to Estimate Your Costs**:
1. **Measure meeting duration** (round up to nearest hour)
2. **Count target languages** (Spanish = 1, Spanish + French = 2)
3. **Estimate words spoken** (~150 words/minute average speech × meeting minutes)
4. **Use Azure Calculator**: Input your values at [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)

| Service | Cost | Calculation |
|---------|------|-------------|
| Azure Speech Translation (2 hrs, 1 target lang) | $5.00 | 2 hours × $2.50/hour |
| Azure Neural TTS (~5,000 words) | $0.08 | 30,000 chars × $15/1M chars (conservative) |
| Internet/Network | Included | Assuming existing infrastructure |
| Operator Time (optional, 2 hrs @ $25/hr) | $50.00 | Local labor rates vary |
| **Total Per Meeting (with operator)** | **$55.08** | |
| **Total Per Meeting (self-service)** | **$5.08** | |

### Annual Cost (24 Meetings/Year)

**Calculation**: Assumes bi-monthly council meetings (24 meetings × 2 hours each)

| Cost Category | Self-Service | Full Service |
|--------------|--------------|-------------|
| One-time Setup | $4,380 | $4,380 |
| Azure costs (24 meetings × $5.08) | $122 | $122 |
| Operator costs (24 meetings × $50) | — | $1,200 |
| **Total Year 1** | **$4,502** | **$5,702** |
| **Subsequent Years** | **$122/year** | **$1,322/year** |

### Cost Monitoring & Optimization

**Track Your Actual Azure Costs**:
1. **Azure Portal** → Cost Management + Billing → Cost Analysis
2. Filter by: Resource Group, Service (Cognitive Services), Date Range
3. Set up **Budget Alerts**: Get notified when costs exceed thresholds
4. Review monthly: Compare estimated vs. actual usage

**How to Reduce Costs**:
- ✅ **Use Demo Mode** for training (no Azure costs)
- ✅ **Shorter meetings** = lower translation costs
- ✅ **Fewer target languages** (1 language = $2.50/hr, 2+ = $0.50/hr extra each)
- ✅ **Disable TTS** if only text captions needed (saves ~$0.08-0.45 per meeting)
- ✅ **Turn off when not in use** (stop recognition between agenda items)
- ⚠️ **Free Tier**: Azure offers limited free tier (5 audio hours/month for Standard) - check current limits
- 💡 **Consider standard Speech Translation** vs Live Interpreter based on your needs

**Cost Comparison to Alternatives**:
- **Human Interpreter**: $200-400/hour = $400-800 per 2-hour meeting
- **Traditional IR System**: $10,000+ upfront + interpreter costs
- **Azure Live Interpreter**: $5-10 per meeting (automated)
- **Savings**: ~98% cost reduction vs. human interpreters for routine meetings

**Get Exact Pricing for Your Scenario**:
1. Visit [Azure Pricing Calculator](https://azure.microsoft.com/en-us/pricing/calculator/)
2. Add "Speech Services" → "Speech Translation"
3. Enter your parameters:
   - Hours per month: (meetings/month × hours/meeting)
   - Target languages: 1, 2, or 3+
   - Region: Select your Azure region
4. Add "Text to Speech" if using audio synthesis
5. Export estimate as PDF for budget approval

## Best Practices

1. **Always Test Before Live**:
   - Run practice translation 30 minutes before
   - Test all audio paths
   - Verify captions displaying

2. **Have Backup Plans**:
   - Human interpreter on standby
   - Backup internet connection
   - Spare batteries/equipment
   - Printed materials in both languages

3. **Monitor Continuously**:
   - Watch translation accuracy
   - Check attendee headsets working
   - Monitor internet connection
   - Log any issues for improvement

4. **Gather Feedback**:
   - Survey attendees after meeting
   - Ask about audio quality
   - Check translation accuracy
   - Improve setup based on feedback

5. **Maintain Equipment**:
   - Clean microphones regularly
   - Update software monthly
   - Test batteries before meetings
   - Keep spare cables/adapters

## Alternative Solutions

If Azure Live Interpreter doesn't meet needs:

1. **Professional Human Interpreters**:
   - Cost: $200-400/hour per language
   - Pros: Highest accuracy, cultural context
   - Cons: Expensive, scheduling required

2. **Simultaneous Interpretation Equipment**:
   - Traditional IR system with human interpreters
   - Cost: $10,000+ for system
   - Pros: Industry standard, reliable
   - Cons: High cost, requires interpreters

3. **Hybrid Approach**:
   - Use Azure for most translations
   - Have human interpreter review/correct
   - Best of both worlds

## Additional Resources

- Azure Speech Service Documentation
- Audio equipment vendor guides
- Professional AV installer contacts
- Accessibility compliance guidelines
- Sample meeting templates

---

**Questions?** See main project README.md or contact support.
