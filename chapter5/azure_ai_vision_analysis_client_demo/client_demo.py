from azure.ai.vision.imageanalysis import ImageAnalysisClient as VisionAnalysisClient
from azure.ai.vision.imageanalysis.models import VisualFeatures
from azure.core.credentials import AzureKeyCredential
import os

with open("owl.png", "rb") as f:
    image_data = f.read()

vision_client = VisionAnalysisClient(
    endpoint=os.environ.get("AZURE_VISION_ENDPOINT"), 
    credential=AzureKeyCredential(os.environ.get("AZURE_SUBSCRIPTION_KEY"))
)

analysis_result = vision_client.analyze(
    image_data=image_data, 
    visual_features=[VisualFeatures.CAPTION], 
    gender_neutral_caption=True, 
    language="en" 
)
print(f" '{analysis_result.caption.text}', Confidence {analysis_result.caption.confidence:.4f}")