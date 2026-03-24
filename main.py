from speech_to_text import convert_audio_to_text
from vishing_detector import detect_vishing

audio_path = "scam_2.wav"

text = convert_audio_to_text(audio_path)
print("Call Text:", text)

result = detect_vishing(text)
print("Result:", result)
