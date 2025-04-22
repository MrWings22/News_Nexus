import requests
import json
from google.cloud import translate_v2 as translate
from google.cloud import language_v1

PERSPECTIVE_API_KEY = "AIzaSyDpv06_Q3VuOYpr-DW2dpNnLSVfZwFaVH4"  # Replace with your key
# Function to detect language using LibreTranslate (FREE)
def detect_language(text):
    try:
        url = "https://libretranslate.com/detect"
        response = requests.post(url, data={'q': text})
        response.raise_for_status()
        detected = response.json()
        if detected:
            return detected[0]['language']
        else:
            return 'en'
    except Exception as e:
        print(f"Language detection failed: {e}")
        return 'en'

# Function to translate text to English using LibreTranslate (FREE)
def translate_to_english(text, source_language):
    if source_language == 'en':
        return text  # No need to translate
    try:
        url = "https://libretranslate.com/translate"
        payload = {
            'q': text,
            'source': source_language,
            'target': 'en',
            'format': 'text'
        }
        response = requests.post(url, data=payload)
        response.raise_for_status()
        return response.json()['translatedText']
    except Exception as e:
        print(f"Translation failed: {e}")
        return text  # Fallback to original text

def analyze_comment(comment_text):
    language = detect_language(comment_text)  # Detect the language of the comment
    translated_text = translate_to_english(comment_text, language)  # Translate if needed

    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    
    data = {
        'comment': {'text': translated_text},
        'requestedAttributes': {'TOXICITY': {}}
    }

    params = {
        'key': PERSPECTIVE_API_KEY
    }

    # Send the request to the Perspective API
    response = requests.post(url, json=data, params=params)
    response.raise_for_status()  # Will raise error for bad responses

    
    # Log the entire response to debug
    print("API Response:", response.json())

    result = response.json()

    try:
        # Check if the toxicity score is present
        score = result['attributeScores']['TOXICITY']['summaryScore']['value']
        return score
    except KeyError:
        print("Error: Toxicity score not found in the response.")
        return None  # Handle errors gracefully if the key is missing


