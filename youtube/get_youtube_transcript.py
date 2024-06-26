from youtube_transcript_api import YouTubeTranscriptApi
from urllib.parse import urlparse, parse_qs
import json
from django.views.decorators.csrf import csrf_exempt

# Function to get the transcript of a YouTube video, which'll be fed to GPT-4o for summary in .swift appp
@csrf_exempt
def get_youtube_transcript(request):

    # Get url from request body
    data = json.loads(request.body.decode('utf-8'))
    url = data.get('url')

    # Parse the URL
    parsed_url = urlparse(url)

    # Check the domain of the URL to determine how to extract the video ID
    if 'youtu.be' in parsed_url.netloc:
        # This is a shortened YouTube URL, so the video ID is the first element in the path
        video_id = parsed_url.path.split('/')[1]
    else:
        # This is a standard YouTube URL, so parse the query parameters to get the video ID
        video_id = parse_qs(parsed_url.query).get('v', [None])[0]

    # Ensure that a video ID was found
    if not video_id:
        raise ValueError("No video ID found in URL")

    # Get the transcript for the video
    transcript = YouTubeTranscriptApi.get_transcript(video_id)

    # Extract the sentences from the transcript
    sentences = [entry['text'] for entry in transcript]

    # Join the sentences into a single string (transcript)
    entire_transcript = " ".join(sentences)
    
    # Return the transcript
    return entire_transcript
