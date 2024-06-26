from django.views.decorators.csrf import csrf_exempt
from django.http import JsonResponse
from .recommendations import recommend_talks
import os, markdown, json
 
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
    for root, dirs, files in os.walk(directory):
        for filename in files:
            if filename.endswith('.md') and user_input.lower() in filename.lower():
                return os.path.join(root, filename)
    return None

@csrf_exempt
def get_tedtalk_transcripts(request):
    if request.method == 'POST':
        try:
            data = json.loads(request.body)  # Load JSON data from request body
            titles = data.get('titles')  # Extract 'titles' from JSON data (expecting a list of titles)
            title = data.get('title')  # Extract 'title' from JSON data (expecting a single title)

            if titles and isinstance(titles, list):
                transcripts = {}
                for title in titles:
                    file_path = find_tedtalk_file(title, BASE_DIRECTORY)
                    if file_path:
                        transcript = load_transcript_from_markdown(file_path)
                        if transcript:
                            transcripts[title] = transcript
                        else:
                            transcripts[title] = 'Transcript not found'
                    else:
                        transcripts[title] = 'TED Talk not found'
                return JsonResponse({'transcripts': transcripts})
            
            elif title and isinstance(title, str):
                transcripts = {}
                file_path = find_tedtalk_file(title, BASE_DIRECTORY)
                if file_path:
                    transcript = load_transcript_from_markdown(file_path)
                    if transcript:
                        transcripts[title] = transcript
                    else:
                        transcripts[title] = 'Transcript not found'
                else:
                    transcripts[title] = 'TED Talk not found'
                return JsonResponse({'transcripts': transcripts})
            else:
                return JsonResponse({'error': 'Invalid request, title or titles missing or incorrect format'}, status=400)
        
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
    
def get_user_interests(request):
    interests = request.GET.get('interests', '')
    recommended_talks = recommend_talks(interests)
    talks = [{'title': talk.title, 'id': talk.id} for talk in recommended_talks]
    return JsonResponse({'recommended_talks': talks})