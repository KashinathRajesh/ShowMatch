import os
import requests
from dotenv import load_dotenv

load_dotenv()

class ShowFetcher:
    def __init__(self):
        self.api_key = os.getenv("TMDB_API_KEY")
        self.base_url = "https://api.themoviedb.org/3"
        self.img_base = "https://image.tmdb.org/t/p/w500"

    def get_vibe(self, title):
        search_url = f"{self.base_url}/search/tv"
        params = {"api_key": self.api_key, "query": title}
        try:
            res = requests.get(search_url, params=params, timeout=10).json()
            if not res.get('results'): return None
            show = res['results'][0]
            show_id = show['id']
            
            kw_url = f"{self.base_url}/tv/{show_id}/keywords"
            kw_res = requests.get(kw_url, params={"api_key": self.api_key}).json()
            keywords = [item['name'] for item in kw_res.get('results', [])]

            watch_url = f"{self.base_url}/tv/{show_id}/watch/providers"
            watch_res = requests.get(watch_url, params={"api_key": self.api_key}).json()
            providers = watch_res.get('results', {}).get('IN', {})

            return {
                "id": show_id,
                "title": show.get('name'),
                "keywords": keywords,
                "poster": f"{self.img_base}{show.get('poster_path')}" if show.get('poster_path') else None,
                "description": show.get('overview'),
                "rating": round(show.get('vote_average', 0), 1),
                "watch_link": providers.get('link'),
                "stream_on": [p['provider_name'] for p in providers.get('flatrate', [])] if providers.get('flatrate') else []
            }
        except:
            return None