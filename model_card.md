# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

**MusiMe 0.1.0** 

---

## 2. Intended Use  

MusiMe is a content-based music recommender. Give a user's taste profile, it'll rank every song in a small CSV catalog and return the top k (5 by default). Each result comes with a similarity score from 0 to 1 and a short "Reasons" string to justify scoring decisions. It lists features that matched closely like "mood match," and flags a genre mismatch penalty when one applies.

**What it recommends:** Songs from the catalog whose attributes are numerically close to the user's stated preferences. It scores genre, mood, energy, valence, acousticness, tempo, danceability, instrumentallness and popularity. Energy and mood carry the most weight out of all of them. It doesn't recommend based on listening history, other users' behavior or lyrics.

**Assumptions about the user:**
- The user can state their taste up front, explicitly identifying their favorite genres and moods as well as setting optional numeric targets like energy or tempo.
- Taste is stable and rigid to a single "ideal." People who enjoy mixed playlists are not accounted for.
- The user doesn't seek novelty, as the model has no means of deviating from its scoring system to suggest anything new.
- Unset preferences don't matter to the user, as they are skipped rather than guessed.

**Who or what is this for?:** 
This is for classroom exploration only. The catalog is tiny, most genres have one or two songs, and the moods skew towards happy and upbeat. The example profiles are test cases rather than real people or approximations of a person's varied tastes. The project is meant for studying how a weighted scoring recommender works conceptually, and to practice documenting systems using a Model Card.

---

## 3. How the Model Works  

**The features of each song used are:**
- Its Genre
- Mood
- Energy
- Tempo in beats-per-minute
- Valence
- Danceability
- Acousticness
- Instrumentalness
- Popularity

**The user preferences considered are:**
- Favorite Genres
- Favorite Moods
- Target energy
- Target valence
- Target acousticness
- Target tempo
- Target danceability
- Target instrumentalness
- Target popularity

**How does the model turn these into a score?:**
THe model first assigns a weight to each song feature, which prioritizes some over others as the most important distinguishing features of a song. Then, it scores a feature based upon its closeness to the user preference for it, and multiplies that score by the weight of that feature to normalize it to a fraction of 1, 1 being the highest possible score.  

**Changes I made from the starter logic:**
- The pipeline for load_songs, score_song, and recommend_songs was implemented.
- Songs are now loaded from a CSV, turning numeric columns into numbers for scoring.
- I added instrumentalness and popularity as new song features
- The user profile is richer, allowing the user to input lists of favorite genres and moods alongside (optional) additional targets for features like energy, valence, acousticness, tempo, and others for the occasional power user.
- A weighted scoring model was added, which combines the weighted scores of each feature to a "similarity score" from 0 to 1.
- Missing preferences are skipped, so a user doesn't need to set all targets to get song recommendations. This is achieved by dividing the final score by the combined weight of the features the user did set.
- Added explanations for any feature that scores 0.7 or higher, which displays in the output under "Reasons."
- Every song put into a ranking, which is sorted from highest to lowest. Only the top k songs are listed in the output.
- I replaced the sample profile in main.py with three test profiles: Intense Rock, Chill Lofi, and a deliberately conflicting one (high energy plus acoustic) to test the limits of my scoring algorithm.

---

## 4. Data  

There are 49 songs in the dataset, and over 30 genres. Some genres are very similar to one another but aren't merged together or given bonuses for similarity, so they aren't considered properly in the scoring.

I added most of the songs in this dataset, as well as the instrumentalness and popularity features.

---

## 5. Strengths  

This system works well for users who like high energy pop songs or lofi, as those are the two niches best represented in the song dataset.

The scoring is good at identifying songs of the desired energy level, due to how strongly it is weighted in recommender.py.

The recommendations matched my intuition most closely with the HIGH ENERGY POP and CHILL LOFI profiles.

---

## 6. Limitations and Bias 

