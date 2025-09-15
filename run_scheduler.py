import schedule
import time
import os
from datetime import datetime
from dotenv import load_dotenv
load_dotenv()

# Absolute path to your project folder
PROJECT_PATH = os.getenv("PROJECT_PATH")
PYTHON_CMD = "python3"  # or full path like /usr/bin/python3 if needed


# Define tasks
def run_calendar():
    print(f"[{datetime.now()}] 📅 Running: generate_calendar.py")
    os.system(f"cd {PROJECT_PATH} && {PYTHON_CMD} generate_calendar.py")


def run_post_generation():
    print(f"[{datetime.now()}] ✍️ Running: generate_posts.py")
    os.system(f"cd {PROJECT_PATH} && {PYTHON_CMD} generate_posts.py")


def run_post_to_x():
    print(f"[{datetime.now()}] 🐦 Running: post_to_x.py")
    os.system(f"cd {PROJECT_PATH} && {PYTHON_CMD} post_to_x.py")


# Schedule tasks
# schedule.every().monday.at("09:00").do(run_calendar)         # Weekly calendar generation
# schedule.every().day.at("09:01").do(run_post_generation)     # Daily post prep
# schedule.every(1).minutes.do(run_post_to_x)                  # Post every minute if scheduled

schedule.every(1).minutes.do(run_calendar)
schedule.every(2).minutes.do(run_post_generation)
schedule.every(1).minutes.do(run_post_to_x)

print("📡 Scheduler is running... Press Ctrl+C to stop.\n")

# Run loop
try:
    while True:
        schedule.run_pending()
        time.sleep(30)
except KeyboardInterrupt:
    print("\n🛑 Scheduler stopped.")
