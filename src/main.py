"""
Command line runner for the Music Recommender Simulation.

Loads the song catalog, defines several user taste profiles,
and prints the top-5 recommendations for each profile.
"""

from recommender import load_songs, recommend_songs


# ── User Profiles ──────────────────────────────────────────────────────────
PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.8},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.4},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9},
}


def display_recommendations(profile_name: str, user_prefs: dict,
                            songs: list, k: int = 5) -> None:
    """Print a nicely formatted recommendation block for one profile."""
    recs = recommend_songs(user_prefs, songs, k=k)

    print("=" * 60)
    print(f"  Profile: {profile_name}")
    print(f"  Prefs  : genre={user_prefs['genre']}, "
          f"mood={user_prefs['mood']}, energy={user_prefs['energy']}")
    print("=" * 60)

    for rank, (song, score, explanation) in enumerate(recs, start=1):
        print(f"  #{rank}  {song['title']} by {song['artist']}")
        print(f"       Score : {score:.2f}")
        print(f"       Why   : {explanation}")
        print()

    print()


def main() -> None:
    songs = load_songs("data/songs.csv")

    for name, prefs in PROFILES.items():
        display_recommendations(name, prefs, songs)


if __name__ == "__main__":
    main()
