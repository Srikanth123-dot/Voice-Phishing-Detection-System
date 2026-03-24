from faster_whisper import WhisperModel

print("Loading model...")
model = WhisperModel("small", device="cpu", compute_type="int8")
print("Model loaded")

segments, info = model.transcribe("test.wav", language="en")

for seg in segments:
    print(seg.text)
