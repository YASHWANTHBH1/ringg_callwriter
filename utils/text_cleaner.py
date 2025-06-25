# utils/text_cleaner.py

import re

def clean_html_text(text: str) -> str:
    """Clean HTML or scraped content by removing excess whitespace."""
    text = re.sub(r'\n+', '\n', text)
    text = re.sub(r'\s+', ' ', text)
    return text.strip()

