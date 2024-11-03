import os
import sys
import time
import uuid
import requests
import json
from dotenv import load_dotenv

def get_video_indexer_credentials():
    """
    Retrieves Azure Video Indexer credentials from environment variables.
    """
    load_dotenv()  # Load environment variables from .env file
    account_id = os.getenv('VIDEO_INDEXER_ACCOUNT_ID')
    api_key = os.getenv('VIDEO_INDEXER_API_KEY')
    location = os.getenv('VIDEO_INDEXER_LOCATION')  # e.g., "trial" or specific region like "westus2"

    if not account_id or not api_key or not location:
        print("Error: VIDEO_INDEXER_ACCOUNT_ID, VIDEO_INDEXER_API_KEY, and VIDEO_INDEXER_LOCATION must be set in the .env file.")
        sys.exit(1)

    return account_id, api_key, location

def get_access_token(api_key, location):
    """
    Obtains an access token for the Video Indexer API.

    Args:
        api_key (str): Azure Video Indexer API key.
        location (str): Location of the Video Indexer account.

    Returns:
        str: Access token.
    """
    url = f"https://api.videoindexer.ai/Auth/{location}/Accounts/{account_id}/AccessToken?allowEdit=true"
    headers = {
        'Ocp-Apim-Subscription-Key': api_key
    }

    try:
        response = requests.get(url, headers=headers)
        response.raise_for_status()
        access_token = response.text.strip('"')  # Remove quotes from the token
        return access_token
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while obtaining the access token: {e}")
        sys.exit(1)

def upload_video(access_token, account_id, video_path, video_name):
    """
    Uploads a video to Azure Video Indexer.

    Args:
        access_token (str): Access token for authentication.
        account_id (str): Azure Video Indexer Account ID.
        video_path (str): Path to the video file.
        video_name (str): Name to assign to the uploaded video.

    Returns:
        str: Video ID.
    """
    upload_url = f"https://api.videoindexer.ai/{location}/Accounts/{account_id}/Videos?accessToken={access_token}&name={video_name}&privacy=Private"

    headers = {
        'Content-Type': 'multipart/form-data'
    }

    try:
        with open(video_path, 'rb') as video_file:
            files = {
                'file': (os.path.basename(video_path), video_file, 'video/mp4')
            }
            response = requests.post(upload_url, headers=headers, files=files)
            response.raise_for_status()
            video_id = response.json()['id']
            print(f"Video '{video_name}' uploaded successfully with Video ID: {video_id}")
            return video_id
    except FileNotFoundError:
        print(f"Error: The file {video_path} was not found.")
        sys.exit(1)
    except requests.exceptions.RequestException as e:
        print(f"An error occurred while uploading the video: {e}")
        sys.exit(1)

def check_video_processing(access_token, account_id, video_id):
    """
    Checks the processing status of the uploaded video.

    Args:
        access_token (str): Access token for authentication.
        account_id (str): Azure Video Indexer Account ID.
        video_id (str): ID of the uploaded video.

    Returns:
        dict: Video index information.
    """
    while True:
        status_url = f"https://api.videoindexer.ai/{location}/Accounts/{account_id}/Videos/{video_id}/Index?accessToken={access_token}"
        try:
            response = requests.get(status_url)
            response.raise_for_status()
            video_index = response.json()

            status = video_index.get('state', 'Processing')
            print(f"Video processing status: {status}")

            if status.lower() == 'processed':
                return video_index
            elif status.lower() in ['failed', 'error']:
                print("Video processing failed.")
                sys.exit(1)
            else:
                time.sleep(10)  # Wait for 10 seconds before checking again
        except requests.exceptions.RequestException as e:
            print(f"An error occurred while checking video status: {e}")
            sys.exit(1)

def analyze_video(video_index):
    """
    Analyzes the video index and prints insights.

    Args:
        video_index (dict): Video index information.
    """
    print("\n=== Video Insights ===\n")

    # Spoken Words
    print("** Spoke Words **")
    if 'videos' in video_index and len(video_index['videos']) > 0:
        video = video_index['videos'][0]
        if 'insights' in video and 'transcript' in video['insights']:
            for transcript in video['insights']['transcript']:
                print(f"[{transcript['begin']} - {transcript['end']}] {transcript['text']}")
        else:
            print("No transcript available.")

    # Identified Faces
    print("\n** Identified Faces **")
    if 'insights' in video and 'faces' in video['insights']:
        for face in video['insights']['faces']:
            print(f"Name: {face.get('name', 'Unknown')}, Age: {face.get('age', 'N/A')}, Emotion: {face.get('emotion', 'N/A')}")
    else:
        print("No faces identified.")

    # Emotions
    print("\n** Emotions **")
    if 'insights' in video and 'emotions' in video['insights']:
        for emotion in video['insights']['emotions']:
            print(f"Emotion: {emotion['name']}, Confidence: {emotion['confidence']:.2f}")
    else:
        print("No emotions detected.")

    # Topics
    print("\n** Topics **")
    if 'insights' in video and 'topics' in video['insights']:
        for topic in video['insights']['topics']:
            print(f"Topic: {topic['name']}, Confidence: {topic['confidence']:.2f}")
    else:
        print("No topics identified.")

def main():
    """
    Main function to execute the Azure AI Video Indexer workflow.
    """
    account_id, api_key, location = get_video_indexer_credentials()
    access_token = get_access_token(api_key, location)

    print("\nOptions:")
    print("1: Upload and Index a Video from Local System")
    print("2: Exit")
    print()

    user_choice = input("Choose an option: ").strip()

    if user_choice == '1':
        video_path = input("Enter the path to the video file (e.g., videos/sample_video.mp4): ").strip()
        video_name = input("Enter a name for the video: ").strip()

        if not video_path or not video_name:
            print("Error: Video path and name must be provided.")
            sys.exit(1)

        video_id = upload_video(access_token, account_id, video_path, video_name)
        video_index = check_video_processing(access_token, account_id, video_id)
        analyze_video(video_index)

    else:
        print("Exiting...")
        sys.exit(0)

if __name__ == "__main__":
    main()
