import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore
from datetime import datetime

# Use a service account.
cred = credentials.Certificate('service-account.json')

# Initialize Firebase Admin SDK
firebase_admin.initialize_app(cred)

# Connect to Firestore
db = firestore.client()

# Your sentiment analysis results
sentiment_results = [
    {"filename": "call-center-audio (2).wav", "number": 1, "text": "this is NDTV", "sentiment": 0.967466772, "magnitude": 2.89, "timestamp": 2.89},
    {"filename": "call-center-audio (2).wav", "number": 2, "text": "and you're watching classics", "sentiment": 0.966408074, "magnitude": 1.52, "timestamp": 6.2},
    {"filename": "call-center-audio (2).wav", "number": 3, "text": "can I have the telephone number to today", "sentiment": 0.895835578, "magnitude": 2.89, "timestamp": 31.44},
    {"filename": "call-center-audio (2).wav", "number": 4, "text": "this is John could you please provide me the billing telephone number of the account number", "sentiment": 0.91801697, "magnitude": 2.89, "timestamp": 43.3},
           
]

# Function to convert timestamp to date
def timestamp_to_date(timestamp):
    return datetime.utcfromtimestamp(timestamp).strftime('%Y-%m-%d')
                  
# Loop through sentiment results and store in Firestore
for result in sentiment_results:
    doc_data = {
        "wav_filename": result["filename"],
        "sentence_number": result["number"],
        "sentence_text": result["text"],
        "sentiment": result["sentiment"],
        "magnitude": result["magnitude"],
        "transcription_date": timestamp_to_date(result["timestamp"]),
    }

    # Create a new document in the Firestore collection
    doc_ref = db.collection("call_center_records").add(doc_data)
    print(f"Document added with ID: {doc_ref[1].id}")
