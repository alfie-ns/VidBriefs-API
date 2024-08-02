# ted_talks/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register_user, name='register_user'),
    path('get-transcript/', views.get_tedtalk_transcript, name='get_tedtalk_transcript'),
    path('list_all_talks/', views.list_all_talks, name='list_all_talks'),
    path('recommendations/', views.get_recommendations, name='get_recommendations'),
    path('mark_watched/', views.mark_talk_as_watched, name='mark_talk_as_watched'),
    path('recommend_talks/', views.recommend_talks, name='recommend_talks'),
    path('test/', views.test_view, name='test_view'),
]