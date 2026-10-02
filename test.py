import os
import requests
from dotenv import load_dotenv

load_dotenv()

api_key = os.getenv("GROQ_API_KEY")

if not api_key:
    print("GROQ_API_KEY is not found in your .env file!")
else:
    print(f"Key found: {api_key[:8]}...")
    url = "https://api.groq.com/openai/v1/models"
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    response = requests.get(url, headers=headers)
    
    if response.status_code == 200:
        models = [m['id'] for m in response.json().get('data', [])]
        print("\n✅ Available Models for your API Key:")
        for m in models:
            print(f" - {m}")
    else:
        print(f"\n Error {response.status_code}: {response.text}")