import streamlit as st
import toml
import json
from utils.text_cleaner import clean_html_text
from core.generator import generate_scripts
from core.scraper import scrape_website

# Page setup
st.set_page_config(page_title="CallWriter for Ringg.ai", layout="wide")
st.image("assets/ringg_logo.png", width=100)
st.title("🧠 CallWriter for Ringg.ai")
st.caption("Turn websites & FAQs into production-ready AI voice agent scripts")
st.markdown("---")

# Load Groq API key
try:
    secrets = toml.load(".streamlit/secrets.toml")
    GROQ_API_KEY = secrets["default"]["GROQ_API_KEY"]
except Exception as e:
    st.error(f"❌ Missing or invalid API key: {e}")
    st.stop()

def normalize_url(url):
    if not url.startswith("http://") and not url.startswith("https://"):
        url = "https://" + url
    return url

# Input section
input_type = st.radio("📥 Input Type", ["Website URL", "Paste Text"], horizontal=True)
raw_text = ""

if input_type == "Website URL":
    url = st.text_input("🔗 Enter website (e.g., ringg.ai or https://www.ringg.ai)")
    if url:
        try:
            full_url = normalize_url(url.strip())
            with st.spinner("🔍 Scraping content..."):
                raw_text = scrape_website(full_url)
                if not raw_text:
                    st.warning("⚠️ No content found on the page.")
        except Exception as e:
            st.error(f"❌ Error loading site: {e}")
else:
    raw_text = st.text_area("📄 Paste content or FAQs here")

# Generation Options
tone = st.selectbox("🎙️ Choose Tone", ["Friendly", "Professional", "Casual"])
topic = st.selectbox(
    "🗂️ Select Domain for Script Generation",
    ["General", "Sales", "Technical Support", "Product Info", "Healthcare", "Travel", "Food Delivery", "Finance"]
)
num_scripts = st.slider("📞 Number of Call Intents", 1, 6, 3)

# Generate scripts
if st.button("🚀 Generate Call Scripts"):
    if not raw_text.strip():
        st.warning("⚠️ Please enter valid content.")
    else:
        with st.spinner("🤖 Generating scripts using Groq LLM..."):
            cleaned = clean_html_text(raw_text)
            result = generate_scripts(cleaned, tone, num_scripts, GROQ_API_KEY, topic)

            if result:
                st.success("✅ Done!")
                for i, intent in enumerate(result, 1):
                    st.subheader(f"📞 Intent {i}: {intent['intent']}")
                    for turn in intent["script"]:
                        st.markdown(f"**👤 User:** {turn['user']}" if "user" in turn else "")
                        st.markdown(f"**🤖 AI:** {turn['ai']}" if "ai" in turn else "")
                    st.markdown("---")
                st.download_button("⬇️ Download JSON", data=json.dumps(result, indent=2),
                                   file_name="callwriter_output.json", mime="application/json")
            else:
                st.error("❌ Failed to generate. Check API key or content.")


