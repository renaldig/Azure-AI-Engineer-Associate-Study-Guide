import os
from dotenv import load_dotenv
from langchain_openai.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage

load_dotenv()

# Load environment variables
azure_endpoint = os.getenv("AZURE_OPENAI_ENDPOINT")
azure_api_key = os.getenv("AZURE_OPENAI_API_KEY")
deployment_name = os.getenv("AZURE_OPENAI_DEPLOYMENT_NAME")
api_version = os.getenv("AZURE_OPENAI_API_VERSION")

# Configure AzureChatOpenAI with the correct parameters
model = AzureChatOpenAI(
    azure_endpoint=azure_endpoint,
    azure_deployment=deployment_name,
    api_version=api_version,
    openai_api_key=azure_api_key
)

def chat():
    print("Welcome to the Customer Service Chatbot!")
    print("Type 'exit' or 'quit' to end the chat.\n")
    while True:
        user_input = input("You: ")
        if user_input.lower() in ["exit", "quit"]:
            print("Chatbot: Goodbye!")
            break

        message = HumanMessage(content=user_input)
        response = model([message])
        print(f"Chatbot: {response.content}\n")

if __name__ == "__main__":
    chat()
