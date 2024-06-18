from django.views.decorators.csrf import csrf_exempt
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework import status
from response import get_youtube_transcript
from .youtube_api import get_youtube_data
from django.http import JsonResponse
import os
import markdown

# Base directory where the markdown files are stored
BASE_DIRECTORY = 'TED-talks/cleaned_ted_archive_data/'

# Function to load TED Talk transcripts from Markdown files
def load_transcript_from_markdown(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            transcript_text = file.read()
        # Convert Markdown to HTML
        html = markdown.markdown(transcript_text)
        return html
    except FileNotFoundError:
        return None

# Function to list available TED Talk titles
def list_available_ted_talks(directory):
    return [f.replace('_', ' ').replace('.md', '') for f in os.listdir(directory) if f.endswith('.md')]

# Function to find TED Talk markdown file based on user input
def find_ted_talk_file(user_input, directory):
    for filename in os.listdir(directory):
        if filename.endswith('.md') and user_input.lower() in filename.lower():
            return os.path.join(directory, filename)
    return None

# APIView to handle YouTube URL requests
class GetYoutubeUrl(APIView):
    @csrf_exempt
    def post(self, request):
        response = get_youtube_transcript(request)
        return Response({'response': response}, status=status.HTTP_200_OK)

# APIView to handle YouTube data requests
class GetYoutubeData(APIView):
    @csrf_exempt
    def post(self, request):
        response = get_youtube_data(request)
        return Response({'response': response}, status=status.HTTP_200_OK)

# Function-Based View to fetch TED Talk transcript
@csrf_exempt
def get_ted_talk_transcript(request):
    if request.method == 'POST':
        user_input = request.POST.get('title')
        if user_input:
            file_path = find_ted_talk_file(user_input, BASE_DIRECTORY)
            if file_path:
                transcript = load_transcript_from_markdown(file_path)
                if transcript:
                    return JsonResponse({'transcript': transcript})
                else:
                    return JsonResponse({'error': 'Transcript not found'}, status=404)
            else:
                return JsonResponse({'error': 'TED Talk not found'}, status=404)
        else:
            return JsonResponse({'error': 'Invalid request, title missing'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

# Function-Based View to list available TED Talks
def list_ted_talks(request):
    if request.method == 'GET':
        talks = list_available_ted_talks(BASE_DIRECTORY)
        return JsonResponse({'ted_talks': talks})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)