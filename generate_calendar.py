from openai import OpenAI
import os
from dotenv import load_dotenv

load_dotenv()
client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
import pandas as pd
from datetime import datetime
import os
from dotenv import load_dotenv
import fitz  # PyMuPDF
from collections import Counter

load_dotenv()

file_path = "data/content_calendar.csv"


# 🧠 Load context from PDF
def extract_context_from_pdf(path):
    if not os.path.exists(path):
        return ""
    doc = fitz.open(path)
    return "\n".join([page.get_text("text") for page in doc]).strip()


context_text = extract_context_from_pdf("context_anchor.pdf")

# 📄 Load existing calendar if it exists
if os.path.exists(file_path):
    df = pd.read_csv(file_path)
else:
    df = pd.DataFrame(columns=pd.Index([
        "Date",
        "Time",
        "Topic",
        "Topic Finalized?",
        "Post Type",
        "Post Text",
        "Post Finalized?",
        "Tweet ID",
    ]))

# Count how many posts already exist per date
existing_date_counts = df["Date"].astype(str).value_counts()
today = datetime.today().strftime("%Y-%m-%d")
existing_today = int(existing_date_counts.get(today, 0) or 0)
MAX_POSTS_PER_DAY = 8
new_posts = 0

# Only generate if we have space left
if existing_today < MAX_POSTS_PER_DAY:
    start_hour = 9
    end_hour = 21  # Until 9PM

    # Existing date/time entries to avoid duplicates
    existing_entries = set(zip(df["Date"].astype(str), df["Time"].astype(str)))

    for hour in range(start_hour, end_hour + 1, 2):
        if new_posts + existing_today >= MAX_POSTS_PER_DAY:
            break  # stop when daily cap is reached

        t = f"{hour:02d}:00"
        # Only add a new row if there is no row for today at this time
        if not ((df["Date"] == today) & (df["Time"] == t)).any():
            prompt = (
                f"Based on the following context:\n\n{context_text}\n\n"
                "Suggest a unique and engaging post title (max 15 words) for a Twitter post. "
                "Avoid repetitive phrases like 'Boost' or 'Unlock'. Focus on meaningful insights, relatable struggles, "
                "tech in action, cozy productivity, or personal stories. Vary tone and sound human, not robotic."
            )
            try:
                response = client.chat.completions.create(
                    model="gpt-4o", messages=[{"role": "user", "content": prompt}]
                )
                topic = response.choices[0].message.content.strip() if response.choices[0].message.content else "Placeholder topic (edit me!)"
            except Exception as e:
                print(f"❌ Failed to generate topic for {today} {t}: {e}")
                topic = "Placeholder topic (edit me!)"

            new_row = {
                "Date": today,
                "Time": t,
                "Topic": topic,
                "Topic Finalized?": "No",
                "Post Type": "Short Post",
                "Post Text": "",
                "Post Finalized?": "No",
                "Tweet ID": "",
            }

            df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
            new_posts += 1

# ✅ Maintain correct column order
df = df[
    [
        "Date",
        "Time",
        "Topic",
        "Topic Finalized?",
        "Post Type",
        "Post Text",
        "Post Finalized?",
        "Tweet ID",
    ]
]

df.to_csv(file_path, index=False)
print(f"✅ Calendar updated with {new_posts} new post(s) for {today}.")
