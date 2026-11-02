from dataclasses import asdict

import pytest

from src.recommender import (
    RANKING_MODES, Song, UserProfile, Recommender, make_scorer,
    profile_to_prefs, recommend_songs,
)


def make_song(**overrides) -> Song:
    fields = dict(
        id=1, title="Test Pop Track", artist="Test Artist",
        genre="pop", mood="happy", energy=0.8, tempo_bpm=120, valence=0.9,
        danceability=0.8, acousticness=0.2, instrumentalness=0.05,
        popularity=0.7, mood_tags=["happy", "upbeat"], loudness_db=-6.0,
        language="en", activity_fit=["workout"], release_decade=2020,
    )
    fields.update(overrides)
    return Song(**fields)


def make_small_recommender(**kwargs) -> Recommender:
    songs = [
        make_song(),
        make_song(
            id=2, title="Chill Lofi Loop", genre="lofi", mood="chill",
            energy=0.4, tempo_bpm=80, valence=0.6, danceability=0.5,
            acousticness=0.9, mood_tags=["chill"], activity_fit=["study"],
        ),
    ]
    return Recommender(songs, **kwargs)


def make_user() -> UserProfile:
    return UserProfile(
        favorite_genres=["pop"],
        favorite_moods=["happy"],
        target_energy=0.8,
    )


def test_recommend_returns_songs_sorted_by_score():
    rec = make_small_recommender()
    results = rec.recommend(make_user(), k=2)

    assert len(results) == 2
    assert all(isinstance(s, Song) for s in results)
    # The pop, happy, high energy song should score higher
    assert results[0].genre == "pop"
    assert results[0].mood == "happy"


def test_recommend_respects_k():
    assert len(make_small_recommender().recommend(make_user(), k=1)) == 1


def test_explain_recommendation_returns_non_empty_string():
    rec = make_small_recommender()
    explanation = rec.explain_recommendation(make_user(), rec.songs[0])
    assert isinstance(explanation, str)
    assert explanation.strip() != ""


def test_custom_scorer_is_used():
    # A scorer that prefers the lowest-energy song overrides the default.
    def low_energy_scorer(prefs, song):
        return 1.0 - song["energy"], ["low energy"]

    rec = make_small_recommender(scorer=low_energy_scorer)
    assert rec.recommend(make_user(), k=1)[0].genre == "lofi"
    assert "low energy" in rec.explain_recommendation(make_user(), rec.songs[0])


def test_recommend_songs_accepts_custom_scorer():
    songs = [{"n": 1}, {"n": 2}]
    ranked = recommend_songs({}, songs, k=1, scorer=lambda p, s: (s["n"], []))
    assert ranked[0][0] == {"n": 2}


def test_profile_to_prefs_omits_unset_values():
    prefs = profile_to_prefs(UserProfile(favorite_genres=[], favorite_moods=["happy"]))
    # An empty genre list must be dropped, not passed on (it would penalize every song)
    assert prefs == {"mood": ["happy"]}


# --- Ranking modes ----------------------------------------------------------

def make_mode_catalog():
    """
    Two songs that pull in opposite directions for the pop / happy user:
      genre_song: right genre, wrong mood, far-off energy (low score)
      mood_song:  wrong genre, right mood, perfect energy (high score)
    """
    genre_song = make_song(
        id=1, title="Genre Match", genre="pop", mood="sad", energy=0.1,
        mood_tags=["sad"],
    )
    mood_song = make_song(
        id=2, title="Mood Match", genre="rock", mood="happy", energy=0.8,
        mood_tags=["happy"],
    )
    return [genre_song, mood_song]


def top_title(mode_name: str) -> str:
    mode = RANKING_MODES[mode_name]
    rec = Recommender(make_mode_catalog(), scorer=mode.scorer, key=mode.key)
    return rec.recommend(make_user(), k=1)[0].title


def test_ranking_modes_pick_different_top_songs():
    assert top_title("genre-first") == "Genre Match"
    assert top_title("mood-first") == "Mood Match"
    assert top_title("genre-first") != top_title("mood-first")


def test_genre_first_is_a_hard_priority_not_a_boost():
    # The genre match has the LOWER score, yet genre-first still ranks it first.
    mode = RANKING_MODES["genre-first"]
    prefs = profile_to_prefs(make_user())
    songs = [asdict(s) for s in make_mode_catalog()]
    by_score = recommend_songs(prefs, songs, k=2)  # no key: pure score order
    by_genre = recommend_songs(prefs, songs, k=2, scorer=mode.scorer, key=mode.key)

    assert by_score[0][0]["title"] == "Mood Match"
    assert by_genre[0][0]["title"] == "Genre Match"
    assert by_genre[0][1] < by_genre[1][1]


def test_balanced_mode_matches_default_behavior():
    prefs = profile_to_prefs(make_user())
    songs = [asdict(s) for s in make_mode_catalog()]
    mode = RANKING_MODES["balanced"]
    assert recommend_songs(prefs, songs, scorer=mode.scorer, key=mode.key) == \
        recommend_songs(prefs, songs)


def test_make_scorer_rejects_unknown_feature():
    with pytest.raises(ValueError):
        make_scorer({"not_a_feature": 0.5})
