import csv
from typing import Callable, List, Dict, Tuple, Optional
from dataclasses import dataclass, field, asdict

REASON_THRESHOLD = 0.7 # minimum per-feature score that earns a reason
GENRE_MISMATCH_PENALTY = 0.15 # subtracted from the final score when genre doesn't match


# --- Scoring strategies -----------------------------------------------------
# Each strategy turns (user target, song value) into a 0-1 similarity. The
# `label` is the word used in the human-readable reason ("genre match", ...).

def _as_set(target) -> set:
    """Normalizes a target that may be a single string or a list of values."""
    return {target} if isinstance(target, str) else set(target)


class ExactMatch:
    """1.0 if the song's value is one of the accepted values, else 0.0."""
    label = "match"

    def __call__(self, target, value) -> float:
        return 1.0 if value in _as_set(target) else 0.0


class AnyOverlap:
    """1.0 if the two tag lists share at least one tag, else 0.0."""
    label = "match"

    def __call__(self, target, value) -> float:
        return 1.0 if set(target) & set(value) else 0.0


class Jaccard:
    """Jaccard overlap (|A and B| / |A or B|) between two tag lists."""
    label = "overlap"

    def __call__(self, target, value) -> float:
        wanted, actual = set(target), set(value)
        union = wanted | actual
        return len(wanted & actual) / len(union) if union else 0.0


class ScaledDistance:
    """1 - gap / scale, clamped to 0-1, for features not on a 0-1 scale."""
    label = "close"

    def __init__(self, scale: float):
        self.scale = scale

    def __call__(self, target, value) -> float:
        gap = abs(value - target) / self.scale
        return 1.0 - min(max(gap, 0.0), 1.0)


class UnitDistance:
    """1 - |difference|, for features already on a 0-1 scale."""
    label = "close"

    def __call__(self, target, value) -> float:
        return 1.0 - abs(value - target)


# Feature registry: feature name -> (scoring strategy, weight).
# To add a feature, add one line here (and the field to Song/UserProfile).
FEATURES = {
    "genre":            (ExactMatch(),        0.20),
    "energy":           (UnitDistance(),      0.20),
    "mood":             (ExactMatch(),        0.15),
    "mood_tags":        (AnyOverlap(),        0.10),
    "valence":          (UnitDistance(),      0.06),
    "acousticness":     (UnitDistance(),      0.05),
    "tempo_bpm":        (ScaledDistance(120), 0.04),  # BPM
    "danceability":     (UnitDistance(),      0.03),
    "instrumentalness": (UnitDistance(),      0.03),
    "loudness_db":      (ScaledDistance(30),  0.03),  # dB
    "language":         (ExactMatch(),        0.03),
    "activity_fit":     (Jaccard(),           0.03),
    "release_decade":   (ScaledDistance(60),  0.03),  # years
    "popularity":       (UnitDistance(),      0.02),
}
WEIGHTS = {name: weight for name, (_, weight) in FEATURES.items()}
assert abs(sum(WEIGHTS.values()) - 1.0) < 1e-9, "WEIGHTS must sum to 1.0"


# --- Skip rules and adjustments ---------------------------------------------
# Skip rules run per feature, before scoring: return True to leave a feature
# out entirely (its weight is not counted). Adjustments run once, after the
# weighted average: each returns the new score plus any reasons to record.

def _skip_mood_tags_when_mood_matched(feature: str, user_prefs: Dict, song: Dict) -> bool:
    """Avoids double-counting mood: tags are redundant once mood already matched."""
    if feature != "mood_tags":
        return False
    mood_target = user_prefs.get("mood")
    return mood_target is not None and ExactMatch()(mood_target, song["mood"]) == 1.0


