from typing import List, Dict, Tuple, Optional
from dataclasses import dataclass
import csv

@dataclass
class Song:
    """
    Represents a song and its attributes.
    Required by tests/test_recommender.py
    """
    id: int
    title: str
    artist: str
    genre: str
    mood: str
    energy: float
    tempo_bpm: float
    valence: float
    danceability: float
    acousticness: float

@dataclass
class UserProfile:
    """
    Represents a user's taste preferences.
    Required by tests/test_recommender.py
    """
    favorite_genre: str
    favorite_mood: str
    target_energy: float
    likes_acoustic: bool

class Recommender:
    """
    OOP implementation of the recommendation logic.
    Required by tests/test_recommender.py
    """
    def __init__(self, songs: List[Song]):
        self.songs = songs

    def recommend(self, user: UserProfile, k: int = 5) -> List[Song]:
        """
        Recommend songs based on user profile.
        Returns top k songs sorted by recommendation score (highest first).
        """
        # Convert Song objects to dicts for scoring
        user_prefs = {
            'genre': user.favorite_genre,
            'mood': user.favorite_mood,
            'energy': user.target_energy,
            'likes_acoustic': user.likes_acoustic,
        }

        # Score each song
        scored_songs = []
        for song in self.songs:
            song_dict = {
                'energy': song.energy,
                'mood': song.mood,
                'genre': song.genre,
                'acousticness': song.acousticness,
            }
            score = _score_song(user_prefs, song_dict)
            scored_songs.append((song, score))

        # Sort by score descending
        scored_songs.sort(key=lambda x: x[1], reverse=True)

        # Return top k songs
        return [song for song, score in scored_songs[:k]]

    def explain_recommendation(self, user: UserProfile, song: Song) -> str:
        """
        Generate a natural language explanation for why a song was recommended.
        """
        factors = []

        # Check mood match
        if song.mood == user.favorite_mood:
            factors.append(f"{song.mood} mood matches your preference")

        # Check genre match
        if song.genre == user.favorite_genre:
            factors.append(f"{song.genre} genre matches your preference")

        # Check energy proximity
        energy_distance = abs(song.energy - user.target_energy)
        if energy_distance < 0.15:
            factors.append(f"energy level is aligned with your target")

        # Check acoustic preference
        is_acoustic = song.acousticness > 0.5
        if is_acoustic == user.likes_acoustic:
            acoustic_pref = "acoustic" if user.likes_acoustic else "non-acoustic"
            factors.append(f"has the {acoustic_pref} quality you prefer")

        if factors:
            explanation = "Matches: " + ", ".join(factors)
        else:
            explanation = "Closest match based on audio characteristics"

        return explanation

def load_songs(csv_path: str) -> List[Dict]:
    """
    Loads songs from a CSV file.
    Required by src/main.py
    """
    songs = []
    with open(csv_path, 'r', encoding='utf-8') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Convert numeric fields to appropriate types
            song = {
                'id': int(row['id']),
                'title': row['title'],
                'artist': row['artist'],
                'genre': row['genre'],
                'mood': row['mood'],
                'energy': float(row['energy']),
                'tempo_bpm': float(row['tempo_bpm']),
                'valence': float(row['valence']),
                'danceability': float(row['danceability']),
                'acousticness': float(row['acousticness']),
            }
            songs.append(song)
    return songs

