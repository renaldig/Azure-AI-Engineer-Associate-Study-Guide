from openai import AzureOpenAI
import os
import requests
from dotenv import load_dotenv
from PIL import Image
import json

load_dotenv()

azure_client = AzureOpenAI(
    api_version = os.getenv("AZURE_OPENAI_API_VERSION"),
    api_key=os.environ["AZURE_OPENAI_API_KEY"],
    azure_endpoint=os.environ['AZURE_OPENAI_ENDPOINT']
)

response = azure_client.images.generate(
    model="dall-e-3",
    prompt="A multi-colored umbrella on the beach, disposable camera",
    n=1
)

parsed_response = json.loads(response.model_dump_json())

output_dir = os.path.join(os.curdir, 'output_images')
if not os.path.exists(output_dir):
    os.makedirs(output_dir)

output_file = os.path.join(output_dir, 'output_image.png')
image_url = parsed_response["data"][0]["url"]
image_data = requests.get(image_url).content

with open(output_file, "wb") as file:
    file.write(image_data)

Image.open(output_file).show()
