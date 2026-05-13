from genres import GENRE_PROFILES
from analysis import SUPPORTED_FORMATS


def print_genres() -> None:
    genres = sorted(GENRE_PROFILES.keys())
    col_width = 20
    cols = 3
    print("\nAvailable genres:")
    for i, g in enumerate(genres):
        print(f"  {g:<{col_width}}", end="\n" if (i + 1) % cols == 0 else "")
    if len(genres) % cols != 0:
        print()


def pick_genre() -> tuple[str, dict]:
    print_genres()
    while True:
        raw = input("\nGenre: ").strip().lower()
        if raw in GENRE_PROFILES:
            return raw, GENRE_PROFILES[raw]

        matches = [g for g in GENRE_PROFILES if raw in g or g in raw]
        if len(matches) == 1:
            print(f"  Matched: {matches[0]}")
            return matches[0], GENRE_PROFILES[matches[0]]
        elif len(matches) > 1:
            print(f"  Did you mean: {', '.join(matches)}?")
        else:
            print("  Genre not recognised. Try from the list, or press Enter to default to 'trap'.")
            confirm = input("  Use 'trap'? (y/n): ").strip().lower()
            if confirm in ("y", "yes", ""):
                return "trap", GENRE_PROFILES["trap"]


def pick_skill_level() -> str:
    print("\nSkill level:")
    print("  1. Beginner      — new to production, need plain-English explanations")
    print("  2. Intermediate  — know the basics, want technique-focused feedback")
    print("  3. Advanced      — experienced, want dense technical feedback")
    while True:
        choice = input("\nYour level (1 / 2 / 3): ").strip().lower()
        if choice in ("1", "beginner", "b"):
            return "beginner"
        if choice in ("2", "intermediate", "i", "inter"):
            return "intermediate"
        if choice in ("3", "advanced", "a", "adv"):
            return "advanced"
        print("  Enter 1, 2, or 3.")


def print_banner() -> None:
    print("=" * 50)
    print("   FL Studio Beat Review Tool")
    print("   Drop your beat. Get real feedback.")
    print("=" * 50)
    print(f"\nSupported formats: {', '.join(f.lstrip('.').upper() for f in SUPPORTED_FORMATS)}")
    print()
