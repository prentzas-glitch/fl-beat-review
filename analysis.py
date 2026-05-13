import os
import numpy as np
import librosa

SUPPORTED_FORMATS = (".wav", ".mp3", ".flac", ".aiff", ".ogg")

PITCH_CLASSES = ["C", "C#", "D", "D#", "E", "F", "F#", "G", "G#", "A", "A#", "B"]

# Krumhansl-Schmuckler key profiles
_MAJOR_PROFILE = np.array([6.35, 2.23, 3.48, 2.33, 4.38, 4.09, 2.52, 5.19, 2.39, 3.66, 2.29, 2.88])
_MINOR_PROFILE = np.array([6.33, 2.68, 3.52, 5.38, 2.60, 3.53, 2.54, 4.75, 3.98, 2.69, 3.34, 3.17])


def detect_key(y: np.ndarray, sr: int) -> dict:
    # Strip drums and bass transients before analysis so key detection
    # runs only on harmonic content (melodies, chords, pads)
    y_harmonic, _ = librosa.effects.hpss(y)
    chroma = librosa.feature.chroma_cqt(y=y_harmonic, sr=sr)
    chroma_mean = chroma.mean(axis=1)

    best_key = ""
    best_score = -np.inf

    for i, root in enumerate(PITCH_CLASSES):
        rotated = np.roll(chroma_mean, -i)
        major_corr = float(np.corrcoef(rotated, _MAJOR_PROFILE)[0, 1])
        minor_corr = float(np.corrcoef(rotated, _MINOR_PROFILE)[0, 1])

        if major_corr > best_score:
            best_score = major_corr
            best_key = f"{root} major"
        if minor_corr > best_score:
            best_score = minor_corr
            best_key = f"{root} minor"

    return {"key": best_key, "confidence": round(best_score, 3)}


def interpret_audio(data: dict) -> dict:
    tags = []

    if data["peak"] > 0.95:
        tags.append("clipping risk — peak near 0 dBFS")
    elif data["peak"] < 0.5:
        tags.append("underutilised headroom — mix is quiet")

    if data["rms_avg"] < 0.01:
        tags.append("very low RMS — mix lacks energy or density")
    elif data["rms_avg"] > 0.3:
        tags.append("high RMS — mix is loud/heavily compressed")

    freq = data["frequency_balance"]
    total = freq["low"] + freq["mid"] + freq["high"]
    if total > 0:
        low_pct = freq["low"] / total
        mid_pct = freq["mid"] / total
        high_pct = freq["high"] / total

        if low_pct > 0.6:
            tags.append("bass-heavy — lows dominate the mix")
        elif low_pct < 0.2:
            tags.append("thin low end — 808 or kick may be weak")
        if mid_pct < 0.2:
            tags.append("scooped mids — melody or chords may be buried")
        if high_pct < 0.1:
            tags.append("dark/dull mix — hi-hats or air frequencies are low")
        elif high_pct > 0.45:
            tags.append("bright mix — high end may be harsh")

    centroid = data["spectral_centroid_hz"]
    if centroid < 1500:
        tags.append(f"low spectral centroid ({centroid} Hz) — mix sounds muddy or dark")
    elif centroid > 4000:
        tags.append(f"high spectral centroid ({centroid} Hz) — mix sounds bright or thin")
    else:
        tags.append(f"spectral centroid at {centroid} Hz — balanced brightness")

    data["interpretation"] = tags if tags else ["no major issues flagged by analysis"]
    return data


def analyze_audio(file_path: str) -> dict:
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    if not file_path.lower().endswith(SUPPORTED_FORMATS):
        raise ValueError(f"Unsupported format. Supported: {', '.join(SUPPORTED_FORMATS)}")

    print("Analyzing audio...")
    y, sr = librosa.load(file_path, mono=True)

    tempo, _ = librosa.beat.beat_track(y=y, sr=sr)
    bpm = round(float(np.mean(tempo)), 1)

    rms = librosa.feature.rms(y=y)[0]
    rms_avg = float(np.mean(rms))
    rms_std = float(np.std(rms))
    peak = float(np.max(np.abs(y)))

    stft = np.abs(librosa.stft(y))
    freqs = librosa.fft_frequencies(sr=sr)

    low_mask = (freqs >= 20) & (freqs < 250)
    mid_mask = (freqs >= 250) & (freqs < 4000)
    high_mask = (freqs >= 4000) & (freqs < 16000)

    low_band = float(stft[low_mask].mean()) if np.any(low_mask) else 0.0
    mid_band = float(stft[mid_mask].mean()) if np.any(mid_mask) else 0.0
    high_band = float(stft[high_mask].mean()) if np.any(high_mask) else 0.0

    centroid_avg = round(float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))), 1)

    onset_env = librosa.onset.onset_strength(y=y, sr=sr)
    onset_rate = round(float(np.mean(onset_env > np.percentile(onset_env, 75))), 4)

    key_data = detect_key(y, sr)

    raw = {
        "bpm": bpm,
        "key": key_data["key"],
        "key_confidence": key_data["confidence"],
        "duration_sec": round(len(y) / sr, 2),
        "peak": round(peak, 4),
        "rms_avg": round(rms_avg, 6),
        "rms_std": round(rms_std, 6),
        "spectral_centroid_hz": centroid_avg,
        "transient_density": onset_rate,
        "frequency_balance": {
            "low": round(low_band, 4),
            "mid": round(mid_band, 4),
            "high": round(high_band, 4),
        },
    }

    return interpret_audio(raw)
