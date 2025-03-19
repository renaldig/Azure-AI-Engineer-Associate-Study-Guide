import requests
import json
import pandas as pd
from azure.storage.blob import BlobServiceClient

endpoint = 'YOUR_TEXT_ANALYTICS_ENDPOINT'
key = 'YOUR_TEXT_ANALYTICS_KEY'
headers = {"Ocp-Apim-Subscription-Key": key}
sentiment_url = f"{endpoint}/text/analytics/v3.0/sentiment"

storage_account_name = 'YOUR_STORAGE_ACCOUNT_NAME'
storage_account_key = 'YOUR_STORAGE_ACCOUNT_KEY'
input_container_name = 'input'
output_container_name = 'output'
input_blob_name = 'customer-feedback.csv'
output_blob_name = 'sentiment-analysis-results.json'

blob_service_client = BlobServiceClient(
    account_url=f"https://{storage_account_name}.blob.core.windows.net",
    credential=storage_account_key
)

try:
    input_blob_client = blob_service_client.get_blob_client(
        container=input_container_name, blob=input_blob_name
    )
    downloaded_blob = input_blob_client.download_blob().readall()
    with open(input_blob_name, 'wb') as f:
        f.write(downloaded_blob)
    print(f"Downloaded blob '{input_blob_name}' successfully.")
except Exception as e:
    print(f"Error downloading blob: {e}")
    raise

try:
    df = pd.read_csv(input_blob_name, encoding='utf-8')
    df = df[df['feedback'].str.strip().astype(bool)]
    documents = {
        "documents": [
            {"id": str(i), "language": "en", "text": row["feedback"]}
            for i, row in df.iterrows()
        ]
    }
    print("JSON payload to be sent:")
    print(json.dumps(documents, indent=2))
except Exception as e:
    print(f"Error processing CSV file: {e}")
    raise

try:
    response = requests.post(sentiment_url, headers=headers, json=documents)
    if response.status_code != 200:
        print("Error response content:")
        print(response.text)
    response.raise_for_status()
    sentiments = response.json()
    print("Sentiment analysis response:")
    print(json.dumps(sentiments, indent=2))
except Exception as e:
    print(f"Error calling Text Analytics API: {e}")
    raise


results_filename = 'sentiment-analysis-results.json'
try:
    with open(results_filename, 'w') as f:
        json.dump(sentiments, f)
    print(f"Sentiment analysis results saved to {results_filename}.")
except Exception as e:
    print(f"Error saving results to file: {e}")
    raise

try:
    output_blob_client = blob_service_client.get_blob_client(
        container=output_container_name, blob=output_blob_name
    )
    with open(results_filename, 'rb') as data:
        output_blob_client.upload_blob(data, overwrite=True)
    print("Sentiment analysis results have been uploaded to the output container.")
except Exception as e:
    print(f"Error uploading results to blob storage: {e}")
    raise