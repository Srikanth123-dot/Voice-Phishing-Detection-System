def extract_features(audio_file):

    y, sr = librosa.load(audio_file, sr=16000)

    mfcc = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=20)
    delta = librosa.feature.delta(mfcc)

    spectral_centroid = librosa.feature.spectral_centroid(y=y, sr=sr)
    zcr = librosa.feature.zero_crossing_rate(y)
    chroma = librosa.feature.chroma_stft(y=y, sr=sr)

    features = np.hstack([

        np.mean(mfcc, axis=1),
        np.std(mfcc, axis=1),

        np.mean(delta, axis=1),
        np.std(delta, axis=1),

        np.mean(spectral_centroid),
        np.std(spectral_centroid),

        np.mean(zcr),
        np.std(zcr),

        np.mean(chroma, axis=1)

    ])

    return features