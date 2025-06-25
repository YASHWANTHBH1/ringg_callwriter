import requests
import json
import re

def generate_scripts(raw_text, tone, count, api_key, topic="General"):
    if not api_key:
        raise ValueError("❌ API Key missing")

    prompt = f"""
You are a voice UX AI assistant.

Generate {count} realistic and friendly customer voice call scripts for a company in the **{topic}** domain.

Each script must follow this structure:
- Starts with: AI says "Hi! How can I help you today?"
- Then the user responds naturally (e.g. "What does your company do?")
- AI gives a clear explanation of what the company does
- Continue for 1–2 more exchanges

🧠 Important:
- Return only valid JSON — no markdown, no commentary
- Each script must be in this format:
[
  {{
    "intent": "Intent title here",
    "script": [
      {{"ai": "Hi! How can I help you today?"}},
      {{"user": "What do you do?"}},
      {{"ai": "We help automate websites with AI-powered voice agents."}}
    ]
  }}
]

Here is the company content to use for background:

{raw_text[:3000]}
"""

    data = {
        "model": "llama3-70b-8192",
        "messages": [
            {"role": "system", "content": "You are a voice UX expert."},
            {"role": "user", "content": prompt}
        ],
        "temperature": 0.6
    }

    try:
        res = requests.post(
            "https://api.groq.com/openai/v1/chat/completions",
            headers={
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            },
            json=data
        )
        if res.status_code != 200:
            print("❌ API response:", res.status_code, res.text)
            return None

        content = res.json()["choices"][0]["message"]["content"]
        content = content.strip()

        # Remove markdown/code block if exists
        if content.startswith("```json"):
            content = re.sub(r"```json|```", "", content).strip()

        return json.loads(content)

    except Exception as e:
        print("❌ Failed to parse LLM output:", e)
        return None




