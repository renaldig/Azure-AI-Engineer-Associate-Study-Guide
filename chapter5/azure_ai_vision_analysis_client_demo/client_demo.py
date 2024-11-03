from azure.ai.vision import ImageAnalysisClient as VisionAnalysisClient
from azure.core.credentials import AzureKeyCredential
import os

vision_client = VisionAnalysisClient(
    endpoint=os.environ.get("AZURE_VISION_ENDPOINT"), 
    credential=AzureKeyCredential(os.environ.get("AZURE_SUBSCRIPTION_KEY"))
)

analysis_result = vision_client.analyze_image(
    image_url="<your_image_url_here>", 
    visual_features=["Captions", "Read"], 
    description_gender_neutral=True, 
    language="en" 
)
