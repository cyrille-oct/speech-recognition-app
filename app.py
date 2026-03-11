import speech_recognition as sr

recognizer = sr.Recognizer()

APIS = {
    "1": "Google",
    "2": "Sphinx"
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

def transcribe_speech(api_choice):
    with sr.Microphone() as source:
        print("\n🎤 Speak now...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        if api_choice == "1":
            text = recognizer.recognize_google(audio)
        elif api_choice == "2":
            text = recognizer.recognize_sphinx(audio)

        print("📝 Transcription:", text)

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
    transcribe_speech(api_choice)

if __name__ == "__main__":
    main()