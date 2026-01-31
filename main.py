import os
from dotenv import load_dotenv
from google import genai

load_dotenv()
key = os.environ.get("GEMINI_API_KEY")

if key == None:
    raise RuntimeError("API key not found...")

client = genai.Client(api_key=key)

res = client.models.generate_content(model="gemini-2.5-flash", contents="Why is Boot.dev such a great place to learn backend development? Use one paragraph maximum.")

print(res.text)

def main():
    print("Hello from agentai!")


if __name__ == "__main__":
    main()
