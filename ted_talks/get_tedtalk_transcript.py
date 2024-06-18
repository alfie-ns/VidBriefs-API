import os
from bs4 import BeautifulSoup
import markdown, requests

def extract_markdown_text(md_file_path):
    """
    Extracts all text from a .md markdown file.
    Copy:param md_file_path: Path to the markdown file
    :return: Plain text content of the markdown file
    """
    try:
        with open(md_file_path, 'r') as file:
            md_text = file.read()

        # Convert markdown to HTML using the markdown library
        html = markdown.markdown(md_text)

        # Parse the HTML using BeautifulSoup
        soup = BeautifulSoup(html, 'html.parser')

        # Extract the plain text from the parsed HTML
        plain_text = soup.get_text()

        return plain_text.strip()
    except FileNotFoundError:
        print(f"File not found: {md_file_path}")
        return None
    except Exception as e:
        print(f"An error occurred while processing the markdown file: {e}")
        return None
    
# ------------------------------------------------------------------------------------------------------------------------------------------------ 

def summarize_text(text, api_url, api_key):
    """
    Sends text to an API for summarization.
    Copy:param text: Text to be summarized
    :param api_url: API endpoint for summarization
    :param api_key: API key for authorization
    :return: Summarized text or None if summarization fails
    """
    try:
        headers = {
            'Authorization': f'Bearer {api_key}',
            'Content-Type': 'application/json'
        }
        payload = {
            'model': 'gpt-4',  # Model used for summarization
            'messages': [
                {'role': 'system', 'content': 'Summarize the following text.'},
                {'role': 'user', 'content': text}
            ]
        }
        response = requests.post(api_url, headers=headers, json=payload)
        response.raise_for_status()  # Raise an exception for HTTP errors

        result = response.json()
        if 'choices' in result and len(result['choices']) > 0:
            return result['choices'][0]['message']['content']
        else:
            print("Summarization failed: No choices in response.")
            return None
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while sending the text for summarization: {e}")
        return None