"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs

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

def main() -> None:
    songs = load_songs("data/songs.csv") 

    user_prefs = {}
    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\nTop recommendations:\n")
    for rec in recommendations:
        # You decide the structure of each returned item.
        # A common pattern is: (song, score, explanation)
        song, score, explanation = rec
        print(f"{song['title']} - Score: {score:.2f}")
        print(f"Because: {explanation}")
        print()


if __name__ == "__main__":
    main()
