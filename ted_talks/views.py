# ted_talks/views.py

from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from .models import TedTalk, UserWatchedTalk
from .recommendations import get_user_interests, recommend_talks, summarize_talk
import os, markdown, json, re, datetime
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

# Build paths inside the project like this: BASE_DIR / 'subdir'.
BASE_DIR = Path(__file__).resolve().parent.parent

# Define TED_TALKS_DIR with the correct path
TED_TALKS_DIR = BASE_DIR / 'ted_talks' / 'TED-talks' / 'cleaned_ted_archive_data'


logger = logging.getLogger(__name__)

def test_view(request):
    return JsonResponse({"message": "Test view working"})


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
    logger.info("get_tedtalk_transcript view function called") # print
    if request.method == 'POST': # if post
        try: # try to fetch specified ted talk and extract transcript
            data = json.loads(request.body)
            title = data.get('title')
            
            logger.info(f"""
                        Searching for title: {title}
                        """) # print
            logger.info(f"""
                        TED_TALKS_DIR: {TED_TALKS_DIR}
                        """) # print
            
            if not title:
                return JsonResponse({'error': 'Title is required'}, status=400)

            search_title = title.lower().replace(' ', '_').replace('.md', '') # title of talk searches for is clenaed up link('test_talk.md' -> 'test talk')
            logger.info(f"""
                        Search title: {search_title}
                        """)
            # glob: Iterate over this subtree and yield all existing files (of any kind, including directories) matching the given relative pattern
            for file in TED_TALKS_DIR.glob('**/*.md'): # for every file inside TED-talks
                if search_title in file.stem.lower():
                    logger.info(f"""
                                Found file: {file}
                                """)
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
        all_talks = get_all_talks(TED_TALKS_DIR)
        if not all_talks:
            return JsonResponse({
                'error': 'No talks found',
                'debug_info': {
                    'TED_TALKS_DIR': TED_TALKS_DIR,
                    'directory_exists': os.path.exists(TED_TALKS_DIR),
                    'directory_contents': os.listdir(TED_TALKS_DIR) if os.path.exists(TED_TALKS_DIR) else 'Directory not found'
                }
            }, status=404)
        return JsonResponse({'ted_talks': all_talks})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)

def get_all_talks(directory):
    talks = []
    for filename in os.listdir(directory):
        if filename.endswith('.md'):
            # Remove the .md extension and replace underscores with spaces
            talk_name = os.path.splitext(filename)[0].replace('_', ' ')
            talks.append(talk_name)
    return talks

def parse_talk_metadata(content):
    metadata = {}
    
    # Extract title
    title_match = re.search(r'# (.*)', content)
    if title_match:
        metadata['title'] = title_match.group(1)
    
    # Extract speaker
    speaker_match = re.search(r'## Speaker: (.*)', content)
    if speaker_match:
        metadata['speaker'] = speaker_match.group(1)
    
    # Extract date
    date_match = re.search(r'## Date: (.*)', content)
    if date_match:
        try:
            date = datetime.strptime(date_match.group(1), '%B %Y')
            metadata['date'] = date.strftime('%Y-%m-%d')
        except ValueError:
            metadata['date'] = date_match.group(1)  # Keep original if parsing fails
    
    # Extract duration
    duration_match = re.search(r'## Duration: (.*)', content)
    if duration_match:
        metadata['duration'] = duration_match.group(1)
    
    # Extract views (if available)
    views_match = re.search(r'## Views: (.*)', content)
    if views_match:
        metadata['views'] = views_match.group(1)
    
    # Extract a brief description (first paragraph after "## Transcript")
    transcript_match = re.search(r'## Transcript\s+(.+?)(?=\n\n|\Z)', content, re.DOTALL)
    if transcript_match:
        metadata['description'] = transcript_match.group(1).strip()
    
    return metadata

# Remove or update these as needed
def get_recommendations(request):
    # ... 
    pass

def recommend_talks(request):
    pass