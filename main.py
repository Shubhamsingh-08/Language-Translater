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

# Supported languages (can be expanded as needed)
supported_languages = {
    'fr': 'French',
    'es': 'Spanish',
    'de': 'German',
    'it': 'Italian',
    'ja': 'Japanese',
    'ko': 'Korean',
    'zh-Hans': 'Chinese (Simplified)',
    'ru': 'Russian',
    'pt': 'Portuguese',
    'hi': 'Hindi'
}

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
    
    body = [{'text': text}]
    
    # Make the translation request
    response = requests.post(constructed_url, headers=headers, json=body)
    response.raise_for_status()  # Raise an error for bad responses
    translation = response.json()
    
    # Extract the translated text
    translated_text = translation[0]['translations'][0]['text']
    return translated_text

def text_to_speech(text, lang='en'):
    # Set language-specific voice if available
    voices = engine.getProperty('voices')
    
    for voice in voices:
        if lang in voice.languages:
            engine.setProperty('voice', voice.id)
            break
    
    engine.say(text)
    engine.runAndWait()

if __name__ == "__main__":
    # Input text and target language
    text = input("Enter text to translate: ")
    
    print("Supported languages:")
    for code, language in supported_languages.items():
        print(f"{code}: {language}")
    
    target_language = input("Enter target language code: ").strip()
    
    if target_language not in supported_languages:
        print("Unsupported language code.")
    else:
        # Perform translation
        translated_text = translate_text(text, target_language)
        print(f"Translated text: {translated_text}")
        
        # Read out the translated text
        text_to_speech(translated_text, target_language)
