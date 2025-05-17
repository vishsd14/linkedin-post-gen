import openai
import os
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
openai.api_key = os.getenv("OPENAI_API_KEY")

# Set your Google Sheet and worksheet details
GOOGLE_SHEET_ID = "14st8t45SC9EfqY5Pv4buZ_xA9mdCs6X1xAxGvL3_Y0Q"
WORKSHEET_NAME = "Sheet2"

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

def generate_post(custom_bio, topic, tone, persona, mode="full", real_life_note="", style_note="", post_type=""):
    prompt = f"""
You are {custom_bio}.

Your job is to craft highly relatable, story-driven, emotionally resonant LinkedIn posts that:
- Stop the scroll
- Build human connection
- Make readers feel seen and understood
- Spark real conversations (not fake engagement)

---
Task:
Write a powerful LinkedIn post based on these inputs:
- Topic: {topic}
- Tone: {tone}
- Target Audience: {persona}
- Writing Style: {style_note or 'Relatable, witty, punchy, emotionally resonant'}
- Real-Life Insight to weave into the story: {real_life_note or 'Include a specific lived experience or micro-story to anchor the insight'}
- Post Type: {post_type}
- Post Length Mode: {mode}

---
Post Structure:

1. **Hook**:
   - Start with a bold, short emotional line or question.
   - No emojis. No "Problem:" or "Story:" tags.
   - Make it scroll-stopping.

2. **Story**:
   - Share a small, vivid real-world scenario, personal struggle, unexpected realisation, or client situation.
   - Use short, broken sentences for rhythm and white space.
   - Mobile-optimised flow: no dense paragraphs.

3. **Insight**:
   - Deliver a sharp emotional insight.
   - Let the reader "feel" the truth, not just be told advice.

4. **Takeaway**:
   - Give one transformational shift, lesson, or mindset tweak.

5. **Call to Action**:
   - End with a soft, reflective, emotionally inviting question that feels human — not salesy.
   - (Example: "What’s something you’ve learned the hard way?" or "Ever felt stuck in this phase too?")

---
Style Instructions:
- Avoid emojis, hashtags, bold formatting.
- Avoid giving "5 tips" or "Here’s why" style posts — prefer narrative and lived experience.
- Prioritise **emotion > logic**, **story > tips**, **relatability > polish**.
- Feel like a casual but powerful diary entry someone would post after deep realisation.
- Length: Max 12–18 lines for full mode, 3–5 lines for quick mode.

---
Important:
Your goal is to build trust, relatability, and thoughtfulness — not perfection.
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

def save_post_to_google_sheet(sheet, post, topic, tone, persona):
    if post:
        sheet.append_row([topic, tone, persona, post])
        print("Post saved to Google Sheet!")
    else:
        print("Post not saved due to generation error.")

if __name__ == "__main__":
    print("=== LinkedIn Post Generator ===")
    custom_bio = input("Enter your LinkedIn persona/bio (this will shape the post tone): ")
    topic = input("Enter topic: ")
    tone = input("Choose tone (Motivational / Informative / Guiding / Candid / Relatable): ")
    persona = input("Target audience (Freelance Client / Hiring Manager / Marketer / Entrepreneur / Agency Owner / Brand Strategist / Content Creator / Founder / SEO Specialist): ")
    mode = input("Post length (quick / full): ")
    real_life_note = input("Add a real-life example, experience, or scenario to include (optional): ")
    style_note = input("Describe your writing style preferences (e.g., witty, tough love, philosophical, punchy) (optional): ")
    post_type = input("Type of post (e.g., Lesson Learned / Framework Reveal / Myth-Busting / Hot Take / Mindset / Case Study / Open Reflection): ")

    post = generate_post(custom_bio, topic, tone, persona, mode, real_life_note, style_note, post_type)
    print("\nGenerated Post:\n")
    print(post if post else "No post generated.")

    if post:
        sheet = connect_to_google_sheet(GOOGLE_SHEET_ID, WORKSHEET_NAME)
        save_post_to_google_sheet(sheet, post, topic, tone, persona)
