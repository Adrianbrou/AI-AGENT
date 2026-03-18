import os
import sys
import argparse
from config import MAX_ITERATIONS
from dotenv import load_dotenv
from google import genai
from google.genai import types
from prompts.prompts import system_prompt
from call_function.call_function import available_functions, call_function

# Maximum number of agentic loop iterations before we give up.
# This prevents runaway token consumption if the model never settles.



def main():
    """
    Entry point for the Gemini AI coding agent CLI.

    Boots the agent, sends the user's prompt, and runs an agentic loop:
    the model decides which tools to call, we execute them, feed the results
    back, and repeat — until the model produces a final text response or the
    iteration limit is hit.

    CLI Usage:
        uv run main.py "your prompt here"
        uv run main.py "your prompt here" --verbose

    Environment:
        GEMINI_API_KEY (str): Required. Stored in .env.

    Exits:
        0 — Normal exit after a final response.
        1 — Max iterations reached without a final response.
    """
    load_dotenv()

    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("GEMINI_API_KEY not found in .env file")

    client = genai.Client(api_key=api_key)

    # --- CLI arguments ---
    parser = argparse.ArgumentParser(description="Gemini AI coding agent")
    parser.add_argument("user_prompt", type=str, help="Task or question for the agent")
    parser.add_argument("--verbose", action="store_true", help="Print token usage and function results")
    args = parser.parse_args()

    if args.verbose:
        print(f"User prompt: {args.user_prompt}")

    # Seed the conversation with the user's prompt.
    # The messages list grows each iteration as the model and tools exchange turns.
    messages = [
        types.Content(role="user", parts=[types.Part(text=args.user_prompt)])
    ]

    # --- Agentic loop ---
    # Each iteration:
    #   1. Ask the model what to do next.
    #   2. Append the model's response to conversation history.
    #   3. If no function calls → model is done, print final answer and exit.
    #   4. Otherwise, execute each requested function and collect results.
    #   5. Append tool results to history so the model sees them next iteration.
    for _ in range(MAX_ITERATIONS):

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=messages,
            config=types.GenerateContentConfig(
                tools=[available_functions],
                system_instruction=system_prompt,
                temperature=0,
            ),
        )

        if args.verbose:
            print(f"Prompt tokens: {response.usage_metadata.prompt_token_count}")
            print(f"Response tokens: {response.usage_metadata.candidates_token_count}")

        # Keep the model's response in history so future iterations have context.
        for candidate in response.candidates:
            messages.append(candidate.content)

        # No function calls means the model has a final answer — we're done.
        if not response.function_calls:
            print(response.text)
            break

        # Execute each function the model requested and collect the results.
        function_responses = []
        for function_call in response.function_calls:
            result = call_function(function_call, args.verbose)
            if args.verbose:
                print(f"-> {result.parts[0].function_response.response}")
            function_responses.append(result.parts[0])

        # Feed tool results back into the conversation as a "user" turn.
        # The model will see these on the next iteration.
        messages.append(types.Content(role="user", parts=function_responses))

    else:
        # The for loop exhausted all iterations without hitting a break.
        print("Error: max iterations reached without a final response")
        sys.exit(1)


if __name__ == "__main__":
    main()