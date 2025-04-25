import pandas as pd
import os
import cohere
from dotenv import load_dotenv
import gspread
from google.oauth2.service_account import Credentials
from gspread_dataframe import set_with_dataframe, get_as_dataframe

# Load environment variables from .env file
load_dotenv()

# Set up Cohere
API_KEY = os.getenv('COHERE_API_KEY')
if API_KEY is None:
    raise ValueError("Please set the COHERE_API_KEY environment variable.")
co = cohere.ClientV2(API_KEY)

# Set up Google Sheets credentials
scopes = ["https://www.googleapis.com/auth/spreadsheets"]
creds = Credentials.from_service_account_file("GOOGLE_SHEETS_CREDS.json", scopes=scopes)
client = gspread.authorize(creds)

sheet_id = "1yZBl7ew1tHOkVADUQZZ5thsAirXXoWYWuHONYFA96q4"

# Open your sheet
sheet = client.open_by_key(sheet_id)
worksheet = sheet.worksheet("Sheet1")  # Change to your sheet name

# Load data into a DataFrame
df = get_as_dataframe(worksheet)
df = df.dropna(subset=['Review']).reset_index(drop=True)

# Summarize function
def summarize_text(user_review):
    try:
        if len(user_review) > 250:
            response = co.summarize(
                length="short",
                extractiveness="low",
                additional_command="Generate a summary that is concise and focuses on keypoints of one sentence length",
                text=user_review
            )
            return response.summary
        else:
            return user_review
    except Exception as e:
        print(f"Error in summarizing text: {e}")
        return None

# Sentiment function
def get_sentiment(user_review):
    try:
        response = co.classify(
            model="fb6124bf-bfd0-43ae-8d27-b661a78bda0a-ft",  # your fine-tuned model
            inputs=[user_review]
        )
        return response.classifications[0].prediction
    except Exception as e:
        print(f"Error in getting sentiment: {e}")
        return None