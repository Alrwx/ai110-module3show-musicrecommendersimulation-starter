"""Command-line runner for the Music Recommender Simulation.

The script prints recommendations for a few sample user profiles and then
summarizes a small reliability check so the project shows measurable behavior,
not just a static demo.
"""

from __future__ import annotations

import argparse
import logging

from recommender import (
    confidence_from_recommendations,
    evaluate_profiles,
    load_songs,
    recommend_songs,
)


logging.basicConfig(level=logging.INFO, format="[%(levelname)s] %(message)s")


# Sample user profiles shown in the demo output.
PROFILES = {
    "High-Energy Pop": {"genre": "pop", "mood": "happy", "energy": 0.8},
    "Chill Lofi": {"genre": "lofi", "mood": "chill", "energy": 0.4},
    "Deep Intense Rock": {"genre": "rock", "mood": "intense", "energy": 0.9},
}


# Reliability cases use expected top picks so the app can report pass/fail.
RELIABILITY_CASES = {
    "High-Energy Pop": {
        "genre": "pop",
        "mood": "happy",
        "energy": 0.8,
        "expected_top": "Sunrise City",
    },
    "Chill Lofi": {
        "genre": "lofi",
        "mood": "chill",
        "energy": 0.4,
        "expected_top": "Night Shift Notes",
    },
    "Deep Intense Rock": {
        "genre": "rock",
        "mood": "intense",
        "energy": 0.9,
        "expected_top": "Thunder Chapel",
    },
}


def display_recommendations(profile_name: str, user_prefs: dict, songs: list, k: int = 5) -> None:
    """Print a nicely formatted recommendation block for one profile."""
    recs = recommend_songs(user_prefs, songs, k=k)
    confidence = confidence_from_recommendations(recs)

    print("=" * 66)
    print(f"Profile: {profile_name}")
    print(
        f"Prefs  : genre={user_prefs['genre']}, mood={user_prefs['mood']}, "
        f"energy={user_prefs['energy']}"
    )
    print(f"Confidence: {confidence:.2f} (higher means a clearer top choice)")
    print("=" * 66)

    for rank, (song, score, explanation) in enumerate(recs, start=1):
        print(f"#{rank}  {song['title']} by {song['artist']}")
        print(f"    Score : {score:.2f}")
        print(f"    Why   : {explanation}")
        print()


def print_reliability_report(songs: list) -> None:
    """Print a short evaluation summary for the sample profiles."""
    report = evaluate_profiles(RELIABILITY_CASES, songs, k=5)
    print("\nRELIABILITY CHECK")
    print("-" * 66)
    print(
        f"Matched expected top picks: {report['matched']}/{report['evaluated']} "
        f"(average confidence {report['average_confidence']:.2f})"
    )
    for item in report["details"]:
        status = "PASS" if item["passed"] else "FAIL"
        print(
            f"[{status}] {item['profile']}: top={item['top_title']} | "
            f"expected={item['expected_top']} | confidence={item['confidence']:.2f}"
        )


def _prompt_float(prompt: str, default: float) -> float:
    raw = input(prompt).strip()
    if not raw:
        return default
    try:
        return float(raw)
    except ValueError:
        print(f"Invalid number '{raw}'. Using default {default}.")
        return default


def _prompt_profile() -> dict:
    print("\nEnter a custom profile (press Enter to use each default):")
    genre = input("Genre [pop]: ").strip().lower() or "pop"
    mood = input("Mood [happy]: ").strip().lower() or "happy"
    energy = _prompt_float("Energy 0.0-1.0 [0.8]: ", 0.8)
    likes_acoustic_raw = input("Likes acoustic songs? (y/n) [n]: ").strip().lower()
    likes_acoustic = likes_acoustic_raw in {"y", "yes", "true", "1"}

    return {
        "genre": genre,
        "mood": mood,
        "energy": energy,
        "likes_acoustic": likes_acoustic,
    }


def run_interactive_mode(songs: list) -> None:
    print("Interactive Mode")
    print("-" * 66)
    print("Type different user preferences to generate recommendations.")
    print("Use this mode in your video to demonstrate multiple input cases.\n")

    case_number = 1
    while True:
        prefs = _prompt_profile()
        display_recommendations(f"Custom Case {case_number}", prefs, songs)
        case_number += 1

        again = input("Run another custom case? (y/n) [n]: ").strip().lower()
        if again not in {"y", "yes"}:
            break


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Music Recommender Simulation")
    parser.add_argument(
        "--interactive",
        action="store_true",
        help="Run prompt-based custom inputs instead of only built-in demo profiles.",
    )
    return parser.parse_args()


def main() -> None:
    args = parse_args()
    songs = load_songs("data/songs.csv")

    print("Music Recommender Simulation")
    print("=" * 66)
    print(f"Loaded {len(songs)} songs from the catalog.\n")

    if args.interactive:
        run_interactive_mode(songs)
    else:
        for name, prefs in PROFILES.items():
            display_recommendations(name, prefs, songs)

    print_reliability_report(songs)


if __name__ == "__main__":
    main()
