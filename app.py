import os
import requests
import pyttsx3
from dotenv import load_dotenv
import tkinter as tk  # Importing tkinter module
from ui import TranslatorApp

load_dotenv()

# Load Azure credentials from .env
TRANSLATOR_KEY = os.getenv("TRANSLATOR_KEY")
TRANSLATOR_ENDPOINT = os.getenv("TRANSLATOR_ENDPOINT")
TRANSLATOR_LOCATION = os.getenv("TRANSLATOR_LOCATION")

engine = pyttsx3.init()

def translate_text(text, target_language):
    path = '/translate?api-version=3.0'
    params = f'&to={target_language}'
    constructed_url = TRANSLATOR_ENDPOINT + path + params
    
    headers = {
        'Ocp-Apim-Subscription-Key': TRANSLATOR_KEY,
        'Ocp-Apim-Subscription-Region': TRANSLATOR_LOCATION,
        'Content-type': 'application/json'
    }
    
    body = [{'text': text}]
    
    response = requests.post(constructed_url, headers=headers, json=body)
    response.raise_for_status()
    translation = response.json()
    
    translated_text = translation[0]['translations'][0]['text']
    return translated_text

def text_to_speech(text):
    engine.say(text)
    engine.runAndWait()

def reset():
    # Reset any necessary state or values if needed
    pass

if __name__ == "__main__":
    root = tk.Tk()  # This line initializes the Tkinter window
    app = TranslatorApp(root, translate_text, reset)
    root.mainloop()
