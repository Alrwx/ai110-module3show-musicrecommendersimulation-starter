"""Music recommender engine with weighted content-based scoring.

The module keeps the original rule-based recommender API, but now also
includes validation, logging, confidence scoring, and a small evaluation
helper so the app can report how reliably the rankings behave.
"""

from __future__ import annotations

import csv
import logging
import os
from dataclasses import dataclass
from typing import Any, Dict, List, Tuple


logger = logging.getLogger(__name__)


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
                "likes_acoustic": user.likes_acoustic,
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
            "likes_acoustic": user.likes_acoustic,
        }
        score, reasons = score_song(user_dict, song_dict)
        return f"Score {score:.2f} — " + "; ".join(reasons)


# ---------------------------------------------------------------------------
# Functional helpers used by src/main.py
# ---------------------------------------------------------------------------


def _normalize_text(value: Any) -> str:
    if value is None:
        return ""
    return str(value).strip().lower()


def _safe_float(value: Any, default: float = 0.0, field_name: str = "value") -> float:
    try:
        return float(value)
    except (TypeError, ValueError):
        logger.warning("Invalid %s %r; using default %.2f.", field_name, value, default)
        return default


def _coerce_bool(value: Any) -> bool:
    if isinstance(value, bool):
        return value
    if isinstance(value, str):
        return value.strip().lower() in {"1", "true", "t", "yes", "y", "on"}
    return bool(value)


def validate_user_prefs(user_prefs: Dict[str, Any]) -> Dict[str, Any]:
    """Normalize and guardrail user inputs before scoring."""
    validated = {
        "genre": _normalize_text(user_prefs.get("genre", "")),
        "mood": _normalize_text(user_prefs.get("mood", "")),
    }

    energy = _safe_float(user_prefs.get("energy", 0.5), default=0.5, field_name="energy")
    if energy < 0.0 or energy > 1.0:
        logger.warning("Energy %.2f is out of range; clamping to 0.0-1.0.", energy)
        energy = max(0.0, min(1.0, energy))
    validated["energy"] = energy

    if "likes_acoustic" in user_prefs:
        validated["likes_acoustic"] = _coerce_bool(user_prefs.get("likes_acoustic"))

    return validated


def confidence_from_recommendations(
    recommendations: List[Tuple[Dict, float, str]]
) -> float:
    """Return a 0-1 confidence score derived from the gap between the top two items."""
    if not recommendations:
        return 0.0

    if len(recommendations) == 1:
        return 1.0

    gap = max(0.0, recommendations[0][1] - recommendations[1][1])
    confidence = gap / 1.5
    return round(min(1.0, confidence), 2)


def evaluate_profiles(
    profile_specs: Dict[str, Dict[str, Any]], songs: List[Dict[str, Any]], k: int = 5
) -> Dict[str, Any]:
    """Run a lightweight reliability check over a set of named profile cases."""
    details: List[Dict[str, Any]] = []
    evaluated = 0
    matched = 0
    confidence_values: List[float] = []

    for profile_name, spec in profile_specs.items():
        prefs = dict(spec)
        expected_top = prefs.pop("expected_top", None)
        recommendations = recommend_songs(prefs, songs, k=k)
        top_title = recommendations[0][0]["title"] if recommendations else None
        confidence = confidence_from_recommendations(recommendations)

        if expected_top is not None:
            evaluated += 1
            if top_title == expected_top:
                matched += 1

        confidence_values.append(confidence)
        details.append(
            {
                "profile": profile_name,
                "top_title": top_title,
                "expected_top": expected_top,
                "confidence": confidence,
                "passed": expected_top is None or top_title == expected_top,
            }
        )

    average_confidence = round(sum(confidence_values) / len(confidence_values), 2) if confidence_values else 0.0
    return {
        "evaluated": evaluated,
        "matched": matched,
        "average_confidence": average_confidence,
        "details": details,
    }


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and return a list of dictionaries."""
    if not os.path.isabs(csv_path):
        base = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
        csv_path = os.path.join(base, csv_path)

    songs: List[Dict[str, Any]] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        reader = csv.DictReader(f)
        for row in reader:
            try:
                row["id"] = int(row["id"])
                row["energy"] = float(row["energy"])
                row["tempo_bpm"] = float(row["tempo_bpm"])
                row["valence"] = float(row["valence"])
                row["danceability"] = float(row["danceability"])
                row["acousticness"] = float(row["acousticness"])
            except (KeyError, TypeError, ValueError) as exc:
                logger.warning("Skipping malformed song row %r: %s", row.get("title", row), exc)
                continue

            songs.append(row)

    logger.info("Loaded %d songs from %s", len(songs), csv_path)
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
    user_prefs = validate_user_prefs(user_prefs)
    score = 0.0
    reasons: List[str] = []

    if _normalize_text(song.get("genre")) == user_prefs.get("genre", ""):
        score += 2.0
        reasons.append("genre match (+2.0)")

    if _normalize_text(song.get("mood")) == user_prefs.get("mood", ""):
        score += 1.0
        reasons.append("mood match (+1.0)")

    target_energy = _safe_float(user_prefs.get("energy", 0.5), default=0.5, field_name="energy")
    song_energy = _safe_float(song.get("energy", 0.5), default=0.5, field_name="song energy")
    energy_score = max(0.0, round(1.0 - abs(target_energy - song_energy), 2))
    score += energy_score
    reasons.append(f"energy similarity (+{energy_score})")

    if _safe_float(song.get("danceability", 0), default=0.0, field_name="danceability") > 0.7:
        score += 0.3
        reasons.append("high danceability (+0.3)")

    if "likes_acoustic" in user_prefs:
        likes_acoustic = _coerce_bool(user_prefs.get("likes_acoustic"))
        acousticness = _safe_float(song.get("acousticness", 0), default=0.0, field_name="acousticness")
        if likes_acoustic and acousticness >= 0.7:
            score += 0.4
            reasons.append("acoustic texture match (+0.4)")
        elif not likes_acoustic and acousticness <= 0.2:
            score += 0.2
            reasons.append("clean/electronic texture bonus (+0.2)")

    score = round(score, 2)
    return score, reasons


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort descending, and return the top-k results."""
    if k <= 0:
        logger.warning("Requested k=%d recommendations; returning an empty list.", k)
        return []

    scored = []
    for song in songs:
        total, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons)
        scored.append((song, total, explanation))

    scored.sort(key=lambda x: x[1], reverse=True)
    return scored[:k]
