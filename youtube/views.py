'''This file contains the classes that will handle the POST request from the app.'''

from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .get_youtube_transcript import get_youtube_transcript
from django.http import JsonResponse
from .models import Video, UserInteraction
from googleapiclient.discovery import build
import os

class GetYoutubeUrl(APIView):
    @csrf_exempt
    def post(self, request):
        try:
            response = get_youtube_transcript(request)
            return Response({'response': response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
    
class GetYoutubeData(APIView):
    @csrf_exempt
    def post(self, request):
        try:
            response = get_youtube_data(request)
            return Response({'response': response}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class GetTedTalkTranscript(APIView):
    @csrf_exempt
    def post(self, request):
        try:
            # Your logic to get TED talk transcript here
            return Response({"message": "TED Talk Transcript"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
class RecordInteraction(APIView):
    @csrf_exempt
    def post(self, request):
        try:
            # Your logic to record interaction here
            return Response({"message": "Interaction recorded"}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

class RecommendationInfo(APIView):
    @csrf_exempt
    def get(self, request, user_id):
        try:
            # Your logic to get recommendations here
            return Response({"recommendations": []}, status=status.HTTP_200_OK)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
  
#def record_interaction(request):
#    # Endpoint to record user interactions
#    # Extract interaction data from request
#    # Save to UserInteraction model
#    pass
#
#def recommendation_info(request, user_id):
#    # Endpoint to provide recommendations
#    # Use user_id to tailor recommendations
#    pass

