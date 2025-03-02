import streamlit as st
import sounddevice as sd
import numpy as np
import speech_recognition as sr
from deep_translator import GoogleTranslator
from pydub import AudioSegment
import os
import tempfile
import wave

os.environ["PATH"] += os.pathsep + "/path/to/ffmpeg/bin"  # Update with your actual FFmpeg path

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

language_code = st.selectbox("Select Language Code", list(languages.keys()))
st.write(f"Selected Language: **{languages[language_code]}**")

# Function to record audio
def record_audio(duration=5, samplerate=44100):
    st.write("Recording... Speak now!")
    audio_data = sd.rec(int(duration * samplerate), samplerate=samplerate, channels=1, dtype=np.int16)
    sd.wait()  # Wait until recording is finished
    return audio_data, samplerate

def save_audio(audio_data, samplerate):
    with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmpfile:
        with wave.open(tmpfile.name, 'w') as wf:
            wf.setnchannels(1)
            wf.setsampwidth(2)  # 16-bit audio
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
    except Exception as e:
        st.error(f"Error: {e}")

if st.button("Clear"):
    st.session_state.recognized_text = ""
    st.session_state.translated_text = ""
    st.success("Text cleared!")
