# 🎵 Music Recommender Simulation

## Project Summary

Real-world recommendations work by utilizing a hybrid scoring approach that combines collaborative filtering and content-based filtering. Collaborative filtering scores songs based on user behavior at scale. Content-based filtering scores individual songs based on descriptive features and metadata of those songs, and how close those align with what a user seems to like. Songs are then ranked amongst each other based on their scores to determine what songs to recommend and in which order. 

My version will rely on content-based filtering for scoring songs, prioritizing the attributes that most strongly distinguish songs such as energy, mood, valence, and acousticness. 

---

## How The System Works

Explain your design in plain language.

Some prompts to answer:

- What features does each `Song` use in your system
  - For example: genre, mood, energy, tempo
- What information does your `UserProfile` store
- How does your `Recommender` compute a score for each song
- How do you choose which songs to recommend

You can include a simple diagram or bullet list if helpful.

### Algorithm Recipe

Features each `Song` uses in my system:
-   genre
-   mood
-   energy
-   tempo_bpm
-   valence
-   danceability
-   acousticness
-   instrumentalness
-   popularity

My `UserProfile` stores the following information:
-   genre
-   mood
-   energy
-   tempo_bpm
-   valence
-   danceability
-   acousticness
-   instrumentalness
-   popularity

How does `Recommender` compute a score for each song?:
- Score each feature from 0 to 1.
  - Genre and mood are binary: 1.0 on a match,
    0.0 otherwise.
  - Numeric features use proximity: 1 - abs(song -  
    target). Tempo divides the difference by        TEMPO_RANGE and clamps to [0, 1].
- Multiply the score by that feature's weight and 
  add it to a running total.
- Skip features the user didn't set (None targets)
- Divide by the sum of the weights that were used.
- Record a reason for every feature that scored   
  well.

Potential biases I expect:
- Energy and valence are dominant, so songs with  
  extreme values may score poorly while songs with moderate values will show up for almost everybody -- regardless of other features.
- Weights encode my assumptions, not the user's. 
  Everybody gets the same weights, but some features (like genre, or energy) are more important to some people than others.
- The catalog is thin, and the genre weight favors 
  the genre above almost everything else. Song recommendations from more niche genres will not be tailored as effectively to the user as mainstream genres would.
---

## Getting Started

### Setup

1. Create a virtual environment (optional but recommended):

   ```bash
   python -m venv .venv
   source .venv/bin/activate      # Mac or Linux
   .venv\Scripts\activate         # Windows

2. Install dependencies

```bash
pip install -r requirements.txt
```

3. Run the app:

```bash
python -m src.main
```

### Running Tests

Run the starter tests with:

```bash
pytest
```

You can add more tests in `tests/test_recommender.py`.

---

## Sample Recommendation Output

```
Loaded songs: 49

============================================================
 INTENSE ROCK
============================================================

1. Storm Runner  —  Voltline
   Score: 0.99  ████████████████████
   Reasons:
     • genre match (+0.20)
     • energy close (+0.20)
     • mood match (+0.17)
     • valence close (+0.13)
     • acousticness close (+0.10)
     • tempo_bpm close (+0.06)
     • danceability close (+0.05)
     • instrumentalness close (+0.05)
     • popularity close (+0.04)
------------------------------------------------------------

2. Gym Hero  —  Max Pulse
   Score: 0.71  ██████████████░░░░░░
   Reasons:
     • energy close (+0.20)
     • mood match (+0.17)
     • acousticness close (+0.10)
     • tempo_bpm close (+0.05)
     • instrumentalness close (+0.05)
     • popularity close (+0.03)
------------------------------------------------------------

3. Burn the Map  —  Static Riot
   Score: 0.58  ████████████░░░░░░░░
   Reasons:
     • energy close (+0.20)
     • valence close (+0.12)
     • acousticness close (+0.10)
     • tempo_bpm close (+0.05)
     • danceability close (+0.04)
     • instrumentalness close (+0.05)
     • popularity close (+0.03)
------------------------------------------------------------

4. Iron Requiem  —  Black Cathedral
   Score: 0.57  ███████████░░░░░░░░░
   Reasons:
     • energy close (+0.19)
     • valence close (+0.10)
     • acousticness close (+0.09)
     • tempo_bpm close (+0.05)
     • danceability close (+0.05)
     • instrumentalness close (+0.05)
     • popularity close (+0.04)
------------------------------------------------------------

5. Basement Show  —  Rusty Halo
   Score: 0.57  ███████████░░░░░░░░░
   Reasons:
     • energy close (+0.19)
     • valence close (+0.11)
     • acousticness close (+0.10)
     • tempo_bpm close (+0.04)
     • danceability close (+0.04)
     • instrumentalness close (+0.05)
     • popularity close (+0.03)
------------------------------------------------------------

============================================================
 CHILL LOFI
============================================================

1. Library Rain  —  Paper Lanterns
   Score: 0.98  ████████████████████
   Reasons:
     • genre match (+0.20)
     • energy close (+0.19)
     • mood match (+0.17)
     • valence close (+0.13)
     • acousticness close (+0.09)
     • tempo_bpm close (+0.06)
     • danceability close (+0.05)
     • instrumentalness close (+0.05)
     • popularity close (+0.04)
------------------------------------------------------------

2. Midnight Coding  —  LoRoom
   Score: 0.97  ███████████████████░
   Reasons:
     • genre match (+0.20)
     • energy close (+0.19)
     • mood match (+0.17)
     • valence close (+0.13)
     • acousticness close (+0.09)
     • tempo_bpm close (+0.06)
     • danceability close (+0.05)
     • instrumentalness close (+0.05)
     • popularity close (+0.04)
------------------------------------------------------------

3. Focus Flow  —  LoRoom
   Score: 0.82  ████████████████░░░░
   Reasons:
     • genre match (+0.20)
     • energy close (+0.20)
     • valence close (+0.13)
     • acousticness close (+0.10)
     • tempo_bpm close (+0.06)
     • danceability close (+0.05)
     • instrumentalness close (+0.05)
     • popularity close (+0.04)
------------------------------------------------------------

4. Spacewalk Thoughts  —  Orbit Bloom
   Score: 0.72  ██████████████░░░░░░
   Reasons:
     • energy close (+0.18)
     • mood match (+0.17)
     • valence close (+0.12)
     • acousticness close (+0.09)
     • tempo_bpm close (+0.05)
     • instrumentalness close (+0.05)
     • popularity close (+0.03)
------------------------------------------------------------

5. Coffee Shop Stories  —  Slow Stereo
   Score: 0.58  ████████████░░░░░░░░
   Reasons:
     • energy close (+0.20)
     • valence close (+0.11)
     • acousticness close (+0.09)
     • tempo_bpm close (+0.05)
     • danceability close (+0.05)
     • instrumentalness close (+0.04)
     • popularity close (+0.04)
------------------------------------------------------------
```

**Screenshot or video** *(optional)*: <!-- Insert a screenshot or demo video link here -->

---

## Experiments You Tried

Use this section to document the experiments you ran. For example:

- What happened when you changed the weight on genre from 2.0 to 0.5
- What happened when you added tempo or valence to the score
- How did your system behave for different types of users

---

## Limitations and Risks

Summarize some limitations of your recommender.

Examples:

- It only works on a tiny catalog
- It does not understand lyrics or language
- It might over favor one genre or mood

You will go deeper on this in your model card.

---

## Reflection

Read and complete `model_card.md`:

[**Model Card**](model_card.md)

Write 1 to 2 paragraphs here about what you learned:

- about how recommenders turn data into predictions
- about where bias or unfairness could show up in systems like this



