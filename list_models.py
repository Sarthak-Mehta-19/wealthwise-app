import os
from dotenv import load_dotenv
import google.generativeai as genai

# Load your vault
load_dotenv()
genai.configure(api_key=os.getenv('GEMINI_API_KEY'))

print("✅ Your API Key is valid! You have access to these text models:")
print("-" * 50)

# Ask Google for the exact list of available models
for m in genai.list_models():
    if 'generateContent' in m.supported_generation_methods:
        # We strip the "models/" prefix to give you the exact string to copy-paste
        print(m.name.replace('models/', ''))