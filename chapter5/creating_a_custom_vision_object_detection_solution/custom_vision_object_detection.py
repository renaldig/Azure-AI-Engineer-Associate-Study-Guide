import os
import sys
import time
import uuid
from dotenv import load_dotenv
from azure.cognitiveservices.vision.customvision.training import CustomVisionTrainingClient
from azure.cognitiveservices.vision.customvision.training.models import (
    ImageFileCreateBatch,
    ImageFileCreateEntry,
    Region
)
from msrest.authentication import ApiKeyCredentials

def get_custom_vision_credentials():
    """
    Retrieves Azure Custom Vision credentials from environment variables.
    """
    load_dotenv()  # Load environment variables from .env file
    training_key = os.getenv('CUSTOM_VISION_TRAINING_KEY')
    endpoint = os.getenv('CUSTOM_VISION_ENDPOINT')

    if not training_key or not endpoint:
        print("Error: CUSTOM_VISION_TRAINING_KEY and CUSTOM_VISION_ENDPOINT must be set in the .env file.")
        sys.exit(1)

    return training_key, endpoint

def initialize_training_client(training_key, endpoint):
    """
    Initializes the CustomVisionTrainingClient with the provided credentials.

    Args:
        training_key (str): Azure Custom Vision training key.
        endpoint (str): Azure Custom Vision endpoint URL.

    Returns:
        CustomVisionTrainingClient: An instance of the training client.
    """
    credentials = ApiKeyCredentials(in_headers={"Training-key": training_key})
    trainer = CustomVisionTrainingClient(endpoint, credentials)
    return trainer

def get_object_detection_domain(trainer):
    """
    Retrieves the Object Detection domain from available domains.

    Args:
        trainer (CustomVisionTrainingClient): Initialized training client.

    Returns:
        Domain: The Object Detection domain.
    """
    domains = trainer.get_domains()
    try:
        obj_detection_domain = next(domain for domain in domains if domain.type == "ObjectDetection")
        return obj_detection_domain
    except StopIteration:
        print("Object Detection domain not found.")
        sys.exit(1)

def create_project(trainer, project_name, domain_id):
    """
    Creates a new Custom Vision project.

    Args:
        trainer (CustomVisionTrainingClient): Initialized training client.
        project_name (str): Name of the project.
        domain_id (str): ID of the Object Detection domain.

    Returns:
        Project: The created project.
    """
    project = trainer.create_project(project_name, domain_id=domain_id)
    return project

def create_tags(trainer, project_id, tag_names):
    """
    Creates tags within the project.

    Args:
        trainer (CustomVisionTrainingClient): Initialized training client.
        project_id (str): ID of the project.
        tag_names (list): List of tag names to create.

    Returns:
        dict: A dictionary mapping tag names to their IDs.
    """
    tags = {}
    for tag_name in tag_names:
        tag = trainer.create_tag(project_id, tag_name)
        tags[tag_name] = tag.id
    return tags

def upload_images(trainer, project_id, tag_id, images_folder, num_images):
    """
    Uploads images to the project with specified tags.

    Args:
        trainer (CustomVisionTrainingClient): Initialized training client.
        project_id (str): ID of the project.
        tag_id (str): ID of the tag.
        images_folder (str): Path to the folder containing images.
        num_images (int): Number of images to upload.

    Returns:
        None
    """
    image_list = []
    for image_num in range(1, num_images + 1):
        file_name = f"image_{image_num}.jpg"
        image_path = os.path.join(images_folder, file_name)
        if not os.path.exists(image_path):
            print(f"Warning: {image_path} does not exist. Skipping.")
            continue
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()
            # Define the bounding box for the object in the image
            # For simplicity, assuming the object occupies the center 80% of the image
            # Modify these values based on actual object location
            regions = [
                Region(tag_id=tag_id, left=0.1, top=0.1, width=0.8, height=0.8)
            ]
            image_entry = ImageFileCreateEntry(name=file_name, contents=image_data, regions=regions)
            image_list.append(image_entry)

    if not image_list:
        print("No images to upload.")
        return

    batch = ImageFileCreateBatch(images=image_list)
    upload_result = trainer.create_images_from_files(project_id, batch=batch)

    if upload_result.is_batch_successful:
        print(f"Successfully uploaded {len(upload_result.images)} images for tag.")
    else:
        print("Some images failed to upload:")
        for image in upload_result.images:
            if image.status != "OK":
                print(f"Image {image.name} failed to upload. Error: {image.status}")

def train_model(trainer, project_id):
    """
    Trains the Custom Vision model.

    Args:
        trainer (CustomVisionTrainingClient): Initialized training client.
        project_id (str): ID of the project.

    Returns:
        Iteration: The trained iteration.
    """
    print("Training the model...")
    iteration = trainer.train_project(project_id)

    while iteration.status != "Completed":
        iteration = trainer.get_iteration(project_id, iteration.id)
        print(f"Training status: {iteration.status}")
        time.sleep(1)

    print("Training completed.")
    return iteration

def publish_model(trainer, project_id, iteration_id, model_name, prediction_resource_id):
    """
    Publishes the trained model.

    Args:
        trainer (CustomVisionTrainingClient): Initialized training client.
        project_id (str): ID of the project.
        iteration_id (str): ID of the trained iteration.
        model_name (str): Name to assign to the published model.
        prediction_resource_id (str): Resource ID of the prediction resource.

    Returns:
        None
    """
    trainer.publish_iteration(project_id, iteration_id, model_name, prediction_resource_id)
    print(f"Model '{model_name}' published.")

def main():
    """
    Main function to execute the Custom Vision Object Detection workflow.
    """
    training_key, endpoint = get_custom_vision_credentials()
    trainer = initialize_training_client(training_key, endpoint)
    domain = get_object_detection_domain(trainer)

    project_name = "My Object Detection Project"
    print(f"Creating project '{project_name}'...")
    project = create_project(trainer, project_name, domain.id)
    print(f"Project '{project.name}' created with ID: {project.id}")

    tag_names = ["fork", "scissors"]
    print(f"Creating tags: {tag_names}...")
    tags = create_tags(trainer, project.id, tag_names)
    print(f"Tags created: {tags}")

    images_folder = "flowers"  # Replace with your images folder
    num_images_per_tag = 30  # Minimum 30 images per tag

    for tag_name, tag_id in tags.items():
        print(f"Uploading images for tag '{tag_name}'...")
        upload_images(trainer, project.id, tag_id, images_folder, num_images_per_tag)

    iteration = train_model(trainer, project.id)

    model_name = "myModel"
    prediction_resource_id = "<YOUR_PREDICTION_RESOURCE_ID>"  # Replace with your Prediction resource ID
    publish_model(trainer, project.id, iteration.id, model_name, prediction_resource_id)

    print("Model trained and published successfully. You can now use it to predict objects in new images.")
    print("Visit https://www.customvision.ai/projects to view your projects.")

if __name__ == "__main__":
    main()
