from django.urls import path
from .views import get_tedtalk_transcripts, list_all_talks

urlpatterns = [
    path('get_tedtalk_transcripts/', get_tedtalk_transcripts, name='get_tedtalk_transcript'),
    path('list_all_talks/', list_all_talks, name='list_all_talks'),
]