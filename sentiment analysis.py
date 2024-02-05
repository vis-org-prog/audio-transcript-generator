from google.cloud import language_v1
import os
import pandas as pd

# Set the environment variable
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "service-account.json"

# Instantiates a client
client = language_v1.LanguageServiceClient()

def analyze_sentiment(text):
    # The text to analyze
    document = language_v1.types.Document(
        content=text, type_=language_v1.types.Document.Type.PLAIN_TEXT
    )

    # Detects the sentiment of the text
    sentiment = client.analyze_sentiment(
        request={"document": document}
    ).document_sentiment

    return sentiment

# trasncription data
transcription_data = [
    "this is NDTV",
    "and you're watching classics",
    "can I have the telephone number to today",
    "this is John could you please provide me the billing telephone number of the account number",
]

# Create a dataframe
df = pd.DataFrame(transcription_data, columns = ['transcription'])


# Add columns for sentiment analysis
df['sentiment_score'] = 0.0
df['sentiment_magnitude'] = 0.0

# Loop through each transcription and perform sentiment analysis
for index, row in df.iterrows():
    transcription = row['transcription']
    sentiment = analyze_sentiment(transcription)
    df.at[index, 'sentiment_score'] = sentiment.score
    df.at[index, 'sentiment_magnitude'] = sentiment.magnitude

    # Display the dataframe
print(df)

# Save the DataFrame as a CSV file
df.to_csv("sentiment_analysis_results.csv", index=False)

# Compute average Sentiment and Magnitude
average_sentiment = df["sentiment_score"].mean()
average_magnitude = df["sentiment_magnitude"].mean()

# Display the results
print("Average Sentiment:", average_sentiment)
print("Average Magnitude:", average_magnitude)