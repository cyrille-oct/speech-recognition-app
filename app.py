import speech_recognition as sr
import threading
import time

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

# Global flags
paused = False
running = True

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
    global paused, running

    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)

        while running:
            if paused:
                time.sleep(0.5)
                continue

            try:
                print("\n🎤 Speak now...")
                audio = recognizer.listen(source, timeout=5)

                if api_choice == "1":
                    text = recognizer.recognize_google(audio, language=language)
                elif api_choice == "2":
                    text = recognizer.recognize_sphinx(audio)

                print("📝 Transcription:", text)

                save_option = input("Save transcription to file? (y/n): ")
                if save_option.lower() == "y":
                    save_transcription(text)

            except sr.UnknownValueError:
                print("❌ Speech not understood. Please speak clearly and try again.")
            except sr.RequestError as e:
                print(f"⚠ API connection failed.\nDetails: {e}")
            except sr.WaitTimeoutError:
                print("⏱ No speech detected. Waiting...")
            except OSError:
                print("🎙 Microphone not found. Please check your audio device.")
            except Exception as e:
                print(f"🔴 Unexpected error: {e}")

def control_commands():
    global paused, running

    print("\nCommands: pause / resume / stop\n")

    while running:
        command = input("").strip().lower()

        if command == "pause":
            paused = True
            print("⏸ Recognition paused.")

        elif command == "resume":
            paused = False
            print("▶ Recognition resumed.")

        elif command == "stop":
            running = False
            print("🛑 Stopping program.")
            break

def main():
    print("=== Speech Recognition App ===")
    api_choice = choose_api()
    print(f"\n✅ Using: {APIS[api_choice]}")
    language = choose_language()
    print(f"🌍 Language set to: {language}")

    # Start two threads
    recognition_thread = threading.Thread(target=transcribe_speech, args=(api_choice, language))
    control_thread = threading.Thread(target=control_commands)

    recognition_thread.start()
    control_thread.start()

    recognition_thread.join()
    control_thread.join()

if __name__ == "__main__":
    main()