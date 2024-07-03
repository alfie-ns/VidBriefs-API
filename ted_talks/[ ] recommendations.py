# recommendations.py

'''
This file contains functionality to recommend the next TED Talk to watch based on user interests.

Features:
- Recommends TED Talks based on user interests using TF-IDF and cosine similarity
- Handles cases where there are no talks or insufficient talks in the database
- Filters out talks with no keywords
- Uses caching to improve performance for repeated calls
'''

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from django.core.cache import cache
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
    # Fetch all TED Talks from the database with non-empty keywords
    talks = TedTalk.objects.exclude(keywords__isnull=True).exclude(keywords__exact='')
    
    if not talks:
        return []

    # Check if we have a cached TF-IDF matrix
    tfidf_matrix = cache.get('tfidf_matrix')
    tfidf_vectorizer = cache.get('tfidf_vectorizer')
    
    if tfidf_matrix is None or tfidf_vectorizer is None:
        # If not cached, compute the TF-IDF matrix
        keywords = [talk.keywords for talk in talks]
        tfidf_vectorizer = TfidfVectorizer(stop_words='english')
        tfidf_matrix = tfidf_vectorizer.fit_transform(keywords)
        
        # Cache the results for future use
        cache.set('tfidf_matrix', tfidf_matrix, timeout=3600)  # Cache for 1 hour
        cache.set('tfidf_vectorizer', tfidf_vectorizer, timeout=3600)

    # Transform the user interests into the TF-IDF space
    user_tfidf = tfidf_vectorizer.transform([user_interests])
    
    # Compute the cosine similarities between user interests and TED Talks
    cosine_similarities = linear_kernel(user_tfidf, tfidf_matrix).flatten()
    
    # Get the indices of the top-n similar TED Talks
    recommended_indices = cosine_similarities.argsort()[::-1]
    
    # Return the recommended TED Talks, up to top_n
    recommended_talks = []
    for index in recommended_indices:
        if len(recommended_talks) >= top_n:
            break
        recommended_talks.append(talks[index])
    
    return recommended_talks

def get_user_interests(user):
    """
    Retrieves user interests from the user profile or history.
    This is a placeholder function and should be implemented based on your user model.
    """
    # Placeholder implementation
    return "technology innovation science"  # Replace with actual user interests
