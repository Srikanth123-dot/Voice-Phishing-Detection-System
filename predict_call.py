import os
import shutil
from datetime import datetime
import pickle
import re
import librosa
import numpy as np
import speech_recognition as sr
from send_alert_email import send_scam_alert


# =========================
# LOAD TRAINED MODEL
# =========================
with open("vishing_model.pkl", "rb") as f:
    model = pickle.load(f)

EXPECTED_FEATURES = 100


# =========================
# SCAM KEYWORDS
# =========================
SCAM_KEYWORDS = [
    "technical support", "tech support",
    "unusual activity", "security alert",
    "malware", "virus", "hacked",
    "account blocked", "kyc", "verification",
    "otp", "one time password",
    "upi", "electricity bill", "power bill",
    "service will be disconnected",
    "bank account", "credit card",
    "amazon", "lenovo", "microsoft"
]


# =========================
# REGEX FOR SENSITIVE INFO
# =========================
REGEX_PATTERNS = {
    "Phone Number": r"\b\d{10}\b",
    "Amount": r"(₹|\bINR\b|\bRs\b)?\s?\d{3,7}",
    "UPI ID": r"\b[\w.\-]+@[\w]+\b"
}


# =========================
# FEATURE EXTRACTION
# =========================
def extract_features(audio_file):
    y, sr = librosa.load(audio_file, sr=16000)

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)

    features = np.hstack([
        np.mean(mfcc, axis=1),
        np.std(mfcc, axis=1),
        np.var(mfcc, axis=1),
        np.max(mfcc, axis=1),
        np.min(mfcc, axis=1)
    ])

    return features  # 20 × 5 = 100 features

# =========================
# SPEECH TO TEXT
# =========================
def audio_to_text(audio_file, language="en-IN"):
    recognizer = sr.Recognizer()

    with sr.AudioFile(audio_file) as source:
        audio = recognizer.record(source)

    try:
        return recognizer.recognize_google(audio, language=language)
    except:
        return ""


# =========================
# LANGUAGE SELECTION
# =========================
print("\nSelect Audio Language:")
print("1️⃣ Telugu")
print("2️⃣ English")
choice = input("Enter choice (1 or 2): ").strip()

language = "te-IN" if choice == "1" else "en-IN"


# =========================
# ENTER CALLER PHONE NUMBER
# =========================
phone_number = input("\nEnter 10-digit caller phone number: ").strip()
# Mask phone number for reporting
def mask_number(number):
    if len(number) == 10 and number.isdigit():
        return number[:5] + "XXXXX"
    return "UNKNOWN"

masked_number = mask_number(phone_number)


# =========================
# AUDIO FILE PATH
# =========================
audio_file = "TEST_CALLS/Test1.wav"   # Change file if needed


print("\n📢 Converting FULL audio to text...")
text = audio_to_text(audio_file, language=language)

print("\n📄 FULL AUDIO TRANSCRIPTION:")
print(text if text else "[No speech detected]")

text_lower = text.lower()


# =========================
# KEYWORD DETECTION
# =========================
found_keywords = [kw for kw in SCAM_KEYWORDS if kw in text_lower]


# =========================
# SENSITIVE INFO DETECTION
# =========================
found_sensitive = {}

for label, pattern in REGEX_PATTERNS.items():
    matches = re.findall(pattern, text_lower)
    if matches:
        found_sensitive[label] = matches


# =========================
# ML PREDICTION
# =========================
features = extract_features(audio_file)
scam_probability = model.predict_proba([features])[0][1]


# =========================
# FINAL DECISION LOGIC
# =========================
if found_keywords or found_sensitive:
    decision = "⚠️ SCAM CALL (Content-Based Fraud)"
    is_scam = True
elif scam_probability > 0.6:
    decision = "⚠️ SCAM CALL (Voice Pattern)"
    is_scam = True
else:
    decision = "✅ NORMAL CALL"
    is_scam = False


# =========================
# OUTPUT SECTION
# =========================
print("\n🧠 Scam-related keywords found:")
print(found_keywords if found_keywords else "None")

print("\n🆔 Sensitive information detected:")
print(found_sensitive if found_sensitive else "None")

print("\n🤖 ML Scam Probability:")
print(f"{scam_probability * 100:.2f}%")

print("\n🔍 FINAL DECISION:")
print(decision)

# =========================
# SAVE EVIDENCE + SEND EMAIL
# =========================
if is_scam and phone_number.isdigit() and len(phone_number) == 10:

    print("\n📁 Creating scam evidence record...")

    # Mask number
    masked_number = phone_number[:3] + "xxxxx"

    # Create folder for phone number
    folder_path = os.path.join("SCAM_RECORDS", phone_number)
    os.makedirs(folder_path, exist_ok=True)

    # Save audio copy
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    saved_audio_path = os.path.join(folder_path, f"{timestamp}.wav")

    shutil.copy(audio_file, saved_audio_path)

    # Append to log file
    log_file = os.path.join("SCAM_RECORDS", "scam_log.txt")

    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} | {masked_number} | {decision}\n")

    print("✅ Evidence saved successfully!")

    print("\n📧 Sending scam alert email...")

    send_scam_alert(
        masked_number,
        saved_audio_path,
        scam_probability * 100,
        found_keywords,
        found_sensitive,
        decision
    )