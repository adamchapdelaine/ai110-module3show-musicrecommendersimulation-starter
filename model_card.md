# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  
Example: **VibeFinder 1.0**  

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate  
- What assumptions does it make about the user  
- Is this for real users or classroom exploration  

---

## 3. How the Model Works  

The features of each song used are:
- Its Genre
- Mood
- Energy
- Tempo in beats-per-minute
- Valence
- Danceability
- Acousticness
- Instrumentalness
- Popularity

The user preferences considered are:
- Favorite Genres
- Favorite Moods
- Target energy
- Target valence
- Target acousticness
- Target tempo
- Target danceability
- Target instrumentalness
- Target popularity

How does the model turn these into a score?:
THe model first assigns a weight to each song feature, which prioritizes some over others as the most important distinguishing features of a song. Then, it scores a feature based upon its closeness to the user preference for it, and multiplies that score by the weight of that feature to normalize it to a fraction of 1, 1 being the highest possible score.  

Changes I made from the starter logic:
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

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset  

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  

---

## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  
