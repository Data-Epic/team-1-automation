# 📊 Team 1 Google Sheets Automation

This project uses **Cohere's NLP APIs** and **Google Sheets** to automatically analyze customer reviews. It:

- ✅ Summarizes long reviews
- ✅ Classifies sentiment (Positive / Neutral / Negative)
- ✅ Adds an “Action needed?” column for negative feedback
- ✅ Visualizes sentiment distribution with a pie chart directly inside Google Sheets

---

## 🚀 Features

| Feature                  | Description |
|--------------------------|-------------|
| **AI Summarization**     | Uses Cohere's `summarize` endpoint to reduce lengthy reviews into short one-sentence summaries. |
| **Sentiment Analysis**   | Custom fine-tuned Cohere model classifies each review into Positive, Neutral, or Negative. |
| **Smart Actions Column** | Flags reviews needing attention based on sentiment. |
| **Live Google Sheet Sync** | Reads and writes reviews and outputs to a Google Sheet using the `gspread` API. |
| **Pie Chart Generator**  | Automatically adds a visual pie chart of sentiment breakdown in your Google Sheet. |

---

## 🛠️ Requirements

Make sure you have these installed:

```bash
pip install pandas cohere gspread gspread_dataframe python-dotenv google-auth google-api-python-client
```

---

## 🔐 Setup

1. **Clone this repo**  
   Or copy the script into your working directory.

2. **Create `.env` file**  
   ```bash
   touch .env
   ```

   Inside `.env`, add your Cohere API key:
   ```
   COHERE_API_KEY=your_cohere_api_key
   ```

3. **Google Sheets Access**  
   - Create a service account in [Google Cloud Console](https://console.cloud.google.com/).
   - Enable the Google Sheets API and download the service account key as `GOOGLE_SHEETS_CREDS.json`.
   - Share your Google Sheet with the service account email (ending in `@project.iam.gserviceaccount.com`).

4. **Update sheet ID**  
   In the script, replace:
   ```python
   sheet_id = "your_google_sheet_id_here"
   ```
   with the actual ID from your Google Sheet URL.

5. **Provide Your Fine-Tuned Model**  
   Replace this line with your actual Cohere model ID:
   ```python
   model="your-fine-tuned-model-id"
   ```

---

## 📈 Output Example

Your Google Sheet will be updated to include:

- `AI Summary`
- `AI Sentiment`
- `Action needed?`
- A pie chart showing the percentage of each sentiment

### Original Google Sheet

![Original Google Sheet](<Google Sheet Before.png>)

### Google Sheet after running auto.py

![Google Sheet after running auto.py](<Google Sheet After.png>)

### Sentiment Pie Chart

![Sentiment Pie Chart](<Google Sheet Pie Chart.png>)

---

## 📂 Folder Structure

```
project-folder/
├── .gitignore
├── .env
├── Google Sheet Before.png
├── Google Sheet After.png
├── Google Sheet Pie Chart.png
├── GOOGLE_SHEETS_CREDS.json
├── sentiment-classification.jsonl
├── trained-finetuned-model.py
├── auto.py
└── README.md
```

---

## 🙋‍♀️ Authors
- Chidimma Ijoma
    - [GitHub](https://github.com/chidi-ijoma)
- Khadijat Agboola
    - [GitHub](https://github.com/KhadijahAgboola)

---
