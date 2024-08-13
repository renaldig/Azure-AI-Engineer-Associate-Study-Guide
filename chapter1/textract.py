# Import the required libraries
from azure.ai.textanalytics import TextAnalyticsClient
from azure.core.credentials import AzureKeyCredential

# Function to authenticate the Text Analytics client
def authenticate_client():
    key = "<YOUR_AUTHENTICATION_KEY_HERE>"
    endpoint = "<YOUR_ENDPOINT_HERE>"
    return TextAnalyticsClient(endpoint=endpoint, credential=AzureKeyCredential(key))

# Function to analyze sentiment
def sentiment_analysis(client):
    # Prompt the user to enter a sentence
    user_input = input("Enter a sentence to analyze sentiment: ")

    # Analyze the sentiment of the user's input
    response = client.analyze_sentiment(documents=[user_input])[0]
    print("Sentiment analysis result:")
    print("Overall sentiment:", response.sentiment)
    print("Scores: positive={0:.2f}; neutral={1:.2f}; negative={2:.2f}".format(
        response.confidence_scores.positive,
        response.confidence_scores.neutral,
        response.confidence_scores.negative,
    ))

# Main function
def main():
    client = authenticate_client()
    sentiment_analysis(client)

if __name__ == "__main__":
    main()
