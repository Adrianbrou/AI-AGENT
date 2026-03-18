import os
import argparse
from prompts.prompts import system_prompt
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    """
    Entry point for the Gemini AI agent CLI.

    Loads the Gemini API key from a .env file, accepts a user prompt via
    the command line, sends it to the Gemini model, and prints the response.
    Optionally prints token usage metadata in verbose mode.

    CLI Usage:
        uv run main.py "your prompt here"
        uv run main.py "your prompt here" --verbose

    Environment:
        GEMINI_API_KEY (str): Required. Your Gemini API key, stored in .env.

    Raises:
        RuntimeError: If GEMINI_API_KEY is missing from the environment.
        RuntimeError: If the API response contains no usage metadata.
    """

    # Load environment variables from .env into os.environ.
    load_dotenv()

    # Retrieve the API key — fail fast if it's missing rather than getting
    # a cryptic error later when the API call is made.
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("API key not found in .env file")

    # The client is the gateway to all Gemini API calls.
    client = genai.Client(api_key=api_key)

    # Set up the CLI — user_prompt is required, --verbose is optional.
    parser = argparse.ArgumentParser(description="Gemini AI agent")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")
    args = parser.parse_args()

    # Gemini expects a list of Content objects representing the conversation.
    # Each Content has a role ("user" or "model") and a list of Parts (text, images, etc.).
    # Here we start a fresh single-turn conversation with the user's prompt.
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    # Send the message to Gemini and get a GenerateContentResponse object.
    response = client.models.generate_content(
        model="gemini-2.5-flash",
        contents=messages,
        config=types.GenerateContentConfig(system_instruction=system_prompt)
    )

    # usage_metadata tracks token consumption for this request.
    # prompt_token_count  — tokens used by the input (our messages).
    # candidates_token_count — tokens used by the model's response.
    if not response.usage_metadata:
        raise RuntimeError("No usage metadata returned from API")

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
        print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

    # .text is a convenience property that returns the model's response as a string.
    print(response.text)


if __name__ == "__main__":
    main()