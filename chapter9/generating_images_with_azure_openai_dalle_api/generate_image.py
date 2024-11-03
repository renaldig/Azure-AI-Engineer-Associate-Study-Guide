import os
from dotenv import load_dotenv
import openai

# Load environment variables
load_dotenv()

# Set up OpenAI API credentials
openai.api_type = "azure"
openai.api_key = os.getenv("AZURE_OPENAI_API_KEY")
openai.api_base = os.getenv("AZURE_OPENAI_ENDPOINT")
openai.api_version = "2023-08-01-preview"  # Use the latest API version

# Define the deployment name
dalle_deployment_name = os.getenv("AZURE_OPENAI_DALLE_DEPLOYMENT_NAME")

# Define the prompt
prompt = "A multi-colored umbrella on the beach, disposable camera"

# Make the API request
response = openai.Image.create(
    prompt=prompt,
    n=1,
    size="1024x1024",
    model=dalle_deployment_name
)

# Print the URL of the generated image
print("Generated Image URL:\n")
print(response['data'][0]['url'])
