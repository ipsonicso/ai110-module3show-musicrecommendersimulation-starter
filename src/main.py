"""
Command line runner for the Music Recommender Simulation.

This file helps you quickly run and test your recommender.

You will implement the functions in recommender.py:
- load_songs
- score_song
- recommend_songs
"""

from recommender import load_songs, recommend_songs, _get_component_scores


def format_recommendation(song, score, user_prefs, components):
    lines = []

    # Compute match values
    mood_pct   = int(round((components['mood']  / 0.40) * 100))
    genre_pct  = int(round((components['genre'] / 0.30) * 100))
    energy_pct = int(round((1 - abs(song['energy'] - user_prefs['energy'])) * 100))
    is_acoustic = song['acousticness'] > 0.5
    user_likes_acoustic = user_prefs.get('likes_acoustic', False)
    acoustic_match = is_acoustic == user_likes_acoustic
    acoustic_pct = 100 if acoustic_match else 0
    pref_label = 'acoustic' if user_likes_acoustic else 'non-acoustic'

    # Title and score
    lines.append(f"\n{'=' * 70}")
    lines.append(f"{song['title']} - Final Score: {score:.2f}")
    lines.append('=' * 70)

    # Summary
    matched = []
    if components['mood'] > 0:
        matched.append(f"{song['mood']} mood")
    if components['genre'] > 0:
        matched.append(f"{song['genre']} genre")
    if energy_pct >= 85:
        matched.append("well-matched energy")
    elif energy_pct >= 70:
        matched.append("close energy match")
    if acoustic_match:
        matched.append(f"{pref_label} quality")

    summary = f"Strong match: {', '.join(matched)}" if matched else "Best available match based on weighted preferences"
    lines.append(f"\nSummary: {summary}")

    # Detailed breakdown
    lines.append("\nDetailed Analysis:")

    mood_symbol = '[+]' if components['mood'] > 0 else '[-]'
    mood_verb = "matches" if components['mood'] > 0 else "does not match"
    lines.append(f"  {mood_symbol} Mood:     '{song['mood']}' mood {mood_verb} your preference '{user_prefs['mood']}' ({mood_pct}% match, +{components['mood']:.2f})")

    genre_symbol = '[+]' if components['genre'] > 0 else '[-]'
    genre_verb = "matches" if components['genre'] > 0 else "does not match"
    lines.append(f"  {genre_symbol} Genre:    '{song['genre']}' genre {genre_verb} your preference '{user_prefs['genre']}' ({genre_pct}% match, +{components['genre']:.2f})")

    energy_symbol = '[+]' if energy_pct >= 85 else ('[~]' if energy_pct >= 70 else '[-]')
    energy_verb = "is aligned with" if energy_pct >= 85 else ("is close to" if energy_pct >= 70 else "is not aligned with")
    lines.append(f"  {energy_symbol} Energy:   energy level {energy_verb} your target {user_prefs['energy']:.2f} (proximity: {energy_pct}%, +{components['energy']:.2f})")

    acoustic_symbol = '[+]' if acoustic_match else '[-]'
    acoustic_verb = "has" if acoustic_match else "does not have"
    lines.append(f"  {acoustic_symbol} Acoustic: {acoustic_verb} the {pref_label} quality you prefer ({acoustic_pct}% match, +{components['acoustic']:.2f})")

    return '\n'.join(lines)


VALID_GENRES = ["pop", "lofi", "rock", "ambient", "jazz", "synthwave", "electronic", "indie pop", "indie"]
VALID_MOODS  = ["happy", "chill", "intense", "relaxed", "moody", "focused"]


SAMPLE_PREFS = {"genre": "pop", "mood": "happy", "energy": 0.8, "likes_acoustic": False}


def get_user_prefs() -> dict:
    print("\n" + "BUILD YOUR PROFILE".center(70, "="))
    print("  1. Use sample profile (pop | happy | energy 0.8 | non-acoustic)")
    print("  2. Enter my own preferences")
    while True:
        choice = input("\nChoose an option (1 or 2): ").strip()
        if choice == "1":
            print(f"  Using sample profile: {SAMPLE_PREFS}")
            return SAMPLE_PREFS
        elif choice == "2":
            break
        print("  Please enter 1 or 2.")

    print(f"\nAvailable genres: {', '.join(VALID_GENRES)}")
    while True:
        genre = input("Enter your favorite genre: ").strip().lower()
        if genre in VALID_GENRES:
            break
        print(f"  Invalid genre. Choose from: {', '.join(VALID_GENRES)}")

    print(f"\nAvailable moods: {', '.join(VALID_MOODS)}")
    while True:
        mood = input("Enter your favorite mood: ").strip().lower()
        if mood in VALID_MOODS:
            break
        print(f"  Invalid mood. Choose from: {', '.join(VALID_MOODS)}")

    while True:
        try:
            energy = float(input("\nEnter your target energy level (0.0 = very calm, 1.0 = very intense): ").strip())
            if 0.0 <= energy <= 1.0:
                break
            print("  Please enter a value between 0.0 and 1.0.")
        except ValueError:
            print("  Please enter a number like 0.7.")

    while True:
        acoustic = input("\nDo you prefer acoustic songs? (yes/no): ").strip().lower()
        if acoustic in ("yes", "y"):
            likes_acoustic = True
            break
        elif acoustic in ("no", "n"):
            likes_acoustic = False
            break
        print("  Please answer yes or no.")

    return {"genre": genre, "mood": mood, "energy": energy, "likes_acoustic": likes_acoustic}


def main() -> None:
    songs = load_songs("data/songs.csv")

    user_prefs = get_user_prefs()

    recommendations = recommend_songs(user_prefs, songs, k=5)

    print("\n" + "TOP RECOMMENDATIONS".center(70, "="))
    print(f"Profile: {user_prefs['mood']} {user_prefs['genre']} | energy {user_prefs['energy']:.0%} | {'acoustic' if user_prefs['likes_acoustic'] else 'non-acoustic'}")

    titles = "  ".join(f"{i}. {s['title']}" for i, (s, _, _) in enumerate(recommendations, 1))
    print(f"Results: {titles}")

    for song, score, _ in recommendations:
        components = _get_component_scores(user_prefs, song)
        print(format_recommendation(song, score, user_prefs, components))

    print(f"\n{'=' * 70}\n")


if __name__ == "__main__":
    main()