Genre is exact-match, so users who look up "indie pop" instead of "pop" won't get any same-genre songs.

Only 3 of 31 genres have more than 2 songs, which over-prioritizes those genres compared to the more niche ones.

Mid-energy users get a weak signal, as there are only 8 songs within the energy band of 0.5 to 0.7. 

Happy playlists are over-prioritized compared to sad playlists, as are very few songs fitting a "sad" or "melancholic" mood and far more with happy or upbeat moods.

---

## 7. Evaluation  

**I tested the following user profiles:**
- INTENSE ROCK
- CHILL LOFI
- HIGH-ENERGY POP
- MELLOW JAZZ
- SAD BANGER
- UPBEAT JAZZ
- INSTRUMENTAL HYPE

In the recommendations, I looked for same-genre songs as well as songs with matching moods or energy, as those three categories are the most important characteristics of the scoring algorithm.

**Profile Evaluation:**
- INTENSE ROCK profile prefers high energy songs with "intense" mood; CHILL LOFI prefers low energy songs with a "chill" mood.
    - Output for INTENSE ROCK profile doesn't make sense, due to including a pop song in it's top 3. CHILL LOFI's output does make sense, especially with the fact it lists 3 same-genre songs with a similar energy level.
- HIGH-ENERGY POP prefers high energy, upbeat songs; MELLOW JAZZ prefers low energy songs with high acousticness.
    - Output for HIGH-ENERGY POP makes sense, with non-pop songs being from similar genres such as k-pop. Output for MELLOW JAZZ is flawed due to the lack of jazz songs.
- SAD BANGER prefers high energy pop songs with low valence; UPBEAT JAZZ prefers high energy, high valence jazz songs.
    - Output for SAD BANGER  doesn't make sense due to amount of upbeat songs, but the output for UPBEAT JAZZ matches the intended vibe (in spite of the lack of Jazz songs).
- INSTRUMENTAL HYPE prefers high energy, "intense" mood songs.
    - Output doesn't make sense, because first recommendation is a traditional rock song rather than an "instrumental" song.

**What surprised me about the results:**
- The overrepresentation of Gym Hero - Max Pulse in 4 out of the 7 user profiles.
- How few same-genre songs there were for each user profile.
- The lack of melancholic songs, leading to a "happy" song, Sunrise City - Neon Echo, being listed as #1 for SAD BANGER.
---

## 8. Future Work  

**How I would improve the model next:**
- Emphasize genre more strongly in the weights.
- Consolidating genres and adding the capability for similar genres to be clustered together so similar genres may be scored favorably.
- Consolidating moods in a similar fashion to the idea above.
- Add a rule or MMR that limits the same artists and genres from filling the entire recommendation so that the user can receive at least one "stretch" suggestion.

---

## 9. Personal Reflection  

**What was my biggest learning moment during this project?:**
The most significant thing I learnt during this project was how to implement a content-based filtering system for scoring songs. I also learnt about the amount of work and fine-tuning that goes into a very basic simulation of a music recommender. 

**How did using AI tools help me, and when did I need to double-check them?:**
The use of AI tools helped me primarily with understanding the pre-existing logic of files such as main.py and recommender.py. It also helped critique my design choices, produce user profiles, and fill songs.csv with more variety.

**What surprised me about how simple algorithms can still "feel" like recommendations?:**
I was surprised by how such an impersonal algorithm could produce relatively accurate recommendations. It was just a matter of assigning arbitrary weights to a modest list of numerical representations of song features, and the model manipulated those numeric values into tailored recommendations. I wonder if more sophisticated recommendation algorithms like the one used for Youtube or Spotify incorporate elements of this simple project in their own algorithms.

**What would I try next if I extended this project?:**
If I were to extend this project, I would do the following:
- Add Advanced Song Features
- Create Multiple Scoring Modes
- Implement Diversity and Fairness Logic
- Add a Visual Summary Table