def _score_song(user_prefs: Dict, song: Dict) -> float:
    """
    Calculate recommendation score using mood-first metric.

    score = (mood_match × 0.40) +
            (genre_match × 0.30) +
            (1 - |energy_distance| × 0.20) +
            (acoustic_match × 0.10)

    Returns a score between 0 and 1.0 (higher is better).
    """
    # Mood match (0.40 weight) - primary filter
    mood_match = 1.0 if song['mood'] == user_prefs['mood'] else 0.0
    mood_score = mood_match * 0.40

    # Genre match (0.30 weight) - secondary filter
    genre_match = 1.0 if song['genre'] == user_prefs['genre'] else 0.0
    genre_score = genre_match * 0.30

    # Energy distance (0.20 weight) - fine-tuning
    energy_distance = abs(song['energy'] - user_prefs['energy'])
    energy_score = (1.0 - energy_distance) * 0.20

    # Acoustic match (0.10 weight) - tiebreaker
    is_acoustic = song['acousticness'] > 0.5
    user_likes_acoustic = user_prefs.get('likes_acoustic', False)
    acoustic_match = 1.0 if is_acoustic == user_likes_acoustic else 0.0
    acoustic_score = acoustic_match * 0.10

    return mood_score + genre_score + energy_score + acoustic_score


def _get_component_scores(user_prefs: Dict, song: Dict) -> Dict:
    """
    Calculate individual component scores for explanation purposes.
    Returns dict with mood, genre, energy, acoustic, and total scores.
    """
    # Mood match (0.40 weight)
    mood_match = 1.0 if song['mood'] == user_prefs['mood'] else 0.0
    mood_score = mood_match * 0.40

    # Genre match (0.30 weight)
    genre_match = 1.0 if song['genre'] == user_prefs['genre'] else 0.0
    genre_score = genre_match * 0.30

    # Energy distance (0.20 weight)
    energy_distance = abs(song['energy'] - user_prefs['energy'])
    energy_score = (1.0 - energy_distance) * 0.20

    # Acoustic match (0.10 weight)
    is_acoustic = song['acousticness'] > 0.5
    user_likes_acoustic = user_prefs.get('likes_acoustic', False)
    acoustic_match = 1.0 if is_acoustic == user_likes_acoustic else 0.0
    acoustic_score = acoustic_match * 0.10

    total_score = mood_score + genre_score + energy_score + acoustic_score

    return {
        'mood': mood_score,
        'genre': genre_score,
        'energy': energy_score,
        'acoustic': acoustic_score,
        'total': total_score,
    }


def recommend_songs(user_prefs: Dict, songs: List[Dict], k: int = 5) -> List[Tuple[Dict, float, str]]:
    """
    Functional implementation of the recommendation logic.
    Required by src/main.py
    """
    # Score all songs
    scored_songs = []
    for song in songs:
        score = _score_song(user_prefs, song)
        explanation = _explain_score(user_prefs, song, score)
        scored_songs.append((song, score, explanation))

    # Sort by score descending (highest first)
    scored_songs.sort(key=lambda x: x[1], reverse=True)

    # Return top k
    return scored_songs[:k]


def _explain_score(user_prefs: Dict, song: Dict, score: float) -> str:
    """Generate natural language explanation with component scores in bold parentheses."""
    components = _get_component_scores(user_prefs, song)
    factors = []

    # Check mood match
    if song['mood'] == user_prefs['mood']:
        factors.append(f"{song['mood']} mood matches (mood: {components['mood']:.2f})")

    # Check genre match
    if song['genre'] == user_prefs['genre']:
        factors.append(f"{song['genre']} genre matches (genre: {components['genre']:.2f})")

    # Check energy proximity
    energy_distance = abs(song['energy'] - user_prefs['energy'])
    if energy_distance < 0.15:
        factors.append(f"energy level is close to your preference (energy: {components['energy']:.2f})")

    # Check acoustic preference
    is_acoustic = song['acousticness'] > 0.5
    user_likes_acoustic = user_prefs.get('likes_acoustic', False)
    if is_acoustic == user_likes_acoustic:
        acoustic_pref = "acoustic" if user_likes_acoustic else "non-acoustic"
        factors.append(f"is {acoustic_pref} as you prefer (acoustic: {components['acoustic']:.2f})")

    if factors:
        explanation = "Because " + ", ".join(factors)
    else:
        explanation = "Closest match based on audio characteristics"

    return explanation

