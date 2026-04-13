# 🎧 Model Card: Music Recommender Simulation

## 1. Model Name  

Give your model a short, descriptive name.  

# Taste Tuner

---

## 2. Intended Use  

Describe what your recommender is designed to do and who it is for. 

Prompts:  

- What kind of recommendations does it generate     X
- What assumptions does it make about the user      X
- Is this for real users or classroom exploration   X

> A song is defined by id,title,artist,genre,mood,energy,tempo_bpm,valence,danceability,acousticness.
> The model uses user profile for preferences in mood, genre, energy, and acousticness to compare to song.csv weighed on a scale of 0.0 to 0.1 match. 
> The model suggests the top 5 songs, ranked by relevance to that taste profile.
> This model is limited and for classroom exploration only.

---

## 3. How the Model Works  

Explain your scoring approach in simple language.  

Prompts:  
- What features of each song are used (genre, energy, mood, etc.)  
- What user preferences are considered  
- How does the model turn those into a score  
- What changes did you make from the starter logic  
Avoid code here. Pretend you are explaining the idea to a friend who does not program.

> The model uses Mood, Genre, Energy, and BPM primarily (in that order) to  
> Adding up to 1.0
> score = 
>   (genre_match * 0.4) +           # Most important
>   (mood_match * 0.3) +            # Very important
>   (1 - |energy_distance| * 0.2) + # Continuous tuning
>   (acoustic_match * 0.1)          # Tiebreaker

---

## 4. Data  

Describe the dataset the model uses.  

Prompts:  

- How many songs are in the catalog  
- What genres or moods are represented  
- Did you add or remove data  
- Are there parts of musical taste missing in the dataset

> The model is based on a catalog of 20 songs
> There are 9 unique genres, with pop and lofi having the most repeats (4).
> There are 6 unique moods, with moody and focused having the fewest repeats (2, compared to the rest having 4).

---

## 5. Strengths  

Where does your system seem to work well  

Prompts:  

- User types for which it gives reasonable results  
- Any patterns you think your scoring captures correctly  
- Cases where the recommendations matched your intuition  

---
> Successfully ranks the top results.
> Successfully matches mood and genre preference above all else.

## 6. Limitations and Bias 

Where the system struggles or behaves unfairly. 

Prompts:  

- Features it does not consider  
- Genres or moods that are underrepresented  
- Cases where the system overfits to one preference  
- Ways the scoring might unintentionally favor some users  


> The metadata it currently draws is limited. It's from can't take into account language and lyrics, year, bands vs artists, or 
> The model doesn't consider genres close to each other yet, so "indie pop" results as 0% match to "pop."
> So, less specific genres will be more common, but may be less common than they are overall because the subgenres are not considered related.

---

## 7. Evaluation  

How you checked whether the recommender behaved as expected. 

Prompts:  

- Which user profiles you tested  
- What you looked for in the recommendations  
- What surprised you  
- Any simple tests or comparisons you ran  

No need for numeric metrics unless you created some.

> After 10 tests, pop + happy songs were most recommended.
>   Sunrise City was overrecommended the most because its energy level was about in the middle, even if the genre and mood didn't match.
> One genre I tried was chill pop, which surprisingly only had as high as a 61% match, a sign the selection wasn't wide enough

---

## 8. Future Work  

Ideas for how you would improve the model next.  

Prompts:  

- Additional features or preferences  
- Better ways to explain recommendations  
- Improving diversity among the top results  
- Handling more complex user tastes  


> A potential future model expanded for real users would include user intake information for preferred genre, mood, BPM or corresponding high/medium/low tempo, energy, and acousticness.
>   Model will allow user to build up a user taste profile through likes/dislikes and skips.
>   Model will connect related genres, artists, moods, etc. through LLM language analysis or other users' listening patterns on a larger scale.
>   Built-in matching based on other factors (such as a workout recommender based on BPM or Mood playlist based on genres,artists user has already liked in that mood)
>   (Copilot suggestion) IDF-style downweighting, so common genres contribute a little less than rarer ones.

---
## 9. Personal Reflection  

A few sentences about your experience.  

Prompts:  

- What you learned about recommender systems  
- Something unexpected or interesting you discovered  
- How this changed the way you think about music recommendation apps  

> Considering how I only used the 4 most relevant categories from a system with only 10, I think bigger platforms must involve very complex algorithms with a lot of alternating parts (especially for songs with more or less information) in their recommendations, and I wonder how they account for missing and moving parts.
> I thought about music recommenders like Spotify that categorize and recategorize all your listening tastes in their yearly Wrapped, assigning a super specific genre <https://artists.spotify.com/blog/how-spotify-discovers-the-genres-of-tomorrow> 
> I wonder how similar the earliest music recommender or the earliest version of Spotify would look to my simple program, and what I can do to bridge the gap to that version if I choose to continue this project.
