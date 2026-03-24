from faster_whisper import WhisperModel

# Load model once (CPU friendly)
model = WhisperModel(
    "small",
    device="cpu",
    compute_type="int8"
)

def whisper_audio_to_text(audio_file, language="en"):
    segments, info = model.transcribe(
        audio_file,
        language=language,
        beam_size=5
    )

    full_text = ""
    for segment in segments:
        full_text += segment.text + " "

    return full_text.strip()
