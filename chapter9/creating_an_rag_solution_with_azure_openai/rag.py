import os
import openai
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import QueryType
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Set up OpenAI API credentials
openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = "2023-08-01-preview"  # Use the latest API version

# Define deployment names
chat_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_ID_CHAT")
embedding_deployment = os.getenv("AZURE_OPENAI_DEPLOYMENT_ID_EMBEDDING")

# Set up Azure AI Search credentials
search_endpoint = os.getenv("AZURE_AI_SEARCH_ENDPOINT")
search_api_key = os.getenv("AZURE_AI_SEARCH_API_KEY")
index_name = os.getenv("AZURE_AI_SEARCH_INDEX")

# Initialize the Azure Search client
search_client = SearchClient(
    endpoint=search_endpoint,
    index_name=index_name,
    credential=AzureKeyCredential(search_api_key)
)

def search_documents(query, top_k=5):
    """
    Search the Azure AI Search index for relevant documents based on the query.
    """
    results = search_client.search(search_text=query, query_type=QueryType.FULL, top=top_k)
    documents = [doc for doc in results]
    return documents

def get_embeddings(text):
    """
    Get embeddings for the input text using the embedding model.
    """
    response = openai.Embedding.create(
        engine=embedding_deployment,
        input=text
    )
    embeddings = response['data'][0]['embedding']
    return embeddings

def get_openai_response(prompt):
    """
    Get a response from the OpenAI chat model based on the prompt.
    """
    response = openai.Completion.create(
        engine=chat_deployment,
        prompt=prompt,
        max_tokens=150,
        temperature=0.7,
        top_p=0.9,
        frequency_penalty=0,
        presence_penalty=0
    )
    return response.choices[0].text.strip()

if __name__ == "__main__":
    user_query = input("Enter your query about available health plans: ")
    documents = search_documents(user_query)
    
    if not documents:
        print("No relevant documents found.")
    else:
        context = "\n".join([doc["content"] for doc in documents])
        prompt = f"Based on the following documents:\n\n{context}\n\nAnswer the question: {user_query}"
        answer = get_openai_response(prompt)
        print("\nAnswer:")
        print(answer)
