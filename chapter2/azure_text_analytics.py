import requests
import json

subscription_key = '<YOUR_SUBSCRIPTION_KEY_HERE>'
endpoint = '<YOUR_ENDPOINT_HERE>' + '/text/analytics/v3.1/'

headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Content-Type': 'application/json',
    'Accept': 'application/json'
}

body = {
    "documents": [
        {
            "language": "en",
            "id": "1",
            "text": "Hello world. This is a test for Azure AI Language."
        }
    ]
}

def key_phrase_extraction():
    key_phrase_url = endpoint + 'keyPhrases'
    response = requests.post(key_phrase_url, headers=headers, json=body)
    key_phrases = response.json()
    phrases = key_phrases['documents'][0]['keyPhrases']
    print("\nKey Phrases:")
    print(phrases)

def language_detection():
    language_url = endpoint + 'languages'
    response = requests.post(language_url, headers=headers, json=body)
    languages = response.json()
    detected_language = languages['documents'][0]['detectedLanguage']
    print("\nDetected Language:")
    print(detected_language)

key_phrase_extraction()
language_detection()
