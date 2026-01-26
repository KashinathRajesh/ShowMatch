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

            cert_url = f"{self.base_url}/tv/{show_id}/content_ratings"
            cert_res = requests.get(cert_url, params={"api_key": self.api_key}).json()
            
            results = cert_res.get('results', [])
            india_rating = next((r['rating'] for r in results if r['iso_3166_1'] == 'IN'), None)
            us_rating = next((r['rating'] for r in results if r['iso_3166_1'] == 'US'), None)
            certification = india_rating or us_rating or "NR"

            return {
                "id": show_id,
                "title": show.get('name'),
                "keywords": keywords,
                "genres": show.get('genre_ids', []),
                "certification": certification,
                "language": show.get('original_language'),
                "year": show.get('first_air_date', '')[:4] if show.get('first_air_date') else None,
                "poster": f"{self.img_base}{show.get('poster_path')}" if show.get('poster_path') else None,
                "description": show.get('overview'),
                "rating": round(show.get('vote_average', 0), 1)
            }
        except:
            return None