def _genre_mismatch_penalty(score: float, user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """Subtracts a flat penalty when a genre target is given and doesn't match."""
    genre_target = user_prefs.get("genre")
    if genre_target is not None and ExactMatch()(genre_target, song["genre"]) == 0.0:
        return score - GENRE_MISMATCH_PENALTY, [f"genre mismatch (-{GENRE_MISMATCH_PENALTY:.2f})"]
    return score, []


SKIP_RULES = [_skip_mood_tags_when_mood_matched]
ADJUSTMENTS = [_genre_mismatch_penalty]

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

# A scorer takes (user_prefs, song) as dicts and returns (score, reasons).
Scorer = Callable[[Dict, Dict], Tuple[float, List[str]]]


def score_song(user_prefs: Dict, song: Dict) -> Tuple[float, List[str]]:
    """
    Scores one song against user preferences, returning (score, reasons).

    Only features present in user_prefs are scored. Each feature is scored by
    the strategy registered for it in FEATURES (see the strategy classes
    above) and weighted; the weighted sum is divided by the weight actually
    used, so the result is 0-1. SKIP_RULES can exclude a feature for a given
    song, and ADJUSTMENTS (e.g. the genre mismatch penalty) modify the final
    score; the result is floored at 0. Features scoring at least
    REASON_THRESHOLD add a human-readable entry to reasons.
    Required by recommend_songs() and src/main.py
    """
    total = 0.0
    used_weight = 0.0
    reasons: List[str] = []

    for feature, (scorer, weight) in FEATURES.items():
        target = user_prefs.get(feature)
        if target is None or target == []:
            continue
        if any(rule(feature, user_prefs, song) for rule in SKIP_RULES):
            continue

        feature_score = scorer(target, song[feature])
        contribution = feature_score * weight
        total += contribution
        used_weight += weight

        if feature_score >= REASON_THRESHOLD:
            reasons.append(f"{feature} {scorer.label} (+{contribution:.2f})")

    score = total / used_weight if used_weight > 0 else 0.0

    for adjust in ADJUSTMENTS:
        score, extra_reasons = adjust(score, user_prefs, song)
        reasons.extend(extra_reasons)

    return max(score, 0.0), reasons

def recommend_songs(
    user_prefs: Dict,
    songs: List[Dict],
    k: int = 5,
    scorer: Scorer = score_song,
) -> List[Tuple[Dict, float, str]]:
    """
    Returns the top k songs for a user as (song, score, explanation) tuples.

    Scores every song with `scorer` (default score_song), joins its reasons
    into a single "; "-separated explanation string, and sorts by score
    descending.
    Required by src/main.py
    """
    scored = []
    for song in songs:
        score, reasons = scorer(user_prefs, song)
        scored.append((song, score, "; ".join(reasons)))
    return sorted(scored, key=lambda item: item[1], reverse=True)[:k]


def profile_to_prefs(user: UserProfile) -> Dict:
    """
    Converts a UserProfile into the prefs dict that score_song() expects.

    Unset (None) and empty-list preferences are omitted so they are skipped
    by scoring (an empty genre list would otherwise trigger the mismatch
    penalty on every song).
    """
    prefs = {
        "genre": user.favorite_genres,
        "mood": user.favorite_moods,
        "energy": user.target_energy,
        "valence": user.target_valence,
        "acousticness": user.target_acousticness,
        "tempo_bpm": user.target_tempo_bpm,
        "danceability": user.target_danceability,
        "instrumentalness": user.target_instrumentalness,
        "popularity": user.target_popularity,
        "mood_tags": user.favorite_mood_tags,
        "loudness_db": user.target_loudness_db,
        "language": user.favorite_languages,
        "activity_fit": user.favorite_activities,
        "release_decade": user.target_release_decade,
    }
    return {k: v for k, v in prefs.items() if v is not None and v != []}


class Recommender:
    """
    OOP wrapper around the functional scoring API.

    Converts Song/UserProfile objects to the dict form and delegates to
    recommend_songs(), so both entry points share one scoring path.
    A custom `scorer` can be injected; it defaults to score_song.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song], scorer: Scorer = score_song):
        """Stores the song catalog and the scoring function to use."""
        self.songs = songs
        self.scorer = scorer

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """Returns the top k songs for the given user profile."""
        song_dicts = [asdict(song) for song in self.songs]
        by_dict_id = {id(d): s for d, s in zip(song_dicts, self.songs)}
        ranked = recommend_songs(
            profile_to_prefs(user), song_dicts, k, scorer=self.scorer
        )
        return [by_dict_id[id(d)] for d, _score, _why in ranked]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """Returns a human-readable explanation of why a song was recommended."""
        score, reasons = self.scorer(profile_to_prefs(user), asdict(song))
        why = "; ".join(reasons) if reasons else "no strong feature matches"
        return f"{song.title} (score {score:.2f}): {why}"
