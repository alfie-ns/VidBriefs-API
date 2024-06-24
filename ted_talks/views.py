from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
import os
import markdown
import json

# Adjusted Base directory where the markdown files are stored
BASE_DIRECTORY = os.path.join(os.path.dirname(__file__), 'TED-talks')

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

# Function to list available TED Talk titles in a given directory
def list_ted_talks_in_directory(directory):
    return [f.replace('_', ' ').replace('.md', '') for f in os.listdir(directory) if f.endswith('.md')]

# Recursive function to list all TED Talk titles in the base directory
def list_all_ted_talks(directory):
    all_talks = []
    for root, dirs, files in os.walk(directory):
        for file in files:
            if file.endswith('.md'):
                file_path = os.path.join(root, file)
                title = file.replace('_', ' ').replace('.md', '')
                all_talks.append(title)
    return all_talks

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

# New endpoint to list all TED Talks
def list_all_talks(request):
    if request.method == 'GET':
        all_talks = list_all_ted_talks(BASE_DIRECTORY)
        return JsonResponse({'ted_talks': all_talks})
    else:
        return JsonResponse({'error': 'Invalid request method'}, status=405)