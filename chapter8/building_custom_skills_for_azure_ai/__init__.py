import logging
import azure.functions as func
import json
from azure.core.credentials import AzureKeyCredential
from azure.ai.formrecognizer import DocumentAnalysisClient
import base64

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Custom Document Skill Function processed a request.')

    try:
        req_body = req.get_json()
        # Extract the document content (assuming Base64 encoded)
        document_content = req_body['values'][0]['data']['document']

        # Decode the Base64 content
        document_bytes = base64.b64decode(document_content)

        # Replace with your endpoint, key, and custom model ID
        endpoint = "<your-endpoint>"
        key = "<your-key>"
        model_id = "<your-custom-model-id>"

        document_analysis_client = DocumentAnalysisClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key)
        )

        # Analyze the document
        poller = document_analysis_client.begin_analyze_document(
            model_id=model_id,
            document=document_bytes
        )
        result = poller.result()

        # Process the result
        extracted_data = {}
        for document in result.documents:
            for name, field in document.fields.items():
                extracted_data[name] = field.value if field.value else field.content

        # Prepare the response
        response = {
            "values": [
                {
                    "recordId": req_body['values'][0]['recordId'],
                    "data": {
                        "processedText": json.dumps(extracted_data)
                    }
                }
            ]
        }

        return func.HttpResponse(
            json.dumps(response),
            mimetype="application/json",
            status_code=200
        )

    except Exception as e:
        logging.error(f"Error: {str(e)}")
        return func.HttpResponse(
            f"Error processing the document: {str(e)}",
            status_code=400
        )
