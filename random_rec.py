import streamlit as st
import speech_recognition as sr
from deep_translator import GoogleTranslator

st.title("Speech Recognition and Translation App")

recognizer = sr.Recognizer()

if "recognized_text" not in st.session_state:
    st.session_state.recognized_text = ""
if "translated_text" not in st.session_state:
    st.session_state.translated_text = ""

# List of Indian languages with codes and full names
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

if st.button("Start Recording"):
    with sr.Microphone() as source:
        st.write("Say something...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

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

if st.button("Clear"):
    st.session_state.recognized_text = ""
    st.success("Text cleared!")