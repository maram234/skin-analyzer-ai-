import os
import google.generativeai as genai
from dotenv import load_dotenv

def test_key(path):
    print(f"Testing key in {path}...")
    load_dotenv(path, override=True)
    api_key = os.getenv("GEMINI_API_KEY")
    if not api_key:
        print("No key found.")
        return
    genai.configure(api_key=api_key)
    try:
        print("Available models:")
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"  - {m.name}")
        model = genai.GenerativeModel('gemini-3.1-flash-lite-preview')
        response = model.generate_content("Hello")
        print(f"Success! Response: {response.text[:20]}...")
    except Exception as e:
        print(f"Failed: {e}")

test_key("c:/Users/TRUE TECH/OneDrive/Desktop/skin analyzer/backend/.env")
test_key("c:/Users/TRUE TECH/OneDrive/Desktop/skin analyzer/.env")
