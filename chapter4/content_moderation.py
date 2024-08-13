import os
from azure.ai.contentsafety import ContentSafetyClient
from azure.core.credentials import AzureKeyCredential
from azure.core.exceptions import HttpResponseError

def analyze_text(input_text):
    key = os.environ["CONTENT_SAFETY_KEY"]
    endpoint = os.environ["CONTENT_SAFETY_ENDPOINT"]
    client = ContentSafetyClient(endpoint, AzureKeyCredential(key))

    try:
        response = client.analyze_text({"data": input_text})
        for category_analysis in response.categories_analysis:
            print(f"Category: {category_analysis.category}, Severity: {category_analysis.severity}")
    except HttpResponseError as e:
        print("An error occurred:", e.message)

def handle_action(category, severity):
    if category == "Hate" and severity >= 0.5:
        print("Hate speech detected. Initiating content flagging and review process.")
    elif category == "SelfHarm" and severity >= 0.5:
        print("Self-harm content detected. Sending alert to support team.")
    elif category == "Sexual" and severity >= 0.5:
        print("Sexual content detected. Removing content automatically.")
    elif category == "Violence" and severity >= 0.5:
        print("Violent content detected. Escalating for immediate review.")
    else:
        print("Content is safe or below the action threshold.")

if __name__ == "__main__":
    input_text = "Your text here"
    analyze_text(input_text)
