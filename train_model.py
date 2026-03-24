# train_model.py
import os
import numpy as np
import librosa
import pickle
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import StratifiedKFold
from sklearn.metrics import accuracy_score
from features import extract_features

NORMAL_DIR = "NORMAL_CALLS"
SCAM_DIR = "SCAM_CALLS"

def augment_audio(y, sr):
    return [
        librosa.effects.pitch_shift(y, sr=sr, n_steps=2),
        librosa.effects.time_stretch(y, rate=0.9),
        y + 0.005 * np.random.randn(len(y))
    ]

X, y_labels = [], []

print("🔹 Loading NORMAL calls...")
for file in os.listdir(NORMAL_DIR):
    if file.endswith(".wav"):
        path = os.path.join(NORMAL_DIR, file)
        y_audio, sr = librosa.load(path, sr=16000)

        X.append(extract_features(path))
        y_labels.append(0)

        for aug in augment_audio(y_audio, sr):
            mfcc = librosa.feature.mfcc(y=aug, sr=sr, n_mfcc=20)
            features = np.hstack([
                np.mean(mfcc, axis=1),
                np.std(mfcc, axis=1),
                np.var(mfcc, axis=1),
                np.max(mfcc, axis=1),
                np.min(mfcc, axis=1)
            ])
            X.append(features)
            y_labels.append(0)

print("🔹 Loading SCAM calls...")
for file in os.listdir(SCAM_DIR):
    if file.endswith(".wav"):
        path = os.path.join(SCAM_DIR, file)
        y_audio, sr = librosa.load(path, sr=16000)

        X.append(extract_features(path))
        y_labels.append(1)

        for aug in augment_audio(y_audio, sr):
            mfcc = librosa.feature.mfcc(y=aug, sr=sr, n_mfcc=20)
            features = np.hstack([
                np.mean(mfcc, axis=1),
                np.std(mfcc, axis=1),
                np.var(mfcc, axis=1),
                np.max(mfcc, axis=1),
                np.min(mfcc, axis=1)
            ])
            X.append(features)
            y_labels.append(1)

X = np.array(X)
y_labels = np.array(y_labels)

print(f"\n✅ Total samples: {len(X)}")

model = RandomForestClassifier(
    n_estimators=600,
    max_depth=25,
    min_samples_split=3,
    class_weight={0: 1, 1: 2},
    random_state=42,
    n_jobs=-1
)

skf = StratifiedKFold(n_splits=5, shuffle=True, random_state=42)
scores = []

print("\n🔁 5-Fold Cross Validation...")
for train_idx, test_idx in skf.split(X, y_labels):
    model.fit(X[train_idx], y_labels[train_idx])
    preds = model.predict(X[test_idx])
    scores.append(accuracy_score(y_labels[test_idx], preds))

print(f"\n🎯 Average CV Accuracy: {np.mean(scores) * 100:.2f}%")

model.fit(X, y_labels)

with open("vishing_model.pkl", "wb") as f:
    pickle.dump(model, f)

print("\n✅ Model saved as vishing_model.pkl")
print("🎉 Training completed successfully!")
