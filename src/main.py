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
    "Conflicting (high energy + acoustic)": {
        "genre": "folk", "mood": "wistful", "energy": 0.90,
        "acousticness": 0.90, "tempo_bpm": 140,
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
