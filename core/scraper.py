import requests
from bs4 import BeautifulSoup

def scrape_website(url):
    try:
        res = requests.get(url)
        soup = BeautifulSoup(res.content, 'html.parser')
        return "\n".join(p.get_text() for p in soup.find_all('p'))
    except Exception:
        return ""
