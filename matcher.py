import pandas as pd
from sklearn.feature_extraction.text import CountVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class VibeMatcher:
    def __init__(self, library_data):
        self.df= pd.DataFrame(library_data)
        self.df['vibe_string']=self.df['keywords'].apply(lambda x: " ".join(x))

    def get_recommendations(self, target_title, top_n=3):
        cv=CountVectorizer()
        vibe_matrix=cv.fit_transform(self.df['vibe_string'])
        similarity=cosine_similarity(vibe_matrix)

        try:
            show_idx=self.df[self.df['title']==target_title].index[0]
        except IndexError:
            return f"Show '{target_title}' not found in local bank."

        scores=list(enumerate(similarity[show_idx]))
        sorted_scores=sorted(scores,key=lambda x: x[1], reverse=True)[1:top_n+1]

        recommendations = [self.df.iloc[i[0]]['title'] for i in sorted_scores]
        return recommendations

if __name__ == "__main__":
    # Small test bank to verify the logic
    test_library = [
        {"title": "Stranger Things", "keywords": ["1980s", "monster", "supernatural", "kids"]},
        {"title": "Dark", "keywords": ["time travel", "supernatural", "mystery", "small town"]},
        {"title": "The Office", "keywords": ["comedy", "workplace", "documentary"]},
        {"title": "Super 8", "keywords": ["1980s", "monster", "kids", "sci-fi"]}
    ]

    matcher = VibeMatcher(test_library)
    recs = matcher.get_recommendations("Stranger Things")
    print(f"If you like the vibe of Stranger Things, try: {recs}")