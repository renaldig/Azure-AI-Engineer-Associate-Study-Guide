from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Replace with your Key Vault name
key_vault_name = "contosokeyvault"
kv_uri = f"https://{key_vault_name}.vault.azure.net/"

# Authenticate to Azure using DefaultAzureCredential
credential = DefaultAzureCredential()

# Create a SecretClient to interact with the Key Vault
client = SecretClient(vault_url=kv_uri, credential=credential)

# Replace with your secret name
secret_name = "openai-api-key"

# Retrieve the secret from the Key Vault
retrieved_secret = client.get_secret(secret_name)

# Use the secret value
openai_api_key = retrieved_secret.value
