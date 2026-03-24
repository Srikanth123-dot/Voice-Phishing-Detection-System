from pydub import AudioSegment

audio = AudioSegment.from_file("ttsMP3.com_VoiceText_2026-1-23_10-31-30.mp3")
audio = audio.set_channels(1).set_frame_rate(16000)

audio.export("sample_call.wav", format="wav")

print("✅ Converted to proper PCM WAV")
