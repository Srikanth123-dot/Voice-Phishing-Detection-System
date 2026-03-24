import speech_recognition as sr
from pydub import AudioSegment
import os
import uuid

def audio_to_text(audio_file, language="en-IN"):
    recognizer = sr.Recognizer()

    temp_wav = f"temp_{uuid.uuid4().hex}.wav"
    AudioSegment.from_file(audio_file).set_channels(1).set_frame_rate(16000).export(temp_wav, format="wav")

    with sr.AudioFile(temp_wav) as source:
        audio = recognizer.record(source)

    try:
        text = recognizer.recognize_google(audio, language=language)
    except sr.UnknownValueError:
        text = ""
    except sr.RequestError as e:
        text = f"[API Error: {e}]"

    os.remove(temp_wav)
    return text
