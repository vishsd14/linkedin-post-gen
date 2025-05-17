import openai
import os
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Directly set your OpenAI API key here
openai.api_key = "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"

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

def generate_post(topic, tone, persona, mode="full", real_life_note="", style_note="", post_type=""):
    prompt = f"""
I'm Vishnu Sudevan, an SEO strategist and growth marketer with nearly a decade of experience driving organic success for fintech, SaaS, D2C, and B2B brands. I specialize in building scalable SEO systems, automating repetitive workflows, and extracting real growth from content and search data. On LinkedIn, I talk about the real stuff — the wins, the mental blocks, the back-end chaos behind SEO success — all while helping other marketers, founders, and SEO professionals work smarter, not just harder.

Write a high-performing, narrative-style LinkedIn post based on the following inputs:
- Topic: {topic}
- Tone: {tone}
- Audience: {persona}
- Post Type: {post_type or 'Value-Driven'}
- Style: {style_note or 'Relatable, witty, punchy, emotionally resonant'}
- Real Life: {real_life_note or 'Include a specific personal story or client experience to anchor the insight'}

Formatting and style principles to follow:
- Start with a strong, disruptive hook. One line. No labels. No emojis. Just scroll-stopping.
- Use a casual, broken-paragraph style with short, impactful sentences.
- Use rhythm and whitespace to create tension and flow. Ideal for mobile readers.
- Build emotional connection using wit, pain, or lived truths. Let the reader feel seen.
- Present a sharp, relatable problem.
- Follow with a reflective or slightly satirical insight (without preachy advice).
- Deliver a strong POV with clear but simple language.
- End with a call to action that makes people reflect or comment — ideally in question form.

Additional instructions:
- No emojis, no hashtags, no section titles (like “Problem” or “Insight”).
- Prioritize storytelling that hits shared SEO/growth/automation struggles and the irony of hustle culture.
- Draw inspiration from posts that are darkly humorous, raw, and break patterns.
- Length: 12–18 lines max. Ensure it feels like a punchy, compact monologue.
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

def save_post_to_google_sheet(sheet, post, topic, tone, persona):
    if post:
        sheet.append_row([topic, tone, persona, post])
        print("Post saved to Google Sheet!")
    else:
        print("Post not saved due to generation error.")

if __name__ == "__main__":
    print("=== LinkedIn Post Generator ===")
    topic = input("Enter topic: ")
    tone = input("Choose tone (Motivational / Informative / Guiding / Candid / Relatable): ")
    persona = input("Target audience (Freelance Client / Hiring Manager / Marketer / Entrepreneur / Agency Owner / Brand Strategist / Content Creator / Founder / SEO Specialist): ")
    mode = input("Post length (quick / full): ")
    real_life_note = input("Add a real-life example, experience, or scenario to include (optional): ")
    style_note = input("Describe your writing style preferences (e.g., witty, tough love, philosophical, punchy) (optional): ")
    post_type = input("Type of post (e.g., Lesson Learned / Framework Reveal / Myth-Busting / Hot Take / Mindset / Case Study / Open Reflection): ")

    post = generate_post(topic, tone, persona, mode, real_life_note, style_note, post_type)
    print("\nGenerated Post:\n")
    print(post if post else "No post generated.")

    if post:
        sheet = connect_to_google_sheet(GOOGLE_SHEET_ID, WORKSHEET_NAME)
        save_post_to_google_sheet(sheet, post, topic, tone, persona)
