from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient

# Replace with your search service details
search_service_endpoint = "https://<your-search-service-name>.search.windows.net"
index_name = "invoices-index"
api_key = "<your-search-service-api-key>"

search_client = SearchClient(
    endpoint=search_service_endpoint,
    index_name=index_name,
    credential=AzureKeyCredential(api_key)
)

# Perform a search
results = search_client.search(search_text="*")

# Print the results
for result in results:
    print(result)
