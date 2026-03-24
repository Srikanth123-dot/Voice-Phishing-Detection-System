# features.py
import librosa
import numpy as np

EXPECTED_FEATURES = 100

def extract_features(audio_path):
    y, sr = librosa.load(audio_path, sr=16000)

    # MFCCs
    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)

    features = np.hstack([
        np.mean(mfcc, axis=1),
        np.std(mfcc, axis=1),
        np.var(mfcc, axis=1),
        np.max(mfcc, axis=1),
        np.min(mfcc, axis=1)
    ])

    return features  # EXACTLY 100 FEATURES
