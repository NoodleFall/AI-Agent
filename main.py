import argparse
import json
import os

from dotenv import load_dotenv
from openai import OpenAI

from call_function import available_functions
from prompts import system_prompt


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
    parser.add_argument("user_prompt", type=str, help="User prompt",)
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    messages = [
        {"role": "system", "content": system_prompt},
        {"role": "user", "content": args.user_prompt},
    ]
    if args.verbose:
            print(f"User prompt: {args.user_prompt}\n")

    generate_response(client, messages, args.verbose)


def generate_response(client, messages, verbose: bool):
    response = client.chat.completions.create(
        model="openrouter/free",
        messages=messages,
        tools = available_functions,
        temperature=0,
    )
    if not response.usage:
        raise RuntimeError("There is no token usage")

    if verbose:
        print(f"Prompt tokens: {response.usage.prompt_tokens}")
        print(f"Response tokens: {response.usage.completion_tokens}")

    message = response.choices[0].message
    if not message.tool_calls:
        print("Response:")
        print(message.content)
        return

    for tool_call in message.tool_calls:
        if tool_call.type != "function":
            continue
        function_args = json.loads(tool_call.function.arguments or "{}")
        print(f"Calling function: {tool_call.function.name}({function_args})")

if __name__ == "__main__":
    main()
