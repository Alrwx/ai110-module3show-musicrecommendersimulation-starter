# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name

Model

---

## 2. Intended Use

It suggests the top 5 songs from a small catalog based on a user's stated genre, mood, and energy preferences. It is designed for educational exploration of how recommendation algorithms work, not for production use with real listeners.

The system assumes each user has a single favorite genre, a single preferred mood, and one target energy level. It is not designed for users with complex or multi-genre tastes.

---

## 3. How the Model Works

For every song in the catalog, the model adds up points based on how well the song matches the user's profile. A matching genre is worth 2 points, a matching mood is worth 1 point, and the energy score rewards songs whose energy level is close to what the user asked for (up to 1 point — the closer the better). There is also a small 0.3-point bonus for songs with high danceability. The system then ranks all songs by total score and shows the top 5 with an explanation of exactly which rules contributed.

Think of it like a judge at a talent show holding up scorecards: each song gets rated on three or four criteria, the scores are added together, and the highest total wins.

---

## 4. Data

The catalog contains 18 songs stored in `data/songs.csv`. The original starter set had 10 songs, and I added 8 more to cover genres and moods that were missing, including folk, metal, EDM, country, electropop, and acoustic. Moods now include melancholy, focused, and relaxed in addition to the original happy, chill, intense, and moody.

The dataset still skews toward upbeat and electronic styles. Genres like classical, R&B, hip-hop, and Latin are completely absent, so the recommender cannot serve users who prefer those styles. The data mostly reflects a narrow slice of English-language indie and electronic music.

---

## 5. Strengths

It works well for "clean" profiles where the user's genre, mood, and energy all point in the same direction. For example, a "pop/happy/high-energy" user gets "Sunrise City" at the top, which is exactly what you would expect. The lofi/chill profile correctly surfaces "Midnight Coding" and "Library Rain" ahead of everything else.

The explanations attached to each recommendation make the system transparent — you can see precisely why a song scored the way it did, which is something most real-world recommenders do not offer.

The simplicity of the scoring rule also makes it easy to experiment with. Changing one weight immediately changes the output in a predictable way, which is valuable for understanding how algorithmic choices shape user experience.

---

## 6. Limitations and Bias

The system over-prioritizes genre because the genre weight (+2.0) is the largest single factor. This means a user who says "pop" will almost always see pop songs at the top, even if a non-pop song matches their mood and energy perfectly. This creates a filter bubble where the user never gets exposed to music outside their declared favorite.

The dataset is small and unbalanced. With 18 songs, several genres have only one representative. If the catalog happened to have five pop songs and one metal song, pop listeners get variety while metal listeners get one recommendation and then random filler.

The system treats energy as a single number, but real musical energy is more nuanced. A song can feel energetic because of fast drums or because of loud guitars — those are very different vibes, and a single 0-to-1 scale flattens that distinction.

There is no collaborative filtering, so the system cannot learn from patterns across users. Two users with identical profiles always get identical results, regardless of their actual listening history.

---

## 7. Evaluation

I tested three user profiles: High-Energy Pop, Chill Lofi, and Deep Intense Rock. For each, I checked whether the top results intuitively matched what a real person with those preferences would want to hear.

I also ran a weight-shift experiment where I halved the genre weight and doubled the energy multiplier. This caused the rankings to shift noticeably — songs that matched on energy moved up even if they were from a different genre. It confirmed that genre weight is the dominant factor in the baseline system.

Finally, I temporarily removed the mood check entirely and observed that the Chill Lofi profile started ranking "focused" and "chill" songs almost identically, which felt wrong. That experiment validated that mood matching, even at only +1.0, plays an important role in distinguishing between similar-energy songs.

---

## 8. Future Work

If I kept developing this, I would add support for multi-genre preferences so a user could say they enjoy both "lofi" and "jazz." I would also experiment with a diversity bonus that penalizes consecutive recommendations from the same genre, to avoid the filter bubble problem.

Adding tempo matching and valence (musical positivity) to the scoring formula would let the system capture more nuance. I would also want to test with a much larger catalog — at least 100 songs — to see how the algorithm performs when there are many close candidates to choose from.

Lastly, adding a simple feedback loop where the user can thumbs-up or thumbs-down a recommendation and have the weights adjust over time would move the system closer to how real recommenders learn.

---

## 9. Personal Reflection

The thing that surprised me most was how much a small catalog limits what you can learn about an algorithm. With only 18 songs, there are not enough candidates to really stress-test the scoring, and the "right" answer often feels obvious just by scanning the data manually. I imagine that at scale, subtle weight differences would produce much more dramatic ranking shifts, and debugging unexpected results would be way harder.

Building this changed how I think about real music recommenders. When Spotify suggests a song, I used to assume there was something deeply intelligent going on. Now I realize that the core idea is not that different from what I built here — match features, add up scores, rank — it is just happening across millions of songs with hundreds of features and layers of machine learning on top. The "intelligence" comes more from the data and the iteration than from any single clever formula.

I also noticed that the places where my system felt most unfair were the places where the data was thin. If there is only one folk song in the catalog, a folk lover gets a terrible experience no matter how good the algorithm is. That made me think about how real-world bias often comes from data gaps rather than from intentionally bad code — the algorithm can only work with what it is given.
