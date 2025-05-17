import openai
import os
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set your Google Sheet and worksheet details
GOOGLE_SHEET_ID = "14st8t45SC9EfqY5Pv4buZ_xA9mdCs6X1xAxGvL3_Y0Q"
WORKSHEET_NAME = "Sheet2"

def connect_to_google_sheet(sheet_id, worksheet_name):
    scope = [
        'https://www.googleapis.com/auth/spreadsheets',
        'https://www.googleapis.com/auth/drive'
    ]
    creds = Credentials.from_service_account_file('seo-agents-452809-a76c4931190d.json', scopes=scope)
    client = gspread.authorize(creds)
    sheet = client.open_by_key(sheet_id)
    worksheet = sheet.worksheet(worksheet_name)
    return worksheet

def generate_post(custom_bio, topic, tone, persona, mode="full", real_life_note="", style_note="", post_type=""):
    prompt = f"""
{custom_bio}

Write a high-performing, narrative-style LinkedIn post based on the following inputs:
- Topic: {topic}
- Tone: {tone}
- Audience: {persona}
- Post Type: {post_type or 'Value-Driven'}
- Style: {style_note or 'Relatable, witty, punchy, emotionally resonant'}
- Real Life: {real_life_note or 'Include a specific personal story or client experience to anchor the insight'}

Formatting and style principles:
- Strong hook (no labels, no emojis)
- Casual, broken-paragraph style for mobile readability
- Rhythm and whitespace for tension and flow
- Emotional connection using wit, pain, or lived truths
- Sharp problem, reflective insight, and clear POV
- No emojis, no hashtags, no \"Problem:\" or \"Solution:\" labels
- 12–18 lines max, compact and punchy
"""

    response = openai.chat.completions.create(
        model="gpt-4-1106-preview",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def save_post_to_google_sheet(sheet, post, topic, tone, persona):
    if post:
        sheet.append_row([topic, tone, persona, post])
        print("Post saved to Google Sheet!")
    else:
        print("Post not saved due to generation error.")
