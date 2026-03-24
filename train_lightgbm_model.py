import os
import librosa
import numpy as np
import pickle
import lightgbm as lgb
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, classification_report

# ---------------- PATHS ----------------
NORMAL_DIR = "NORMAL_CALLS"
SCAM_DIR = "SCAM_CALLS"
MODEL_OUT = "lgbm_vishing_model.pkl"
SR = 16000
# --------------------------------------

def extract_features(file_path):
    y, sr = librosa.load(file_path, sr=SR)

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    delta = librosa.feature.delta(mfcc)
    delta2 = librosa.feature.delta(mfcc, order=2)

    zcr = librosa.feature.zero_crossing_rate(y)
    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)

    features = np.hstack([
        np.mean(mfcc, axis=1),
        np.mean(delta, axis=1),
        np.mean(delta2, axis=1),
        np.mean(zcr),
        np.mean(spectral_centroid)
    ])

    return features


def load_dataset():
    X, y = [], []

    print("🔹 Loading NORMAL calls...")
    for f in os.listdir(NORMAL_DIR):
        if f.endswith(".wav"):
            X.append(extract_features(os.path.join(NORMAL_DIR, f)))
            y.append(0)

    print("🔹 Loading SCAM calls...")
    for f in os.listdir(SCAM_DIR):
        if f.endswith(".wav"):
            X.append(extract_features(os.path.join(SCAM_DIR, f)))
            y.append(1)

    return np.array(X), np.array(y)


# -------- LOAD DATA --------
X, y = load_dataset()
print(f"\n✅ Total samples loaded: {len(y)}")

# -------- SPLIT --------
X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

# -------- MODEL --------
model = lgb.LGBMClassifier(
    n_estimators=300,
    max_depth=7,
    learning_rate=0.05,
    class_weight="balanced",
    random_state=42
)

print("\n🔹 Training LightGBM model...")
model.fit(X_train, y_train)

# -------- EVALUATION --------
y_pred = model.predict(X_test)
acc = accuracy_score(y_test, y_pred)

print(f"\n🎯 Model Accuracy: {acc * 100:.2f}%")
print("\n📊 Classification Report:")
print(classification_report(y_test, y_pred))

# -------- SAVE MODEL --------
with open(MODEL_OUT, "wb") as f:
    pickle.dump(model, f)

print(f"\n✅ Model saved as {MODEL_OUT}")
