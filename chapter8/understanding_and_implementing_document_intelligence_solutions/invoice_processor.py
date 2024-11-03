from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import json

# Set up the endpoint and key variables
endpoint = "<your-endpoint>"
key = "<your-key>"

# Initialize the client
document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

# Open the invoice file
with open("sample-invoice.pdf", "rb") as invoice_file:
    poller = document_analysis_client.begin_analyze_document(
        "prebuilt-invoice", invoice_file
    )

result = poller.result()

# Extract and print the fields
invoices_data = []

for idx, document in enumerate(result.documents):
    print(f"----- Invoice {idx + 1} -----")
    invoice_info = {}
    for name, field in document.fields.items():
        field_value = field.value if field.value else field.content
        invoice_info[name] = field_value
        print(f"{name}: {field_value} (Confidence: {field.confidence})")
    invoices_data.append(invoice_info)

# Save the extracted data to a JSON file
with open("invoices.json", "w") as json_file:
    json.dump(invoices_data, json_file)
