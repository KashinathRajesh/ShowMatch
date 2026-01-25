import os
from fetcher import ShowFetcher
from matcher import VibeMatcher

def run_vibecheck():
    fetcher= ShowFetcher()

    user_query=input("Enter a show you love: ")
    print(f"--- Searching TMDB for '{user_query}' vibe profile... ---")

    target_data=fetcher.get_vibe(user_query)

    if not target_data:
        print("Sorry, I couldn't find that show!")
        return
    
    print(f"Found: {target_data['title']}")
    print(f"Vibe Tags: {', '.join(target_data['keywords'][:5])}...\n")

    local_bank = [
        {"title": "Dark", "keywords": ["small town", "time travel", "supernatural", "mystery", "parallel world", "disappearance"]},
        {"title": "The Haunting of Hill House", "keywords": ["horror", "supernatural", "ghost", "family drama", "haunted house"]},
        {"title": "Yellowjackets", "keywords": ["survival", "mystery", "teens", "supernatural", "psychological horror"]},
        {"title": "The Office", "keywords": ["comedy", "workplace", "documentary", "mockumentary"]},
        {"title": "Twin Peaks", "keywords": ["small town", "mystery", "surreal", "supernatural", "investigation"]},
        {"title": "Wednesday", "keywords": ["goth", "supernatural", "school", "mystery", "monster"]}
    ]

    local_bank.append(target_data)
    matcher= VibeMatcher(local_bank)
    recommendations = matcher.get_recommendations(target_data['title'])

    print(f"--- If you like the vibe of {target_data['title']}, try these: ---")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")

if __name__ == "__main__":
    run_vibecheck()