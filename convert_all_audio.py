import os
from pydub import AudioSegment

# 🔥 FORCE FFmpeg path (bypass Windows PATH)
AudioSegment.converter = r"C:\Voice_Phishing_Detection\ffmpeg-8.0.1-essentials_build\bin\ffmpeg.exe"

folders = ["NORMAL_CALLS", "SCAM_CALLS"]

for folder in folders:
    if not os.path.exists(folder):
        print(f"Folder not found: {folder}")
        continue

    for file in os.listdir(folder):
        input_path = os.path.join(folder, file)

        if file.lower().endswith(".wav"):
            continue

        try:
            audio = AudioSegment.from_file(input_path)
            audio = audio.set_channels(1).set_frame_rate(16000)

            output_name = os.path.splitext(file)[0] + ".wav"
            output_path = os.path.join(folder, output_name)

            audio.export(output_path, format="wav")
            print(f"Converted: {file} → {output_name}")

        except Exception as e:
            print(f"Failed: {file} → {e}")
