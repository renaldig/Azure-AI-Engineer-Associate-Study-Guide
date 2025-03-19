import os
import sys
import uuid
import requests
from dotenv import load_dotenv

def get_translator_credentials():
    load_dotenv()
    """
    Retrieves Azure Translator credentials from environment variables.
    """
    subscription_key = os.getenv('TRANSLATOR_SUBSCRIPTION_KEY')
    region = os.getenv('TRANSLATOR_REGION')

    if not subscription_key or not region:
        print("Error: TRANSLATOR_SUBSCRIPTION_KEY and TRANSLATOR_REGION environment variables must be set.")
        sys.exit(1)

    return subscription_key, region

def translate_text(subscription_key, region, text, from_lang, to_langs):
    """
    Translates text from a source language to one or multiple target languages using Azure Translator Text API.

    Args:
        subscription_key (str): Azure Translator subscription key.
        region (str): Azure service region.
        text (str): The text to translate.
        from_lang (str): Source language code (e.g., 'en').
        to_langs (list): List of target language codes (e.g., ['es', 'fr']).
    """
    endpoint = "https://api.cognitive.microsofttranslator.com"
    path = '/translate?api-version=3.0'
    params = f"&from={from_lang}" + ''.join([f"&to={lang}" for lang in to_langs])
    constructed_url = endpoint + path + params

    headers = {
        'Ocp-Apim-Subscription-Key': subscription_key,
        'Ocp-Apim-Subscription-Region': region,
        'Content-type': 'application/json',
        'X-ClientTraceId': str(uuid.uuid4())
    }

    body = [{
        'text': text
    }]

    try:
        response = requests.post(constructed_url, headers=headers, json=body)
        response.raise_for_status()
        result = response.json()

        for translation in result[0]['translations']:
            print(f"Translated into {translation['to']}: {translation['text']}")
    except requests.exceptions.RequestException as e:
        print(f"Request failed: {e}")
    except KeyError:
        print("Unexpected response structure.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    """
    Main function to prompt user for input and perform text translation.
    """
    subscription_key, region = get_translator_credentials()

    print("Azure Translator Text API Demo")
    text = input("Enter the text you want to translate: ").strip()
    if not text:
        print("No text entered. Exiting.")
        sys.exit(1)

    from_lang = input("Enter the source language code (e.g., 'en' for English): ").strip()
    if not from_lang:
        from_lang = 'en'  # Default to English if not provided

    to_langs_input = input("Enter target language codes separated by commas (e.g., 'es,fr'): ").strip()
    to_langs = [lang.strip() for lang in to_langs_input.split(',') if lang.strip()]
    if not to_langs:
        print("No target languages entered. Exiting.")
        sys.exit(1)

    translate_text(subscription_key, region, text, from_lang, to_langs)

if __name__ == "__main__":
    main()
