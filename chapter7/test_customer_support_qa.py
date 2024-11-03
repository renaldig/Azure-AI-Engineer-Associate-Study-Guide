import requests
import json

# Replace the placeholders with your actual values
endpoint = "https://<your-resource-name>.cognitiveservices.azure.com"
api_key = "<your-api-key>"
project_name = "CustomerSupportQA"
deployment_name = "CustomerSupportQADep"

# The endpoint for calling the deployed question answering model
url = f"{endpoint}/language/:query-knowledgebases?api-version=2021-10-01"

# Headers including the API key
headers = {
    "Ocp-Apim-Subscription-Key": api_key,
    "Content-Type": "application/json"
}

# The question to ask
question = "How can I track my shipment?"

# The data to send in the request
data = {
    "question": question,
    "top": 1,
    "confidenceScoreThreshold": 0.2,
    "includeUnstructuredSources": True,
    "shortAnswerOptions": {
        "confidenceScoreThreshold": 0.2,
        "top": 1,
        "answerSpanRequest": {
            "enable": True,
            "confidenceScoreThreshold": 0.2,
            "topAnswersWithSpan": 1
        }
    },
    "knowledgeBaseQuestionAnsweringOptions": {
        "enable": True
    },
    "projectName": project_name,
    "deploymentName": deployment_name
}

# Send the request
response = requests.post(url, headers=headers, json=data)
result = response.json()

# Print the result
print(json.dumps(result, indent=2))
