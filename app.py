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
    platform: str = "All"
):
    target_data = fetcher.get_vibe(title)
    if not target_data: return {"error": "Show not found"}
    save_to_bank(target_data, bank)

    filtered_bank = []
    adult_keywords = ["nudity", "sex", "violence", "gore", "suicide", "horror"]
    
    for show in bank:
        show_keywords = [k.lower() for k in show.get('keywords', [])]
        show_platforms = [p.lower() for p in show.get('stream_on', [])]
        if show.get('rating', 0) < min_rating: continue
        if not include_animation and "animation" in show_keywords: continue
        if not adult and any(k in adult_keywords for k in show_keywords): continue
        if platform != "All" and platform.lower() not in show_platforms: continue
        filtered_bank.append(show)

    if not filtered_bank: return {"error": "No matching shows found with current filters"}

    matcher = VibeMatcher(filtered_bank)
    rec_titles = matcher.get_recommendations(target_data['title'], top_n=limit)
    
    full_recs = []
    for t in rec_titles:
        match = next((item for item in filtered_bank if item["title"] == t), None)
        if match: full_recs.append(match)

    return {"target": target_data, "recommendations": full_recs}

if __name__ == "__main__":
    uvicorn.run(app, host="0.0.0.0", port=8000)