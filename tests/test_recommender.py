from src.recommender import (
    Song, UserProfile, Recommender, profile_to_prefs, recommend_songs,
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
