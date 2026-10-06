import os

from dotenv import load_dotenv
from openai import OpenAI
import argparse

def main():
    load_dotenv()
    api_key = os.environ.get("OPENROUTER_API_KEY")

    if api_key == None:
        raise RuntimeError("api key not found")

    client = OpenAI(
        base_url="https://openrouter.ai/api/v1",
        api_key=api_key,
    )

    parser = argparse.ArgumentParser(description="AI Agent")
    parser.add_argument("user_prompt", type=str, help="User prompt")
    args = parser.parse_args()

    messages = [{"role": "user", "content": args.user_prompt},]
    generate_response(client, messages)

def generate_response(client, messages):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
    )
    if response.usage != None:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")
        print("Response:")
    else:
        raise RuntimeError("There is no token usage")
    print(response.choices[0].message.content)

if __name__ == "__main__":
    main()
