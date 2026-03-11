import speech_recognition as sr

recognizer = sr.Recognizer()

APIS = {
    "1": "Google",
    "2": "Sphinx"
}

LANGUAGES = {
    "1": ("English", "en-US"),
    "2": ("French", "fr-FR"),
    "3": ("Spanish", "es-ES"),
    "4": ("Arabic", "ar-SA")
}

def choose_api():
    print("\n=== Choose Speech Recognition API ===")
    for key, value in APIS.items():
        print(f"{key} - {value}")
    choice = input("Enter API number: ")
    if choice not in APIS:
        print("⚠ Invalid choice. Using Google by default.")
        return "1"
    return choice

def choose_language():
    print("\n=== Choose Language ===")
    for key, (lang, code) in LANGUAGES.items():
        print(f"{key} - {lang} ({code})")
    choice = input("Enter language number: ")
    if choice not in LANGUAGES:
        print("⚠ Invalid choice. Using English by default.")
        return "en-US"
    return LANGUAGES[choice][1]

def save_transcription(text):
    filename = input("Enter filename (without extension): ")
    with open(filename + ".txt", "a") as f:
        f.write(text + "\n")
    print(f"✅ Transcription saved to {filename}.txt")

def transcribe_speech(api_choice, language):
    with sr.Microphone() as source:
        print("\n🎤 Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        if api_choice == "1":
            text = recognizer.recognize_google(audio, language=language)
        elif api_choice == "2":
            text = recognizer.recognize_sphinx(audio)

        print("📝 Transcription:", text)

        save_option = input("\nSave transcription to file? (y/n): ")
        if save_option.lower() == "y":
            save_transcription(text)

    except sr.UnknownValueError:
        print("❌ Speech not understood. Please speak clearly and try again.")
    except sr.RequestError as e:
        print(f"⚠ API connection failed. Check your internet connection.\nDetails: {e}")
    except sr.WaitTimeoutError:
        print("⏱ No speech detected. Please try again.")
    except OSError:
        print("🎙 Microphone not found. Please check your audio device.")
    except Exception as e:
        print(f"🔴 Unexpected error: {e}")

def main():
    print("=== Speech Recognition App ===")
    api_choice = choose_api()
    print(f"\n✅ Using: {APIS[api_choice]}")
    language = choose_language()
    print(f"🌍 Language set to: {language}")
    transcribe_speech(api_choice, language)

if __name__ == "__main__":
    main()