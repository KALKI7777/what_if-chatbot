import speech_recognition as sr
import os
from dotenv import load_dotenv
load_dotenv()

WIT_AI_KEY = os.getenv("WIT_AI_KEY")  # Replace with your actual Wit.ai API key

def transcribe_audio():
    transcription = ""
    audio_dir = "audio"
    r = sr.Recognizer()

    for filename in os.listdir(audio_dir):
        if filename.endswith(".mp3"):
            fpath = os.path.join(audio_dir, filename)
            try:
                with sr.AudioFile(fpath) as source:
                    audio = r.record(source)
                transcription += r.recognize_wit(audio, key=WIT_AI_KEY) + "\\n"
            except sr.UnknownValueError:
                print(f"Wit.ai could not understand audio from {filename}")
                transcription += f"Wit.ai could not understand audio from {filename}" + "\\n"
            except sr.RequestError as e:
                print(f"Could not request results from Wit.ai service; {e}")
                transcription += f"Could not request results from Wit.ai service; {e}" + "\\n"
    return transcription

def simulate_stt():
    """
    Simulates getting text input from the user, or uses the transcribed audio.
    """
    use_audio = input("Use audio transcription? (y/n): ").lower()
    if use_audio == 'y':
        print("\\n[STT Service] Transcribing audio...")
        transcription = transcribe_audio()
        print(f"[STT Service] Transcribed audio: '{transcription}'")
        return transcription
    else:
        print("\\n[STT Service] Listening... (Please type your 'what if' question)")
        user_input = input("You: ")
        print(f"[STT Service] Recognized text: '{user_input}'")
        return user_input