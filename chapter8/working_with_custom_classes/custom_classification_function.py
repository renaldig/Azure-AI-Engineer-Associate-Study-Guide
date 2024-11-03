import logging
import azure.functions as func
import json
from azure.core.credentials import AzureKeyCredential
from azure.ai.textanalytics import TextAnalyticsClient

def main(req: func.HttpRequest) -> func.HttpResponse:
    logging.info('Custom Classification Function processed a request.')

    try:
        req_body = req.get_json()
        document_text = req_body['values'][0]['data']['text']

        # Replace with your endpoint and key
        endpoint = "<your-text-analytics-endpoint>"
        key = "<your-text-analytics-key>"
        project_name = "<your-project-name>"
        deployment_name = "<your-deployment-name>"

        # Initialize Text Analytics client
        text_analytics_client = TextAnalyticsClient(
            endpoint=endpoint,
            credential=AzureKeyCredential(key)
        )

        # Analyze the document
        poller = text_analytics_client.begin_analyze_document(
            project_name=project_name,
            deployment_name=deployment_name,
            documents=[document_text]
        )
        result = poller.result()

        # Extract the classification categories
        classifications = result[0].classifications
        categories = [c.category for c in classifications]

        # Prepare the response
        response = {
            "values": [
                {
                    "recordId": req_body['values'][0]['recordId'],
                    "data": {
                        "categories": categories
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
