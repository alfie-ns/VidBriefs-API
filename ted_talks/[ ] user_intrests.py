# ted_talks/user_interests.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from collections import Counter
import numpy as np
from .models import TedTalk

def guess_user_interests(watched_talks):
    """
    Guess user interests based on their watched TED Talks.
    
    :param watched_talks: QuerySet of TedTalk objects that the user has watched
    :return: List of guessed user interests
    """
    all_keywords = []
    for talk in watched_talks:
        all_keywords.extend(talk.keywords.split(','))
    
    # Count keyword occurrences
    keyword_counts = Counter(all_keywords)
    
    # Get the top 10 most common keywords as user interests
    user_interests = [keyword for keyword, _ in keyword_counts.most_common(10)]
    
    return user_interests

def recommend_talks(user_interests, all_talks, top_n=5):
    """
    Recommends TED Talks based on user interests.

    :param user_interests: List of user interests
    :param all_talks: QuerySet of all available TedTalk objects
    :param top_n: Number of recommendations to return (default: 5)
    :return: List of recommended TedTalk objects
    """
    if not all_talks:
        return []

    # Extract keywords from the talks
    keywords = [talk.keywords for talk in all_talks]
    
    # Initialize the TF-IDF Vectorizer
    tfidf = TfidfVectorizer(stop_words='english')
    
    # Create the TF-IDF matrix for TED Talk keywords
    tfidf_matrix = tfidf.fit_transform(keywords)
    
    # Transform the user interests into the TF-IDF space
    user_tfidf = tfidf.transform([' '.join(user_interests)])
    
    # Compute the cosine similarities between user interests and TED Talks
    cosine_similarities = linear_kernel(user_tfidf, tfidf_matrix).flatten()
    
    # Get the indices of the top-n similar TED Talks
    recommended_indices = cosine_similarities.argsort()[-top_n:][::-1]
    
    # Return the recommended TED Talks
    return [all_talks[i] for i in recommended_indices]

def summarize_talk(talk):
    """
    Generate a summary of a TED Talk.
    
    :param talk: TedTalk object
    :return: Dictionary with talk summary
    """
    return {
        "title": talk.title,
        "type_of_talk": talk.type_of_talk,
        "keywords": talk.keywords
    }