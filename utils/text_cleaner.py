import re
from bs4 import BeautifulSoup

def clean_html_text(html_text: str) -> str:
    """
    Clean and extract readable content from HTML or raw scraped text.
    """
    # Remove script/style tags and their content
    soup = BeautifulSoup(html_text, 'html.parser')
    for tag in soup(['script', 'style', 'noscript']):
        tag.decompose()

    text = soup.get_text(separator=' ')
    
    # Normalize spaces and newlines
    text = re.sub(r'\s+', ' ', text)
    text = re.sub(r'\n+', '\n', text)
    
    # Remove unwanted characters
    text = re.sub(r'[^\x00-\x7F]+', ' ', text)  # Remove non-ASCII chars
    text = re.sub(r'\s{2,}', ' ', text)         # Multiple spaces → one

    return text.strip()


