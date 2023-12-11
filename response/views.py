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
        # Parse JSON data from the request body
        response = get_youtube_transcript(request)
        # Return response to app
        return Response({'response': response}, status=status.HTTP_200_OK)
    
def record_interaction(request):
    # Endpoint to record user interactions
    # Extract interaction data from request
    # Save to UserInteraction model
    pass

def recommendation_info(request, user_id):
    # Endpoint to provide recommendations
    # Use user_id to tailor recommendations
    pass
