from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import json
import datetime

# Set up the endpoint and key variables
endpoint = "<your-endpoint>"
key = "<your-key>"

document_analysis_client = DocumentAnalysisClient(endpoint=endpoint, credential=AzureKeyCredential(key))

with open("sample-invoice.pdf", "rb") as invoice_file:
    poller = document_analysis_client.begin_analyze_document("prebuilt-invoice", invoice_file)

result = poller.result()

for idx, document in enumerate(result.documents):
    print(f"----- Invoice {idx + 1} -----")
    for name, field in document.fields.items():
        field_value = field.value if field.value else field.content
        print(f"{name}: {field_value} (Confidence: {field.confidence})")

# Function to serialize complex objects
def serialize_field(field_value):
    if isinstance(field_value, (datetime.datetime, datetime.date)):
        return field_value.isoformat()
    elif isinstance(field_value, (int, float, str, bool)):
        return field_value
    elif isinstance(field_value, list):
        return [serialize_field(item) for item in field_value]
    elif isinstance(field_value, dict):
        return {key: serialize_field(value) for key, value in field_value.items()}
    elif hasattr(field_value, '__dict__'):
        return {key: serialize_field(value) for key, value in vars(field_value).items()}
    else:
        return str(field_value)


invoices_data = []

for idx, document in enumerate(result.documents):
    invoice_info = {}
    for name, field in document.fields.items():
        field_value = field.value if field.value else field.content
        invoice_info[name] = serialize_field(field_value)
    invoices_data.append(invoice_info)

with open("invoices.json", "w") as json_file:
    json.dump(invoices_data, json_file, indent=4)