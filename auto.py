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



# Apply transformations
df['AI Summary'] = df['Review'].apply(summarize_text)
df['AI Summary'] = df['AI Summary'].str.replace('\n', '')
df['AI Sentiment'] = df['Review'].apply(get_sentiment)
df['Action needed?'] = df['AI Sentiment'].apply(lambda x: 'Yes' if x == 'Negative' else 'No')


# Write updated DataFrame back to Google Sheets

worksheet.clear()
set_with_dataframe(worksheet, df)

print("✅ Google Sheet updated with AI Summary and Sentiment columns.")

from googleapiclient.discovery import build



# Build the Sheets API service
sheets_service = build('sheets', 'v4', credentials=creds)


# Count each sentiment for the pie chart
sentiment_counts = df['AI Sentiment'].value_counts().reset_index()
sentiment_counts.columns = ['Sentiment', 'Count']


# Find where to write the chart data (you can adjust if needed)
chart_data_start_row = len(df) + 5 #Give a space of 5 rows from the original data
chart_range = f"AI Summary!A{chart_data_start_row}:B{chart_data_start_row + len(sentiment_counts)}"



# Update the sheet with chart data
chart_sheet = sheet.worksheet("AI Summary") if "AI Summary" in [ws.title for ws in sheet.worksheets()] else worksheet
chart_sheet.update(f"A{chart_data_start_row}",[sentiment_counts.columns.tolist()] + sentiment_counts.values.tolist())



# Create and insert the pie chart
requests = [{
    "addChart": {
        "chart": {
            "spec": {
                "title": "Sentiment Breakdown",
                "pieChart": {
                    "legendPosition": "RIGHT_LEGEND",
                    "threeDimensional": False,
                    "domain": {
                        "sourceRange": {
                            "sources": [{
                                "sheetId": chart_sheet._properties['sheetId'],
                                "startRowIndex": chart_data_start_row - 1,
                                "endRowIndex": chart_data_start_row - 1 + len(sentiment_counts) + 1,
                                "startColumnIndex": 0,
                                "endColumnIndex": 1
                            }]
                        }
                    },
                    "series": {
                        "sourceRange": {
                            "sources": [{
                                "sheetId": chart_sheet._properties['sheetId'],
                                "startRowIndex": chart_data_start_row - 1,
                                "endRowIndex": chart_data_start_row - 1 + len(sentiment_counts) + 1,
                                "startColumnIndex": 1,
                                "endColumnIndex": 2
                            }]
                        }
                    }
                }
            },
            "position": {
                "overlayPosition": {
                    "anchorCell": {
                        "sheetId": chart_sheet._properties['sheetId'],
                        "rowIndex": chart_data_start_row - 1,
                        "columnIndex": 3
                    },
                    "offsetXPixels": 20,
                    "offsetYPixels": 20
                }
            }
        }
    }
}]



# Send the request to add the chart
sheets_service.spreadsheets().batchUpdate(
    spreadsheetId=sheet_id,
    body={"requests": requests}
).execute()


print("📊 Pie chart of sentiment breakdown has been added to the Google Sheet.")



