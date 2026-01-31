# ShowMatch AI 
### The Genetic DNA Matcher for Movies & Shows

**ShowMatch AI** is a high-accuracy discovery engine that bypasses traditional "Genre" categories. It uses **TF-IDF Vectorization** to map the hidden thematic DNA of over 3,000 shows.



## Key Features
* **Genetic Vibe Matching:** Uses Scikit-Learn to calculate cosine similarity between show metadata, ignoring broad genres to find true thematic matches.
* **Age-Gate Certification:** A secure filtering system that uses official regional certifications (U, UA, A, R) instead of unreliable keyword guessing.
* **Dynamic Metadata Engine:** Integration with TMDB API for real-time show analysis and database seeding.
* **Pro Dashboard UI:** A dark-mode, sidebar-driven interface optimized for deep catalog exploration.

## Tech Stack
* **Backend:** FastAPI (Python)
* **Machine Learning:** Scikit-Learn (TF-IDF, Cosine Similarity)
* **Data Handling:** Pandas
* **Frontend:** Tailwind CSS, Vanilla JS
* **Data Source:** TMDB API

## Setup
1. Clone the repo: `git clone https://github.com/your-username/ShowMatch-AI.git`
2. Install dependencies: `pip install -r requirements.txt`
3. Add your TMDB API Key to a `.env` file: `TMDB_API_KEY=your_key_here`
4. Run the engine: `python app.py`

## Forensic Accuracy
Unlike standard algorithms that suggest "Action" shows if you watch *Squid Game*, ShowMatch AI identifies the "Survival-Dystopia" DNA, prioritizing matches like *Alice in Borderland* or *3%* regardless of their origin or genre label.
