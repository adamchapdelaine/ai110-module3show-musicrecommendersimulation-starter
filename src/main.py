"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

import argparse

from src.recommender import RANKING_MODES, load_songs, recommend_songs

PROFILES = {
    "Intense Rock": {
        "genre": "rock", "mood": "intense", "energy": 0.92, "valence": 0.45,
        "acousticness": 0.10, "tempo_bpm": 150, "danceability": 0.50,
        "instrumentalness": 0.05, "popularity": 0.60,
        "mood_tags": ["intense", "driving", "aggressive"], "loudness_db": -6.0,
        "language": "en", "activity_fit": ["workout", "commute"],
        "release_decade": 2010,
    },
    "Chill Lofi": {
        "genre": "lofi", "mood": "chill", "energy": 0.38, "valence": 0.58,
        "acousticness": 0.80, "tempo_bpm": 76, "danceability": 0.60,
        "instrumentalness": 0.88, "popularity": 0.50,
        "mood_tags": ["chill", "calm", "cozy"], "loudness_db": -14.0,
        "language": "instrumental", "activity_fit": ["study", "focus"],
        "release_decade": 2020,
    },
    "High-Energy Pop": {
        "genre": "pop", "mood": "happy", "energy": 0.88, "valence": 0.85,
        "acousticness": 0.12, "tempo_bpm": 128, "danceability": 0.85,
        "instrumentalness": 0.02, "popularity": 0.90,
        "mood_tags": ["happy", "upbeat", "bright"], "loudness_db": -5.0,
        "language": "en", "activity_fit": ["workout", "party"],
        "release_decade": 2020,
    },
    "Mellow Jazz": {
        "genre": "jazz", "mood": "relaxed", "energy": 0.30, "valence": 0.65,
        "acousticness": 0.92, "tempo_bpm": 90, "danceability": 0.45,
        "instrumentalness": 0.60, "popularity": 0.35,
        "mood_tags": ["relaxed", "warm", "cozy"], "loudness_db": -15.0,
        "language": "instrumental", "activity_fit": ["relax", "study"],
        "release_decade": 2000,
    },
    "Sad Banger": {
        "genre": "pop", "mood": "melancholic", "energy": 0.80, "valence": 0.20,
        "acousticness": 0.15, "tempo_bpm": 120, "danceability": 0.80,
        "instrumentalness": 0.02, "popularity": 0.80,
        "mood_tags": ["melancholic", "dark", "energetic"], "loudness_db": -6.0,
        "language": "en", "activity_fit": ["late-night", "commute"],
        "release_decade": 2020,
    },
    "Upbeat Jazz": {
        "genre": "jazz", "mood": "upbeat", "energy": 0.78, "valence": 0.85,
        "acousticness": 0.60, "tempo_bpm": 105, "danceability": 0.85,
        "instrumentalness": 0.30, "popularity": 0.55,
        "mood_tags": ["upbeat", "playful", "warm"], "loudness_db": -9.0,
        "language": "instrumental", "activity_fit": ["social", "party"],
        "release_decade": 2000,
    },
    "Instrumental Hype": {
        "mood": "intense", "energy": 0.92, "valence": 0.35,
        "acousticness": 0.05, "tempo_bpm": 135, "danceability": 0.70,
        "instrumentalness": 0.90, "popularity": 0.45,
        "mood_tags": ["intense", "driving", "dark"], "loudness_db": -6.0,
        "language": "instrumental", "activity_fit": ["workout", "focus"],
        "release_decade": 2010,
    },
}

WIDTH = 60
BAR_LEN = 20


def score_bar(score: float) -> str:
    filled = round(score * BAR_LEN)
    return "█" * filled + "░" * (BAR_LEN - filled)


def print_recommendations(name: str, recommendations: list, mode_name: str) -> None:
    print("=" * WIDTH)
    print(f" {name}".upper())
    print(f" MODE: {mode_name}")
    print("=" * WIDTH)

    for rank, (song, score, explanation) in enumerate(recommendations, start=1):
        print(f"\n{rank}. {song['title']}  —  {song['artist']}")
        print(f"   Score: {score:.2f}  {score_bar(score)}")
        print("   Reasons:")
        reasons = [r for r in explanation.split("; ") if r]
        if reasons:
            for reason in reasons:
                print(f"     • {reason}")
        else:
            print("     • no strong feature matches")
        print("-" * WIDTH)
    print()


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description="Music Recommender Simulation")
    parser.add_argument(
        "--mode",
        choices=list(RANKING_MODES),
        default="balanced",
        help="ranking mode: "
        + "; ".join(f"{m.name} = {m.description}" for m in RANKING_MODES.values()),
    )
    return parser.parse_args()


def main() -> None:
    mode = RANKING_MODES[parse_args().mode]
    songs = load_songs("data/songs.csv")

    print(f"Loaded songs: {len(songs)}\n")

    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(
            user_prefs, songs, k=5, scorer=mode.scorer, key=mode.key
        )
        print_recommendations(name, recommendations, mode.name)


if __name__ == "__main__":
    main()
