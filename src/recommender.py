import csv
from typing import List, Dict, Tuple
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
    """OOP wrapper around the scoring + ranking logic."""

    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Return the top k songs for a given user profile."""
        prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        scored = []
        for s in self.songs:
            song_dict = s.__dict__
            score, _ = score_song(prefs, song_dict)
            scored.append((s, score))
        scored.sort(key=lambda pair: pair[1], reverse=True)
        return [pair[0] for pair in scored[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Return a plain-language reason for why a song was picked."""
        prefs = {
            "genre": user.favorite_genre,
            "mood": user.favorite_mood,
            "energy": user.target_energy,
        }
        _, reasons = score_song(prefs, song.__dict__)
        return "; ".join(reasons) if reasons else "no strong match"


def load_songs(csv_path: str) -> List[Dict]:
    """Load songs from a CSV file and convert numeric fields to numbers."""
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
    """Score one song against user preferences and return (score, reasons)."""
    score = 0.0
    reasons = []

    # Default weights. Experiment results are documented in the README;
    # to re-run, try GENRE_WEIGHT=1.0 and ENERGY_WEIGHT=3.0.
    GENRE_WEIGHT = 2.0
    MOOD_WEIGHT = 1.0
    ENERGY_WEIGHT = 1.5

    # Genre match
    if user_prefs.get("genre") and song["genre"] == user_prefs["genre"]:
        score += GENRE_WEIGHT
        reasons.append(f"genre match: {song['genre']} (+{GENRE_WEIGHT})")

    # Mood match
    if user_prefs.get("mood") and song["mood"] == user_prefs["mood"]:
        score += MOOD_WEIGHT
        reasons.append(f"mood match: {song['mood']} (+{MOOD_WEIGHT})")

    # Energy closeness
    if "energy" in user_prefs:
        closeness = 1 - abs(song["energy"] - user_prefs["energy"])
        points = ENERGY_WEIGHT * closeness
        score += points
        reasons.append(f"energy close to {user_prefs['energy']} (+{points:.2f})")

    # Valence closeness: up to +1.0 (only if user gave one)
    if "valence" in user_prefs:
        closeness = 1 - abs(song["valence"] - user_prefs["valence"])
        points = 1.0 * closeness
        score += points
        reasons.append(f"valence close to {user_prefs['valence']} (+{points:.2f})")

    # Tempo closeness: up to +1.0 (divide by 200 to normalize)
    if "tempo" in user_prefs:
        closeness = 1 - abs(song["tempo_bpm"] - user_prefs["tempo"]) / 200
        points = 1.0 * closeness
        score += points
        reasons.append(f"tempo close to {user_prefs['tempo']} bpm (+{points:.2f})")

    return score, reasons


def recommend_songs(
    user_prefs: Dict, songs: List[Dict], k: int = 5
) -> List[Tuple[Dict, float, str]]:
    """Score every song, sort by score, and return the top k."""
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        explanation = "; ".join(reasons) if reasons else "no strong match"
        scored.append((song, score, explanation))

    # sorted() returns a new list (doesn't mutate `songs`); .sort() would
    # change the original list in place. We use sorted() to keep the input safe.
    ranked = sorted(scored, key=lambda item: item[1], reverse=True)
    return ranked[:k]
