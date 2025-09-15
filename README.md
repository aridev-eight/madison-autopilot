# Marketing Content Automation Bot (for X)

An automated content generation system for posting personalized, grounded tweets using OpenAI and the Twitter API. Designed for thoughtful creators who want to blend productivity, tech, creativity, and cozy vibes — without micromanaging content calendars.

## Features

- Context-aware generation from your custom context_anchor.pdf
- Dynamic content calendar generation (topics every 2 hours from 9AM–9PM)
- Tweet generation for finalized topics only
- Scheduled auto-posting to X (Twitter) using OAuth 1.0a
- Edits allowed anytime — finalized fields give you full control
- No accidental overwrites — respects your manual changes
- Credit-efficient — GPT is only called when needed

## Project Structure

```
marketing_bot/
├── data/
│   └── content_calendar.xlsx     # Your content schedule
├── context_anchor.pdf            # Your brand voice / interests file
├── generate_calendar.py          # Generates tweet topics
├── generate_posts.py             # Generates tweet content
├── post_to_x.py                  # Posts finalized tweets at scheduled times
├── run_scheduler.py              # Orchestrates the whole pipeline
├── .env                          # Stores your API keys (not committed)

```

## Setup instructions

1. Install dependencies

```
pip install openai pandas python-dotenv requests requests_oauthlib PyMuPDF schedule openpyxl

```
2. Make sure openai is upgraded to the latest version

```
pip install --upgrade openai
```

3. Setup .env file in the root

```
OPENAI_API_KEY=your_openai_key
TWITTER_API_KEY=your_twitter_api_key
TWITTER_API_SECRET=your_twitter_api_secret
TWITTER_ACCESS_TOKEN=your_access_token
TWITTER_ACCESS_SECRET=your_access_secret
PROJECT_PATH=full_path_to_project_directory
```

You must enable OAuth 1.0a in your Twitter Developer App and use User Context authentication.

## Working

1. Run the scheduler

```
python3 run_scheduler.py
```

This will:

- Run `generate_calendar.py` to create new post slots (max 8/day)
- Run generate_posts.py to generate tweet text only for finalized topics
- Run post_to_x.py to post tweets that are ready & scheduled

Step 2: Edit your content_calendar.xlsx

- Change Topic or Time freely
- Set "Topic Finalized?" = Yes to trigger tweet generation
- Review/edit tweet
- Set "Post Finalized?" = Yes to queue for posting

## Customization

- Update context_anchor.pdf to reflect your tone, story, or brand
- Change generation time slots inside generate_calendar.py
- Adjust OpenAI prompts for more playful, technical, or minimal tones
- Set MAX_POSTS_PER_DAY to control volume

## Safety & Control

- No posts are tweeted unless "Post Finalized?" = Yes
- No GPT calls are made unless a topic or post is missing
- No rows are overwritten unless you manually clear them

## Use Cases

- Solo developers sharing personal updates
- Creators managing a consistent posting schedule
- Interns or students building automated marketing demos
- Anyone who wants AI to help with social media

## Future Scope

- Sync post impressions & analytics to a google sheet for tracking

