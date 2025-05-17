import openai
import os
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv
import time

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set your Google Sheet and worksheet details
GOOGLE_SHEET_ID = "14st8t45SC9EfqY5Pv4buZ_xA9mdCs6X1xAxGvL3_Y0Q"
WORKSHEET_NAME = "Sheet3"

# Google Sheets setup
def connect_to_google_sheet(sheet_id, worksheet_name):
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = Credentials.from_service_account_file('seo-agents-452809-a76c4931190d.json', scopes=scope)
    client = gspread.authorize(creds)

    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.worksheet(worksheet_name)

    print(f"Connected to sheet: {worksheet.title}")
    print(f"Sheet URL: https://docs.google.com/spreadsheets/d/{sheet.id}")
    return worksheet

# Post Generation Function
def generate_post(custom_bio, topic, tone, persona, mode="full", real_life_note="", style_note="", post_type=""):
    prompt = f"""
You are {custom_bio}.

Your job is to craft highly relatable, story-driven, emotionally resonant LinkedIn posts that:
- Stop the scroll
- Build human connection
- Make readers feel seen and understood
- Spark real conversations (not fake engagement)

Task:
Write a powerful LinkedIn post based on these inputs:
- Topic: {topic}
- Tone: {tone}
- Target Audience: {persona}
- Writing Style: {style_note or 'Relatable, witty, punchy, emotionally resonant'}
- Real-Life Insight to weave into the story: {real_life_note or 'Include a specific lived experience or micro-story to anchor the insight'}
- Post Type: {post_type}
- Post Length Mode: {mode}

Post Structure:
1. Hook (strong, short, emotional)
2. Story (vivid real-world scenario)
3. Insight (emotional realization)
4. Takeaway (one clear shift or mindset)
5. CTA (soft human question)

Style Instructions:
- No emojis, hashtags, or labels
- Narrative > tips
- Emotion > logic
- Max 12–18 lines for full mode

Important:
Prioritize authenticity, rawness, and relatability — not polish or advice.
"""

    try:
        response = openai.chat.completions.create(
            model="gpt-4-1106-preview",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        post = response.choices[0].message.content.strip()
        return post
    except Exception as e:
        print(f"Error generating post: {e}")
        return None

# Save to Google Sheet
def save_post_to_google_sheet(sheet, post, topic, tone, persona):
    if post:
        sheet.append_row([topic, tone, persona, post])
    else:
        print("Post not saved due to generation error.")

# ==================== MAIN =====================

if __name__ == "__main__":
    print("=== LinkedIn 30 Days Post Generator ===")
    custom_bio = input("Enter your LinkedIn persona/bio (this will shape the post tone): ")
    topic = input("Main Topic/Niche you want to cover (e.g., Personal Branding / Freelancing / Content Marketing): ")
    tone = input("Choose tone (Motivational / Informative / Guiding / Candid / Relatable): ")
    persona = input("Target audience (Freelance Client / Hiring Manager / Marketer / Entrepreneur / Agency Owner / Brand Strategist / Content Creator / Founder / SEO Specialist): ")
    mode = input("Post length (quick / full): ")
    style_note = input("Writing style (witty, punchy, tough-love, philosophical) (optional): ")

    # Connect to Sheet
    sheet = connect_to_google_sheet(GOOGLE_SHEET_ID, WORKSHEET_NAME)

    # Generate 30 Posts
    for day in range(1, 31):
        print(f"\nGenerating Post {day} of 30...")

        daily_post_type = "Open Reflection"  # We can randomize later if needed
        real_life_note = ""  # Empty for now, can add if you want

        post = generate_post(custom_bio, topic, tone, persona, mode, real_life_note, style_note, daily_post_type)

        if post:
            save_post_to_google_sheet(sheet, post, topic, tone, persona)
            print(f"✅ Post {day} saved!")
        else:
            print(f"⚠️ Post {day} failed!")

        # Sleep for a second between posts to avoid hitting any rate limit
        time.sleep(1)

    print("\n🎯 All 30 Posts Generated and Saved to Google Sheet Successfully!")
