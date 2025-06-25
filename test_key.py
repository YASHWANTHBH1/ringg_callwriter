import toml

try:
    data = toml.load(".streamlit/secrets.toml")
    print("Key Found:", data["default"]["GROQ_API_KEY"][:10], "...")
except Exception as e:
    print("Error:", e)
