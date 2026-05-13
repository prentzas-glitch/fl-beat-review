"""
Sound library scanner.

Scans a local folder for audio files and categorizes them by filename keywords.
Only filenames are read — no audio content is loaded or uploaded anywhere.

Accuracy depends on how well files are named. Most sample packs and drum kits
use descriptive names (e.g. 'Dark_808_C.wav', 'Metro_Snare_Punchy.wav') which
gives the agents enough to make specific, actionable recommendations.
"""

import os
from pathlib import Path

AUDIO_EXTENSIONS = (".wav", ".mp3", ".aiff", ".flac", ".ogg", ".rx2")

# Keywords used to categorize files. Order matters — first match wins.
CATEGORIES = [
    ("808",     ["808", "eight08", "sub_bass", "sub bass"]),
    ("kick",    ["kick", "kik", " bd ", "bassdrum", "bass_drum", "bass drum"]),
    ("snare",   ["snare", "snr", " sd ", "rimshot"]),
    ("clap",    ["clap", "clp"]),
    ("hihat",   ["hihat", "hi-hat", "hi_hat", "hh_", "_hh", "hat_", "_hat",
                  "open hat", "closed hat", "openhat", "closedhat", "ohh", "chh"]),
    ("cymbal",  ["cymbal", "crash", "ride", "china"]),
    ("perc",    ["perc", "shaker", "tamb", "bongo", "conga", "cowbell",
                  "woodblock", "rim", "tom"]),
    ("loop",    ["loop", "lp_", "_lp"]),
    ("melody",  ["melody", "mel_", "_mel", "lead", "arp", "hook", "piano",
                  "keys", "guitar", "flute", "violin", "brass", "horn"]),
    ("pad",     ["pad_", "_pad", "atmosphere", "atm_", "ambient", "texture", "choir"]),
    ("bass",    ["bass", "bas_"]),
    ("vocal",   ["vocal", "vox", "voice", "chop", "adlib", "ad lib"]),
    ("fx",      ["fx_", "_fx", "riser", "downlift", "impact", "transition",
                  "sweep", "reverse", "foley", "noise"]),
]


def scan_library(folder_path: str, max_per_category: int = 20) -> dict:
    """
    Walk a folder recursively, find all audio files, and return them
    grouped by category.

    max_per_category caps how many files per category are returned
    so the agent prompt stays a reasonable size.
    """
    folder = Path(folder_path).expanduser()
    if not folder.exists():
        raise FileNotFoundError(f"Folder not found: {folder_path}")
    if not folder.is_dir():
        raise ValueError(f"Not a directory: {folder_path}")

    # Collect all audio files
    all_files: list[Path] = []
    for root, _dirs, files in os.walk(folder):
        for f in files:
            if Path(f).suffix.lower() in AUDIO_EXTENSIONS:
                all_files.append(Path(root) / f)

    if not all_files:
        return {}

    # Categorize by filename keywords
    categorized: dict[str, list[str]] = {cat: [] for cat, _ in CATEGORIES}
    categorized["other"] = []

    for filepath in all_files:
        name_lower = filepath.stem.lower()
        matched = False
        for cat, keywords in CATEGORIES:
            if any(kw in name_lower for kw in keywords):
                if len(categorized[cat]) < max_per_category:
                    categorized[cat].append(filepath.name)
                matched = True
                break
        if not matched and len(categorized["other"]) < max_per_category:
            categorized["other"].append(filepath.name)

    # Remove empty categories and return total file count too
    result = {k: v for k, v in categorized.items() if v}
    result["_total_files"] = len(all_files)
    return result


def format_library_for_prompt(library: dict, detected_key: str = "") -> str:
    """
    Format the categorized library into a readable block for the agent prompt.
    Puts key-matching files first when a detected key is available.
    """
    if not library:
        return "No sound library provided."

    total = library.pop("_total_files", 0)
    key_hint = detected_key.split()[0].upper() if detected_key else ""

    lines = [f"Producer's sound library ({total} files total):"]

    for category, files in library.items():
        if not files:
            continue

        # Boost key-matching files to the top of each category
        if key_hint:
            key_files  = [f for f in files if key_hint in f.upper()]
            rest_files = [f for f in files if key_hint not in f.upper()]
            ordered = key_files + rest_files
        else:
            ordered = files

        lines.append(f"\n{category.upper()} ({len(files)} files):")
        for f in ordered[:15]:  # show max 15 per category in prompt
            tag = " ← matches key" if key_hint and key_hint in f.upper() else ""
            lines.append(f"  · {f}{tag}")
        if len(files) > 15:
            lines.append(f"  … and {len(files) - 15} more")

    # Restore the total key so callers can still read it
    library["_total_files"] = total

    return "\n".join(lines)
