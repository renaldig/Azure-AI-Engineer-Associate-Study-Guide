from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

# Authenticate with Azure
credential = DefaultAzureCredential()

# Connect to Azure Key Vault
key_vault_uri = "<YOUR_KEY_VAULT_URI_HERE>"
secret_client = SecretClient(vault_url=key_vault_uri, credential=credential)

# Retrieve a secret
secret_name = "AIKey"
retrieved_secret = secret_client.get_secret(secret_name)

print(f"The value of the secret '{secret_name}' is: '{retrieved_secret.value}'")