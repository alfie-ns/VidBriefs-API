from django.urls import path
from .views import get_ted_talk_transcript

urlpatterns = [
    path('get_ted_talk_transcript/', get_ted_talk_transcript, name='get_ted_talk_transcript'),
]