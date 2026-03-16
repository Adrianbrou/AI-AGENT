import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
api_key = os.environ.get("GEMINI_API_KEY")
if not api_key:
    raise RuntimeError("API key not in .env file")

client = genai.Client(api_key=api_key)

def main():
    print("Hello from ai-agent!")


if __name__ == "__main__":
    main()
