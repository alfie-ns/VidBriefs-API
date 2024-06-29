from django.urls import path
from .views import get_youtube_transcript, GetYoutubeUrl

urlpatterns = [
    path('get_youtube_transcript/', GetYoutubeUrl.as_view(), name='get_youtube_transcript'),
    #path('get_youtube_data/', GetYoutubeData.as_view(), name='get_youtube_data'),
    #path('get_ted_talk_transcript/', GetTedTalkTranscript.as_view(), name='get_ted_talk_transcript'),
    #path('record_interaction/', RecordInteraction.as_view(), name='record_interaction'),
    #path('recommendation_info/<int:user_id>/', RecommendationInfo.as_view(), name='recommendation_info'),
]