import os
import requests
from dotenv import load_dotenv

load_dotenv()

class ShowFetcher:
    def __init__(self):
        self.api_key = os.getenv("TMDB_API_KEY")
        self.base_url = "https://api.themoviedb.org/3"

    def get_vibe(self, title):
        # 1. Search for the TV Show
        search_url = f"{self.base_url}/search/tv"
        params = {"api_key": self.api_key, "query": title}

        response = requests.get(search_url, params=params).json()

        if not response.get('results'):
            return None
        
        # 2. Extract ID and Name (TV uses 'name')
        show_id = response['results'][0]['id']
        show_title = response['results'][0]['name']

        # 3. Get Keywords for the ID
        keyword_url = f"{self.base_url}/tv/{show_id}/keywords"
        kw_response = requests.get(keyword_url, params={"api_key": self.api_key}).json()
        keywords = [item['name'] for item in kw_response.get('results', [])]

        return {
            "title": show_title,
            "keywords": keywords
        }
    
if __name__ == "__main__":
    fetcher = ShowFetcher()
    data = fetcher.get_vibe("Stranger Things")
    
    if data:
        print(f"Vibe for {data['title']}: {data['keywords']}")
    else:
        print("Show not found!")