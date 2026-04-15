# 🎧 Model Card: VibeFinder 1.0

## 1. Model Name

**VibeFinder 1.0** — a tiny content-based music recommender built as a classroom simulation.

---

## 2. Goal / Task

VibeFinder tries to predict which songs a user will enjoy based on their stated taste (favorite genre, favorite mood, target energy). Given a small catalog of songs, it scores every one of them against the user's preferences and returns the top 5 as recommendations. The goal is to explore *how* recommenders turn data into suggestions, not to ship anything real.

---

## 3. Data Used

- **Catalog size:** 20 songs in `data/songs.csv`.
- **Features per song:** id, title, artist, genre, mood, energy (0–1), tempo_bpm, valence (0–1), danceability (0–1), acousticness (0–1).
- **Genres covered:** pop, lofi, rock, ambient, jazz, synthwave, indie pop, classical, edm, country, world, hip hop, blues, techno, folk, r&b.
- **Moods covered:** happy, chill, intense, relaxed, focused, moody, sad, peaceful, confident, melancholy, hype, nostalgic.
- **Limits:** only 20 songs total, no lyrics, no release year, no cultural/regional info, Western-centric labels, and only 1–2 songs per niche genre.

---

## 4. Algorithm Summary

For each song, the system checks five things and adds up points. Genre match gives +2. Mood match gives +1. Energy, valence, and tempo each give up to a small number of points based on how close the song's value is to what the user wanted (closer = more points, farther = fewer). All the points get added into one total score. Then every song in the catalog is sorted from highest score to lowest, and the top 5 are shown with a short list of reasons explaining why each one ranked where it did. It's not machine learning — it's a weighted sum that any middle-schooler could verify on paper.

---

## 5. Observed Behavior / Biases

The biggest pattern I noticed is that **genre dominates the rankings** because it's worth 2 points while mood is only 1 and the numeric features only contribute fractional points. A song in the right genre almost always beats a song in the wrong genre, even if the wrong-genre song matches mood and energy better. This means users who like hybrid or borderline genres (like "indie pop" when there's only "pop" and "indie pop" as separate labels) get fewer good matches. I also noticed a "jack-of-all-trades" pattern — Gym Hero kept appearing in unrelated top-5s because it's pop + intense + very high energy, so it partially satisfies both pop-happy users and rock-intense users. Finally, with a 20-song catalog, any genre with only 1–2 songs barely gets represented, which unfairly punishes users with niche taste.

---

## 6. Evaluation Process

I tested five user profiles through `src/main.py`:

1. **High-Energy Pop** — well-aligned preferences
2. **Chill Lofi Study** — well-aligned in a different direction
3. **Deep Intense Rock** — well-aligned, opposite end of the catalog
4. **Conflicting (Sad but Hype)** — adversarial, mood and energy disagree
5. **Numbers-Only** — edge case with no genre/mood at all

For each profile I checked: does the top pick match my gut feeling? Do different profiles produce visibly different top-5 lists (no universal winner)? Does the adversarial profile break the system?

I also ran one weight experiment — doubled energy weight (1.5 → 3.0) and halved genre weight (2.0 → 1.0). The top picks stayed the same for clean profiles, but lower ranks shifted as energy started outweighing genre identity. I reverted to the original weights because the shifted results felt *different* but not *better*.

Detailed pair-by-pair comparisons live in [reflection.md](reflection.md).

---

## 7. Intended Use and Non-Intended Use

**Intended use:** classroom demo for learning how a content-based recommender scores and ranks items; a sandbox for experimenting with feature weights and seeing how rankings change.

**Not intended for:**
- Real users or production music apps.
- Anything where fairness or representation matters — the dataset is too small and too biased.
- Cultural or cross-lingual music discovery — the system has no language or regional data.
- Any high-stakes decision (curation, royalty splits, playlisting).

---

## 8. Ideas for Improvement

1. **Fuzzy genre matching** — treat "pop" and "indie pop" as partially similar instead of unrelated; let the user's preferred genre get partial credit for adjacent genres.
2. **Bigger catalog** — at least 100 songs with balanced genre coverage so niche-taste users aren't starved.
3. **Diversity in the top 5** — add a small penalty when the top picks are all by the same artist or all from the same genre, to avoid the filter-bubble effect.

---

## 9. Personal Reflection

**Biggest learning moment:** realizing that a "recommender" is just a weighted sum plus a sort. For weeks I thought Spotify's magic came from some deep neural net, and while the real systems do use fancy models, the *skeleton* of every recommender is this simple scoring-and-ranking loop. That made the whole field feel approachable instead of intimidating. The second big moment was watching my weight choices shape the output — picking `GENRE_WEIGHT = 2.0` felt arbitrary when I typed it, but it completely changed which songs got surfaced. That's where bias enters a system: not through evil intent, but through casual numeric choices nobody thinks to question.

**Where AI tools helped vs. where I had to double-check:** Copilot was great for boilerplate — writing the `csv.DictReader` loop, suggesting the `sorted(..., key=lambda)` pattern, generating dataset rows in CSV format. It was less trustworthy when I asked "which features should I use?" — it confidently suggested features that *sounded* music-y without checking whether they were actually in my CSV, so I learned to verify against the real file before acting on suggestions. It also tended to over-engineer — suggesting error handling and type guards I didn't need for a 20-song simulation. I kept trimming it back.

**What surprised me:** how much the output *feels* like a recommendation, even though the logic is trivial. When Library Rain showed up for "chill lofi study" with reasons printed next to it ("genre match: lofi, mood match: chill, energy close to 0.35"), it felt *personal* — not because the algorithm is smart, but because the output format tells a little story. That's a design lesson too: transparency makes a dumb system feel competent, while black-box systems feel suspicious even when they're good.

**What I'd try next:** adding a thumbs-up/thumbs-down prompt in the CLI so the user's feedback tweaks the weights over the session — a tiny version of online learning. I'd also want to try a collaborative-filtering toy version by hand-writing 3–4 user profiles and recommending based on *which other user most resembles you*, just to feel the difference between CBF and CF on the same dataset.
