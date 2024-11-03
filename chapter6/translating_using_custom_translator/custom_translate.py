# custom_translate.py

import os
import sys
import uuid
import requests
import json

def get_translator_credentials():
    """
    Retrieves Azure Translator credentials from environment variables.
    """
    subscription_key = os.environ.get('TRANSLATOR_SUBSCRIPTION_KEY')
    endpoint = os.environ.get('TRANSLATOR_ENDPOINT')
    region = os.environ.get('TRANSLATOR_REGION')

    if not subscription_key or not endpoint or not region:
        print("Error: TRANSLATOR_SUBSCRIPTION_KEY, TRANSLATOR_ENDPOINT, and TRANSLATOR_REGION environment variables must be set.")
        sys.exit(1)

    return subscription_key, endpoint, region

def translate_text(subscription_key, endpoint, region, text, from_lang, to_langs, category_id=None):
    """
    Translates text from a source language to one or multiple target languages using Azure Translator Text API with a custom model.

    Args:
        subscription_key (str): Azure Translator subscription key.
        endpoint (str): Azure Translator endpoint URL.
        region (str): Azure service region.
        text (str): The text to translate.
        from_lang (str): Source language code (e.g., 'en').
        to_langs (list): List of target language codes (e.g., ['de', 'es']).
        category_id (str, optional): Custom model's category ID. Defaults to None.
    """
    path = '/translate?api-version=3.0'
    params = f"&from={from_lang}" + ''.join([f"&to={lang}" for lang in to_langs])

    if category_id:
        # Ensure the category parameter starts with a '/'
        if not category_id.startswith('/'):
            category_id = f'/{category_id}'
        params += f"&category={category_id}"

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

        print("\nTranslation Results:")
        for translation in result[0]['translations']:
            print(f"Translated into {translation['to']}: {translation['text']}")
    except requests.exceptions.HTTPError as http_err:
        print(f"HTTP error occurred: {http_err} - {response.text}")
    except requests.exceptions.RequestException as req_err:
        print(f"Request exception occurred: {req_err}")
    except KeyError:
        print("Unexpected response structure. Please check the API response.")
    except Exception as e:
        print(f"An error occurred: {e}")

def main():
    """
    Main function to prompt user for input and perform text translation using a custom model.
    """
    subscription_key, endpoint, region = get_translator_credentials()

    print("Azure Custom Translator Demo")
    text = input("Enter the text you want to translate: ").strip()
    if not text:
        print("No text entered. Exiting.")
        sys.exit(1)

    from_lang = input("Enter the source language code (e.g., 'en' for English): ").strip()
    if not from_lang:
        from_lang = 'en'  # Default to English if not provided

    to_langs_input = input("Enter target language codes separated by commas (e.g., 'de,es'): ").strip()
    to_langs = [lang.strip() for lang in to_langs_input.split(',') if lang.strip()]
    if not to_langs:
        print("No target languages entered. Exiting.")
        sys.exit(1)

    use_custom_model = input("Do you want to use a custom translation model? (yes/no): ").strip().lower()
    category_id = None
    if use_custom_model in ['yes', 'y']:
        category_id = input("Enter your custom model's category ID: ").strip()
        if not category_id:
            print("No category ID entered. Proceeding with default model.")
            category_id = None

    translate_text(subscription_key, endpoint, region, text, from_lang, to_langs, category_id)

if __name__ == "__main__":
    main()
