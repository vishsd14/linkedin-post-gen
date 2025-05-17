import openai
import os
import gspread
from google.oauth2.service_account import Credentials

# Set your OpenAI API Key
openai.api_key = "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"

# Google Sheets setup
GOOGLE_SHEET_ID = "14st8t45SC9EfqY5Pv4buZ_xA9mdCs6X1xAxGvL3_Y0Q"
WORKSHEET_NAME = "Sheet3"

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

def generate_post(topic, post_type, real_life_note=""):
    prompt = f"""
You are Vishnu Sudevan, an SEO strategist and growth marketer with nearly a decade of experience helping brands scale organically using advanced SEO, AI automation, and content-driven growth systems. Your writing style on LinkedIn is bold, structured, actionable, and deeply insightful — similar to elite content strategists like Jayati.

Write a high-performing, narrative-style LinkedIn post based on these inputs:
- Topic: {topic}
- Post Type: {post_type or 'Value-Driven'}
- Real Life Note or Context: {real_life_note or 'Mention relevant SEO data shifts, AI impact, or evolving digital strategies.'}

Follow this structure:
1. **Start with a bold hook challenging conventional thinking.** (1 line, scroll-stopping, no labels, no emojis)
2. **Briefly state the old belief vs the new reality.**
3. **Anchor the insight with a credible trend, stat, or behavior shift.**
4. **Present 3–5 punchy, scannable points (listicle format with 1️⃣ 2️⃣ 3️⃣ format).** Each point must have a bold mini-headline + a sharp supporting line.
5. **Conclude with a strong, reflective summation.**
6. **End with a thought-provoking CTA (one clear reflective question).**
7. **Optional: Add 5–8 clean professional hashtags at the bottom.**

Writing Principles:
- Short broken sentences. Strong rhythm and flow for mobile.
- Zero fluff. Clear bold insights.
- No emojis inside text. Only number emojis (1️⃣ 2️⃣ 3️⃣) for listicle points.
- Tone: Authoritative yet relatable, strategic but easy to grasp.
- Word choices: vivid, direct, no vague business jargon.
- Post length: Max 18–20 lines.

Strictly follow the above structure and rules.

Now, write the full LinkedIn post.
"""
    try:
        response = openai.chat.completions.create(
            model="gpt-4o",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        post = response.choices[0].message.content.strip()
        return post
    except Exception as e:
        print(f"Error generating post: {e}")
        return None

def process_sheet(sheet):
    records = sheet.get_all_records()

    for idx, row in enumerate(records, start=2):  # Start from row 2 because of header
        topic = row.get('Post Idea') or ''
        post_type = row.get('Post Type') or 'Value-Driven'
        real_life_note = row.get('Goal') or ''

        if topic:  # If topic exists
            print(f"Generating post for: {topic}")
            post = generate_post(topic, post_type, real_life_note)

            if post:
                cell = f'G{idx}'
                sheet.update(cell, [[post]])
                print(f"✅ Post for '{topic}' saved in row {idx}")
            else:
                print(f"❌ Skipping row {idx} due to generation error.")

if __name__ == "__main__":
    print("=== LinkedIn Calendar Post Generator ===")
    sheet = connect_to_google_sheet(GOOGLE_SHEET_ID, WORKSHEET_NAME)
    process_sheet(sheet)
