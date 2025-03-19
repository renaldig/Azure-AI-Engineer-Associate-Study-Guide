import os
import sys
from os.path import join as join_paths
from azure.ai.vision.imageanalysis import ImageAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
from dotenv import load_dotenv

def execute_main_process():
    load_dotenv()
    endpoint = os.getenv('VISION_API_ENDPOINT')
    key = os.getenv('VISION_API_KEY')

    if not endpoint or not key:
        print("Error: VISION_API_ENDPOINT and VISION_API_KEY must be set in the .env file.")
        sys.exit(1)

    print('\nOptions:')
    print('1: Analyze "Lincoln.jpg" using OCR (Printed Text)')
    print('2: Decode handwriting in "Note.jpg" (Handwritten Text)')
    print('Press any other key to exit\n')
    
    user_choice = input('Choose an option: ').strip()
    
    if user_choice == '1':
        path_to_image = join_paths('images', 'Lincoln.jpg')
        if not os.path.exists(path_to_image):
            print(f"Error: The file {path_to_image} does not exist.")
            sys.exit(1)
        process_text_extraction(path_to_image, endpoint, key)
    elif user_choice == '2':
        path_to_image = join_paths('images', 'Note.jpg')
        if not os.path.exists(path_to_image):
            print(f"Error: The file {path_to_image} does not exist.")
            sys.exit(1)
        process_text_extraction(path_to_image, endpoint, key)
    else:
        print("Exiting...")

def process_text_extraction(path_to_image, endpoint, key):
    """
    Processes the image for text extraction using Azure Vision API.

    Args:
        path_to_image (str): The file path to the image.
        endpoint (str): The Azure Vision API endpoint.
        key (str): The Azure Vision API subscription key.
    """
    try:
        # Initialize the Image Analysis Client
        credential = AzureKeyCredential(key)
        client = ImageAnalysisClient(endpoint=endpoint, credential=credential)
        
        # Read the image data
        with open(path_to_image, "rb") as image_file:
            image_data = image_file.read()
        
        # Perform image analysis
        result = client.analyze(image_data=image_data, visual_features=[VisualFeatures.READ])
        
        # Extract and print text if available
        if result.read is not None:
            print("\nExtracted Text:")
            for page in result.read.blocks[0].lines:
                for line in page.words:
                    print(line.text)
        else:
            print("No text recognized.")
    
    except Exception as e:
        print(f"An error occurred during text extraction: {e}")

if __name__ == "__main__":
    execute_main_process()
