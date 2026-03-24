import os
import pickle
import librosa
import numpy as np
from sklearn.metrics import accuracy_score, classification_report

# =========================
# LOAD TRAINED MODEL
# =========================
with open("vishing_model.pkl", "rb") as f:
    model = pickle.load(f)

EXPECTED_FEATURES = 98

# =========================
# FEATURE EXTRACTION (SAME AS TRAINING)
# =========================
def extract_features(audio_path):
    y, sr = librosa.load(audio_path, sr=16000)

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)

    features = np.hstack([
        np.mean(mfcc, axis=1),
        np.std(mfcc, axis=1),
        np.var(mfcc, axis=1),
        np.max(mfcc, axis=1),
        np.min(mfcc, axis=1)
    ])

    # Ensure fixed feature length
    if len(features) < EXPECTED_FEATURES:
        features = np.pad(features, (0, EXPECTED_FEATURES - len(features)))
    else:
        features = features[:EXPECTED_FEATURES]

    return features

# =========================
# TEST DATA PATHS
# =========================
NORMAL_TEST_DIR = "TEST_CALLS/NORMAL"
SCAM_TEST_DIR = "TEST_CALLS/SCAM"

X_test = []
y_test = []

# =========================
# LOAD NORMAL TEST CALLS
# =========================
print("🔹 Loading NORMAL test calls...")
for file in os.listdir(NORMAL_TEST_DIR):
    if file.endswith(".wav"):
        path = os.path.join(NORMAL_TEST_DIR, file)
        X_test.append(extract_features(path))
        y_test.append(0)

# =========================
# LOAD SCAM TEST CALLS
# =========================
print("🔹 Loading SCAM test calls...")
for file in os.listdir(SCAM_TEST_DIR):
    if file.endswith(".wav"):
        path = os.path.join(SCAM_TEST_DIR, file)
        X_test.append(extract_features(path))
        y_test.append(1)

X_test = np.array(X_test)
y_test = np.array(y_test)

# =========================
# EVALUATION
# =========================
preds = model.predict(X_test)

accuracy = accuracy_score(y_test, preds)

print("\n🎯 Test Accuracy:", f"{accuracy * 100:.2f}%")
print("\n📊 Classification Report:\n")
print(classification_report(y_test, preds, target_names=["Normal", "Scam"]))
