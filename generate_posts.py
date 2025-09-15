from openai import OpenAI
import os
import pandas as pd
from dotenv import load_dotenv
import fitz  # PyMuPDF

load_dotenv()

client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))


# Load context from PDF
def get_context_from_pdf(path="context_anchor.pdf"):
    doc = fitz.open(path)
    return "\n".join([page.get_text("text") for page in doc]).strip()


context = get_context_from_pdf()

# Load the content calendar
df = pd.read_csv("data/content_calendar.csv")

for index, row in df.iterrows():
    topic_finalized = str(row.get("Topic Finalized?", "")).strip().lower() if row.get("Topic Finalized?") is not None else ""
    post_finalized = str(row.get("Post Finalized?", "")).strip().lower() if row.get("Post Finalized?") is not None else ""
    post_text = row.get("Post Text", "") if row.get("Post Text") is not None else ""

    if topic_finalized == "yes" and (
        not isinstance(post_text, str) or not post_text.strip()
    ):
        topic = row.get("Topic", "a tech-related topic")

        prompt = (
            f"{context}\n\n"
            f"Based on the above context, write a short tweet (around 100 characters) "
            f'on the topic: "{topic}". Make it punchy, friendly, and useful. '
            f"Add an emoji if it fits. No links or hashtags."
        )

        try:
            response = client.chat.completions.create(
                model="gpt-4o", messages=[{"role": "user", "content": prompt}]
            )
            generated = response.choices[0].message.content.strip()
            df.at[index, "Post Text"] = generated
            df.at[index, "Post Finalized?"] = "No"
            print(f"✅ Generated post for: {topic}")
        except Exception as e:
            print(f"❌ Error at row {index}: {e}")


# Save updated calendar
df.to_csv("data/content_calendar.csv", index=False)
print("✅ All eligible rows updated with post content.")
