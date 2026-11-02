import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass

WEIGHTS = {
    "genre": 0.10, "energy": 0.40, "mood": 0.142,
    "valence": 0.108, "acousticness": 0.083, "tempo_bpm": 0.050,
    "danceability": 0.042, "instrumentalness": 0.042,
    "popularity": 0.033
}
TEMPO_RANGE = 120 # normalizes BPM differences to roughly 0-1
BINARY_FEATURES = {"genre", "mood"}
REASON_THRESHOLD = 0.7 # minimum per-feature score that earns a reason
GENRE_MISMATCH_PENALTY = 0.15 # subtracted from the final score when genre doesn't match

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
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
    instrumentalness: float
    popularity: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genres: list[str]
    favorite_moods: list[str]
    target_energy: Optional[float] = None
    target_valence: Optional[float] = None
    target_acousticness: Optional[float] = None
    target_tempo_bpm: Optional[float] = None
    target_danceability: Optional[float] = None
    target_instrumentalness: Optional[float] = None
    target_popularity: Optional[float] = None 



class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        """Stores the song catalog to recommend from."""
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k songs for the given user profile."""
        # TODO: Implement recommendation logic
        return self.songs[:k]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable explanation of why a song was recommended."""
        # TODO: Implement explanation logic
        return "Explanation placeholder"

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    int_fields = ("id",)
    float_fields = (
        "energy", "tempo_bpm", "valence", "danceability",
        "acousticness", "speechiness", "instrumentalness", "popularity",
    )

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for field in int_fields:
                row[field] = int(row[field])
            for field in float_fields:
                row[field] = float(row[field])
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores a single song against user preferences.
    Required by recommend_songs() and src/main.py
    """
    total = 0.0
    used_weight = 0.0
    reasons: List[str] = []

    for feature, weight in WEIGHTS.items():
        target = user_prefs.get(feature)
        if target is None:
            continue

        if feature in BINARY_FEATURES:
            feature_score = 1.0 if song[feature] == target else 0.0
        elif feature == "tempo_bpm":
            diff = abs(song[feature] - target) / TEMPO_RANGE
            feature_score = 1.0 - min(max(diff, 0.0), 1.0)
        else:
            feature_score = 1.0 - abs(song[feature] - target)

        contribution = feature_score * weight
        total += contribution
        used_weight += weight

        if feature_score >= REASON_THRESHOLD:
            label = "match" if feature in BINARY_FEATURES else "close"
            reasons.append(f"{feature} {label} (+{contribution:.2f})")

    score = total / used_weight if used_weight > 0 else 0.0

    genre_target = user_prefs.get("genre")
    if genre_target is not None and song["genre"] != genre_target:
        score -= GENRE_MISMATCH_PENALTY
        reasons.append(f"genre mismatch (-{GENRE_MISMATCH_PENALTY:.2f})")

    score = max(score, 0.0)
    return score, reasons

def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
