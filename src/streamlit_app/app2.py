import streamlit as st
import azure.cognitiveservices.speech as speechsdk
import tempfile
import time
import os

# Azure Speech credentials
SPEECH_KEY = os.getenv("SPEECH_KEY", "YOUR_AZURE_SPEECH_KEY")
SPEECH_REGION = os.getenv("SPEECH_REGION", "YOUR_AZURE_REGION")

# Simulated transcript
transcript = [
    {"speaker": "Speaker 1", "lang": "en-US", "text": "Good afternoon, everyone. Thank you for joining. Today, we’ll discuss the new community park project and its budget allocation."},
    {"speaker": "Speaker 2", "lang": "es-ES", "text": "Gracias. Este proyecto es muy importante para nuestra comunidad. Queremos asegurarnos de que el diseño incluya áreas verdes y espacios para niños."},
    {"speaker": "Speaker 1", "lang": "en-US", "text": "I completely agree. We also need to consider accessibility for seniors and people with disabilities."},
    {"speaker": "Speaker 2", "lang": "es-ES", "text": "Perfecto. ¿Cuándo planeamos comenzar la construcción?"},
    {"speaker": "Speaker 1", "lang": "en-US", "text": "The goal is to start in early spring, once the budget is approved."}
]

# Streamlit UI
st.title("Simulated Council Meeting with Live Interpretation")
st.write("Captions and audio playback powered by Azure Speech SDK")

caption_placeholder = st.empty()
translation_placeholder = st.empty()
audio_placeholder = st.empty()

# Configure translation
translation_config = speechsdk.translation.SpeechTranslationConfig(
    subscription=SPEECH_KEY,
    region=SPEECH_REGION
)
translation_config.add_target_language("en")
translation_config.add_target_language("es")

# Create push audio stream
push_stream = speechsdk.audio.PushAudioInputStream()
audio_config = speechsdk.audio.AudioConfig(stream=push_stream)
recognizer = speechsdk.translation.TranslationRecognizer(
    translation_config=translation_config,
    audio_config=audio_config
)

# Event handler for recognized speech
def recognized(evt):
    if evt.result.reason == speechsdk.ResultReason.TranslatedSpeech:
        caption_placeholder.text(f"Original: {evt.result.text}")
        translations = evt.result.translations
        translation_placeholder.text(f"Translations: {translations}")

recognizer.recognized.connect(recognized)
recognizer.start_continuous_recognition_async().get()

# Function to synthesize and push audio
def synthesize_and_push(text, lang):
    speech_config = speechsdk.SpeechConfig(subscription=SPEECH_KEY, region=SPEECH_REGION)
    speech_config.speech_synthesis_language = lang
    synthesizer = speechsdk.SpeechSynthesizer(speech_config=speech_config, audio_config=None)
    result = synthesizer.speak_text_async(text).get()
    if result.reason == speechsdk.ResultReason.SynthesizingAudioCompleted:
        # Push audio to recognizer
        push_stream.write(result.audio_data)
        # Play audio in UI
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
        temp_file.write(result.audio_data)
        temp_file.close()
        audio_placeholder.audio(temp_file.name, format="audio/wav")
        os.unlink(temp_file.name)
        time.sleep(2)

# Simulate meeting
st.write("Starting simulation...")
for line in transcript:
    st.write(f"**{line['speaker']} says:** {line['text']}")
    synthesize_and_push(line["text"], line["lang"])

time.sleep(5)
recognizer.stop_continuous_recognition_async().get()
push_stream.close()
st.write("Simulation complete!")