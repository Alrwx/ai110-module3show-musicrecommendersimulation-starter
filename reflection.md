# Reflection — Profile Comparisons

## High-Energy Pop vs. Chill Lofi

The High-Energy Pop profile pulls in upbeat, danceable tracks like "Sunrise City" and "Gym Hero," while the Chill Lofi profile surfaces mellow, low-energy songs like "Midnight Coding" and "Library Rain." The two lists share zero overlap, which makes sense — they are about as far apart on the energy and mood spectrum as you can get. What stood out to me is that the Lofi profile's top songs are almost all from the same artist pool (LoRoom, Paper Lanterns), because the dataset only has a handful of low-energy tracks. A real lofi listener would notice the lack of variety pretty quickly.

## High-Energy Pop vs. Deep Intense Rock

These two profiles both want high energy, but they diverge on genre and mood. The Pop profile gets "Sunrise City" (pop/happy) at the top, while the Rock profile gets "Storm Runner" (rock/intense). Interestingly, "Gym Hero" appears in both top-5 lists — it is a pop song but its intense energy and high danceability give it crossover appeal. That tells me that the energy and danceability bonuses can push a song into a list even when it does not match the target genre, which is a nice emergent behavior of the scoring.

## Chill Lofi vs. Deep Intense Rock

This pair is the most dramatic contrast. The Lofi profile's top pick scores 3.98 and the Rock profile's top pick scores 3.99 — nearly identical totals, but for completely different reasons. The Lofi winner earns its points from genre + mood + energy closeness at the low end, while the Rock winner earns them from genre + mood + energy closeness at the high end. The system is basically doing the same math in two opposite directions, which is reassuring — it means the algorithm is not inherently biased toward high or low energy, it just rewards proximity to whatever the user asked for.

## Weight-Shift Experiment Observations

When I halved genre weight and doubled energy weight, the biggest change was that "Gym Hero" dropped from #2 to #4 in the Pop profile. Songs like "Rooftop Lights" (indie pop) and "Neon Bounce" (electropop) jumped up because their energy was very close to 0.8, and with the doubled multiplier that closeness was worth more than Gym Hero's genre match. This experiment made it clear that genre weight is doing most of the heavy lifting in the baseline — when you reduce it, the rankings start to feel more "vibe-based" and less "genre-locked," which could actually be a better experience for some users.

## Feature Removal Observation

Removing the mood check entirely made the Chill Lofi profile recommend "Focus Flow" (mood: focused) at almost the same rank as "Midnight Coding" (mood: chill). To a real listener, those are different vibes — chill is about relaxation, focused is about concentration. Without the mood signal, the system cannot tell the difference, and it just groups everything by genre and energy. That one-point mood bonus is small, but it does meaningful work in separating songs that otherwise look similar on paper.
