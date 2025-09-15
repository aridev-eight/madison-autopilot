import pandas as pd
import requests
import os
from dotenv import load_dotenv
from datetime import datetime, time as dt_time
from requests_oauthlib import OAuth1

load_dotenv()

# Load OAuth 1.0a credentials
api_key = os.getenv("TWITTER_API_KEY")
api_secret = os.getenv("TWITTER_API_SECRET")
access_token = os.getenv("TWITTER_ACCESS_TOKEN")
access_secret = os.getenv("TWITTER_ACCESS_SECRET")

auth = OAuth1(api_key, api_secret, access_token, access_secret)

df = pd.read_csv("data/content_calendar.csv")

now = datetime.now()
now_str = now.strftime("%Y-%m-%d %H:%M")

# Handle Excel time objects or strings
def normalize_time(raw_time):
    if pd.isna(raw_time):
        return "09:00"

    if isinstance(raw_time, dt_time):
        return raw_time.strftime("%H:%M")

    if isinstance(raw_time, datetime):
        return raw_time.strftime("%H:%M")

    try:
        return datetime.strptime(str(raw_time).strip(), "%H:%M").strftime("%H:%M")
    except:
        try:
            return datetime.strptime(str(raw_time).strip(), "%H:%M:%S").strftime("%H:%M")
        except:
            print(f"⚠️ Unrecognized time format: {raw_time}")
            return "09:00"

for index, row in df.iterrows():
    date = str(row.get("Date")).split(" ")[0]
    parsed_time = normalize_time(row.get("Time"))
    scheduled = f"{date} {parsed_time}"

    post_finalized = str(row.get("Post Finalized?", "")).strip().lower() if row.get("Post Finalized?") is not None else ""
    post_text = row.get("Post Text", "") if row.get("Post Text") is not None else ""
    tweet_id = row.get("Tweet ID", "") if row.get("Tweet ID") is not None else ""

    if (
        scheduled == now_str and
        post_finalized == "yes" and
        post_text and
        (not isinstance(tweet_id, str) or not tweet_id.strip())
    ):
        data = {"text": post_text}
        response = requests.post("https://api.twitter.com/2/tweets", auth=auth, json=data)

        if response.status_code in [200, 201]:
            tweet_id = response.json().get("data", {}).get("id", "")
            df.at[index, "Tweet ID"] = tweet_id
            print(f"✅ Posted tweet for {scheduled}: {tweet_id}")
        else:
            print(f"❌ Failed to post tweet for {scheduled}: {response.status_code} → {response.text}")

df.to_csv("data/content_calendar.csv", index=False)
