import os
import sys
import uuid
import azure.cognitiveservices.speech as speechsdk
import simpleaudio as sa

def get_speech_credentials():
    """
    Retrieves Azure Speech Service credentials from environment variables.
    """
    subscription_key = os.environ.get('SPEECH_SUBSCRIPTION_KEY')
    region = os.environ.get('SPEECH_REGION')

    if not subscription_key or not region:
        print("Error: SPEECH_SUBSCRIPTION_KEY and SPEECH_REGION environment variables must be set.")
        sys.exit(1)

    return subscription_key, region

def configure_translation(subscription_key, region):
    """
    Configures the Speech Translation settings.

    Args:
        subscription_key (str): Azure Speech Service subscription key.
        region (str): Azure service region.

    Returns:
        TranslationRecognizer: Configured translation recognizer.
    """
    # Initialize Speech Translation Configuration
    translation_config = speechsdk.translation.SpeechTranslationConfig(
        subscription=subscription_key, region=region)
    translation_config.speech_recognition_language = 'en-US'

    # Add target languages
    translation_config.add_target_language('es')
    translation_config.add_target_language('fr')

    # Set voice for synthesized speech
    translation_config.set_voice_name('es', 'es-ES-AlvaroNeural')  # Spanish voice
    translation_config.set_voice_name('fr', 'fr-FR-DeniseNeural')  # French voice

    # Configure audio input to use the default microphone
    audio_config = speechsdk.audio.AudioConfig(use_default_microphone=True)

    # Create Translation Recognizer
    translator = speechsdk.translation.TranslationRecognizer(
        translation_config=translation_config, audio_config=audio_config)

    return translator

def play_audio(audio_data):
    """
    Plays audio data using simpleaudio.

    Args:
        audio_data (bytes): The audio data to play.
    """
    try:
        play_obj = sa.play_buffer(audio_data, 1, 2, 16000)
        play_obj.wait_done()
    except Exception as e:
        print(f"An error occurred during audio playback: {e}")

def recognizing_handler(evt):
    """
    Handles intermediate recognition results.

    Args:
        evt: The event containing the recognition result.
    """
    print(f"Recognizing: {evt.result.text}")

def recognized_handler(evt):
    """
    Handles final recognition results and prints translations.

    Args:
        evt: The event containing the recognition result.
    """
    print(f"Recognized: {evt.result.text}")
    for lang in evt.result.translations:
        translation = evt.result.translations[lang]
        print(f"Translated into {lang}: {translation}")

def canceled_handler(evt):
    """
    Handles cancellation events.

    Args:
        evt: The event containing cancellation details.
    """
    print(f"Canceled: {evt.reason}")
    if evt.reason == speechsdk.CancellationReason.Error:
        print(f"Error details: {evt.error_details}")

def synthesizing_handler(evt):
    """
    Handles the synthesizing event to play translated speech.

    Args:
        evt: The event containing the synthesized audio data.
    """
    if evt.result.reason == speechsdk.ResultReason.TranslatingSpeech:
        print(f"Synthesizing translation audio for {evt.result.translations}")
        audio_data = evt.result.audio
        if audio_data:
            play_audio(audio_data)
        else:
            print("No audio data available for the translation.")

def main():
    """
    Main function to set up translation and handle user interaction.
    """
    subscription_key, region = get_speech_credentials()
    translator = configure_translation(subscription_key, region)

    # Connect event handlers
    translator.recognizing.connect(recognizing_handler)
    translator.recognized.connect(recognized_handler)
    translator.canceled.connect(canceled_handler)
    translator.synthesizing.connect(synthesizing_handler)

    print("Speak into your microphone. Press Ctrl+C to stop.")

    # Start continuous recognition
    translator.start_continuous_recognition()

    try:
        while True:
            pass  # Keep the program running
    except KeyboardInterrupt:
        print("\nStopping translation...")
        translator.stop_continuous_recognition()
        print("Translation stopped.")

if __name__ == "__main__":
    main()
