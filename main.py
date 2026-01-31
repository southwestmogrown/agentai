import os
import argparse
from dotenv import load_dotenv
from google import genai

load_dotenv()

def get_and_check_key(key_name):
    key = os.environ.get(key_name)
    if key == None:
        raise RuntimeError("API key not found...")
    return key

def parse_user_prompt():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    prompt = parser.parse_args()
    return prompt

def prompt_client(prompt, key):
    client = genai.Client(api_key=key)
    res = client.models.generate_content(model="gemini-2.5-flash", contents=prompt.user_prompt)

    if res.usage_metadata == None:
        raise RuntimeError("Response failed...")

    print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
    print(f"Response tokens: {res.usage_metadata.candidates_token_count}")
    print(res.text)


def main():
    user_prompt = parse_user_prompt()
    gemini_key = get_and_check_key("GEMINI_API_KEY")

    prompt_client(user_prompt, gemini_key)


if __name__ == "__main__":
    main()
