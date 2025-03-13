import streamlit as st
import sounddevice as sd
import numpy as np
import speech_recognition as sr
from deep_translator import GoogleTranslator
from pydub import AudioSegment
import os
import tempfile
import wave

os.environ["PATH"] += os.pathsep + "/path/to/ffmpeg/bin"

st.title("Live Speech Recognition & Translation App")

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

source_language = st.selectbox("Select Source Language", list(languages.keys()), format_func=lambda x: languages[x])
target_language = st.selectbox("Select Target Language", list(languages.keys()), format_func=lambda x: languages[x])

st.write(f"Selected Source Language: **{languages[source_language]}**")
st.write(f"Selected Target Language: **{languages[target_language]}**")

def record_audio(duration=5, samplerate=44100):
    st.write("Recording... Speak now!")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()
    return audio_data, samplerate

def save_audio(audio_data, samplerate):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        with wave.open(tmpfile.name, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)
            wf.setframerate(samplerate)
            wf.writeframes(audio_data.tobytes())
        return tmpfile.name

if st.button("Start Recording"):
    audio_data, samplerate = record_audio()
    audio_file = save_audio(audio_data, samplerate)

    try:
        audio_segment = AudioSegment.from_wav(audio_file)
        audio_segment.export(audio_file, format="wav")

        with sr.AudioFile(audio_file) as source:
            audio = recognizer.record(source)

        text = recognizer.recognize_google(audio, language=source_language)
        st.session_state.recognized_text = text
        st.success("You said: " + text)

        translated = GoogleTranslator(source=source_language, target=target_language).translate(text)
        st.session_state.translated_text = translated
        st.success(f"Translated to {languages[target_language]}: " + translated)
    
    except sr.UnknownValueError:
        st.error("Sorry, I could not understand that message.")
    except sr.RequestError:
        st.error("Could not request results; check your network connection.")
    except Exception as e:
        st.error(f"Error: {e}")

if st.button("Clear"):
    st.session_state.recognized_text = ""
    st.session_state.translated_text = ""
    st.success("Text cleared!")
