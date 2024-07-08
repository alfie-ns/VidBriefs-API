from pathlib import Path
import markdown
import json
from django.http import JsonResponse
from django.conf import settings
import logging
from django.views.decorators.csrf import csrf_exempt

logger = logging.getLogger(__name__)

@csrf_exempt
def get_tedtalk_transcript(request):
    if request.method != 'POST':
        logger.warning(f"Invalid request method: {request.method}")
        return JsonResponse({'error': 'Invalid request method'}, status=405)

    try:
        data = json.loads(request.body)
        title = data.get('title')
        
        if not title:
            logger.warning("Title not provided in request")
            return JsonResponse({'error': 'Title is required'}, status=400)

        ted_talks_dir = settings.BASE_DIR / 'TED-talks' / 'cleaned_ted_archive_data'
        logger.debug(f"Searching in directory: {ted_talks_dir}")
        
        search_title = title.lower().replace(' ', '_')
        logger.debug(f"Normalized search title: {search_title}")
        
        for file in ted_talks_dir.glob(f"{search_title}*.md"):
            logger.info(f"Found matching file: {file}")
            content = file.read_text(encoding='utf-8')
            html_content = markdown.markdown(content)
            return JsonResponse({
                'title': file.stem.replace('_', ' '),
                'transcript': html_content
            })

        logger.warning(f"No matching file found for title: {title}")
        return JsonResponse({
            'error': f"TED Talk with title containing '{title}' not found",
            'suggestion': "Try with a different title or check if the file exists"
        }, status=404)
    
    except json.JSONDecodeError:
        logger.error("Invalid JSON in request body")
        return JsonResponse({'error': 'Invalid JSON'}, status=400)
    except Exception as e:
        logger.exception(f"An unexpected error occurred: {str(e)}")
        return JsonResponse({'error': 'An unexpected error occurred'}, status=500)