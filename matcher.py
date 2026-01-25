import pandas as pd
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import cosine_similarity

class VibeMatcher:
    def __init__(self, library_data):
        self.df = pd.DataFrame(library_data)
        
        self.df['vibe_string'] = self.df.apply(
            lambda x: " ".join(x.get('keywords', [])) + " " + str(x.get('description', '')), 
            axis=1
        )

    def get_recommendations(self, target_title, top_n=6):
        tfidf = TfidfVectorizer(stop_words='english', ngram_range=(1, 2))
        
        vibe_matrix = tfidf.fit_transform(self.df['vibe_string'])
        similarity = cosine_similarity(vibe_matrix)

        try:
            show_idx = self.df[self.df['title'] == target_title].index[0]
        except IndexError:
            return []

        scores = list(enumerate(similarity[show_idx]))
        
        sorted_scores = sorted(scores, key=lambda x: x[1], reverse=True)[1:top_n+1]
        recommendations = [self.df.iloc[i[0]]['title'] for i in sorted_scores]
        return recommendations