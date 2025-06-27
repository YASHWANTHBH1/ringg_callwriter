# ringg_callwriter
# 🧠 CallWriter for Ringg.ai

**Turn any website or FAQ into AI voice agent call scripts in seconds.**  
Built for AI-first companies like Ringg.ai to streamline onboarding, automate call flow generation, and scale support.

![Logo](assets/ringg_logo.png)

---

## 🚀 Features

- 🔗 Input via URL or raw FAQ/text
- 🎙️ Tone control: Friendly, Professional, Casual
- 🧠 Groq’s Mixtral LLM: Fast, free, accurate
- 📥 JSON Output: Ready for training or RAG
- ✨ Styled UI matching Ringg's aesthetic

---

## 🛠️ Tech Stack

- Python 3.10+
- Streamlit UI
- Groq API (Mixtral-8x7b-32768)
- BeautifulSoup for web scraping

---

## 📦 Installation

```bash
pip install -r requirements.txt
streamlit run callwriter_app.py
