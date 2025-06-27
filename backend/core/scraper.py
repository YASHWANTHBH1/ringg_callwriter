# core/scraper.py

from bs4 import BeautifulSoup
import asyncio
import sys
from playwright.sync_api import sync_playwright
import requests

# Fix for Windows compatibility
if sys.platform.startswith("win"):
    asyncio.set_event_loop_policy(asyncio.WindowsProactorEventLoopPolicy())

def normalize_url(url):
    if not url.startswith(("http://", "https://")):
        url = "https://" + url
    return url.rstrip("/")

def scrape_with_requests(url):
    try:
        print(f"🌐 Using requests for: {url}")
        res = requests.get(url, timeout=10)
        soup = BeautifulSoup(res.content, 'html.parser')
        content = "\n".join(p.get_text(strip=True) for p in soup.find_all(['p', 'h1', 'h2', 'li']))
        print(f"✅ requests scraped {len(content)} characters")
        return content
    except Exception as e:
        print(f"❌ requests failed: {e}")
        return ""

def scrape_with_playwright(url):
    try:
        print(f"🎭 Using Playwright for: {url}")
        with sync_playwright() as p:
            browser = p.chromium.launch(headless=True)
            page = browser.new_page()
            page.goto(url, timeout=20000)
            page.wait_for_load_state("networkidle")
            html = page.content()
            browser.close()
            soup = BeautifulSoup(html, 'html.parser')
            content = "\n".join(tag.get_text(strip=True) for tag in soup.find_all(['p', 'h1', 'h2', 'li']))
            print(f"✅ Playwright scraped {len(content)} characters")
            return content
    except Exception as e:
        print(f"❌ Playwright Error: {e}")
        return ""  # return empty string to indicate fallback also failed

def scrape_website(url):
    url = normalize_url(url)
    content = scrape_with_requests(url)
    if len(content.strip()) < 100:
        print("🔁 Fallback to Playwright scraping...")
        content = scrape_with_playwright(url)
    return content



