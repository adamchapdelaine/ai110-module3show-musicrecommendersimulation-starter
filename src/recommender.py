import csv
from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass, field

WEIGHTS = {
    "genre": 0.20, "energy": 0.20, "mood": 0.15,
    "mood_tags": 0.10, "valence": 0.06, "acousticness": 0.05,
    "tempo_bpm": 0.04, "danceability": 0.03, "instrumentalness": 0.03,
    "loudness_db": 0.03, "language": 0.03, "activity_fit": 0.03,
    "release_decade": 0.03, "popularity": 0.02,
}
assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9, "WEIGHTS must sum to 1.0"

# Feature value that maps a raw difference to a 0-1 distance (larger gap = lower score)
SCALED_RANGES = {
    "tempo_bpm": 120,      # BPM
    "loudness_db": 30,     # dB
    "release_decade": 60,  # years
}
BINARY_FEATURES = {"genre", "mood", "language"} # exact match -> 1.0 or 0.0
SET_FEATURES = {"activity_fit"} # Jaccard overlap of tag sets
ANY_MATCH_FEATURES = {"mood_tags"} # 1.0 if any tag is shared, else 0.0
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
    mood_tags: list[str]
    loudness_db: float
    language: str
    activity_fit: list[str]
    release_decade: int

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
    favorite_mood_tags: list[str] = field(default_factory=list)
    target_loudness_db: Optional[float] = None
    favorite_languages: list[str] = field(default_factory=list)
    favorite_activities: list[str] = field(default_factory=list)
    target_release_decade: Optional[int] = None



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
    Loads songs from a CSV file into a list of dicts.

    Parses id and release_decade as ints, numeric audio features (including
    loudness_db) as floats, and splits the pipe-delimited mood_tags and
    activity_fit columns into lists of strings. Other columns stay as strings.
    Required by src/main.py
    """
    int_fields = ("id", "release_decade")
    float_fields = (
        "energy", "tempo_bpm", "valence", "danceability",
        "acousticness", "speechiness", "instrumentalness", "popularity",
        "loudness_db",
    )
    list_fields = ("mood_tags", "activity_fit")

    songs: List[Dict] = []
    with open(csv_path, newline="", encoding="utf-8") as f:
        for row in csv.DictReader(f):
            for name in int_fields:
                row[name] = int(row[name])
            for name in float_fields:
                row[name] = float(row[name])
            for name in list_fields:
                row[name] = [tag for tag in row[name].split("|") if tag]
            songs.append(row)
    return songs

def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores one song against user preferences, returning (score, reasons).

    Only features present in user_prefs are scored, using the weights in
    WEIGHTS; the weighted sum is divided by the weight actually used, so the
    result is 0-1. Scoring by feature type:
      - genre, mood, language: 1.0 on exact match (target may be a str or a
        list of acceptable values), else 0.0
      - mood_tags, activity_fit: Jaccard overlap between the user's tag list
        and the song's tag list
      - tempo_bpm, loudness_db, release_decade: 1 - gap / SCALED_RANGES[feature]
      - all other numeric features: 1 - absolute difference (0-1 scale)
    A flat GENRE_MISMATCH_PENALTY is subtracted when a genre target is given
    and the song's genre differs; the final score is floored at 0. Features
    scoring at least REASON_THRESHOLD add a human-readable entry to reasons.
    Required by recommend_songs() and src/main.py
    """
    total = 0.0
    used_weight = 0.0
    reasons: List[str] = []

    mood_target = user_prefs.get("mood")
    mood_matched = mood_target is not None and song["mood"] in (
        {mood_target} if isinstance(mood_target, str)
        else set(mood_target)
    )

    for feature, weight in WEIGHTS.items():
        target = user_prefs.get(feature)
        if target is None or target == []:
            continue
        if feature == "mood_tags" and mood_matched:
            continue

        if feature in BINARY_FEATURES:
            accepted = {target} if isinstance(target, str) else set(target)
            feature_score = 1.0 if song[feature] in accepted else 0.0
            label = "match"
        elif feature in ANY_MATCH_FEATURES:
            feature_score = 1.0 if set(target) & set(song[feature]) else 0.0
            label = "match"
        elif feature in SET_FEATURES:
            wanted, actual = set(target), set(song[feature])
            union = wanted | actual
            feature_score = len(wanted & actual) / len(union) if union else 0.0
            label = "overlap"
        elif feature in SCALED_RANGES:
            diff = abs(song[feature] - target) / SCALED_RANGES[feature]
            feature_score = 1.0 - min(max(diff, 0.0), 1.0)
            label = "close"
        else:
            feature_score = 1.0 - abs(song[feature] - target)
            label = "close"

        contribution = feature_score * weight
        total += contribution
        used_weight += weight

        if feature_score >= REASON_THRESHOLD:
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
    Returns the top k songs for a user as (song, score, explanation) tuples.

    Scores every song with score_song(), joins its reasons into a single
    "; "-separated explanation string, and sorts by score descending.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = score_song(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]
