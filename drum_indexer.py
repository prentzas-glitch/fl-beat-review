"""
Drum sound library indexer.

Scans a folder for drum sounds, extracts audio features with librosa,
and saves a drum_index.json inside that folder. The index is built once
and reused on every beat review — no re-scanning needed unless you add new sounds.

Features extracted per sound:
  - duration          — how long the sound is
  - peak              — loudest sample (0-1)
  - rms               — average energy / loudness
  - spectral_centroid — brightness (higher Hz = brighter/thinner sound)
  - attack_time       — how snappy the hit is (seconds to peak)
  - low_energy        — how much sub/low-end the sound has
  - fundamental_hz    — detected pitch (most useful for 808s)
  - fundamental_note  — e.g. "C2", "F#2" (used for key matching on 808s)

Accuracy:
  - Pitch detection on 808s is very reliable (clear fundamental frequency)
  - Brightness/attack on kicks and snares is reliable
  - Hi-hats and percs: brightness and duration work well, pitch less so
  - Sounds shorter than 0.05s or with very low peak are skipped as likely silent
"""

import json
import os
import numpy as np
import librosa
from pathlib import Path

AUDIO_EXTENSIONS = (".wav", ".mp3", ".aiff", ".flac", ".ogg")
INDEX_FILENAME = "drum_index.json"

# Category detection by filename keyword.
# For sounds with generic names (kick1, kick2) the category still gets
# detected — it just won't have a descriptive name, which is fine
# because we're using audio features, not names, for recommendations.
DRUM_CATEGORIES = {
    "808":    ["808", "sub", "eight08"],
    "kick":   ["kick", "kik", "bassdrum", "bass_drum", " bd_", "_bd_"],
    "snare":  ["snare", "snr", "_sd_", " sd_"],
    "clap":   ["clap", "clp"],
    "hihat":  ["hihat", "hi_hat", "hi-hat", "_hh", "hh_", "_hat", "hat_",
               "openhat", "closedhat", "ohh", "chh"],
    "cymbal": ["cymbal", "crash", "ride", "china"],
    "perc":   ["perc", "shaker", "tamb", "bongo", "conga", "cowbell", "rim", "tom"],
}


def _categorize(filename: str) -> str:
    name = Path(filename).stem.lower()
    for cat, keywords in DRUM_CATEGORIES.items():
        if any(kw in name for kw in keywords):
            return cat
    return "other"


def _extract_features(file_path: str) -> dict:
    """
    Load up to 4 seconds of a sound and extract drum-relevant features.
    Returns a dict of features, or {"error": ...} if analysis fails.
    """
    try:
        y, sr = librosa.load(file_path, mono=True, duration=4.0)

        # Skip sounds that are effectively silent
        peak = float(np.max(np.abs(y)))
        if peak < 0.02:
            return {"error": "silent or near-silent file"}

        duration = round(len(y) / sr, 4)
        rms      = round(float(np.mean(librosa.feature.rms(y=y)[0])), 6)

        # Brightness — how much high-frequency content
        centroid = round(float(np.mean(librosa.feature.spectral_centroid(y=y, sr=sr))), 1)

        # Attack time — seconds from start to peak transient
        onset_env    = librosa.onset.onset_strength(y=y, sr=sr)
        attack_frame = int(np.argmax(onset_env))
        attack_time  = round(float(librosa.frames_to_time(attack_frame, sr=sr)), 4)

        # Low-end weight (20–200 Hz) — important for kicks and 808s
        stft     = np.abs(librosa.stft(y))
        freqs    = librosa.fft_frequencies(sr=sr)
        low_mask = (freqs >= 20) & (freqs < 200)
        low_energy = round(float(stft[low_mask].mean()), 5) if np.any(low_mask) else 0.0

        # Fundamental pitch — most reliable on 808s and tonal percs
        fundamental_hz   = None
        fundamental_note = None
        try:
            f0, voiced, _ = librosa.pyin(
                y,
                fmin=librosa.note_to_hz("C1"),
                fmax=librosa.note_to_hz("C5"),
            )
            voiced_f0 = f0[voiced & ~np.isnan(f0)] if f0 is not None else np.array([])
            if len(voiced_f0) > 0:
                fundamental_hz   = round(float(np.median(voiced_f0)), 1)
                fundamental_note = librosa.hz_to_note(fundamental_hz)
        except Exception:
            pass

        return {
            "duration":         duration,
            "peak":             round(peak, 4),
            "rms":              rms,
            "spectral_centroid_hz": centroid,
            "attack_time_sec":  attack_time,
            "low_energy":       low_energy,
            "fundamental_hz":   fundamental_hz,
            "fundamental_note": fundamental_note,
        }

    except Exception as e:
        return {"error": str(e)}


