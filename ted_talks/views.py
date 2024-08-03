# ted_talks/views.py

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import TedTalk, UserWatchedTalk
from .recommendations import get_user_interests, recommend_talks, summarize_talk
import os, markdown, json
from django.db.models import Q
from django.conf import settings
from pathlib import Path
from django.contrib.auth.models import User
from .auth_utils import create_token_for_user, token_required
from django.contrib.auth.models import User
from .auth_utils import create_token_for_user
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
import json
from .auth_utils import token_required
import logging

logger = logging.getLogger(__name__)

def test_view(request):
    return JsonResponse({"message": "Test view working"})

#@csrf_exempt
#def register_user(request):
#    if request.method == 'POST':
#        try:
#            data = json.loads(request.body)
#            username = data.get('username')
#            password = data.get('password')
#            
#            if not username or not password:
#                return JsonResponse({'error': 'Username and password are required'}, status=400)
#            
#            user = User.objects.create_user(username=username, password=password)
#            token = create_token_for_user(user)
#            
#            return JsonResponse({'token': str(token)})
#        except json.JSONDecodeError:
#            return JsonResponse({'error': 'Invalid JSON'}, status=400)
#        except Exception as e:
#            return JsonResponse({'error': str(e)}, status=500)
#    else:
#        return JsonResponse({'error': 'Invalid request method'}, status=405)

@token_required
def get_recommendations(request):
    if request.method == 'GET':
        user = request.user
        watched_talks = TedTalk.objects.filter(userwatchedtalk__user=user)
        
        user_interests = get_user_interests(watched_talks)
        all_talks = TedTalk.objects.all()
        recommended_talks = recommend_talks(user_interests, all_talks)

        recommendations = [summarize_talk(talk) for talk in recommended_talks]

        return JsonResponse({'recommendations': recommendations})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@token_required
def mark_talk_as_watched(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            talk_id = data.get('talk_id')
            
            if talk_id:
                talk = TedTalk.objects.get(id=talk_id)
                UserWatchedTalk.objects.get_or_create(user=request.user, talk=talk)
                return JsonResponse({'success': True, 'message': 'Talk marked as watched'})
            else:
                return JsonResponse({'error': 'Talk ID is required'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
        except TedTalk.DoesNotExist:
            return JsonResponse({'error': 'Talk not found'}, status=404)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def load_transcript_from_markdown(file_path):
    try:
        with open(file_path, 'r', encoding='utf-8') as file:
            transcript_text = file.read()
        html_book = markdown.markdown(transcript_text)
        return html_book
    except FileNotFoundError:
        return None

def find_tedtalk_file(user_input, directory):
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.md') and user_input.lower() in filename.lower():
                return os.path.join(root, filename)
    return None

@csrf_exempt 
@token_required
def get_tedtalk_transcript(request):
    logger.info("get_tedtalk_transcript view function called")
    if request.method == 'POST':
        try:
            data = json.loads(request.body)
            title = data.get('title')
            
            logger.info(f"Searching for title: {title}")
            logger.info(f"TED_TALKS_DIR: {settings.TED_TALKS_DIR}")
            
            if not title:
                return JsonResponse({'error': 'Title is required'}, status=400)

            search_title = title.lower().replace(' ', '_').replace('.md', '')
            logger.info(f"Search title: {search_title}")
            
            for file in settings.TED_TALKS_DIR.glob('**/*.md'):
                if search_title in file.stem.lower():
                    logger.info(f"Found file: {file}")
                    content = file.read_text(encoding='utf-8')
                    html_content = markdown.markdown(content)
                    return JsonResponse({
                        'title': file.stem.replace('_', ' '),
                        'transcript': html_content
                    })

            logger.warning(f"No file found for search title: {search_title}")
            return JsonResponse({
                'error': f"TED Talk with title containing '{title}' not found",
                'suggestion': "Try with a different title or check if the file exists"
            }, status=404)
        
        except Exception as e:
            logger.exception(f"Error in get_tedtalk_transcript: {str(e)}")
            return JsonResponse({'error': str(e)}, status=500)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

@csrf_exempt
@token_required
def list_all_talks(request):
    if request.method == 'GET':
        all_talks = list_all_talks(TED_TALKS_DIR)
        if not all_talks:
            return JsonResponse({
                'error': 'No talks found',
                'debug_info': {
                    'TED_TALKS_DIR': str(TED_TALKS_DIR),
                    'directory_exists': os.path.exists(TED_TALKS_DIR),
                    'directory_contents': os.listdir(TED_TALKS_DIR) if os.path.exists(TED_TALKS_DIR) else 'Directory not found'
                }
            }, status=404)
        return JsonResponse({'ted_talks': all_talks})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

# Remove or update these as needed
def get_recommendations(request):
    # ... 
    pass

def recommend_talks(request):
    pass