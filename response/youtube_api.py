from django.http import JsonResponse
from googleapiclient.discovery import build
import os

YOUTUBE_API_KEY = os.environ.get('YOUTUBE_API_KEY')

def get_youtube_data(request, video_id):
    youtube = build('youtube', 'v3', developerKey=YOUTUBE_API_KEY)

    # Fetch video details
    video_request = youtube.videos().list(part='snippet,contentDetails,statistics', id=video_id)
    video_response = video_request.execute()

    video_data = {}
    if video_response['items']:
        video_info = video_response['items'][0]['snippet']
        video_data = {
            'title': video_info['title'],
            'description': video_info['description'],
            'channelTitle': video_info['channelTitle'], #TODO: put a channel win as a subheading of the summarisation
            
        }

    # Fetch recommendations
    recommendation_request = youtube.search().list(part='snippet', relatedToVideoId=video_id, type='video', maxResults=10)
    recommendation_response = recommendation_request.execute()

    recommendations = []
    for item in recommendation_response['items']:
        snippet = item['snippet']
        recommendations.append({
            'videoId': item['id']['videoId'],
            'title': snippet['title'],
            'description': snippet['description']
        })

    # Combine both responses
    response_data = {
        'videoDetails': video_data,
        'recommendations': recommendations
    }

    # TODO: append this data to an array or database for future use

    return JsonResponse(response_data)
