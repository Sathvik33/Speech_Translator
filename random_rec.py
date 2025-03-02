import streamlit as st
import sounddevice as sd
import numpy as np
import wave
import os
import tempfile
import speech_recognition as sr
from deep_translator import GoogleTranslator

st.title("Speech Recognition and Translation App")
st.write("Only for INDIANS")
recognizer = sr.Recognizer()

if "recognized_text" not in st.session_state:
    st.session_state.recognized_text = ""
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

languages = {
    "en": "English",
    "hi": "Hindi",
    "bn": "Bengali",
    "te": "Telugu",
    "mr": "Marathi",
    "ta": "Tamil",
    "ur": "Urdu",
    "gu": "Gujarati",
    "kn": "Kannada",
    "or": "Odia (Oriya)",
    "pa": "Punjabi",
    "as": "Assamese",
    "ml": "Malayalam",
    "sa": "Sanskrit",
    "sd": "Sindhi",
    "ks": "Kashmiri",
    "ne": "Nepali",
    "kok": "Konkani",
    "mni": "Manipuri (Meitei)",
    "doi": "Dogri",
    "brx": "Bodo",
    "sat": "Santali"
}

language_code = st.selectbox("Select Language Code", list(languages.keys()))
st.write(f"Selected Language: **{languages[language_code]}**")

def record_audio(duration=5, samplerate=44100):
    st.write("Recording...")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()
    
    temp_wav = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
    with wave.open(temp_wav.name, "wb") as wf:
        wf.setnchannels(1)
        wf.setsampwidth(2)
        wf.setframerate(samplerate)
        wf.writeframes(audio_data.tobytes())

    return temp_wav.name

if st.button("Start Recording"):
    audio_path = record_audio()

    with sr.AudioFile(audio_path) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language=language_code)
        st.session_state.recognized_text = text
        st.success("You said: " + text)

        translated = GoogleTranslator(source="auto", target="en").translate(text)
        st.session_state.translated_text = translated
        st.success("Translated to English: " + translated)
    except sr.UnknownValueError:
        st.error("Sorry, I could not understand that message.")
    except sr.RequestError:
        st.error("Could not request results; check your network connection.")

    os.remove(audio_path)

if st.button("Clear"):
    st.session_state.recognized_text = ""
    st.success("Text cleared!")
