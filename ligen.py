import openai
import os
import pandas as pd
import gspread
from google.oauth2.service_account import Credentials

# Directly set your OpenAI API key here
openai.api_key = "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"

# Set your Google Sheet and worksheet details
GOOGLE_SHEET_ID = "14st8t45SC9EfqY5Pv4buZ_xA9mdCs6X1xAxGvL3_Y0Q"
WORKSHEET_NAME = "Sheet1"

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

def generate_post(topic, tone, persona, mode="full", real_life_note=""):
    prompt = f"""
    You are Jayati — a seasoned SEO strategist and content marketing expert with 10+ years of experience.
    You specialize in B2B, SaaS, and freelance clients. Your writing is sharp, insight-driven, and filled with real-world value.

    Write a high-quality LinkedIn post with the following:
    - Topic: {topic}
    - Audience: {persona}
    - Tone: {tone}
    - Format: Hook → Personal insight or framework → Actionable takeaway → CTA
    - Style: Bold, conversational, expert-led — written like a true thought leader
    - Length: {'2-4 lines' if mode == 'quick' else '8-12 lines'}

    Avoid fluff. Make it relatable, nuanced, and helpful.
    {f"Include this real-life example or scenario in the post: {real_life_note}" if real_life_note else ""}
    """

    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
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
    print("=== Jayati's LinkedIn Post Generator ===")
    topic = input("Enter topic: ")
    tone = input("Choose tone (Motivational / Informative / Guiding): ")
    persona = input("Target audience (Freelance Client / Hiring Manager / Marketer): ")
    mode = input("Post length (quick / full): ")
    real_life_note = input("Add a real-life example, experience, or scenario to include (optional): ")

    post = generate_post(topic, tone, persona, mode, real_life_note)
    print("\nGenerated Post:\n")
    print(post if post else "No post generated.")

    if post:
        sheet = connect_to_google_sheet(GOOGLE_SHEET_ID, WORKSHEET_NAME)
        save_post_to_google_sheet(sheet, post, topic, tone, persona)
