import speech_recognition as sr
import os
import pydub
from pydub import AudioSegment
from dotenv import load_dotenv
load_dotenv()

WIT_AI_KEY = os.getenv("WIT_AI_KEY")  # Replace with your actual Wit.ai API key

def transcribe_audio():
    transcription = ""
    audio_dir = r"R:\KuKu FM project\audio"
    r = sr.Recognizer()

    for filename in os.listdir(audio_dir):
        if filename.endswith(".mp3"):
            fpath = os.path.join(audio_dir, filename)
            try:
                # Convert MP3 to WAV
                try:
                    audio = AudioSegment.from_mp3(fpath)
                    wav_path = fpath.replace(".mp3", ".wav")
                    audio.export(wav_path, format="wav", codec="pcm_s16le")

                    with sr.AudioFile(wav_path) as source:
                        audio_data = r.record(source)

                    transcription += r.recognize_wit(audio_data, key=WIT_AI_KEY) + "\\n"
                    os.remove(wav_path)  # Remove the temporary WAV file
                except FileNotFoundError as e:
                    print(f"FileNotFoundError: {e}")
                    transcription += f"FileNotFoundError: Could not find ffmpeg. Please install ffmpeg and add it to your PATH." + "\\n"
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