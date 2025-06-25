import streamlit as st
import toml
from core.generator import generate_scripts
from core.scraper import scrape_website
from utils.text_cleaner import clean_html_text
import json
import time

# --- Streamlit Page Config ---
st.set_page_config(page_title="CallWriter", layout="wide")

# --- Logo/Header ---
st.image("assets/ringg_logo.png", width=100)
st.title("🧠 CallWriter for Ringg.ai")
st.caption("Turn websites & FAQs into production-ready AI agent call scripts")
st.markdown("---")

# --- Load API Key from .streamlit/secrets.toml ---
try:
    secrets = toml.load(".streamlit/secrets.toml")
    GROQ_API_KEY = secrets["default"]["GROQ_API_KEY"]
    st.success(f"✅ API Key Loaded: {GROQ_API_KEY[:10]}********")
except Exception as e:
    st.error(f"❌ Failed to load API key: {e}")
    st.stop()

# --- Input Section ---
input_type = st.radio("📥 Input Type", ["Website URL", "Paste Text"], horizontal=True)

raw_text = ""
if input_type == "Website URL":
    url = st.text_input("🔗 Enter a website URL")
    if url:
        raw_text = scrape_website(url)
else:
    raw_text = st.text_area("📄 Paste company FAQs or content here")

# --- Script Options ---
tone = st.selectbox("🎙️ Choose Agent Tone", ["Friendly", "Professional", "Casual"])
num_scripts = st.slider("📊 Number of Call Intents", 1, 6, 3)

# --- Generate Button ---
if st.button("🚀 Generate Call Scripts"):
    if not raw_text.strip():
        st.warning("⚠️ Please provide valid content.")
    else:
        with st.spinner("🧠 Generating voice scripts using Groq LLM..."):
            cleaned = clean_html_text(raw_text)
            response = generate_scripts(cleaned, tone, num_scripts, GROQ_API_KEY)

            if response:
                st.success("✅ Call scripts generated!")
                for i, intent in enumerate(response, 1):
                    st.subheader(f"📞 Intent {i}: {intent['intent']}")
                    for line in intent["script"]:
                        st.markdown(f"**👤 User:** {line['user']}")
                        st.markdown(f"**🤖 AI:** {line['ai']}")
                    st.markdown("---")

                st.download_button("⬇️ Download JSON", data=json.dumps(response, indent=2),
                                   file_name="callwriter_output.json", mime="application/json")
            else:
                st.error("❌ Failed to generate. Check input or API key.")

