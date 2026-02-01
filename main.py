import os
import argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types
from functions.call_functions import *
from prompts import *

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
    count = 0
    for _ in range(20):
        count += 1
        res = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=messages,
            config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt
            )
        )

        if res.candidates is not None:
            for c in res.candidates:
                messages.append(c.content)

        if res.usage_metadata == None:
            raise RuntimeError("Response failed...")


        if prompt.verbose:
            print(f"User prompt: {prompt.user_prompt}")
            print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {res.usage_metadata.candidates_token_count}")

        if not res.function_calls:
            print("Response:")
            print(res.text)
            return

        func_results = []
        for call in res.function_calls:
            func_res = call_function(call)
            if (
                not func_res.parts
                or not func_res.parts[0].function_response
                or not func_res.parts[0].function_response.response
            ):
                raise RuntimeError(f"Empty function response for {call.name}")
            
            if prompt.verbose:
                print(f"-> {func_res.parts[0].function_response.response}")
            func_results.append(func_res.parts[0])

        messages.append(types.Content(role="user", parts=func_results))
    
    print("Maximum number of prompts reached")
    exit(1)



def main():
    user_prompt = parse_user_prompt()
    gemini_key = get_and_check_key("GEMINI_API_KEY")

    prompt_client(user_prompt, gemini_key)


if __name__ == "__main__":
    main()
