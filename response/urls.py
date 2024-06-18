from django.urls import path
from .views import get_ted_talk_transcript, get_youtube_transcript



urlpatterns = [
    path('get_youtube_transcript/', get_youtube_transcript.as_view(), name='get_youtube_transcript'),
    #path('get_youtube_data/', GetYoutubeUrl.as_view(), name='get_youtube_data'),
]