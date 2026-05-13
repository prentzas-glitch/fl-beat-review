import os
from pathlib import Path

SUPPORTED_FORMATS = (".wav", ".mp3", ".flac", ".aiff", ".ogg")


def analyze_audio(file_path: str) -> dict:
    """Return basic file metadata. BPM/key/frequency analysis is done by Gemini."""
    if not os.path.exists(file_path):
        raise FileNotFoundError(f"File not found: {file_path}")
    if not file_path.lower().endswith(SUPPORTED_FORMATS):
        raise ValueError(f"Unsupported format. Supported: {', '.join(SUPPORTED_FORMATS)}")

    duration_sec = 0.0
    try:
        from mutagen import File as MutagenFile
        audio = MutagenFile(file_path)
        if audio and audio.info:
            duration_sec = round(float(audio.info.length), 2)
    except Exception:
        pass

    if duration_sec == 0.0 and file_path.lower().endswith(".wav"):
        try:
            import wave
            with wave.open(file_path, "rb") as wf:
                duration_sec = round(wf.getnframes() / wf.getframerate(), 2)
        except Exception:
            pass

    file_size_kb = round(os.path.getsize(file_path) / 1024, 1)

    return {
        "duration_sec": duration_sec,
        "file_size_kb": file_size_kb,
        "bpm": None,
        "key": None,
        "interpretation": [],
    }
