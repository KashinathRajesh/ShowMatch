from fastapi import FastAPI, Query
from fastapi.middleware.cors import CORSMiddleware
from fetcher import ShowFetcher
from matcher import VibeMatcher
from main import load_bank, save_to_bank

app=FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
)

fetcher=ShowFetcher()
bank=load_bank()

@app.get("/recommend")
async def get_recommendation(title: str = Query(..., min_length=1)):
    target_data = fetcher.get_vibe(title)
    
    if not target_data:
        return {"error": "Show not found"}

    save_to_bank(target_data, bank)
    
    matcher = VibeMatcher(bank)
    recommendations = matcher.get_recommendations(target_data['title'])
    
    return {
        "target": target_data['title'],
        "vibe_tags": target_data['keywords'][:8],
        "recommendations": recommendations
    }

if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)