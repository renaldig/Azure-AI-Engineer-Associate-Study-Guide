from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import ImageFileCreateBatch, ImageFileCreateEntry, Region
from msrest.authentication import ApiKeyCredentials
import time

# Replace with your training key and endpoint
credentials = ApiKeyCredentials(in_headers={"Training-key": "<YOUR_TRAINING_KEY_HERE>"})
trainer = CustomVisionTrainingClient("<YOUR_CUSTOM_VISION_TRAINING_ENDPOINT_HERE>", credentials)

# Find the object detection domain
domains = trainer.get_domains()
obj_detection_domain = next(domain for domain in domains if domain.type == "ObjectDetection")

# Create a new project
project = trainer.create_project("My Object Detection Project", domain_id=obj_detection_domain.id)

# Add tags
fork_tag = trainer.create_tag(project.id, "fork")
scissors_tag = trainer.create_tag(project.id, "scissors")

# Upload and tag images
image_list = []
for image_num in range(1, 31):  # Assuming you have 20 images for each tag
    file_name = f"image_{image_num}.jpg"
    with open(f"flowers/{file_name}", "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), regions=[
            Region(tag_id=fork_tag.id, left=0.1, top=0.1, width=0.8, height=0.8)
        ]))

    file_name = f"image_{image_num}.jpg"
    with open(f"flowers/{file_name}", "rb") as image_contents:
        image_list.append(ImageFileCreateEntry(name=file_name, contents=image_contents.read(), regions=[
            Region(tag_id=scissors_tag.id, left=0.1, top=0.1, width=0.8, height=0.8)
        ]))

batch = ImageFileCreateBatch(images=image_list)
upload_result = trainer.create_images_from_files(project.id, batch=batch)

# Train the model
print("Training...")
iteration = trainer.train_project(project.id)
while (iteration.status != "Completed"):
    iteration = trainer.get_iteration(project.id, iteration.id)
    print("Training status: " + iteration.status)
    time.sleep(1)

# Publish the model
trainer.publish_iteration(project.id, iteration.id, "myModel", "<YOUR_MODEL_ID_HERE>")
print("Model trained and published. You can now use it to predict objects in new images.")