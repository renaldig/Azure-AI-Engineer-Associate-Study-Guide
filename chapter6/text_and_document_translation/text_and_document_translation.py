import requests
import uuid

# Replace these placeholders with your actual values
subscription_key = "<YOUR_SUBSCRIPTION_KEY>"
endpoint = "<YOUR_TRANSLATION_ENDPOINT>"

# The path and parameters for our translation request
path = '/translate?api-version=3.0'
params = '&from=en&to=es&to=fr'

# Construct the full URL
constructed_url = endpoint + path + params
headers = {
    'Ocp-Apim-Subscription-Key': subscription_key,
    'Content-type': 'application/json',
    'X-ClientTraceId': str(uuid.uuid4())
}

# Prepare the body with the text to be translated
body = [{
    'text': 'Hello, how are you?'
}]

# Make the POST request to the Translator API
response = requests.post(constructed_url, headers=headers, json=body)

# Parse the JSON response
result = response.json()

# Print out each translated result
for translation in result[0]['translations']:
    print(f"Translated into {translation['to']}: {translation['text']}")
