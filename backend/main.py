# backend/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.text_cleaner import clean_html_text
from core.scraper import scrape_website
from core.generator import generate_scripts
from dotenv import load_dotenv
import os

load_dotenv()  # Load variables from .env file

app = FastAPI()

# Optional: Replace * with specific frontend URLs (e.g., http://localhost:3000)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class GenerationRequest(BaseModel):
    url: str
    mode: str  # Friendly / Professional / Casual
    intentCount: int
    domain: str  # General, Sales, Support, etc.

@app.post("/generate")
def generate_intents(request: GenerationRequest):
    try:
        # Load API key
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        if not GROQ_API_KEY:
            raise HTTPException(status_code=401, detail="GROQ API Key missing")

        # Normalize and scrape
        url = request.url.strip()
        if not url.startswith("http"):
            url = "https://" + url
        raw_text = scrape_website(url)
        if not raw_text:
            raise HTTPException(status_code=404, detail="Could not scrape website content")

        # Clean and generate
        cleaned_text = clean_html_text(raw_text)
        result = generate_scripts(cleaned_text, request.mode, request.intentCount, GROQ_API_KEY, request.domain)

        if result is None:
            raise HTTPException(status_code=500, detail="Script generation failed")

        return {"status": "success", "scripts": result}

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))




