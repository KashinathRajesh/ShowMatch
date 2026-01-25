import os
import json
from fetcher import ShowFetcher
from matcher import VibeMatcher

BANK_FILE="show_bank.json"

def load_bank():
    if not os.path.exists(BANK_FILE):
        return [
            {"title": "The Office", "keywords": ["comedy", "workplace"]},
            {"title": "Dark", "keywords": ["small town", "supernatural", "mystery"]}
        ]
    with open(BANK_FILE, "r") as f:
        return json.load(f)

def save_to_bank(new_show, current_bank):
    titles = [show['title'] for show in current_bank]
    if new_show['title'] not in titles:
        current_bank.append(new_show)
        with open(BANK_FILE, "w") as f:
            json.dump(current_bank, f, indent=4)

def run_vibecheck():
    fetcher= ShowFetcher()
    bank=load_bank()

    user_query=input("Enter a show you love: ")
    target_data=fetcher.get_vibe(user_query)

    if not target_data:
        print("Sorry, I couldn't find that show!")
        return
    
    print(f"Found: {target_data['title']}")
    print(f"Vibe Tags: {', '.join(target_data['keywords'][:5])}...\n")

    if target_data:
        save_to_bank(target_data, bank)
        matcher = VibeMatcher(bank)
        recommendations = matcher.get_recommendations(target_data['title'])

        print(f"\n--- If you like the vibe of {target_data['title']}, try these: ---")
        for i, rec in enumerate(recommendations, 1):
            print(f"{i}. {rec}")

    print(f"--- If you like the vibe of {target_data['title']}, try these: ---")
    for i, rec in enumerate(recommendations, 1):
        print(f"{i}. {rec}")

if __name__ == "__main__":
    run_vibecheck()