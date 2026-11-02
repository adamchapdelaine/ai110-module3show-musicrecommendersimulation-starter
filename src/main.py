"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from src.recommender import load_songs, recommend_songs

PROFILES = {
    "Intense Rock": {
        "genre": "rock", "mood": "intense", "energy": 0.92, "valence": 0.45,
        "acousticness": 0.10, "tempo_bpm": 150, "danceability": 0.50,
        "instrumentalness": 0.05, "popularity": 0.60,
    },
    "Chill Lofi": {
        "genre": "lofi", "mood": "chill", "energy": 0.38, "valence": 0.58,
        "acousticness": 0.80, "tempo_bpm": 76, "danceability": 0.60,
        "instrumentalness": 0.88, "popularity": 0.50,
    },
    "High-Energy Pop": {
        "genre": "pop", "mood": "happy", "energy": 0.88, "valence": 0.85,
        "acousticness": 0.12, "tempo_bpm": 128, "danceability": 0.85,
        "instrumentalness": 0.02, "popularity": 0.90,
    },
    "Mellow Jazz": {
        "genre": "jazz", "mood": "relaxed", "energy": 0.30, "valence": 0.65,
        "acousticness": 0.92, "tempo_bpm": 90, "danceability": 0.45,
        "instrumentalness": 0.60, "popularity": 0.35,
    },
    "Sad Banger": {
        "genre": "pop", "mood": "melancholic", "energy": 0.80, "valence": 0.20,
        "acousticness": 0.15, "tempo_bpm": 120, "danceability": 0.80,
        "instrumentalness": 0.02, "popularity": 0.80,
    },
    "Upbeat Jazz": {
        "genre": "jazz", "mood": "upbeat", "energy": 0.78, "valence": 0.85,
        "acousticness": 0.60, "tempo_bpm": 105, "danceability": 0.85,
        "instrumentalness": 0.30, "popularity": 0.55,
    },
    "Instrumental Hype": {
        "mood": "intense", "energy": 0.92, "valence": 0.35,
        "acousticness": 0.05, "tempo_bpm": 135, "danceability": 0.70,
        "instrumentalness": 0.90, "popularity": 0.45,
    },
}

WIDTH = 60
BAR_LEN = 20


def score_bar(score: float) -> str:
    filled = round(score * BAR_LEN)
    return "█" * filled + "░" * (BAR_LEN - filled)


def print_recommendations(name: str, recommendations: list) -> None:
    print("=" * WIDTH)
    print(f" {name}".upper())
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


def main() -> None:
    songs = load_songs("data/songs.csv")

    print(f"Loaded songs: {len(songs)}\n")

    for name, user_prefs in PROFILES.items():
        recommendations = recommend_songs(user_prefs, songs, k=5)
        print_recommendations(name, recommendations)


if __name__ == "__main__":
    main()
