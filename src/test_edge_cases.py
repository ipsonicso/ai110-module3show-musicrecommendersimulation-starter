"""
Test edge cases for the music recommender system.
Tests unusual user preferences and how the system handles them.
"""

from recommender import load_songs, recommend_songs, UserProfile, Recommender, Song

def test_case_1_high_energy_sad():
    """Edge case: User wants high-energy but sad/intense mood (e.g., angry workout music)"""
    print("=" * 70)
    print("TEST CASE 1: High Energy + Intense Mood (Angry Workout Music)")
    print("=" * 70)

    songs = load_songs("data/songs.csv")
    user_prefs = {
        'genre': 'rock',
        'mood': 'intense',
        'energy': 0.90,  # Very high energy
        'likes_acoustic': False,
    }

    print(f"\nUser Profile: {user_prefs}\n")
    recommendations = recommend_songs(user_prefs, songs, k=5)

    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"{i}. {song['title']} - Score: {score:.2f}")
        print(f"   {explanation}\n")


def test_case_2_acoustic_chill():
    """Edge case: User wants acoustic AND chill mood (relaxing acoustic music)""" #note, this is NOT an edge case...
    print("=" * 70)
    print("TEST CASE 2: Acoustic + Chill Mood (Relaxing Acoustic)")
    print("=" * 70)

    songs = load_songs("data/songs.csv")
    user_prefs = {
        'genre': 'jazz',
        'mood': 'relaxed',
        'energy': 0.30,  # Very low energy
        'likes_acoustic': True,  # Wants acoustic
    }

    print(f"\nUser Profile: {user_prefs}\n")
    recommendations = recommend_songs(user_prefs, songs, k=5)

    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"{i}. {song['title']} - Score: {score:.2f}")
        print(f"   {explanation}\n")


def test_case_3_electronic_happy():
    """Edge case: User wants electronic upbeat/happy (energetic electronic dance)"""
    print("=" * 70)
    print("TEST CASE 3: Electronic + Happy + High Energy (Dance Music)")
    print("=" * 70)

    songs = load_songs("data/songs.csv")
    user_prefs = {
        'genre': 'electronic',
        'mood': 'happy',
        'energy': 0.95,  # Maximum energy
        'likes_acoustic': False,
    }

    print(f"\nUser Profile: {user_prefs}\n")
    recommendations = recommend_songs(user_prefs, songs, k=5)

    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"{i}. {song['title']} - Score: {score:.2f}")
        print(f"   {explanation}\n")


def test_case_4_niche_combo():
    """Edge case: Very specific niche preference that may not exist in catalog"""
    print("=" * 70)
    print("TEST CASE 4: Niche Combo - Ambient + Intense + High Energy")
    print("=" * 70)

    songs = load_songs("data/songs.csv")
    user_prefs = {
        'genre': 'ambient',  # Usually calm
        'mood': 'intense',   # But wants intense (contradiction)
        'energy': 0.85,      # High energy (unusual for ambient)
        'likes_acoustic': True,
    }

    print(f"\nUser Profile: {user_prefs}")
    print("NOTE: This is a contradictory preference - ambient is usually low energy/chill\n")
    recommendations = recommend_songs(user_prefs, songs, k=5)

    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"{i}. {song['title']} - Score: {score:.2f}")
        print(f"   {explanation}\n")


def test_case_5_oop_edge_case():
    """Test OOP implementation with edge case"""
    print("=" * 70)
    print("TEST CASE 5: OOP Implementation - Moody Electronic (Synthwave)")
    print("=" * 70)

    # Create Song objects from CSV
    csv_songs = load_songs("data/songs.csv")
    songs = [
        Song(
            id=s['id'],
            title=s['title'],
            artist=s['artist'],
            genre=s['genre'],
            mood=s['mood'],
            energy=s['energy'],
            tempo_bpm=s['tempo_bpm'],
            valence=s['valence'],
            danceability=s['danceability'],
            acousticness=s['acousticness'],
        )
        for s in csv_songs
    ]

    # Create recommender
    recommender = Recommender(songs)

    # Create user profile with unusual preference
    user = UserProfile(
        favorite_genre='synthwave',
        favorite_mood='moody',
        target_energy=0.75,
        likes_acoustic=False,
    )

    print(f"\nUser Profile:")
    print(f"  Genre: {user.favorite_genre}")
    print(f"  Mood: {user.favorite_mood}")
    print(f"  Target Energy: {user.target_energy}")
    print(f"  Likes Acoustic: {user.likes_acoustic}\n")

    recommendations = recommender.recommend(user, k=5)

    for i, song in enumerate(recommendations, 1):
        explanation = recommender.explain_recommendation(user, song)
        score = _calculate_score(user, song, recommender)
        print(f"{i}. {song.title} - Score: {score:.2f}")
        print(f"   {explanation}\n")


def _calculate_score(user, song, recommender):
    """Helper to calculate score for OOP version"""
    from recommender import _get_component_scores
    user_prefs = {
        'genre': user.favorite_genre,
        'mood': user.favorite_mood,
        'energy': user.target_energy,
        'likes_acoustic': user.likes_acoustic,
    }
    song_dict = {
        'genre': song.genre,
        'mood': song.mood,
        'energy': song.energy,
        'acousticness': song.acousticness,
    }
    components = _get_component_scores(user_prefs, song_dict)
    return components['total']


def test_case_6_all_genre_mismatches():
    """Edge case: User wants a genre that doesn't exist in the catalog"""
    print("=" * 70)
    print("TEST CASE 6: Genre Not in Catalog (Metal Music)")
    print("=" * 70)

    songs = load_songs("data/songs.csv")
    user_prefs = {
        'genre': 'metal',  # NOT in our catalog
        'mood': 'intense',
        'energy': 0.95,
        'likes_acoustic': False,
    }

    print(f"\nUser Profile: {user_prefs}")
    print("NOTE: 'metal' genre doesn't exist in our catalog\n")
    recommendations = recommend_songs(user_prefs, songs, k=5)

    for i, (song, score, explanation) in enumerate(recommendations, 1):
        print(f"{i}. {song['title']} - Score: {score:.2f}")
        print(f"   {explanation}\n")
        print(f"   (Note: No genre match since 'metal' not in catalog)\n")


if __name__ == "__main__":
    test_case_1_high_energy_sad()
    test_case_2_acoustic_chill()
    test_case_3_electronic_happy()
    test_case_4_niche_combo()
    test_case_5_oop_edge_case()
    test_case_6_all_genre_mismatches()

    print("\n" + "=" * 70)
    print("All edge case tests completed!")
    print("=" * 70)
