# Azure Speech Voice Options & Customization Guide

**Document Version**: 1.0  
**Last Updated**: November 17, 2025  
**Applies To**: Live Interpreter API Demo (Streamlit & React Apps)

## Overview

This guide provides comprehensive information on Azure Speech voice options, from prebuilt neural voices to Personal Voice, including style and tone customization. It includes practical guidance for implementing voice configurations in this demo application.

---

## Table of Contents

1. [Voice Types Overview](#voice-types-overview)
2. [Prebuilt Neural Voices](#prebuilt-neural-voices)
3. [Personal Voice](#personal-voice)
4. [Voice Customization Options](#voice-customization-options)
5. [SSML for Advanced Control](#ssml-for-advanced-control)
6. [Implementation in This Demo](#implementation-in-this-demo)
7. [Testing & Validation](#testing--validation)
8. [Best Practices](#best-practices)

---

## Voice Types Overview

Azure Speech Service offers three tiers of voice technology:

| Voice Type | Quality | Customization | Latency | Cost | Approval Required |
|------------|---------|---------------|---------|------|-------------------|
| **Standard Voices** | Good | Limited | Low | Lowest | ❌ No |
| **Neural Voices** | Excellent | SSML styles | Low | Standard | ❌ No |
| **Personal Voice** | Preserves original | Advanced | Low-Medium | Standard | ✅ Yes |

### Voice Technology Evolution

```
Standard Voices (2016)
    ↓ Concatenative synthesis
    ↓ Robotic sound, limited prosody
    
Neural Voices (2018)
    ↓ Deep learning TTS
    ↓ Natural intonation, emotional expression
    ↓ 119 languages, 409+ voices
    
Personal Voice (2023)
    ↓ Speaker-adaptive synthesis
    ↓ Preserves speaker identity
    ↓ Maintains voice characteristics across languages
```

---

## Prebuilt Neural Voices

### What are Neural Voices?

Neural voices use deep neural networks to synthesize human-like speech with natural prosody, emotion, and speaking styles. They are **immediately available** without any approval process.

### Key Features

✅ **Natural Sounding**: Human-like intonation and rhythm  
✅ **Multilingual**: 119 languages and variants  
✅ **Multiple Styles**: Conversational, professional, cheerful, empathetic, etc.  
✅ **Emotion Control**: Adjust emotional expression via SSML  
✅ **Speaking Rates**: Variable speed without pitch distortion  
✅ **Production Ready**: GA (Generally Available) globally  

### Voice Categories

#### 1. General Purpose Voices
Standard neural voices suitable for most applications.

**Popular English Voices**:
| Voice Name | Gender | Age | Style | Best For |
|------------|--------|-----|-------|----------|
| `en-US-JennyNeural` | Female | Adult | Professional, clear | Business meetings, announcements |
| `en-US-GuyNeural` | Male | Adult | Warm, friendly | Customer service, narration |
| `en-US-AriaNeural` | Female | Adult | Conversational | Chatbots, virtual assistants |
| `en-US-DavisNeural` | Male | Adult | Authoritative | News, formal presentations |
| `en-US-JaneNeural` | Female | Adult | Casual, expressive | Storytelling, education |

**Popular Spanish Voices**:
| Voice Name | Gender | Locale | Style | Best For |
|------------|--------|--------|-------|----------|
| `es-ES-ElviraNeural` | Female | Spain | Professional | Council meetings, official events |
| `es-ES-AlvaroNeural` | Male | Spain | Clear, formal | Public announcements |
| `es-MX-DaliaNeural` | Female | Mexico | Natural, warm | Community events |
| `es-MX-JorgeNeural` | Male | Mexico | Friendly | Town halls, public forums |
| `es-US-AlonsoNeural` | Male | US Spanish | Bilingual-friendly | US Hispanic communities |

#### 2. Multilingual Voices
Single voice that can speak multiple languages with native-like quality.

**Multilingual Neural Voices**:
| Voice Name | Languages | Best For |
|------------|-----------|----------|
| `en-US-JennyMultilingualNeural` | English, Spanish, French, German, Italian, Portuguese | International meetings |
| `es-MX-DaliaMultilingualNeural` | Spanish, English | Bilingual US/Mexico events |
| `fr-FR-VivienneMultilingualNeural` | French, English, Spanish | European conferences |

**Advantages**:
- Consistent voice across languages
- Reduced cognitive load for listeners
- Maintains speaker "identity" across translations

#### 3. Long-Form Voices
Optimized for extended content (books, articles, long presentations).

| Voice Name | Language | Characteristics |
|------------|----------|-----------------|
| `en-US-AvaMultilingualNeural` | English + 13 languages | Storytelling, sustained engagement |
| `en-US-BrianMultilingualNeural` | English + 13 languages | Documentary-style narration |

### Accessing Neural Voices

#### Browse All Voices
🔗 [Azure Neural Voices Gallery](https://speech.microsoft.com/portal/voicegallery)

#### Get Voice List via API
```python
import azure.cognitiveservices.speech as speechsdk

speech_config = speechsdk.SpeechConfig(
    subscription="YOUR-KEY",
    region="eastus"
)

synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
result = synthesizer.get_voices_async().get()

# Filter for Spanish neural voices
spanish_voices = [
    voice for voice in result.voices 
    if voice.locale.startswith("es-") and "Neural" in voice.short_name
]

for voice in spanish_voices:
    print(f"{voice.short_name}: {voice.gender}, {voice.locale}")
```

### Regional Availability

All neural voices are available in these regions:
- `eastus`, `eastus2`, `westus`, `westus2`, `westus3`
- `westeurope`, `northeurope`, `uksouth`
- `southeastasia`, `eastasia`, `japaneast`
- `australiaeast`, `brazilsouth`, `canadacentral`

⚠️ **Important**: For Live Interpreter API with personal voice, use only: `eastus`, `westus2`, `westeurope`, `japaneast`, `southeastasia`

---

## Personal Voice

### What is Personal Voice?

Personal Voice is Azure's speaker-adaptive text-to-speech technology that **preserves the unique characteristics of a speaker's voice** across languages. It maintains voice identity, tone, pitch, and speaking style when translating speech.

### When to Use Personal Voice

✅ **High-Profile Speakers**: Politicians, executives, public figures  
✅ **Voice Branding**: Organizations wanting consistent speaker identity  
✅ **Accessibility**: Users who prefer hearing familiar voices  
✅ **Trust Building**: Maintaining speaker authenticity in translations  
✅ **Cultural Sensitivity**: Preserving speaker's vocal identity

❌ **When NOT to Use**:
- General public meetings (prebuilt voices are sufficient)
- Budget-constrained deployments
- Quick proof-of-concept projects
- Speakers uncomfortable with voice replication

### How Personal Voice Works

```
Original Speaker Audio (Source Language)
    ↓
Voice Analysis & Extraction
    ├─ Pitch characteristics
    ├─ Speaking rate patterns
    ├─ Tone and timbre
    └─ Prosody patterns
    ↓
Translation to Target Language
    ↓
Synthesis with Preserved Voice Characteristics
    ↓
Output: Translated speech in speaker's voice
```

### Requirements & Approval Process

#### 1. **Azure Subscription**
- Active Azure subscription with Speech Service
- Approved for Custom Neural Voice access

#### 2. **Apply for Access**
🔗 **Application Portal**: https://aka.ms/customneural

**Required Information**:
- Organization details and use case description
- Intended deployment scenario
- Expected volume of usage
- Consent and ethical use attestation

**Approval Timeline**: Typically 1-2 weeks

#### 3. **Supported Regions** (Live Interpreter with Personal Voice)
Only these regions support Live Interpreter + Personal Voice:
- `eastus`
- `westus2`
- `westeurope`
- `japaneast`
- `southeastasia`

#### 4. **Consent Requirements**

⚠️ **Critical**: You MUST obtain explicit consent from speakers before using Personal Voice.

**Consent Elements**:
- Written agreement from speaker
- Clear explanation of voice replication
- Usage scope and duration
- Data retention policies
- Right to revoke consent

**Sample Consent Form**:
```
I, [Speaker Name], consent to the use of Personal Voice technology 
to replicate my voice characteristics for real-time translation during 
[Event Name] on [Date]. I understand that:

1. My voice characteristics will be analyzed and used for translation
2. The translated audio will sound similar to my natural voice
3. Audio will be used only for this event and not stored
4. I can revoke consent by notifying [Organization] in writing
5. Voice samples will not be used for other purposes

Signature: ________________  Date: __________
```

### Personal Voice Configuration

#### In .env File
```bash
# Enable Live Interpreter with Personal Voice
ENABLE_LIVE_INTERPRETER=true
VOICE_NAME=personal-voice

# Must use approved region
AZURE_SPEECH_REGION=eastus

# Your approved Speech key
AZURE_SPEECH_KEY=your-approved-key-here
```

#### In Python Code
```python
from src.core.translator import LiveInterpreterTranslator
from src.core.config import get_settings

settings = get_settings()

# Create translator with personal voice
translator = LiveInterpreterTranslator(
    settings=settings,
    use_personal_voice=True  # Enable personal voice preservation
)

# Source language detection will preserve speaker's voice
recognizer = translator.create_recognizer_from_microphone(
    auto_detect_languages=["en-US", "es-ES", "fr-FR"]
)
```

### Personal Voice vs. Neural Voice Comparison

| Feature | Neural Voice | Personal Voice |
|---------|--------------|----------------|
| **Setup Time** | Immediate | 1-2 weeks approval |
| **Voice Consistency** | Prebuilt voice | Speaker's actual voice |
| **Language Support** | 119 languages | Same as source |
| **Customization** | SSML styles | Voice characteristics |
| **Cost** | $16/1M chars | $16/1M chars (same) |
| **Use Case** | General meetings | VIP speakers |
| **Approval** | None required | Application required |

---

## Voice Customization Options

### 1. Speaking Styles (Neural Voices Only)

Many neural voices support multiple speaking styles for different contexts.

#### Available Styles by Voice

**en-US-AriaNeural Styles**:
- `default` - Neutral, professional
- `cheerful` - Upbeat, positive
- `empathetic` - Understanding, caring
- `newscast` - Formal news broadcast style
- `customerservice` - Patient, helpful
- `chat` - Casual conversation
- `angry` - Expressing frustration (use carefully!)
- `sad` - Expressing sorrow

**en-US-JennyNeural Styles**:
- `default` - Professional
- `assistant` - Virtual assistant tone
- `chat` - Conversational
- `customerservice` - Service-oriented
- `newscast` - Broadcast news style

**es-MX-DaliaNeural Styles**:
- `default` - Natural conversational
- `cheerful` - Positive, upbeat

#### Style Implementation via SSML

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" 
       xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
    <voice name="en-US-AriaNeural">
        <mstts:express-as style="customerservice" styledegree="2">
            Welcome to the city council meeting. How may I assist you today?
        </mstts:express-as>
    </voice>
</speak>
```

**Style Degree**: Control intensity of style (0.01 to 2.0)
- `0.01` - Subtle hint of style
- `1.0` - Default intensity
- `2.0` - Maximum expression

### 2. Speaking Rate

Control the speed of speech without affecting pitch quality.

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
    <voice name="en-US-JennyNeural">
        <prosody rate="-10%">
            This is spoken 10% slower than normal for clarity.
        </prosody>
    </voice>
</speak>
```

**Rate Values**:
- `+50%` - 50% faster (rapid announcements)
- `+20%` - Slightly faster (time-constrained)
- `0%` or `default` - Normal speed
- `-20%` - Slightly slower (emphasis)
- `-50%` - 50% slower (accessibility)

**Recommended for Council Meetings**: `-10%` to `0%` (clear, professional pace)

### 3. Pitch Adjustment

Modify the pitch of the voice without changing speaking rate.

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
    <voice name="en-US-GuyNeural">
        <prosody pitch="-5%">
            Lower pitch for authoritative tone.
        </prosody>
    </voice>
</speak>
```

**Pitch Values**:
- `+20%` - Higher pitch (younger, energetic)
- `0%` - Default voice pitch
- `-10%` - Lower pitch (authoritative, serious)

⚠️ **Caution**: Large pitch shifts can sound unnatural. Stay within ±20%.

### 4. Volume Control

Adjust the loudness of synthesized speech.

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
    <voice name="en-US-JennyNeural">
        <prosody volume="+10dB">
            This text is louder for emphasis.
        </prosody>
    </voice>
</speak>
```

**Volume Values**:
- `+10dB` - Louder
- `0dB` or `default` - Normal
- `-10dB` - Softer
- Relative: `loud`, `medium`, `soft`, `x-soft`, `x-loud`

### 5. Emphasis & Pauses

Add natural pauses and emphasis for important information.

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
    <voice name="en-US-JennyNeural">
        <emphasis level="strong">This is very important.</emphasis>
        <break time="500ms"/>
        Please take note of the following agenda items.
    </voice>
</speak>
```

**Emphasis Levels**:
- `strong` - Strong emphasis
- `moderate` - Medium emphasis
- `reduced` - De-emphasized

**Break Times**:
- `100ms` - Brief pause (comma)
- `300ms` - Sentence pause (period)
- `500ms` - Paragraph break
- `1s` - Long pause (section break)

### 6. Role Play (Select Voices)

Some voices support role-playing for different speaker personas.

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" 
       xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
    <voice name="en-US-JennyNeural">
        <mstts:express-as role="OlderAdultMale">
            As the senior council member, I propose we table this motion.
        </mstts:express-as>
    </voice>
</speak>
```

**Available Roles** (voice-dependent):
- `YoungAdultFemale`
- `YoungAdultMale`
- `OlderAdultFemale`
- `OlderAdultMale`
- `Girl`
- `Boy`

### 7. Language Mixing (Multilingual Voices)

Mix languages within a single speech output.

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
    <voice name="en-US-JennyMultilingualNeural">
        Welcome to the meeting.
        <lang xml:lang="es-MX">
            Bienvenidos a la reunión.
        </lang>
    </voice>
</speak>
```

---

## SSML for Advanced Control

### What is SSML?

**Speech Synthesis Markup Language (SSML)** is an XML-based markup language that provides fine-grained control over speech synthesis.

### SSML Structure

```xml
<speak version="1.0" 
       xmlns="http://www.w3.org/2001/10/synthesis"
       xmlns:mstts="https://www.w3.org/2001/mstts" 
       xml:lang="en-US">
    <voice name="en-US-JennyNeural">
        <!-- Your text with SSML markup -->
    </voice>
</speak>
```

### Common SSML Patterns for Council Meetings

#### 1. Professional Announcement

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
       xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
    <voice name="en-US-JennyNeural">
        <mstts:express-as style="newscast">
            <prosody rate="-5%">
                Good evening, and welcome to the city council meeting.
                <break time="300ms"/>
                Today's agenda includes budget review and public comment.
            </prosody>
        </mstts:express-as>
    </voice>
</speak>
```

#### 2. Empathetic Public Response

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
       xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
    <voice name="en-US-AriaNeural">
        <mstts:express-as style="empathetic" styledegree="1.5">
            We understand your concerns about the proposed changes.
            <break time="400ms"/>
            Your feedback is valuable to this council.
        </mstts:express-as>
    </voice>
</speak>
```

#### 3. Bilingual Announcement

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
    <voice name="en-US-JennyMultilingualNeural">
        <prosody rate="-10%">
            Please silence your mobile devices.
            <break time="500ms"/>
            <lang xml:lang="es-MX">
                Por favor, silencie sus dispositivos móviles.
            </lang>
        </prosody>
    </voice>
</speak>
```

#### 4. Reading Formal Motion

```xml
<speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="en-US">
    <voice name="en-US-DavisNeural">
        <prosody rate="-15%" pitch="-5%">
            Motion number <say-as interpret-as="cardinal">423</say-as>.
            <break time="300ms"/>
            <emphasis level="moderate">
                Resolved that the council approve the budget amendment
            </emphasis>
            in the amount of <say-as interpret-as="currency">$2,500,000</say-as>.
        </prosody>
    </voice>
</speak>
```

### SSML Python Helper Functions

```python
def create_council_ssml(text: str, voice: str = "en-US-JennyNeural", 
                        style: str = "newscast", rate: str = "-5%") -> str:
    """Generate SSML for professional council meeting speech."""
    return f"""
    <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
           xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
        <voice name="{voice}">
            <mstts:express-as style="{style}">
                <prosody rate="{rate}">
                    {text}
                </prosody>
            </mstts:express-as>
        </voice>
    </speak>
    """

# Usage
ssml = create_council_ssml(
    "Welcome to the city council meeting.",
    voice="en-US-JennyNeural",
    style="newscast",
    rate="-10%"
)
```

---

## Implementation in This Demo

### Configuration Options

#### Option 1: Environment Variables (Simple)

**For Prebuilt Neural Voice** (`.env`):
```bash
ENABLE_LIVE_INTERPRETER=true
VOICE_NAME=en-US-JennyNeural
TARGET_VOICE_ES=es-ES-ElviraNeural
TARGET_VOICE_FR=fr-FR-DeniseNeural

# Optional: Default speaking rate (SSML)
DEFAULT_SPEAKING_RATE=-10%
DEFAULT_STYLE=newscast
```

**For Personal Voice** (`.env`):
```bash
ENABLE_LIVE_INTERPRETER=true
VOICE_NAME=personal-voice
AZURE_SPEECH_REGION=eastus  # Must be approved region
```

#### Option 2: Runtime Configuration (Flexible)

Update `src/core/config.py`:

```python
from pydantic_settings import BaseSettings
from typing import Optional, Dict

class Settings(BaseSettings):
    # Existing settings...
    
    # Voice configuration
    voice_name: str = "en-US-JennyNeural"
    use_personal_voice: bool = False
    
    # Voice preferences per language
    voice_preferences: Dict[str, str] = {
        "en": "en-US-JennyNeural",
        "es": "es-ES-ElviraNeural",
        "fr": "fr-FR-DeniseNeural",
        "de": "de-DE-KatjaNeural",
        "zh": "zh-CN-XiaoxiaoNeural"
    }
    
    # SSML customization
    default_speaking_rate: str = "-10%"
    default_style: Optional[str] = "newscast"
    enable_ssml: bool = False
    
    class Config:
        env_file = ".env"
        case_sensitive = False
```

### Implementing Voice Preferences in Translator

Update `src/core/translator.py`:

```python
class LiveInterpreterTranslator:
    def __init__(
        self, 
        settings: Settings, 
        use_personal_voice: bool = False,
        voice_preferences: Optional[Dict[str, str]] = None,
        enable_ssml: bool = False
    ):
        self.settings = settings
        self.use_personal_voice = use_personal_voice
        self.voice_preferences = voice_preferences or settings.voice_preferences
        self.enable_ssml = enable_ssml
        
        # Initialize speech config
        self.speech_config = speechsdk.SpeechConfig(
            subscription=settings.azure_speech_key,
            region=settings.azure_speech_region
        )
        
        # Configure voice based on mode
        if use_personal_voice:
            self.speech_config.speech_synthesis_voice_name = "personal-voice"
        else:
            # Use default neural voice
            self.speech_config.speech_synthesis_voice_name = settings.voice_name
    
    def create_recognizer_from_microphone(
        self,
        source_language: Optional[str] = None,
        target_languages: Optional[List[str]] = None,
        auto_detect_languages: Optional[List[str]] = None
    ) -> speechsdk.translation.TranslationRecognizer:
        """Create recognizer with voice preferences."""
        
        # Set up translation config
        translation_config = speechsdk.translation.SpeechTranslationConfig(
            subscription=self.settings.azure_speech_key,
            region=self.settings.azure_speech_region
        )
        
        # Configure languages
        if auto_detect_languages:
            # Live Interpreter mode with auto-detection
            auto_detect_config = speechsdk.languageconfig.AutoDetectSourceLanguageConfig(
                languages=auto_detect_languages
            )
        else:
            translation_config.speech_recognition_language = source_language or "en-US"
        
        # Add target languages
        for lang in (target_languages or ["es", "fr"]):
            translation_config.add_target_language(lang)
        
        # Configure voice for each target language
        for lang_code, voice_name in self.voice_preferences.items():
            if lang_code in (target_languages or []):
                # Set voice per language
                translation_config.voice_name = voice_name
        
        # Create audio config
        audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)
        
        # Create recognizer
        if auto_detect_languages:
            recognizer = speechsdk.translation.TranslationRecognizer(
                translation_config=translation_config,
                audio_config=audio_config,
                auto_detect_source_language_config=auto_detect_config
            )
        else:
            recognizer = speechsdk.translation.TranslationRecognizer(
                translation_config=translation_config,
                audio_config=audio_config
            )
        
        return recognizer
    
    def apply_ssml_customization(self, text: str, language: str) -> str:
        """Apply SSML formatting for enhanced speech control."""
        if not self.enable_ssml:
            return text
        
        # Get voice for language
        voice_name = self.voice_preferences.get(language, self.settings.voice_name)
        
        # Determine if voice supports styles
        style_voices = [
            "en-US-AriaNeural", "en-US-JennyNeural", 
            "en-US-GuyNeural", "es-MX-DaliaNeural"
        ]
        
        style = self.settings.default_style if voice_name in style_voices else None
        rate = self.settings.default_speaking_rate
        
        # Build SSML
        if style:
            return f"""
            <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
                   xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="{language}">
                <voice name="{voice_name}">
                    <mstts:express-as style="{style}">
                        <prosody rate="{rate}">
                            {text}
                        </prosody>
                    </mstts:express-as>
                </voice>
            </speak>
            """
        else:
            return f"""
            <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis" xml:lang="{language}">
                <voice name="{voice_name}">
                    <prosody rate="{rate}">
                        {text}
                    </prosody>
                </voice>
            </speak>
            """
```

### Streamlit App Integration

Update `src/streamlit_app/app.py` to include voice selection:

```python
import streamlit as st
from src.core.config import get_settings
from src.core.translator import LiveInterpreterTranslator

# Voice selection UI
st.sidebar.header("Voice Configuration")

# Personal voice toggle
use_personal_voice = st.sidebar.checkbox(
    "Use Personal Voice (Requires Approval)",
    value=False,
    help="Preserve speaker's voice characteristics across languages"
)

if not use_personal_voice:
    # Neural voice selection
    voice_options = {
        "Jenny (Female, Professional)": "en-US-JennyNeural",
        "Guy (Male, Warm)": "en-US-GuyNeural",
        "Aria (Female, Conversational)": "en-US-AriaNeural",
        "Davis (Male, Authoritative)": "en-US-DavisNeural",
    }
    
    selected_voice_label = st.sidebar.selectbox(
        "Select Voice",
        options=list(voice_options.keys()),
        index=0
    )
    
    voice_name = voice_options[selected_voice_label]
    
    # Style selection (for supported voices)
    if voice_name in ["en-US-AriaNeural", "en-US-JennyNeural"]:
        style_options = ["default", "newscast", "customerservice", "chat", "cheerful", "empathetic"]
        selected_style = st.sidebar.selectbox("Speaking Style", style_options)
    else:
        selected_style = "default"
    
    # Speaking rate
    speaking_rate = st.sidebar.slider(
        "Speaking Rate",
        min_value=-50,
        max_value=50,
        value=-10,
        step=5,
        help="Negative = slower, Positive = faster"
    )
    
    # Preview voice
    if st.sidebar.button("Preview Voice"):
        preview_text = "Welcome to the city council meeting. This is a voice preview."
        # Generate and play preview audio
        # (Implementation depends on your audio handler)

# Create translator with configuration
settings = get_settings()
translator = LiveInterpreterTranslator(
    settings=settings,
    use_personal_voice=use_personal_voice,
    voice_preferences={
        "en": voice_name if not use_personal_voice else "personal-voice",
        "es": "es-ES-ElviraNeural",
        "fr": "fr-FR-DeniseNeural"
    },
    enable_ssml=True
)
```

### React App Integration

Update `src/react_app/frontend/src/components/VoiceSelector.tsx`:

```typescript
import React, { useState } from 'react';

interface VoiceOption {
  id: string;
  name: string;
  gender: 'Male' | 'Female';
  description: string;
  styles?: string[];
}

const VOICE_OPTIONS: VoiceOption[] = [
  {
    id: 'en-US-JennyNeural',
    name: 'Jenny',
    gender: 'Female',
    description: 'Professional, clear voice for formal settings',
    styles: ['default', 'newscast', 'customerservice', 'chat']
  },
  {
    id: 'en-US-GuyNeural',
    name: 'Guy',
    gender: 'Male',
    description: 'Warm, friendly voice for community events',
    styles: ['default', 'newscast']
  },
  {
    id: 'en-US-AriaNeural',
    name: 'Aria',
    gender: 'Female',
    description: 'Conversational, engaging for interactive sessions',
    styles: ['default', 'cheerful', 'empathetic', 'chat', 'angry', 'sad']
  },
  {
    id: 'en-US-DavisNeural',
    name: 'Davis',
    gender: 'Male',
    description: 'Authoritative, formal for official announcements',
    styles: ['default', 'newscast']
  }
];

export const VoiceSelector: React.FC = () => {
  const [selectedVoice, setSelectedVoice] = useState<string>('en-US-JennyNeural');
  const [selectedStyle, setSelectedStyle] = useState<string>('default');
  const [speakingRate, setSpeakingRate] = useState<number>(-10);
  const [usePersonalVoice, setUsePersonalVoice] = useState<boolean>(false);

  const currentVoice = VOICE_OPTIONS.find(v => v.id === selectedVoice);

  const handleVoiceChange = (voiceId: string) => {
    setSelectedVoice(voiceId);
    setSelectedStyle('default'); // Reset style when changing voice
  };

  const previewVoice = async () => {
    const previewText = "Welcome to the city council meeting. This is a voice preview.";
    
    // Send configuration to backend
    const config = {
      voice: usePersonalVoice ? 'personal-voice' : selectedVoice,
      style: selectedStyle,
      rate: `${speakingRate}%`,
      text: previewText
    };
    
    // Call preview API
    // (Implementation depends on your WebSocket/API setup)
  };

  return (
    <div className="voice-selector p-4 bg-white rounded-lg shadow">
      <h3 className="text-lg font-semibold mb-4">Voice Configuration</h3>
      
      {/* Personal Voice Toggle */}
      <div className="mb-4">
        <label className="flex items-center space-x-2">
          <input
            type="checkbox"
            checked={usePersonalVoice}
            onChange={(e) => setUsePersonalVoice(e.target.checked)}
            className="form-checkbox"
          />
          <span className="text-sm">
            Use Personal Voice (Requires Approval)
          </span>
        </label>
        {usePersonalVoice && (
          <p className="text-xs text-gray-600 mt-1">
            Preserves speaker's voice characteristics across languages
          </p>
        )}
      </div>

      {!usePersonalVoice && (
        <>
          {/* Voice Selection */}
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">Select Voice</label>
            <div className="grid grid-cols-1 md:grid-cols-2 gap-2">
              {VOICE_OPTIONS.map(voice => (
                <button
                  key={voice.id}
                  onClick={() => handleVoiceChange(voice.id)}
                  className={`p-3 text-left rounded border-2 transition ${
                    selectedVoice === voice.id
                      ? 'border-blue-500 bg-blue-50'
                      : 'border-gray-200 hover:border-gray-300'
                  }`}
                >
                  <div className="font-medium">{voice.name}</div>
                  <div className="text-xs text-gray-600">{voice.gender}</div>
                  <div className="text-xs text-gray-500 mt-1">{voice.description}</div>
                </button>
              ))}
            </div>
          </div>

          {/* Style Selection */}
          {currentVoice?.styles && currentVoice.styles.length > 1 && (
            <div className="mb-4">
              <label className="block text-sm font-medium mb-2">Speaking Style</label>
              <select
                value={selectedStyle}
                onChange={(e) => setSelectedStyle(e.target.value)}
                className="w-full p-2 border rounded"
              >
                {currentVoice.styles.map(style => (
                  <option key={style} value={style}>
                    {style.charAt(0).toUpperCase() + style.slice(1)}
                  </option>
                ))}
              </select>
            </div>
          )}

          {/* Speaking Rate */}
          <div className="mb-4">
            <label className="block text-sm font-medium mb-2">
              Speaking Rate: {speakingRate > 0 ? '+' : ''}{speakingRate}%
            </label>
            <input
              type="range"
              min="-50"
              max="50"
              step="5"
              value={speakingRate}
              onChange={(e) => setSpeakingRate(Number(e.target.value))}
              className="w-full"
            />
            <div className="flex justify-between text-xs text-gray-600">
              <span>Slower</span>
              <span>Normal</span>
              <span>Faster</span>
            </div>
          </div>

          {/* Preview Button */}
          <button
            onClick={previewVoice}
            className="w-full py-2 px-4 bg-blue-500 text-white rounded hover:bg-blue-600 transition"
          >
            Preview Voice
          </button>
        </>
      )}
    </div>
  );
};
```

### Backend WebSocket Handler Update

Update `src/react_app/backend/main.py` to handle voice configuration:

```python
@app.websocket("/ws")
async def websocket_endpoint(websocket: WebSocket):
    await websocket.accept()
    translator = None
    
    try:
        while True:
            data = await websocket.receive_json()
            message_type = data.get("type")
            
            if message_type == "config":
                # Extract voice configuration
                use_personal_voice = data.get("use_personal_voice", False)
                voice_name = data.get("voice_name", "en-US-JennyNeural")
                speaking_style = data.get("style", "default")
                speaking_rate = data.get("rate", "-10%")
                
                voice_preferences = {
                    "en": voice_name if not use_personal_voice else "personal-voice",
                    "es": data.get("target_voice_es", "es-ES-ElviraNeural"),
                    "fr": data.get("target_voice_fr", "fr-FR-DeniseNeural")
                }
                
                # Initialize translator with voice config
                translator = LiveInterpreterTranslator(
                    settings=get_settings(),
                    use_personal_voice=use_personal_voice,
                    voice_preferences=voice_preferences,
                    enable_ssml=True
                )
                
                # Store SSML preferences
                translator.settings.default_style = speaking_style
                translator.settings.default_speaking_rate = speaking_rate
                
                await websocket.send_json({
                    "type": "config_confirmed",
                    "voice_config": {
                        "personal_voice": use_personal_voice,
                        "voice_name": voice_name,
                        "style": speaking_style,
                        "rate": speaking_rate
                    }
                })
            
            elif message_type == "preview_voice":
                # Preview voice with sample text
                preview_text = data.get("text", "This is a voice preview.")
                language = data.get("language", "en-US")
                
                # Generate preview audio
                # (Implementation using audio_handler)
                
    except WebSocketDisconnect:
        logger.info("WebSocket disconnected")
```

---

## Testing & Validation

### 1. Voice Quality Testing

Create test script `tests/test_voice_quality.py`:

```python
import azure.cognitiveservices.speech as speechsdk
from src.core.config import get_settings

def test_voice_quality():
    """Test various voice configurations."""
    settings = get_settings()
    
    test_cases = [
        {
            "voice": "en-US-JennyNeural",
            "style": "newscast",
            "rate": "-10%",
            "text": "Good evening and welcome to the city council meeting."
        },
        {
            "voice": "en-US-AriaNeural",
            "style": "empathetic",
            "rate": "0%",
            "text": "We understand your concerns and appreciate your feedback."
        },
        {
            "voice": "es-ES-ElviraNeural",
            "style": "default",
            "rate": "-5%",
            "text": "Bienvenidos a la reunión del consejo municipal."
        }
    ]
    
    for i, test in enumerate(test_cases, 1):
        print(f"\nTest Case {i}: {test['voice']} ({test['style']})")
        
        # Build SSML
        ssml = f"""
        <speak version="1.0" xmlns="http://www.w3.org/2001/10/synthesis"
               xmlns:mstts="https://www.w3.org/2001/mstts" xml:lang="en-US">
            <voice name="{test['voice']}">
                <mstts:express-as style="{test['style']}">
                    <prosody rate="{test['rate']}">
                        {test['text']}
                    </prosody>
                </mstts:express-as>
            </voice>
        </speak>
        """
        
        # Synthesize
        speech_config = speechsdk.SpeechConfig(
            subscription=settings.azure_speech_key,
            region=settings.azure_speech_region
        )
        synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config)
        
        result = synthesizer.speak_ssml_async(ssml).get()
        
        if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
            print(f"✓ Audio generated successfully ({len(result.audio_data)} bytes)")
        else:
            print(f"✗ Error: {result.reason}")

if __name__ == "__main__":
    test_voice_quality()
```

Run tests:
```bash
cd /home/brittanypugh/live-interpreter-api-demo
python -m pytest tests/test_voice_quality.py -v
```

### 2. A/B Testing Framework

Compare different voice configurations:

```python
def voice_ab_test():
    """Compare two voice configurations side by side."""
    
    test_text = "The motion is approved by a vote of seven to three."
    
    config_a = {
        "name": "Professional Female",
        "voice": "en-US-JennyNeural",
        "style": "newscast",
        "rate": "-10%"
    }
    
    config_b = {
        "name": "Authoritative Male",
        "voice": "en-US-DavisNeural",
        "style": "default",
        "rate": "-5%"
    }
    
    print("Testing Configuration A...")
    synthesize_with_config(test_text, config_a)
    
    input("\nPress Enter to test Configuration B...")
    synthesize_with_config(test_text, config_b)
    
    choice = input("\nWhich configuration do you prefer? (A/B): ")
    return choice.upper()
```

### 3. User Feedback Collection

Implement feedback mechanism in Streamlit:

```python
# In Streamlit app
if st.button("Rate Voice Quality"):
    rating = st.slider("How natural did the voice sound?", 1, 5, 3)
    clarity = st.slider("How clear was the pronunciation?", 1, 5, 3)
    timing = st.slider("Was the speaking pace appropriate?", 1, 5, 3)
    
    feedback = {
        "voice": current_voice,
        "rating": rating,
        "clarity": clarity,
        "timing": timing,
        "timestamp": datetime.now()
    }
    
    # Save to feedback log
    save_feedback(feedback)
    st.success("Thank you for your feedback!")
```

---

## Best Practices

### 1. Voice Selection Guidelines

#### For Formal Council Meetings
- **Primary Voice**: `en-US-JennyNeural` (professional, clear)
- **Style**: `newscast` or `default`
- **Rate**: `-10%` (slightly slower for clarity)
- **Pitch**: `default` (maintain authority)

#### For Community Town Halls
- **Primary Voice**: `en-US-AriaNeural` or `en-US-GuyNeural`
- **Style**: `chat` or `empathetic`
- **Rate**: `-5%` to `0%` (conversational)
- **Pitch**: `default`

#### For Multilingual Events
- **Use**: Multilingual neural voices (e.g., `JennyMultilingualNeural`)
- **Benefit**: Consistent voice across languages
- **Rate**: `-10%` (accommodate non-native speakers)

#### For VIP Speakers
- **Use**: Personal Voice (with approval and consent)
- **Benefit**: Preserves speaker identity
- **Fallback**: High-quality neural voice if personal voice fails

### 2. SSML Best Practices

✅ **DO**:
- Use SSML for professional meetings requiring precise control
- Test SSML markup before live events
- Keep prosody adjustments subtle (±20% maximum)
- Add pauses at natural sentence breaks
- Use emphasis sparingly for key information

❌ **DON'T**:
- Over-customize to the point of sounding unnatural
- Use extreme pitch/rate values (sounds robotic)
- Apply multiple conflicting styles simultaneously
- Forget to escape XML special characters (`<`, `>`, `&`)

### 3. Performance Optimization

```python
# Cache voice configurations
from functools import lru_cache

@lru_cache(maxsize=10)
def get_voice_config(voice_name: str, style: str) -> str:
    """Cache SSML templates for reuse."""
    return create_ssml_template(voice_name, style)

# Preload common phrases
COMMON_PHRASES = {
    "welcome": "Welcome to the city council meeting.",
    "motion_approved": "The motion is approved.",
    "motion_denied": "The motion is denied.",
    "recess": "The council will now take a fifteen-minute recess."
}

# Pre-synthesize and cache audio for common phrases
def preload_common_phrases():
    for phrase_key, phrase_text in COMMON_PHRASES.items():
        audio_data = synthesize_cached(phrase_text)
        cache_audio(phrase_key, audio_data)
```

### 4. Accessibility Considerations

- **Hearing Impaired**: Always provide captions alongside audio
- **Visual Impaired**: Use clear, descriptive announcements
- **Cognitive**: Maintain consistent voice and slower pace
- **Non-Native Speakers**: Reduce speaking rate by 10-15%

### 5. Error Handling

```python
def synthesize_with_fallback(text: str, primary_voice: str, fallback_voice: str):
    """Attempt synthesis with fallback if primary fails."""
    try:
        return synthesize_speech(text, primary_voice)
    except Exception as e:
        logger.warning(f"Primary voice failed: {e}, trying fallback")
        try:
            return synthesize_speech(text, fallback_voice)
        except Exception as e2:
            logger.error(f"Both voices failed: {e2}")
            # Return plain text for captions only
            return None
```

### 6. Cost Management

**Voice Cost Comparison**:
| Voice Type | Cost per 1M chars | Typical Meeting (2hr) | Annual (50 meetings) |
|------------|------------------|----------------------|---------------------|
| Standard | $4 | ~$0.40 | ~$20 |
| Neural | $16 | ~$1.60 | ~$80 |
| Personal | $16 | ~$1.60 | ~$80 |

**Cost Optimization**:
- Use standard voices for routine meetings
- Reserve neural/personal voices for high-profile events
- Cache common phrases to avoid re-synthesis
- Monitor usage with Azure Cost Management

---

## Troubleshooting

### Common Issues

#### Issue: Voice sounds robotic
**Solution**: 
- Use neural voices instead of standard voices
- Reduce prosody adjustments
- Check SSML markup for errors

#### Issue: Personal voice not working
**Solution**:
- Verify approval status at https://aka.ms/customneural
- Confirm using approved region (eastus, westus2, etc.)
- Check that `VOICE_NAME=personal-voice` in `.env`
- Ensure speaker consent obtained

#### Issue: SSML causes synthesis errors
**Solution**:
- Validate SSML with online validator
- Escape XML special characters
- Check voice name spelling
- Verify style is supported by chosen voice

#### Issue: High latency with SSML
**Solution**:
- Simplify SSML markup
- Remove unnecessary tags
- Use plain text for time-critical scenarios
- Pre-cache common SSML templates

---

## Resources

### Official Documentation
- 🔗 [Azure Neural Voices Gallery](https://speech.microsoft.com/portal/voicegallery)
- 🔗 [SSML Reference](https://learn.microsoft.com/azure/ai-services/speech-service/speech-synthesis-markup)
- 🔗 [Personal Voice Documentation](https://learn.microsoft.com/azure/ai-services/speech-service/personal-voice-overview)
- 🔗 [Voice Styles Reference](https://learn.microsoft.com/azure/ai-services/speech-service/speech-synthesis-markup-voice)
- 🔗 [Multilingual Voices](https://learn.microsoft.com/azure/ai-services/speech-service/language-support?tabs=tts#multilingual-voices)

### Interactive Tools
- 🔗 [Speech Studio](https://speech.microsoft.com/) - Test voices in browser
- 🔗 [SSML Validator](https://www.liquid-technologies.com/online-ssml-validator)
- 🔗 [Voice Tuning Tool](https://speech.microsoft.com/portal/audiocontentcreation) - Audio Content Creation

### Code Samples
- 🔗 [Azure Speech SDK Samples](https://github.com/Azure-Samples/cognitive-services-speech-sdk)
- 🔗 [SSML Examples](https://github.com/Azure-Samples/Cognitive-Speech-TTS/tree/master/Samples-Http/SSML)

### Community
- 🔗 [Microsoft Q&A - Speech Service](https://learn.microsoft.com/answers/tags/413/azure-speech)
- 🔗 [Stack Overflow - Azure Speech](https://stackoverflow.com/questions/tagged/azure-speech)

---

## Summary

This demo supports comprehensive voice customization:

### Quick Start Configurations

**Budget-Friendly Setup** (Standard Neural):
```bash
VOICE_NAME=en-US-JennyNeural
TARGET_VOICE_ES=es-ES-ElviraNeural
DEFAULT_SPEAKING_RATE=-10%
```

**Premium Setup** (Personal Voice):
```bash
VOICE_NAME=personal-voice
AZURE_SPEECH_REGION=eastus
ENABLE_LIVE_INTERPRETER=true
```

**Professional Meeting Setup** (SSML Enhanced):
```python
translator = LiveInterpreterTranslator(
    settings=settings,
    voice_preferences={
        "en": "en-US-JennyNeural",
        "es": "es-ES-ElviraNeural"
    },
    enable_ssml=True
)
translator.settings.default_style = "newscast"
translator.settings.default_speaking_rate = "-10%"
```

Choose the configuration that best matches your requirements for voice quality, budget, and customization needs.

---

**Document Version**: 1.0  
**Last Updated**: November 17, 2025  
**Maintained By**: Live Interpreter API Demo Project  
**License**: For informational purposes. Azure pricing and features subject to change.
