"""Command line runner for the Music Recommender Simulation."""

from src.recommender import load_songs, recommend_songs


# A bunch of different user profiles to stress-test the recommender.
PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.9},
    "Chill Lofi Study": {"genre": "lofi", "mood": "chill", "energy": 0.35},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.95},
    # Adversarial / edge case: mood and energy pull in opposite directions.
    # "sad" songs are usually low energy, but this user wants energy 0.9.
    "Conflicting (Sad but Hype)": {"genre": "edm", "mood": "sad", "energy": 0.9},
    # Empty-ish profile: no genre or mood, only a number.
    "Numbers-Only (no genre/mood)": {"energy": 0.5},
}


def print_recs(profile_name: str, user_prefs: dict, songs: list) -> None:
    """Print the top 5 recommendations for one profile in a clean layout."""
    print("=" * 60)
    print(f"Profile: {profile_name}")
    print(f"Prefs: {user_prefs}")
    print("-" * 60)
    recs = recommend_songs(user_prefs, songs, k=5)
    for i, (song, score, explanation) in enumerate(recs, start=1):
        print(f"{i}. {song['title']} by {song['artist']}")
        print(f"   Score: {score:.2f}")
        print(f"   Because: {explanation}")
    print()


def main() -> None:
    songs = load_songs("data/songs.csv")
    print()
    for name, prefs in PROFILES.items():
        print_recs(name, prefs, songs)


if __name__ == "__main__":
    main()
