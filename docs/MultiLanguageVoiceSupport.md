# Multi-Language & Multi-Voice Support Update

## Overview
The app now supports **up to 3 target languages simultaneously** with **customizable voice selection** for each language, including multiple prebuilt neural voices for English and Spanish.

## New Features

### 1. Multiple Target Languages (Up to 3)
- **Primary Target**: Always available
- **Secondary Target**: Optional - enable with checkbox
- **Tertiary Target**: Optional - enable with checkbox

Users can now translate speech into 1, 2, or 3 different languages at the same time.

### 2. Language-Specific Voice Selection
Each target language has its own voice selector with multiple neural voice options:

**English (en-US)** - 9 voices:
- JennyNeural (default)
- GuyNeural
- AriaNeural
- DavisNeural
- AmberNeural
- AnaNeural
- AndrewNeural
- EmmaNeural
- BrianNeural

**Spanish (Spain) (es-ES)** - 10 voices:
- ElviraNeural (default)
- AlvaroNeural
- AbrilNeural
- ArnauNeural
- DarioNeural
- EliasNeural
- EstrellaNeural
- IreneNeural
- LaiaNeural
- LiaNeural

**Spanish (Mexico) (es-MX)** - 10 voices:
- DaliaNeural (default)
- JorgeNeural
- BeatrizNeural
- CandelaNeural
- CarlotaNeural
- CecilioNeural
- GerardoNeural
- LibertoNeural
- LucianoNeural
- MarinaNeural

Plus multiple voices for French, German, Italian, Portuguese, Chinese, Japanese, Korean, and more!

### 3. Automatic Voice Selection
The translator automatically selects the appropriate voice for each target language based on:
1. User's voice preference (if set in UI)
2. Default voice for that language
3. Fallback to en-US-JennyNeural if language not found

## Technical Implementation

### Configuration (`src/core/config.py`)

**NEURAL_VOICES Dictionary**:
```python
NEURAL_VOICES = {
    "en-US": ["en-US-JennyNeural", "en-US-GuyNeural", ...],
    "es-ES": ["es-ES-ElviraNeural", "es-ES-AlvaroNeural", ...],
    # ... more languages
}
```

**Settings Class Updates**:
- Added `voice_en_us`, `voice_es_es`, `voice_es_mx`, etc. fields
- Added `get_voice_for_language(language_code)` method
- Supports 3 target languages via `target_language_3` field

**Helper Function**:
```python
def get_voice_for_language(language_code, preferred_voice=None):
    """Get appropriate voice for a language"""
```

### Translator (`src/core/translator.py`)

**synthesize_translation() Method**:
- Now calls `settings.get_voice_for_language(target_language)`
- Automatically uses the correct voice for each language
- Logs which voice is being used for transparency

### Streamlit App (`src/streamlit_app/app.py`)

**Session State**:
- Added `voice_preferences` dictionary to track user selections

**Sidebar UI**:
- Voice dropdown for each target language
- Displays simplified voice names (removes "Neural" suffix)
- Remembers voice selections per language
- Shows up to 3 target language sections

**Voice Application**:
- Voice preferences applied to settings before creating translator
- Works for both continuous and single-shot modes
- Preferences persist during session

## Usage Guide

### For Users

1. **Select Target Languages**:
   - Choose primary target language
   - Check "Add second target language" for secondary
   - Check "Add third target language" for tertiary

2. **Choose Voices**:
   - Each language has a voice dropdown below it
   - Select your preferred voice (male/female, different accents)
   - Voice names show simplified format (e.g., "Jenny", "Guy", "Elvira")

3. **Start Translation**:
   - Voice preferences are automatically applied
   - Each language uses its selected voice for audio synthesis
   - Translations appear with corresponding audio playback buttons

### Example Use Cases

**Council Meeting (English-Spanish)**:
- Primary: es-ES with ElviraNeural (female, Spain accent)
- Secondary: en-US with GuyNeural (male, US accent)

**International Conference (3 languages)**:
- Primary: es-MX with DaliaNeural
- Secondary: fr-FR with DeniseNeural
- Tertiary: en-US with AriaNeural

**Training Session (Multiple Spanish Accents)**:
- Primary: es-ES with AlvaroNeural (Spain, male)
- Secondary: es-MX with JorgeNeural (Mexico, male)
- Tertiary: en-US with JennyNeural

## Voice Quality
All voices are **Azure Neural TTS** voices with:
- Natural-sounding prosody
- Expressive intonation
- High-quality audio output
- Support for SSML (if needed later)

## Files Modified

1. **src/core/config.py**
   - Added expanded NEURAL_VOICES with 9+ English voices, 10+ Spanish voices
   - Added DEFAULT_VOICES dictionary
   - Added get_voice_for_language() helper function
   - Added voice preference fields to Settings class
   - Added get_voice_for_language() method to Settings

2. **src/core/translator.py**
   - Updated synthesize_translation() to use language-specific voices
   - Added logging for voice selection transparency

3. **src/streamlit_app/app.py**
   - Imported NEURAL_VOICES constant
   - Added voice_preferences session state
   - Enhanced sidebar with voice selectors for each language
   - Added third target language support
   - Applied voice preferences to settings before translation

## Testing Checklist

✅ Syntax validation passed for all files
- [ ] Test single language with custom voice
- [ ] Test 2 languages with different voices
- [ ] Test 3 languages with different voices
- [ ] Test English voices (en-US)
- [ ] Test Spanish Spain voices (es-ES)
- [ ] Test Spanish Mexico voices (es-MX)
- [ ] Test continuous mode with multiple languages
- [ ] Test single-shot mode with multiple languages
- [ ] Verify audio playback uses correct voice per language
- [ ] Verify voice preferences persist during session

## Future Enhancements

Potential improvements:
- Save voice preferences to user profile
- Preview voice samples before selection
- SSML support for advanced voice control
- Emotion/style selection for expressive voices
- Voice speed/pitch controls
- Support for more regional variants (en-AU, en-IN, etc.)

## Benefits

✅ **Flexibility**: Choose voices that match your audience
✅ **Accessibility**: Multiple language support for diverse groups
✅ **Natural Audio**: Neural voices sound more human
✅ **User Control**: Select preferred gender, accent, tone
✅ **Scalability**: Easy to add more languages/voices
✅ **Professional**: High-quality audio for meetings and events
