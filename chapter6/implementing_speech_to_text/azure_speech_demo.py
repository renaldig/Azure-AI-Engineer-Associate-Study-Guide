# azure_speech_demo.py

import os
import sys
from dotenv import load_dotenv
from azure.cognitiveservices.speech import (
    SpeechConfig,
    SpeechSynthesizer,
    AudioConfig,
    SpeechRecognizer,
    ResultReason,
    CancellationReason
)

def get_azure_credentials():
    """
    Retrieves Azure Speech Service credentials from environment variables.
    """
    load_dotenv()
    speech_key = os.environ.get('SPEECH_SUBSCRIPTION_KEY')
    service_region = os.environ.get('SPEECH_REGION')
    
    if not speech_key or not service_region:
        print("Error: SPEECH_KEY and SPEECH_REGION environment variables must be set.")
        sys.exit(1)
    
    return speech_key, service_region

def text_to_speech(text, speech_key, service_region):
    """
    Converts input text to speech using Azure Speech Service.
    
    Args:
        text (str): The text to convert to speech.
        speech_key (str): Azure Speech Service subscription key.
        service_region (str): Azure service region.
    """
    try:
        # Initialize Speech Configuration
        speech_config = SpeechConfig(subscription=speech_key, region=service_region)
        audio_config = AudioConfig(filename="output.wav")
        
        # Create a Speech Synthesizer
        synthesizer = SpeechSynthesizer(speech_config=speech_config, audio_config=audio_config)
        
        # Synthesize speech
        result = synthesizer.speak_text_async(text).get()
        
        # Check result
        if result.reason == ResultReason.SynthesizingAudioCompleted:
            print(f"Speech synthesized successfully for text: \"{text}\"")
        elif result.reason == ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Speech synthesis canceled: {cancellation_details.reason}")
            if cancellation_details.reason == CancellationReason.Error:
                print(f"Error details: {cancellation_details.error_details}")
    except Exception as e:
        print(f"An error occurred during text-to-speech: {e}")

def speech_to_text(speech_key, service_region):
    """
    Converts speech input from the microphone to text using Azure Speech Service.
    
    Args:
        speech_key (str): Azure Speech Service subscription key.
        service_region (str): Azure service region.
    """
    try:
        # Initialize Speech Configuration
        speech_config = SpeechConfig(subscription=speech_key, region=service_region)
        
        # Create a Speech Recognizer
        speech_recognizer = SpeechRecognizer(speech_config=speech_config)
        
        print("Please speak into your microphone...")
        
        # Perform speech recognition
        result = speech_recognizer.recognize_once_async().get()
        
        # Check result
        if result.reason == ResultReason.RecognizedSpeech:
            print(f"Recognized Text: \"{result.text}\"")
        elif result.reason == ResultReason.NoMatch:
            print("No speech could be recognized.")
        elif result.reason == ResultReason.Canceled:
            cancellation_details = result.cancellation_details
            print(f"Speech recognition canceled: {cancellation_details.reason}")
            if cancellation_details.reason == CancellationReason.Error:
                print(f"Error details: {cancellation_details.error_details}")
    except Exception as e:
        print(f"An error occurred during speech-to-text: {e}")

def main():
    """
    Main function to prompt user for action and execute TTS or STT accordingly.
    """
    speech_key, service_region = get_azure_credentials()
    
    while True:
        print("\nAzure Speech Service Demo")
        print("1. Text-to-Speech (TTS)")
        print("2. Speech-to-Text (STT)")
        print("3. Exit")
        
        choice = input("Enter your choice (1/2/3): ").strip()
        
        if choice == '1':
            text = input("Enter the text you want to convert to speech: ").strip()
            if text:
                text_to_speech(text, speech_key, service_region)
            else:
                print("No text entered. Please try again.")
        elif choice == '2':
            speech_to_text(speech_key, service_region)
        elif choice == '3':
            print("Exiting the program. Goodbye!")
            break
        else:
            print("Invalid choice. Please enter 1, 2, or 3.")

if __name__ == "__main__":
    main()
