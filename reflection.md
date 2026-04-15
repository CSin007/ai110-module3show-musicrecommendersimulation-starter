# Reflection: Comparing User Profile Outputs

Below I compare each pair of profiles I tested in `src/main.py`. For each pair I write what changed in the top 5 and why it makes sense.

## High-Energy Pop vs. Chill Lofi Study

The High-Energy Pop profile puts **Sunrise City** and **Gym Hero** at the top — both are pop songs with energy above 0.8. The Chill Lofi Study profile puts **Library Rain** and **Midnight Coding** at the top — both are lofi songs with energy around 0.35–0.42. The two top-5 lists share zero songs. This makes sense: the profiles are almost exact opposites on every dimension (genre, mood, and energy all point in different directions), so there's no reason for the same song to satisfy both. This is the system working correctly — different taste, different results.

## High-Energy Pop vs. Deep Intense Rock

Both profiles want high energy (0.9 and 0.95), but they disagree on genre (pop vs rock) and mood (happy vs intense). Interestingly, **Gym Hero** shows up in both top-5 lists — in Pop it's #2 (genre + energy), in Rock it's #3 (mood + energy). Gym Hero is pop-genre but intense-mood and very high energy, so it's a "jack of all trades" that partially satisfies both. **Storm Runner** (rock/intense) leads the Rock list with a perfect 3-of-3 match, but only limps into #5 on the Pop list via energy alone. The overlap is explained entirely by the shared energy target.

## Chill Lofi Study vs. Deep Intense Rock

These are almost total opposites (low-energy chill lofi vs. high-energy intense rock). Zero songs overlap between the two top-5 lists. Library Rain (energy 0.35) and Storm Runner (energy 0.91) sit at opposite ends of the catalog. This is a good sanity check — if there *were* overlap between these, something would be broken.

## High-Energy Pop vs. Conflicting (Sad but Hype)

Both want high energy, but the Conflicting profile asks for `genre: edm, mood: sad`. The top pick shifts from **Sunrise City** (Pop) to **Bass Drop Circuit** (edm match + energy match). **Heartbreak Highway** (a country/sad song, energy 0.48) sneaks into #2 purely because of the mood match, even though its energy is way below 0.9. This is the adversarial test paying off — it shows that when genre and mood disagree, the system doesn't pick a "compromise" song; it alternates between songs that satisfy *one* dimension well. That's an honest answer for a contradictory user.

## Chill Lofi Study vs. Numbers-Only (energy 0.5)

Numbers-Only has no genre or mood at all, only `energy: 0.5`. The top 5 becomes a grab-bag of songs from totally different genres (country, jazz, r&b, lofi) that all happen to have energy near 0.5. Score spread collapses: in Lofi Study the top score was 4.50 and the fifth was 1.47 (big gap); in Numbers-Only the top is 1.47 and the fifth is 1.35 (tiny gap). This is what "low confidence" looks like in a weighted-sum recommender — without the categorical signals, nothing strongly separates the songs.

## Deep Intense Rock vs. Conflicting (Sad but Hype)

Both want very high energy, but the Rock profile gets a clean 3-of-3 match on Storm Runner (4.44) while the Conflicting profile's best is Bass Drop Circuit (3.42). Storm Runner appears in #3 of the Conflicting list — high energy overlap again. The Conflicting profile's score ceiling is lower overall because no song can satisfy genre=edm AND mood=sad at the same time in this catalog.

---

## The Plain-Language Explanation

Imagine a non-programmer asking: *"Why does Gym Hero keep showing up for people who just want Happy Pop?"*

Gym Hero is labeled pop genre, intense mood, and very high energy. When someone asks for "happy pop with high energy," the system checks three boxes: pop genre ✓ (2 points), mood happy ✗ (0 points, because Gym Hero is "intense" not "happy"), energy close ✓ (1.47 points). That adds up to 3.47 — not the highest possible (Sunrise City is happier), but higher than almost any non-pop alternative. Basically, Gym Hero is a "close enough" song that keeps winning runner-up because it matches *most* of what most energetic-pop fans ask for, even when it misses the mood. To push it down, I'd either need to weight mood more heavily, or add a penalty for mood mismatches instead of just not-awarding points.
