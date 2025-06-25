import requests
import json

def generate_scripts(raw_text, tone, count, api_key):
    if not api_key:
        raise ValueError("❌ API Key missing")

    prompt = f"""
    You are a voice UX AI assistant.

    Based on the content below, generate {count} realistic customer call intents.

    Each intent should have:
    - A title: 'intent'
    - A 'script' with a list of user-AI exchanges.

    Return ONLY a valid JSON array like:
    [
      {{
        "intent": "Billing Inquiry",
        "script": [
          {{"user": "...", "ai": "..."}},
          ...
        ]
      }},
      ...
    ]

    DO NOT include any explanations or markdown — ONLY return valid JSON.

    Content:
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
        print("🔍 LLM Raw Output:", content)

        return json.loads(content)

    except Exception as e:
        print("⚠️ Failed to parse LLM output")
        print("❌ Exception:", e)
        return None



