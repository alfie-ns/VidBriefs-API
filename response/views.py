'''This file contains the classes that will handle the POST request from the app.'''

from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from .get_youtube_transcript import get_youtube_transcript



class GetYoutubeUrl(APIView):
    @csrf_exempt
    def post(self, request):
        # Parse JSON data from the request body
        response = get_youtube_transcript(request)
        # Return response to app
        return Response({'response': response}, status=status.HTTP_200_OK)