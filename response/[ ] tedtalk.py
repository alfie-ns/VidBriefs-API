import requests
from bs4 import BeautifulSoup

def get_tedtalk_transcript(ted_url):
    """
    Fetches the transcript of a TED Talk from the given URL.

    :param ted_url: URL of the TED Talk
    :return: Transcript text or None if not found
    """
    try:
        # Send a GET request to the TED Talk URL
        response = requests.get(ted_url)
        response.raise_for_status()  # Raise an exception for 4xx or 5xx status codes
        
        # Parse the HTML content using BeautifulSoup
        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Find the transcript container
        transcript_container = soup.find('div', class_='Grid Grid--with-gutter')
        
        if transcript_container:
            # Extract the transcript paragraphs
            transcript_paragraphs = transcript_container.find_all('p')
            transcript_text = ' '.join(p.get_text(strip=True) for p in transcript_paragraphs)
            return transcript_text.strip()
        else:
            return None
    
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while fetching the TED Talk: {e}")
        return None