from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
import markdown
import json

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
def find_tedtalk_file(user_input, directory):
    for filename in os.listdir(directory):
        if filename.endswith('.md') and user_input.lower() in filename.lower():
            return os.path.join(directory, filename)
    return None

@csrf_exempt
def get_tedtalk_transcript(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Load JSON data from request body
            user_input = data.get('title')  # Extract 'title' from JSON data
            if user_input:
                file_path = find_tedtalk_file(user_input, BASE_DIRECTORY)
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
        except json.JSONDecodeError:
            return JsonResponse({'error': 'Invalid JSON'}, status=400)
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)