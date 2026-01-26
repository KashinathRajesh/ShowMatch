from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fetcher import ShowFetcher
from matcher import VibeMatcher
from main import load_bank, save_to_bank
import uvicorn

app = FastAPI()
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

fetcher = ShowFetcher()
bank = load_bank()

@app.get("/suggest")
async def get_suggestions(q: str = ""):
    if not q or len(q) < 2: return []
    return [s['title'] for s in bank if q.lower() in s['title'].lower()][:5]

@app.get("/recommend")
async def get_recommendation(
    title: str = Query(..., min_length=1),
    limit: int = 6,
    include_animation: bool = True,
    min_rating: float = 0.0,
    adult: bool = False,
    start_year: int = 1950,
    end_year: int = 2026
):
    target_data = fetcher.get_vibe(title)
    if not target_data: return {"error": "Show not found"}
    
    save_to_bank(target_data, bank)

    restricted_ratings = ["A", "R", "TV-MA", "18", "18+", "NC-17"]
    filtered_bank = []
    
    for show in bank:
        show_cert = show.get('certification', 'U')
        show_genres = show.get('genres', []) or []
        
        try:
            raw_year = show.get('year')
            show_year = int(raw_year) if raw_year and str(raw_year).isdigit() else 0
        except:
            show_year = 0
        
        if not include_animation and 16 in show_genres: continue
        if show.get('rating', 0) < min_rating: continue
        if not adult and show_cert in restricted_ratings: continue
        if show_year != 0 and (show_year < start_year or show_year > end_year): continue

        filtered_bank.append(show)

    if len(filtered_bank) < 2:
        return {"error": "Too many filters active. No matches found."}

    matcher = VibeMatcher(filtered_bank)
    rec_titles = matcher.get_recommendations(target_data['title'], top_n=limit)
    
    full_recs = []
    for t in rec_titles:
        match = next((item for item in filtered_bank if item["title"] == t), None)
        if match: full_recs.append(match)

    return {"target": target_data, "recommendations": full_recs}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)