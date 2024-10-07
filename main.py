import os
import requests
from dotenv import load_dotenv
import pyttsx3

load_dotenv()

# Load Azure credentials from .env
TRANSLATOR_KEY = os.getenv("TRANSLATOR_KEY")
TRANSLATOR_ENDPOINT = os.getenv("TRANSLATOR_ENDPOINT")
TRANSLATOR_LOCATION = os.getenv("TRANSLATOR_LOCATION")

engine = pyttsx3.init()

def translate_text(text, target_language):
    # Set up the translation request
    path = '/translate?api-version=3.0'
    params = f'&to={target_language}'
    constructed_url = TRANSLATOR_ENDPOINT + path + params
    
    headers = {
        'Ocp-Apim-Subscription-Key': TRANSLATOR_KEY,
        'Ocp-Apim-Subscription-Region': TRANSLATOR_LOCATION,
        'Content-type': 'application/json'
    }
    
    body = [{
        'text': text
    }]
    
    # Make the translation request
    response = requests.post(constructed_url, headers=headers, json=body)
    response.raise_for_status()  # Raise an error for bad responses
    translation = response.json()
    
    # Extract the translated text
    translated_text = translation[0]['translations'][0]['text']
    return translated_text

def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    # Input text and target language
    text = input("Enter text to translate: ")
    target_language = input("Enter target language (e.g., 'fr' for French, 'es' for Spanish): ")
    
    # Perform translation
    translated_text = translate_text(text, target_language)
    print(f"Translated text: {translated_text}")
    
    # Read out the translated text
    text_to_speech(translated_text)
