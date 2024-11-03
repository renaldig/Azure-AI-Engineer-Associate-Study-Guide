import os
import sys
import uuid
from dotenv import load_dotenv
from azure.cognitiveservices.vision.face import FaceClient
from msrest.authentication import CognitiveServicesCredentials

def get_face_credentials():
    """
    Retrieves Azure Face API credentials from environment variables.
    """
    subscription_key = os.getenv('FACE_API_KEY')
    endpoint = os.getenv('FACE_API_ENDPOINT')

    if not subscription_key or not endpoint:
        print("Error: FACE_API_KEY and FACE_API_ENDPOINT must be set in the .env file.")
        sys.exit(1)

    return subscription_key, endpoint

def initialize_face_client(subscription_key, endpoint):
    """
    Initializes the FaceClient with the provided credentials.

    Args:
        subscription_key (str): Azure Face API subscription key.
        endpoint (str): Azure Face API endpoint URL.

    Returns:
        FaceClient: An instance of the FaceClient.
    """
    credentials = CognitiveServicesCredentials(subscription_key)
    face_client = FaceClient(endpoint, credentials)
    return face_client

def detect_faces_with_url(face_client, image_url, face_attributes):
    """
    Detects faces in an image provided by a URL.

    Args:
        face_client (FaceClient): Initialized FaceClient instance.
        image_url (str): URL of the image to analyze.
        face_attributes (list): List of face attributes to return.

    Returns:
        list: List of detected face objects.
    """
    try:
        detected_faces = face_client.face.detect_with_url(
            url=image_url,
            return_face_attributes=face_attributes
        )
        return detected_faces
    except Exception as e:
        print(f"An error occurred during face detection: {e}")
        return []

def detect_faces_with_stream(face_client, image_path, face_attributes):
    """
    Detects faces in an image provided as a local file.

    Args:
        face_client (FaceClient): Initialized FaceClient instance.
        image_path (str): Path to the image file to analyze.
        face_attributes (list): List of face attributes to return.

    Returns:
        list: List of detected face objects.
    """
    try:
        with open(image_path, "rb") as image_file:
            image_data = image_file.read()

        detected_faces = face_client.face.detect_with_stream(
            image=image_data,
            return_face_attributes=face_attributes
        )
        return detected_faces
    except Exception as e:
        print(f"An error occurred during face detection: {e}")
        return []

def analyze_detected_faces(detected_faces):
    """
    Analyzes and prints attributes of detected faces.

    Args:
        detected_faces (list): List of detected face objects.
    """
    if not detected_faces:
        print("No faces detected.")
        return

    for idx, face in enumerate(detected_faces, start=1):
        print(f"\nFace {idx}:")
        print(f"  Face ID: {face.face_id}")
        print(f"  Age: {face.face_attributes.age}")
        print(f"  Gender: {face.face_attributes.gender}")
        print(f"  Emotions:")
        for emotion, score in face.face_attributes.emotion.as_dict().items():
            print(f"    {emotion.capitalize()}: {score:.2f}")

def identify_faces(face_client, person_group_id, face_ids):
    """
    Identifies faces by matching them against a Person Group.

    Args:
        face_client (FaceClient): Initialized FaceClient instance.
        person_group_id (str): ID of the Person Group.
        face_ids (list): List of face IDs to identify.

    Returns:
        list: List of identification results.
    """
    try:
        results = face_client.face.identify(face_ids, person_group_id)

        for result in results:
            print(f"\nFace ID: {result.face_id}")
            if not result.candidates:
                print("  No person identified for the face.")
                continue
            top_candidate = result.candidates[0]
            person_id = top_candidate.person_id
            confidence = top_candidate.confidence
            person = face_client.person_group_person.get(person_group_id, person_id)
            print(f"  Person identified: {person.name} with confidence {confidence:.2f}")
    except Exception as e:
        print(f"An error occurred during face identification: {e}")

def main():
    """
    Main function to execute facial recognition tasks based on user input.
    """
    load_dotenv()  # Load environment variables from .env file
    subscription_key, endpoint = get_face_credentials()
    face_client = initialize_face_client(subscription_key, endpoint)

    print("\nOptions:")
    print("1: Detect and Analyze Faces from Image URL")
    print("2: Detect and Analyze Faces from Local Image File")
    print("3: Identify Faces (Requires Person Group Setup)")
    print("Press any other key to exit\n")

    user_choice = input("Choose an option: ").strip()

    face_attributes = ['age', 'gender', 'emotion']

    if user_choice == '1':
        image_url = input("Enter the URL of the image: ").strip()
        if not image_url:
            print("No URL entered. Exiting.")
            sys.exit(1)
        detected_faces = detect_faces_with_url(face_client, image_url, face_attributes)
        analyze_detected_faces(detected_faces)

    elif user_choice == '2':
        image_path = input("Enter the path to the image file: ").strip()
        if not image_path or not os.path.exists(image_path):
            print("Invalid file path. Exiting.")
            sys.exit(1)
        detected_faces = detect_faces_with_stream(face_client, image_path, face_attributes)
        analyze_detected_faces(detected_faces)

    elif user_choice == '3':
        person_group_id = input("Enter your Person Group ID: ").strip()
        if not person_group_id:
            print("No Person Group ID entered. Exiting.")
            sys.exit(1)

        image_path = input("Enter the path to the image file for identification: ").strip()
        if not image_path or not os.path.exists(image_path):
            print("Invalid file path. Exiting.")
            sys.exit(1)

        detected_faces = detect_faces_with_stream(face_client, image_path, face_attributes)
        if not detected_faces:
            print("No faces detected for identification.")
            sys.exit(1)

        face_ids = [face.face_id for face in detected_faces]
        identify_faces(face_client, person_group_id, face_ids)

    else:
        print("Exiting...")

if __name__ == "__main__":
    main()
