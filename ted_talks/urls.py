# ted_talks/urls.py

from django.urls import path
from .views import get_tedtalk_transcripts, list_all_talks, recommend_talks
from . import views

urlpatterns = [
    path('get_tedtalk_transcript/', get_tedtalk_transcripts, name='get_tedtalk_transcript'),
    path('list_all_talks/', list_all_talks, name='list_all_talks'),
    path('recommend_talks/', recommend_talks, name='recommend_talks'),
    path('recommendations/', views.get_recommendations, name='get_recommendations'),
]