# recommendations.py
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from .models import TedTalk

def recommend_talks(user_interests, top_n=5):
    """
    Recommends TED Talks based on user interests.

    Parameters:
    - user_interests (str): A string of keywords representing user interests.
    - top_n (int): The number of recommendations to return. Default is 5.

    Returns:
    - list: A list of recommended TedTalk objects.
    """
    # Fetch all TED Talks from the database
    talks = TedTalk.objects.all()
    if not talks:
        return []

    # Extract keywords from the talks
    keywords = [talk.keywords for talk in talks]
    
    # Initialize the TF-IDF Vectorizer
    tfidf = TfidfVectorizer(stop_words='english')
    
    # Create the TF-IDF matrix for TED Talk keywords
    tfidf_matrix = tfidf.fit_transform(keywords)
    
    # Transform the user interests into the TF-IDF space
    user_tfidf = tfidf.transform([user_interests])
    
    # Compute the cosine similarities between user interests and TED Talks
    cosine_similarities = linear_kernel(user_tfidf, tfidf_matrix).flatten()
    
    # Get the indices of the top-n similar TED Talks
    recommended_indices = cosine_similarities.argsort()[-top_n:][::-1]
    
    # Return the recommended TED Talks
    return [talks[i] for i in recommended_indices]