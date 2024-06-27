# ted_talks/user_interests.py

from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
from collections import Counter
import numpy as np
from .models import TedTalk

def guess_user_interests(watched_talks):
    """
    Guess user interests based on their watched TED Talks.
    
    :param watched_talks: List of TedTalk objects that the user has watched
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
    :param all_talks: List of all available TedTalk objects
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
    :return: String summary of the talk
    """
    # This is a placeholder function. In a real-world scenario, you'd use
    # more advanced NLP techniques to generate a meaningful summary.
    return f"Title: {talk.title}\nType: {talk.type_of_talk}\nKeywords: {talk.keywords}"

# Example usage (commented out for production use)
"""
if __name__ == "__main__":
    # Sample TED Talks data
    sample_talks = [
        TedTalk("The power of introverts", "Psychology", "In a culture where being social...", "introversion,psychology,personality"),
        TedTalk("The puzzle of motivation", "Business", "Career analyst Dan Pink examines...", "motivation,business,psychology"),
        TedTalk("Your body language may shape who you are", "Psychology", "Body language affects how others see us...", "body language,psychology,communication"),
        TedTalk("The power of vulnerability", "Personal Growth", "Brené Brown studies human connection...", "vulnerability,courage,shame"),
        TedTalk("How great leaders inspire action", "Leadership", "Simon Sinek has a simple but powerful model...", "leadership,inspiration,business"),
        TedTalk("The happy secret to better work", "Psychology", "We believe we should work hard in order to be happy...", "happiness,productivity,psychology"),
        TedTalk("Your elusive creative genius", "Creativity", "Elizabeth Gilbert muses on the impossible things...", "creativity,inspiration,writing"),
    ]

    # Simulate user's watched talks
    watched_talks = sample_talks[:3]  # User has watched the first 3 talks

    # Guess user interests
    user_interests = guess_user_interests(watched_talks)
    print("Guessed user interests:", user_interests)

    # Get recommendations
    recommendations = recommend_talks(user_interests, sample_talks)

    # Print recommendations with summaries
    print("\nRecommended TED Talks:")
    for talk in recommendations:
        print("\n" + summarize_talk(talk))
"""