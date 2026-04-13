"""
Comparison test: Mood weight 0.40 vs 0.25 vs 0.10
Shows how recommendations change as mood becomes less important
"""

from recommender import load_songs

def get_component_scores(user_prefs, song, mood_weight):
    """Calculate scores with variable mood weight"""
    mood_match = 1.0 if song['mood'] == user_prefs['mood'] else 0.0
    genre_match = 1.0 if song['genre'] == user_prefs['genre'] else 0.0
    energy_distance = abs(song['energy'] - user_prefs['energy'])
    is_acoustic = song['acousticness'] > 0.5
    acoustic_match = 1.0 if is_acoustic == user_prefs.get('likes_acoustic', False) else 0.0

    # Distribute remaining weight to energy and acoustic
    remaining = 1.0 - mood_weight - 0.30  # 0.30 fixed for genre
    energy_weight = remaining * 0.67  # Give ~2/3 to energy
    acoustic_weight = remaining * 0.33  # Give ~1/3 to acoustic

    return {
        'mood': mood_match * mood_weight,
        'genre': genre_match * 0.30,
        'energy': (1.0 - energy_distance) * energy_weight,
        'acoustic': acoustic_match * acoustic_weight,
    }


def score_song(user_prefs, song, mood_weight):
    """Calculate total score"""
    components = get_component_scores(user_prefs, song, mood_weight)
    return sum(components.values())


def compare_mood_weights(test_name, user_prefs, songs):
    """Compare recommendations across different mood weights"""
    print("\n" + "=" * 90)
    print(f"TEST: {test_name}")
    print("=" * 90)
    print(f"\nUser Profile:")
    print(f"  Genre: {user_prefs['genre']}")
    print(f"  Mood: {user_prefs['mood']}")
    print(f"  Energy: {user_prefs['energy']}")
    print(f"  Likes Acoustic: {user_prefs.get('likes_acoustic', False)}\n")

    # Score with all three weight configurations
    configs = [
        (0.40, "ORIGINAL (Mood 0.40, Genre 0.30, Energy 0.20, Acoustic 0.10)"),
        (0.25, "MODERATE (Mood 0.25, Genre 0.30, Energy 0.34, Acoustic 0.11)"),
        (0.10, "ENERGY-FIRST (Mood 0.10, Genre 0.30, Energy 0.46, Acoustic 0.14)"),
    ]

    scored_by_config = {}

    for mood_weight, label in configs:
        scored = []
        for song in songs:
            total_score = score_song(user_prefs, song, mood_weight)
            components = get_component_scores(user_prefs, song, mood_weight)
            scored.append((song, total_score, components))

        scored.sort(key=lambda x: x[1], reverse=True)
        scored_by_config[mood_weight] = scored

        # Display
        print(label)
        print("-" * 90)
        for i, (song, score, components) in enumerate(scored[:5], 1):
            print(f"{i}. {song['title']:25} | Score: {score:.2f} | "
                  f"M:{components['mood']:.2f} G:{components['genre']:.2f} "
                  f"E:{components['energy']:.2f} A:{components['acoustic']:.2f}")
        print()

    # Impact analysis
    print("Impact Analysis:")
    print("-" * 90)

    top_original = [s[0]['title'] for s in scored_by_config[0.40][:5]]
    top_moderate = [s[0]['title'] for s in scored_by_config[0.25][:5]]
    top_energy = [s[0]['title'] for s in scored_by_config[0.10][:5]]

    print(f"Overlap between 0.40 and 0.25: {len(set(top_original) & set(top_moderate))}/5")
    print(f"Overlap between 0.40 and 0.10: {len(set(top_original) & set(top_energy))}/5")
    print(f"Overlap between 0.25 and 0.10: {len(set(top_moderate) & set(top_energy))}/5")

    print("\nSongs NEW in 0.25 (not in 0.40): ", end="")
    new_025 = set(top_moderate) - set(top_original)
    print(", ".join(new_025) if new_025 else "None")

    print("Songs NEW in 0.10 (not in 0.40): ", end="")
    new_010 = set(top_energy) - set(top_original)
    print(", ".join(new_010) if new_010 else "None")

    print("\nHigh-energy songs in top 5:")
    for config_val, label in configs:
        high_energy_count = sum(1 for s in scored_by_config[config_val][:5] if s[0]['energy'] > 0.8)
        print(f"  {config_val}: {high_energy_count}/5 songs have energy > 0.8")


if __name__ == "__main__":
    songs = load_songs("data/songs.csv")

    # Test 1: Happy pop (mood match available)
    test_case_1 = {
        'genre': 'pop',
        'mood': 'happy',
        'energy': 0.80,
        'likes_acoustic': False,
    }
    compare_mood_weights("Happy Pop (Mood Match Available)", test_case_1, songs)

    # Test 2: Intense rock (mood match available)
    test_case_2 = {
        'genre': 'rock',
        'mood': 'intense',
        'energy': 0.90,
        'likes_acoustic': False,
    }
    compare_mood_weights("Intense Rock (Mood Match Available)", test_case_2, songs)

    # Test 3: Chill lofi (genre-specific, mood available)
    test_case_3 = {
        'genre': 'lofi',
        'mood': 'chill',
        'energy': 0.40,
        'likes_acoustic': False,
    }
    compare_mood_weights("Chill Lofi (Both Mood & Genre Match)", test_case_3, songs)

    # Test 4: Happy jazz (conflicting - jazz is relaxed, not happy)
    test_case_4 = {
        'genre': 'jazz',
        'mood': 'happy',
        'energy': 0.90,
        'likes_acoustic': False,
    }
    compare_mood_weights("Happy Jazz High-Energy (Conflicting Preferences)", test_case_4, songs)

    # Test 5: Very specific energy preference
    test_case_5 = {
        'genre': 'electronic',
        'mood': 'calm',  # Imaginary mood
        'energy': 0.25,  # Very low energy - electronic usually high
        'likes_acoustic': False,
    }
    compare_mood_weights("Low-Energy Electronic (Energy Mismatch)", test_case_5, songs)

    print("\n" + "=" * 90)
    print("SUMMARY: Mood Weight Impact")
    print("=" * 90)
    print("""
MOOD WEIGHT 0.40 (ORIGINAL - MOOD-FIRST):
  - Emotional context is PRIMARY filter
  - Users discover across genres if mood matches
  - Recommendations feel emotionally coherent
  - Example: Happy songs from ANY genre ranked high

MOOD WEIGHT 0.25 (MODERATE):
  - Mood still important but not dominant
  - Genre becomes more influential (still 0.30)
  - Energy/acoustic start affecting rankings more
  - More balanced approach

MOOD WEIGHT 0.10 (ENERGY-FIRST):
  - Mood barely matters
  - Genre (0.30) + Energy (0.46) dominate
  - Energy preferences drive recommendations
  - Users get high-energy or low-energy songs regardless of mood
  - Example: High-energy songs EVEN IF they're sad/intense

WHAT CHANGES:
  - Lower mood weight = Less cross-genre discovery
  - Lower mood weight = Energy/acoustic become tiebreakers
  - 0.10 favors "energy chemistry" over "emotional match"
  - 0.10 is good for workout/focus (needs energy), bad for mood-based playlists

KEY INSIGHT:
  Reducing mood from 0.40 to 0.10 shifts from:
  "Find me songs that FEEL a certain way"
  to
  "Find me songs that SOUND a certain way and MOVE at a certain pace"
""")
