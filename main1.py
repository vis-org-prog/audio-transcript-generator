import os
import pprint
from google.cloud import storage
from google.cloud import speech

# Create environment variables
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account.json"


def list_blobs(bucket_name):
    """Lists all the blobs in the bucket."""
    # bucket_name = "your-bucket-name"

    storage_client = storage.Client()

    # Note: Client.list_blobs requires at least package version 1.17.0.
    blobs = storage_client.list_blobs(bucket_name)
    return blobs



def extract_audio_gcs(gcs_uri):
    """Asynchronously transcribes the audio file specified by the gcs_uri."""

    client = speech.SpeechClient()

    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        encoding=speech.RecognitionConfig.AudioEncoding.LINEAR16,
        audio_channel_count=2,
        language_code="en-US",
    )

    operation = client.long_running_recognize(config=config, audio=audio)

    print("Waiting for operation to complete...")
    response = operation.result(timeout=100)

    return response



def main():

    bucket_name = "vishnu_gcp1"
    blobs = list_blobs(bucket_name)

    # Print blobs
    for blob in blobs:
        print(blob.name)

        # Extract audio from file
        gcs_uri = "gs://" + bucket_name + "/" + blob.name
        print("\nThis is the uri: {}".format(gcs_uri))

        response = extract_audio_gcs(gcs_uri=gcs_uri)
        pprint.pprint(response)



if __name__ == "__main__":
    main()