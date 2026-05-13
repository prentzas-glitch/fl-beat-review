import json
import sys

from analysis import analyze_audio
from prompt import build_prompt
from ai import get_beat_review, follow_up_loop
from ui import print_banner, pick_genre, pick_skill_level

if __name__ == "__main__":
    print_banner()

    file_path = input("Path to your beat: ").strip().strip("'\"")

    try:
        audio_data = analyze_audio(file_path)
    except (FileNotFoundError, ValueError) as e:
        print(f"\nError: {e}")
        sys.exit(1)

    genre, genre_profile = pick_genre()
    reference = input("\nReference artist or track (e.g. Central Cee, Metro Boomin): ").strip()
    skill_level = pick_skill_level()

    prompt = build_prompt(genre, reference, genre_profile, audio_data, skill_level)

    print("\n" + "─" * 50)
    print("Audio Analysis")
    print("─" * 50)
    print(json.dumps(audio_data, indent=2))

    print("\n" + "─" * 50)
    print("Beat Review")
    print("─" * 50 + "\n")

    try:
        review = get_beat_review(file_path, prompt)
        print(review)
    except Exception as e:
        print(f"\nError getting review: {e}")
        sys.exit(1)

    follow_up_loop(prompt, review, skill_level)
