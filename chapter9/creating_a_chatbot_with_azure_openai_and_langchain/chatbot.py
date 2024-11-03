import os
from dotenv import load_dotenv
from langchain.chat_models import AzureChatOpenAI
from langchain.schema import HumanMessage

# Load environment variables
load_dotenv()

# Set up OpenAI API credentials
openai_api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai_api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai_api_version = os.getenv("AZURE_OPENAI_API_VERSION")
deployment_name = os.getenv("AZURE_OPENAI_GPT35_DEPLOYMENT_NAME")

# Initialize the GPT-3.5 Turbo model
model = AzureChatOpenAI(
    openai_api_base=openai_api_base,
    openai_api_version=openai_api_version,
    deployment_name=deployment_name,
    openai_api_key=openai_api_key,
    openai_api_type="azure"
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
