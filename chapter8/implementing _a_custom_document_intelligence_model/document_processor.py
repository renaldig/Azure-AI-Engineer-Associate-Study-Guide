from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient

# Replace with your endpoint, key, and composed model ID
endpoint = "<your-endpoint>"
key = "<your-key>"
model_id = "<your-composed-model-id>"

# Initialize the client
document_analysis_client = DocumentAnalysisClient(
    endpoint=endpoint, credential=AzureKeyCredential(key)
)

# List of document file names
document_files = ["TestInvoice.pdf", "TestReceipt.pdf", "TestPurchaseOrder.pdf"]

for document_file in document_files:
    with open(document_file, "rb") as doc:
        poller = document_analysis_client.begin_analyze_document(
            model_id, doc
        )
        result = poller.result()

        for idx, analyzed_doc in enumerate(result.documents):
            print(f"----- {document_file} Document {idx + 1} -----")
            for name, field in analyzed_doc.fields.items():
                field_value = field.value if field.value else field.content
                print(f"{name}: {field_value} (Confidence: {field.confidence})")
