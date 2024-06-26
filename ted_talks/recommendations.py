from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from .models import TedTalk

def recommend_talks(user_interests):
    talks = TedTalk.objects.all()
    tfidf = TfidfVectorizer(stop_words='english')
    tfidf_matrix = tfidf.fit_transform([talk.keywords for talk in talks])
    user_tfidf = tfidf.transform([user_interests])
    cosine_similarities = linear_kernel(user_tfidf, tfidf_matrix).flatten()
    recommended_indices = cosine_similarities.argsort()[:-6:-1]
    return [talks[i] for i in recommended_indices]