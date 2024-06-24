from django.urls import path
from .views import get_tedtalk_transcript, list_all_talks

urlpatterns = [
    path('get_tedtalk_transcript/', get_tedtalk_transcript, name='get_tedtalk_transcript'),
    path('list_all_talks/', list_all_talks, name='list_all_talks'),
]