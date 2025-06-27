from bs4 import BeautifulSoup
import asyncio
import sys
from playwright.sync_api import sync_playwright
import requests
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())


def normalize_url(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url.rstrip("/")

def scrape_with_requests(url):
    try:
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.content, 'html.parser')
        return "\n".join(p.get_text(strip=True) for p in soup.find_all(['p', 'h1', 'h2', 'li']))
    except:
        return ""

def scrape_with_playwright(url):
    try:
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=15000)
            page.wait_for_load_state("networkidle")
            html = page.content()
            browser.close()
            soup = BeautifulSoup(html, 'html.parser')
            return "\n".join(tag.get_text(strip=True) for tag in soup.find_all(['p', 'h1', 'h2', 'li']))
    except Exception as e:
        return f"❌ Playwright Error: {e}"

def scrape_website(url):
    url = normalize_url(url)
    content = scrape_with_requests(url)
    if len(content.strip()) < 100:
        return scrape_with_playwright(url)
    return content


