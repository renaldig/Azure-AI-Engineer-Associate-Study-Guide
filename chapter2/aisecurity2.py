from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential
from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

credential = DefaultAzureCredential()

key_vault_name = "<YOUR_KEY_VAULT_NAME_HERE>"  
key_vault_uri = f"https://{key_vault_name}.vault.azure.net/"
secret_client = SecretClient(vault_url=key_vault_uri, credential=credential)
secret_name = "<YOUR_SECRET_NAME_HERE>"  
ta_key = secret_client.get_secret(secret_name).value

ta_endpoint = "<YOUR_TEXT_ANALYTICS_ENDPOINT_HERE>"  
text_analytics_client = TextAnalyticsClient(endpoint=ta_endpoint, credential=AzureKeyCredential(ta_key))

documents = [
    "Microsoft was founded by Bill Gates and Paul Allen on April 4, 1975, to develop and sell BASIC interpreters for the Altair 8800."
]

response = text_analytics_client.recognize_entities(documents=documents)

for doc in response:
    print(f"Entities in document {doc.id}:")
    for entity in doc.entities:
        print(f"...Entity: {entity.text}, Category: {entity.category}, Subcategory: {entity.subcategory}, Confidence Score: {entity.confidence_score}")