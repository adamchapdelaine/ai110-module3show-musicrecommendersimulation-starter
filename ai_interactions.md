# AI Interactions Log

> **Stretch features only.** Only fill in the sections that apply to stretch features you attempted. If you did not attempt a stretch feature, leave its section blank or delete it. This file is not required for the core project.

---

## Agentic Workflow (SF8)

> Document your experience using an AI agent (e.g., Cursor Agent, Claude, Copilot) to make multi-step changes autonomously.

**What task did you give the agent?**

<!-- Describe the goal you asked the agent to accomplish -->
Note: I'm not sure if this is referring to automated Claude tasks or just a short summary of what I asked the agent to do in my prompts.

I instructed the agent to suggest four additional complex features for my dataset, implement them, and guide me while I made manual edits to verify if the changes were working correctly.

**Prompts used:**

<!-- Paste the key prompts you gave the agent -->

 "@data/songs.csv  Suggest four additional complex attributes that are not currently present in the baseline data. See if you can identify attributes that would further increase the accuracy of the model."

 "@data/songs.csv @src/recommender.py Update songs.csv with the following features, and assign appropriate values: mood_tags, loudness_db, language, activity_fit, release_decade.
 
 Then, in src/recommender.py, add these features into the WEIGHTS dictionary and adjust the point distribution to prioritize genre, energy, and mood while keeping the sum of all feature weights is 1.0. Include these new features in the dataclasses Song and UserProfile. Lastly, update the scoring logic to accommodate these new features. Make sure to update load_songs, score_song, and recommend_songs.
 
 For each function, write a brief up-to-date docstring that reflects their current logic."
 
 "@data/songs.csv @src/recommender.py @src/main.py Update PROFILES in main.py to include the new features mood_tags, loudness_db, language, activity_fit, release_decade. Ensure the keys are assigned an appropriate value in the correct data type."

 "@src/recommender.py  I noticed that songs that receive a mood bonus also gain a mood_tag bonus, but I only want the mood_tag bonus to apply when there isn't an exact mood match. Can you give me a suggestion on how and where to implement a change that fixes this in recommender.py?"

**What did the agent generate or change?**

<!-- List the files edited, code generated, or commands run -->

The agent changed songs.csv, main.py, and recommender.py.

**What did you verify or fix manually?**

<!-- Describe anything the agent got wrong or that required human review -->

I ran python -m src.main to check the output, and noticed that the AI implemented mood_tags in such a way that a song with an exact mood match would gain +0.15 for the mood match AND +0.10 for a matching mood_tag, when mood_tag's purpose was to be a fallback for similar moods in case there wasn't an exact match. I implemented the fix manually, but consulted AI for suggestions while doing so.

---

## Design Pattern (SF10)

> Document how AI helped you choose or implement a design pattern.

**Which design pattern did you use?**

<!-- e.g., Strategy, Factory, Observer, etc. -->

I used the Strategy design pattern.

**How did AI help you brainstorm or implement it?**

<!-- Describe the conversation or suggestions that led to your decision -->

Note: I'm very new to design patterns, so I had to defer to AI more than usual this time.

Initial prompt:

 Brainstorm a design pattern that would keep my code in recommender.py modular. What design pattern would be most appropriate for this file? Justify why. Then, explain how you would implement it if you were me.

AI justification:
- score_song is an if/elif ladder, and each new feature type requires that function to be modified. This violates the open/closed principles.
- The "kind of a feature is spread across four sets. A feature's type is implied by which set it appears in, plus a WEIGHTS entry. Strategy puts that knowledge in a single place.
- The branches are interchangeable. Each one takes (target, song_value) and returns a 0-1 score plus a label. This is well-suited for Strategy.
- Each strategy becomes testable alone. Currently, you can only test the formulas by calling all of score_song.
- It lines up with your experiments. With Strategy, each fine-tuning of a formula or adding a small feature touches one small class.

I then worked with AI to implement this. Instead of implementing Genre-First and then branching off with Mood-First, I made a separate branch after refactoring the already existing code to fit the Strategy design pattern with the help of AI. I also restored functionality of the Recommender class and set up additional tests in test_recommender.py to test the changes that were made. This was especially important due to my knowledge gaps, a manual review over each granular part of the code would have taken at least a full day.

**How does the pattern appear in your final code?**

<!-- Point to the relevant class or method -->

The Strategy pattern appears in these cases:

1. Each feature type has its own scoring strategy class  in recommender.py (ExactMatch, Jaccard, ScaledDistance, etc).
2. A whole scorer can be swapped, because recommend_songs and Recommender take a scorer argument, and make_scorer builds variants with different weights. 
3. Ordering can be swapped through the key argument, as in genre_first_key. The RANKING_MODES registry bundles these into named modes, and main.py --mode selects one at runtime. This allows Genre-First, Mood-First, and Balanced all run through the same call: recommend_songs.