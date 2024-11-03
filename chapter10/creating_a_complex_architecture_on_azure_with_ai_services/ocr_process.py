from azure.cognitiveservices.vision.computervision import ComputerVisionClient
from azure.cognitiveservices.vision.computervision.models import OperationStatusCodes
from msrest.authentication import CognitiveServicesCredentials
import time

# Replace with your Azure Cognitive Services key and endpoint
subscription_key = "YOUR_SUBSCRIPTION_KEY"
endpoint = "YOUR_ENDPOINT"

computervision_client = ComputerVisionClient(endpoint, CognitiveServicesCredentials(subscription_key))

# Replace with the SAS URL of your image in Blob Storage
image_url = "URL_OF_YOUR_IMAGE"

# Read the image using the Read API
read_response = computervision_client.read(url=image_url, raw=True)

# Get the operation location (URL with an ID at the end) from the response
operation_location = read_response.headers["Operation-Location"]

# Extract the operation ID from the operation location
operation_id = operation_location.split("/")[-1]

# Wait for the asynchronous operation to complete
while True:
    read_result = computervision_client.get_read_result(operation_id)
    if read_result.status not in ['notStarted', 'running']:
        break
    time.sleep(1)

# Print the detected text line by line
if read_result.status == OperationStatusCodes.succeeded:
    for page in read_result.analyze_result.read_results:
        for line in page.lines:
            print(line.text)
else:
    print("Error in OCR operation.")
