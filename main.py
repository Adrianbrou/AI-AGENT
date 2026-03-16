import os,argparse
from dotenv import load_dotenv
from google import genai
from google.genai import types


def main():
    #load the .env 
    load_dotenv()
    #handle any possible error on loading the api key from .env
    api_key = os.environ.get("GEMINI_API_KEY")
    if not api_key:
        raise RuntimeError("API key not in .env file")
    #create client object that we use to make calls on the api 
    client = genai.Client(api_key=api_key)
    #add arguments parameter for user input
    parser = argparse.ArgumentParser(description="ai agent")
    parser.add_argument("user_prompt", type=str, help="Prompt to send to Gemini")
    parser.add_argument("--verbose", action="store_true", help="Enable verbose output")


    args = parser.parse_args()
    

    # Create a new list of types.Content, and set the user's prompt as the only message
    messages = [types.Content(role="user", parts=[types.Part(text=args.user_prompt)])]

    #this is a generate content response object
    response = client.models.generate_content(model="gemini-2.5-flash",contents = messages)
    """  PROPRETIES     """
    #The user's prompt: 

    # usage_metadata: this proprety help to now how match token tou have consumned from the agent
    if not response.usage_metadata:
        raise RuntimeError("API key not found in .env file")
    if args.verbose:
        print(f"User prompt: {args.user_prompt}")
        print("Prompt tokens:", response.usage_metadata.prompt_token_count)
        print("Response tokens:", response.usage_metadata.candidates_token_count)

    # candidates_token_count property, showing the number of tokens in the model's response.

    #.text proprety to get the text response from the API
    print(response.text)
  

if __name__ == "__main__":
    main()
