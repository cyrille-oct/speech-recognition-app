import streamlit as st
import speech_recognition as sr

recognizer = sr.Recognizer()

LANGUAGES = {
    "English": "en-US",
    "French": "fr-FR",
    "Spanish": "es-ES",
    "Arabic": "ar-SA"
}

st.title("🎤 Speech Recognition App")
st.write("Click the button to start recording from your microphone.")

api_choice = st.selectbox("Choose API", ["Google", "Sphinx"])
language_name = st.selectbox("Choose Language", list(LANGUAGES.keys()))
language_code = LANGUAGES[language_name]

if st.button("🎙 Start Recording"):
    with st.spinner("Listening..."):
        try:
            with sr.Microphone() as source:
                recognizer.adjust_for_ambient_noise(source)
                audio = recognizer.listen(source, timeout=5)

            if api_choice == "Google":
                text = recognizer.recognize_google(audio, language=language_code)
            else:
                text = recognizer.recognize_sphinx(audio)

            st.success(f"📝 Transcription: {text}")

            if st.download_button("💾 Save Transcription", text, file_name="transcription.txt"):
                st.info("✅ File downloaded!")

        except sr.UnknownValueError:
            st.error("❌ Speech not understood. Please try again.")
        except sr.RequestError as e:
            st.error(f"⚠ API connection failed: {e}")
        except sr.WaitTimeoutError:
            st.warning("⏱ No speech detected. Please try again.")
        except Exception as e:
            st.error(f"🔴 Unexpected error: {e}")