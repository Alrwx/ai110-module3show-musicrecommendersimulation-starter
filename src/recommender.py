"""Music recommender engine with weighted content-based scoring."""

import csv
import os
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass


@dataclass
class Song:
    """Represents a song and its attributes."""
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float


@dataclass
class UserProfile:
    """Represents a user's taste preferences."""
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool


class Recommender:
    """OOP implementation of the recommendation logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top-k songs ranked by score for the given user profile."""
        scored = []
        for song in self.songs:
            song_dict = {
                "id": song.id,
                "title": song.title,
                "artist": song.artist,
                "genre": song.genre,
                "mood": song.mood,
                "energy": song.energy,
                "tempo_bpm": song.tempo_bpm,
                "valence": song.valence,
                "danceability": song.danceability,
                "acousticness": song.acousticness,
            }
            user_dict = {
                "genre": user.favorite_genre,
                "mood": user.favorite_mood,
                "energy": user.target_energy,
            }
            score, _ = score_song(user_dict, song_dict)
            scored.append((song, score))

        scored.sort(key=lambda x: x[1], reverse=True)
        return [song for song, _ in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a human-readable explanation of why this song was recommended."""
        song_dict = {
            "id": song.id,
            "title": song.title,
            "artist": song.artist,
            "genre": song.genre,
            "mood": song.mood,
            "energy": song.energy,
            "tempo_bpm": song.tempo_bpm,
            "valence": song.valence,
            "danceability": song.danceability,
            "acousticness": song.acousticness,
        }
        user_dict = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        score, reasons = score_song(user_dict, song_dict)
        return f"Score {score:.2f} — " + "; ".join(reasons)


# ---------------------------------------------------------------------------
# Functional helpers used by src/main.py
# ---------------------------------------------------------------------------

def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dictionaries."""
    # Resolve path relative to project root when running as module
    if not os.path.isabs(csv_path):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(base, csv_path)

    songs = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            row["id"] = int(row["id"])
            row["energy"] = float(row["energy"])
            row["tempo_bpm"] = float(row["tempo_bpm"])
            row["valence"] = float(row["valence"])
            row["danceability"] = float(row["danceability"])
            row["acousticness"] = float(row["acousticness"])
            songs.append(row)

    print(f"Loaded songs: {len(songs)}")
    return songs


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Score a single song against user preferences.

    Algorithm Recipe
    ----------------
    +2.0 points  — genre match
    +1.0 point   — mood match
    energy score — 1.0 minus the absolute difference between the user's
                   target energy and the song's energy (rewards closeness)
    +0.3 bonus   — danceability above 0.7

    Returns (total_score, list_of_reason_strings).
    """
    score = 0.0
    reasons: List[str] = []

    # Genre match (+2.0)
    if song.get("genre", "").lower() == user_prefs.get("genre", "").lower():
        score += 2.0
        reasons.append("genre match (+2.0)")

    # Mood match (+1.0)
    if song.get("mood", "").lower() == user_prefs.get("mood", "").lower():
        score += 1.0
        reasons.append("mood match (+1.0)")

    # Energy similarity (max +1.0, min 0.0)
    target_energy = float(user_prefs.get("energy", 0.5))
    song_energy = float(song.get("energy", 0.5))
    energy_score = round(1.0 - abs(target_energy - song_energy), 2)
    score += energy_score
    reasons.append(f"energy similarity (+{energy_score})")

    # Danceability bonus
    if float(song.get("danceability", 0)) > 0.7:
        score += 0.3
        reasons.append("high danceability (+0.3)")

    score = round(score, 2)
    return score, reasons


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort descending, and return the top-k results."""
    scored = []
    for song in songs:
        total, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, total, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
