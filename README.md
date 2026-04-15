# 🎵 Music Recommender Simulation

## Project Summary

This project simulates a content-based music recommendation system. Given a catalog of 18 songs (stored as CSV) and a user "taste profile" describing preferred genre, mood, and energy level, the system scores every song with a weighted algorithm and returns the top matches along with plain-language explanations of why each song was chosen. The goal is to explore how platforms like Spotify turn raw song attributes into personalized suggestions, and to understand where simple scoring rules succeed and where they fall short.

---

## How The System Works

Each **Song** carries numerical and categorical attributes pulled straight from the CSV: genre, mood, energy (0–1), tempo_bpm, valence, danceability, and acousticness.

A **UserProfile** stores three preference dimensions: favorite_genre (text), favorite_mood (text), and target_energy (a number between 0 and 1).

The recommender scores every song against the profile using a simple additive recipe: +2.0 points for a genre match, +1.0 for a mood match, up to +1.0 for energy similarity (calculated as 1 minus the absolute gap between the user's target and the song's energy), and a small +0.3 bonus for songs with danceability above 0.7. After scoring, the system sorts all songs from highest to lowest score and returns the top k results. Each recommendation includes the numeric score and a list of reasons so the user can see exactly which rules fired.

This approach is purely content-based — it only looks at song attributes, not at what other listeners have enjoyed. Real platforms combine content-based filtering with collaborative filtering (learning from similar users), but content-based scoring is the foundation that makes cold-start recommendations possible.

---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows
   ```

2. Install dependencies:

   ```bash
   pip install -r requirements.txt
   ```

3. Run the app:

   ```bash
   cd src
   python main.py
   ```

### Running Tests

```bash
pytest tests/test_recommender.py
```

---

## Experiments I Tried

**Baseline run** — Three profiles (High-Energy Pop, Chill Lofi, Deep Intense Rock) each returned intuitively correct top picks. "Sunrise City" dominated the pop/happy profile; "Midnight Coding" and "Library Rain" led the lofi profile; "Storm Runner" was the clear winner for intense rock.

**Weight-shift experiment** — I halved the genre weight from 2.0 to 1.0 and doubled the energy multiplier from 1x to 2x. The effect was that non-pop songs with energy values close to 0.8 (like "Rooftop Lights" and "Neon Bounce") climbed above "Gym Hero" in the pop profile, because energy similarity became worth more than a genre match. This showed that genre weight is the main driver of the original ranking — reducing it lets energy dominate, which can be good for "vibe-based" recommendations but bad if users care most about genre.

**Feature removal experiment** — Commenting out the mood check meant that chill and intense songs scored almost identically if their energy happened to be close to the target. The "Chill Lofi" profile started recommending "Focus Flow" (mood: focused) at nearly the same rank as "Midnight Coding" (mood: chill), even though a real lofi listener would probably prefer the chill track.

---

## Limitations and Risks

The catalog is tiny (18 songs), so results are heavily shaped by which songs happen to exist in the CSV. If most songs are pop, the system will over-represent pop for almost any profile.

The scoring ignores lyrics, language, release date, and social context — all things real listeners care about. It also treats every user as having exactly one genre preference, which misses people who enjoy multiple styles.

Because genre carries the heaviest weight (+2.0), a single genre preference can dominate the ranking and create a "filter bubble" where the user never discovers music outside their stated favorite.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Building this recommender made me realize how much of what feels like a "smart" suggestion is really just a few if-statements and some arithmetic. The system does a surprisingly decent job at surfacing the right songs for straightforward profiles, but it completely breaks down for users with mixed or unusual tastes. That gap between "works on paper" and "works for real people" is exactly where bias creeps in — the algorithm only knows what you told it to care about, and everything else is invisible to it. Real-world recommenders layer on collaborative signals, exploration bonuses, and fairness constraints to close that gap, but even those systems inherit biases from the data they train on.
