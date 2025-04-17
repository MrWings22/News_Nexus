import requests
import json

PERSPECTIVE_API_KEY = "AIzaSyDpv06_Q3VuOYpr-DW2dpNnLSVfZwFaVH4"  # Replace with your key


def analyze_comment(comment_text):
    url = "https://commentanalyzer.googleapis.com/v1alpha1/comments:analyze"
    
    data = {
        'comment': {'text': comment_text},
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


