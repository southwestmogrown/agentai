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
    for _ in range(20):
        res = client.models.generate_content(
            model="gemini-2.5-flash", 
            contents=messages,
            config=types.GenerateContentConfig(
            tools=[available_functions], 
            system_instruction=system_prompt
            )
        )

        if res.usage_metadata == None:
            raise RuntimeError("Response failed...")

        if prompt.verbose:
            print(f"User prompt: {prompt.user_prompt}")
            print(f"Prompt tokens: {res.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {res.usage_metadata.candidates_token_count}")

            if res.function_calls is not None:
                for call in res.function_calls:
                    print(f"Calling function: {call.name}({call.args})")
                    func_res = call_function(call)
                    # print(func_res)

                    if len(func_res.parts) == 0 or func_res.parts is None:
                        raise Exception("the parts list is empty")
                    if func_res.parts[0].function_response is None:
                        raise Exception("the FunctionResponse is somehow None")
                    if func_res.parts[0].function_response.response is None:
                        raise Exception("The func response's func response is None")
                    print(f"-> {func_res.parts[0].function_response.response["result"]}")

        
        print(res.text)
    



def main():
    user_prompt = parse_user_prompt()
    gemini_key = get_and_check_key("GEMINI_API_KEY")

    prompt_client(user_prompt, gemini_key)


if __name__ == "__main__":
    main()
