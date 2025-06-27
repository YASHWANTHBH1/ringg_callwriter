# backend/main.py

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from utils.text_cleaner import clean_html_text
from core.scraper import scrape_website
from core.generator import generate_scripts
from dotenv import load_dotenv
import os
import traceback

# Load environment variables
load_dotenv()

app = FastAPI()

# Allow frontend (React/Vercel) to access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Root check (optional)
@app.get("/")
def health_check():
    return {"status": "✅ Backend running", "message": "Hello from CallWriter API!"}

# Request payload structure
class GenerationRequest(BaseModel):
    url: str
    mode: str  # e.g. Friendly / Professional / Casual
    intentCount: int
    domain: str  # Optional domain like sales/support/etc.

# Main generation endpoint
@app.post("/generate")
def generate_intents(request: GenerationRequest):
    try:
        print(f"📥 Request payload: {request.dict()}")

        # Load GROQ API key
        GROQ_API_KEY = os.getenv("GROQ_API_KEY")
        if not GROQ_API_KEY:
            print("❌ Missing GROQ API Key")
            raise HTTPException(status_code=401, detail="GROQ API Key missing")

        # Normalize URL
        url = request.url.strip()
        if not url.startswith("http"):
            url = "https://" + url

        print(f"🔗 Normalized URL: {url}")
        raw_text = scrape_website(url)

        if not raw_text or len(raw_text.strip()) < 50:
            print("❌ Website scraping returned empty or too short.")
            raise HTTPException(status_code=404, detail="Could not scrape website content")

        cleaned_text = clean_html_text(raw_text)
        print(f"🧼 Cleaned content length: {len(cleaned_text)} characters")

        result = generate_scripts(
            raw_text=cleaned_text,
            tone=request.mode,
            count=request.intentCount,
            api_key=GROQ_API_KEY,
            domain=request.domain
        )

        if not result:
            print("❌ Script generation failed")
            raise HTTPException(status_code=500, detail="Script generation failed")

        print("✅ Successfully generated scripts")
        return {
            "status": "success",
            "scripts": result
        }

    except Exception as e:
        print("🔥 Internal error during generation:")
        traceback.print_exc()
        raise HTTPException(status_code=500, detail=f"Unhandled Error: {str(e)}")





