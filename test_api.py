import google.generativeai as genai
import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()
print("Attempting to load GEMINI_API_KEY from .env file...")

try:
    # Get the API key from environment variables
    api_key = os.getenv("GEMINI_API_KEY")

    if not api_key:
        print("\n--- ERROR ---")
        print("GEMINI_API_KEY was not found in your environment.")
        print("Please ensure your .env file is in the correct directory and is formatted correctly.")
        print("----------------\n")
    else:
        # Configure the library with your API key
        genai.configure(api_key=api_key)
        print("API key loaded and configured successfully.")
        
        print("\nAttempting to list available models...")
        # List all models that support the 'generateContent' method
        found_models = False
        for m in genai.list_models():
            if 'generateContent' in m.supported_generation_methods:
                print(f"  - Found available model: {m.name}")
                found_models = True
        
        if found_models:
            print("\n--- SUCCESS ---")
            print("Your API key is working correctly!")
            print("-----------------\n")
        else:
            print("\n--- ERROR ---")
            print("API key is valid, but no models supporting 'generateContent' were found.")
            print("-----------------\n")


except Exception as e:
    print(f"\n--- AN ERROR OCCURRED ---")
    print(f"The test failed with the following error: {e}")
    print("---------------------------\n")