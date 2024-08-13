import requests
import os
import json
import pandas as pd
from azure.storage.blob import BlobServiceClient, BlobClient, ContainerClient

endpoint = 'YOUR_TEXT_ANALYTICS_ENDPOINT'
key = 'YOUR_TEXT_ANALYTICS_KEY'

headers = {"Ocp-Apim-Subscription-Key": key}
sentiment_url = endpoint + "/text/analytics/v3.0/sentiment"

storage_account_name = 'YOUR_STORAGE_ACCOUNT_NAME'
storage_account_key = 'YOUR_STORAGE_ACCOUNT_KEY'
input_container_name = 'input'
output_container_name = 'output'
input_blob_name = 'customer-feedback.csv'
output_blob_name = 'sentiment-analysis-results.json'

blob_service_client = BlobServiceClient(account_url=f"https://{storage_account_name}.blob.core.windows.net", credential=storage_account_key)
input_blob_client = blob_service_client.get_blob_client(container=input_container_name, blob=input_blob_name)

downloaded_blob = input_blob_client.download_blob().readall()
with open('customer-feedback.csv', 'wb') as f:
    f.write(downloaded_blob)

df = pd.read_csv('customer-feedback.csv')
documents = {"documents": [{"id": str(i), "language": "en", "text": row["feedback"]} for i, row in df.iterrows()]}
response = requests.post(sentiment_url, headers=headers, json=documents)
sentiments = response.json()
print(json.dumps(sentiments, indent=2))
with open('sentiment-analysis-results.json', 'w') as f:
    json.dump(sentiments, f)

output_blob_client = blob_service_client.get_blob_client(container=output_container_name, blob=output_blob_name)
with open('sentiment-analysis-results.json', 'rb') as data:
    output_blob_client.upload_blob(data, overwrite=True)

print("Sentiment analysis results have been uploaded to the output container.") 
