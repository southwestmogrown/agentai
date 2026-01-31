import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types

load_dotenv()

def get_and_check_key(key_name):
    key = os.environ.get(key_name)
    if key == None:
        raise RuntimeError("API key not found...")
    return key

def parse_user_prompt():
    parser = argparse.ArgumentParser(description="Chatbot")
    parser.add_argument("user_prompt", type=str, help="User Prompt")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    prompt = parser.parse_args()
    return prompt

def prompt_client(prompt, key):
    client = genai.Client(api_key=key)

    messages = [types.Content(role="user", parts=[types.Part(text=prompt.user_prompt)])]
    res = client.models.generate_content(model="gemini-2.5-flash", contents=messages)

    if res.usage_metadata == None:
        raise RuntimeError("Response failed...")

    if prompt.verbose:
        print(f"User prompt: {prompt.user_prompt}")
        print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {res.usage_metadata.candidates_token_count}")
        
    print(res.text)


def main():
    user_prompt = parse_user_prompt()
    gemini_key = get_and_check_key("GEMINI_API_KEY")

    prompt_client(user_prompt, gemini_key)


if __name__ == "__main__":
    main()
