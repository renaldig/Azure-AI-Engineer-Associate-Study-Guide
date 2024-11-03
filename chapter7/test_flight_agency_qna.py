import requests
import json

# Replace the placeholders with your actual values
endpoint = "https://<your-resource-name>.cognitiveservices.azure.com"
api_key = "<your-api-key>"
project_name = "FlightAgencyQnA"
deployment_name = "<your-deployment-name>"

# The endpoint for calling the deployed question answering model
url = f"{endpoint}/language/:query-knowledgebases?api-version=2021-10-01"

# Headers including the API key
headers = {
    "Ocp-Apim-Subscription-Key": api_key,
    "Content-Type": "application/json"
}

# Initial question
question = "How can I cancel a reservation?"

# The data to send in the initial request
data = {
    "question": question,
    "top": 1,
    "userId": "Default",
    "isTest": False,
    "context": {},
    "projectName": project_name,
    "deploymentName": deployment_name
}

# Send the initial request
response = requests.post(url, headers=headers, json=data)
initial_result = response.json()

# Print the initial result
print("Initial Response:")
print(json.dumps(initial_result, indent=2))

# Check if there are follow-up prompts
if initial_result["answers"] and initial_result["answers"][0]["context"] and initial_result["answers"][0]["context"]["prompts"]:
    # Get the first follow-up prompt
    follow_up_prompt = initial_result["answers"][0]["context"]["prompts"][0]["displayText"]
    qna_id = initial_result["answers"][0]["id"]
    
    # Prepare follow-up request data
    follow_up_data = {
        "question": follow_up_prompt,
        "top": 1,
        "userId": "Default",
        "isTest": False,
        "qnaId": qna_id,
        "context": {
            "previousQnAId": qna_id,
            "previousUserQuery": question
        },
        "projectName": project_name,
        "deploymentName": deployment_name
    }
    
    # Send the follow-up request
    follow_up_response = requests.post(url, headers=headers, json=follow_up_data)
    follow_up_result = follow_up_response.json()
    
    # Print the follow-up result
    print("\nFollow-Up Response:")
    print(json.dumps(follow_up_result, indent=2))
else:
    print("No follow-up prompts available.")