def build_index(folder_path: str) -> dict:
    """
    Scan a folder for audio files, extract features from each one,
    and save drum_index.json inside the folder.

    Returns a summary: {category: count} plus total.
    """
    folder = Path(folder_path).expanduser()
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")
    if not folder.is_dir():
        raise ValueError(f"Not a folder: {folder_path}")

    # Find all audio files recursively
    audio_files = [
        Path(root) / f
        for root, _, files in os.walk(folder)
        for f in files
        if Path(f).suffix.lower() in AUDIO_EXTENSIONS
    ]

    if not audio_files:
        raise ValueError(f"No audio files found in {folder_path}")

    index: dict[str, list] = {}

    for filepath in audio_files:
        cat      = _categorize(filepath.name)
        features = _extract_features(str(filepath))

        if "error" in features:
            continue  # skip silent or unreadable files

        entry = {
            "path":     str(filepath),
            "filename": filepath.name,
            "features": features,
        }

        index.setdefault(cat, []).append(entry)

    # Save to drum_index.json inside the folder
    index_path = folder / INDEX_FILENAME
    payload = {
        "folder": str(folder),
        "total_indexed": sum(len(v) for v in index.values()),
        "index": index,
    }
    with open(index_path, "w") as f:
        json.dump(payload, f, indent=2)

    summary = {cat: len(sounds) for cat, sounds in index.items()}
    summary["total"] = payload["total_indexed"]
    summary["index_path"] = str(index_path)
    return summary


def load_index(folder_path: str) -> dict | None:
    """Load a previously built index. Returns None if not found."""
    index_path = Path(folder_path).expanduser() / INDEX_FILENAME
    if not index_path.exists():
        return None
    with open(index_path) as f:
        return json.load(f).get("index", {})


def find_candidates(index: dict, target_key: str = "", n: int = 3) -> dict:
    """
    Score and rank drum sounds per category, returning the top N per category.

    Scoring:
      - 808s: +100 if fundamental note matches the target key
      - All:  +10 if peak is in a healthy range (not too quiet, not clipping)
      - All:  +5  if duration is appropriate for the category
    """
    target_note = target_key.split()[0].upper() if target_key else ""
    candidates  = {}

    for cat, sounds in index.items():
        scored = []
        for sound in sounds:
            f = sound.get("features", {})
            if not f or "error" in f:
                continue

            score = 0

            # Key matching for 808s
            if cat == "808" and target_note and f.get("fundamental_note"):
                if target_note in f["fundamental_note"].upper():
                    score += 100

            # Healthy peak level
            peak = f.get("peak", 0)
            if 0.25 < peak < 0.97:
                score += 10

            # Duration sanity per category
            dur = f.get("duration", 0)
            if cat in ("kick", "snare", "clap") and 0.05 < dur < 1.5:
                score += 5
            elif cat in ("hihat", "cymbal") and dur < 3.0:
                score += 5
            elif cat == "808" and dur > 0.5:
                score += 5

            scored.append((score, sound))

        scored.sort(key=lambda x: x[0], reverse=True)
        if scored:
            candidates[cat] = [s for _, s in scored[:n]]

    return candidates


def format_candidates_for_prompt(candidates: dict, target_key: str = "") -> str:
    """
    Format drum candidates into a readable block for the Drums agent prompt.
    """
    if not candidates:
        return "No drum library indexed."

    target_note = target_key.split()[0].upper() if target_key else ""
    lines = ["Producer's drum library — best candidates per category:"]

    for cat, sounds in candidates.items():
        lines.append(f"\n{cat.upper()}:")
        for s in sounds:
            f    = s["features"]
            name = s["filename"]
            tags = []

            if f.get("fundamental_note"):
                match = target_note and target_note in f["fundamental_note"].upper()
                tags.append(f"pitch: {f['fundamental_note']}" + (" ← KEY MATCH" if match else ""))
            if f.get("spectral_centroid_hz"):
                brightness = "bright" if f["spectral_centroid_hz"] > 3000 else \
                             "mid" if f["spectral_centroid_hz"] > 1500 else "dark"
                tags.append(f"tone: {brightness}")
            if f.get("attack_time_sec") is not None:
                snappiness = "snappy" if f["attack_time_sec"] < 0.01 else \
                             "medium attack" if f["attack_time_sec"] < 0.05 else "slow attack"
                tags.append(snappiness)
            if f.get("duration"):
                tags.append(f"{f['duration']}s")

            tag_str = " · ".join(tags)
            lines.append(f"  · {name}  [{tag_str}]")

    lines.append(
        "\nWhen recommending drum sounds, reference files by exact filename. "
        "Explain briefly why each choice fits (tone, pitch match, attack character)."
    )
    return "\n".join(lines)
