import time
import requests
from fetcher import ShowFetcher
from main import load_bank, save_to_bank

def seed_database(start_page=1, end_page=5):
    fetcher = ShowFetcher()
    bank = load_bank()
    
    print(f"--- Starting Seeder: Fetching from page {start_page} to {end_page} ---")
    
    # We use range(start, end + 1) to make it inclusive
    for page in range(start_page, end_page + 1):
        url = f"{fetcher.base_url}/tv/popular"
        params = {"api_key": fetcher.api_key, "page": page}
        
        response = requests.get(url, params=params).json()
        popular_results = response.get('results', [])

        for show in popular_results:
            show_name = show.get('name')
            
            # This is the 'Guard' that prevents re-fetching what you already have
            existing_titles = [s['title'] for s in bank]
            if show_name in existing_titles:
                continue
                
            data = fetcher.get_vibe(show_name)
            
            if data:
                save_to_bank(data, bank)
                print(f"Added Page {page}: {data['title']}")
            
            time.sleep(0.2) 
            
    print("--- Seeding Complete! ---")

if __name__ == "__main__":
    seed_database(start_page=77, end_page=150)