import requests
import json

# Replace the placeholders with your actual values
endpoint = "https://<your-resource-name>.cognitiveservices.azure.com"
api_key = "<your-api-key>"
project_name = "TravelChatbotCLU"
deployment_name = "TravelChatbotDeployment"

# The endpoint for calling the deployed model
url = f"{endpoint}/language/:analyze-conversations?api-version=2022-10-01-preview"

# Headers including the API key
headers = {
    "Ocp-Apim-Subscription-Key": api_key,
    "Content-Type": "application/json"
}

# The data to send in the request
data = {
    "kind": "Conversation",
    "analysisInput": {
        "conversationItem": {
            "text": "I want to book a flight to New York next Monday",
            "id": "1",
            "participantId": "user1"
        }
    },
    "parameters": {
        "projectName": project_name,
        "deploymentName": deployment_name,
        "stringIndexType": "TextElement_V8"
    }
}

# Send the request
response = requests.post(url, headers=headers, json=data)
result = response.json()

# Print the result
print(json.dumps(result, indent=2))
