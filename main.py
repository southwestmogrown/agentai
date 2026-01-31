import os
import argparse
from dotenv import load_dotenv
from google import genai


def main():
    load_dotenv()
    key = os.environ.get("GEMINI_API_KEY")
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    prompt = parser.parse_args()

    if key == None:
        raise RuntimeError("API key not found...")

    client = genai.Client(api_key=key)

    res = client.models.generate_content(model="gemini-2.5-flash", contents=prompt.user_prompt)

    if res.usage_metadata == None:
        raise RuntimeError("Response failed...")

    print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {res.usage_metadata.candidates_token_count}")
    print(res.text)


if __name__ == "__main__":
    main()
