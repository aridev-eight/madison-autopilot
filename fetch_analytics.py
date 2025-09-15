import requests
import pandas as pd
import os
from dotenv import load_dotenv
import gspread
from oauth2client.service_account import ServiceAccountCredentials

load_dotenv()
bearer_token = os.getenv("TWITTER_BEARER_TOKEN")

# Google Sheets setup
scope = ["https://spreadsheets.google.com/feeds", "https://www.googleapis.com/auth/drive"]
creds_path = os.getenv("GOOGLE_SHEETS_CREDS")
creds = ServiceAccountCredentials.from_json_keyfile_name(creds_path, scope)
client = gspread.authorize(creds)
sheet = client.open("X Analytics").sheet1

# Read calendar
df = pd.read_excel("data/content_calendar.xlsx")

for index, row in df.iterrows():
    tweet_id = row.get("Tweet ID")
    if isinstance(tweet_id, str) and tweet_id:
        url = f"https://api.twitter.com/2/tweets/{tweet_id}?tweet.fields=public_metrics"
        headers = {"Authorization": f"Bearer {bearer_token}"}
        response = requests.get(url, headers=headers)
        if response.status_code == 200:
            metrics = response.json()["data"]["public_metrics"]
            sheet.append_row([
                tweet_id,
                row["Date"],
                metrics.get("impression_count", 0),
                metrics.get("like_count", 0),
                metrics.get("retweet_count", 0),
                metrics.get("reply_count", 0)
            ])
            print(f"Logged analytics for {tweet_id}")
        else:
            print(f"Failed to fetch tweet analytics: {response.text}")
