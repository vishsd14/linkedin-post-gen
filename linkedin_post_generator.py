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
    I'm Vishnu Sudevan, an SEO strategist and growth marketer with nearly a decade of experience helping brands scale their organic presence through advanced SEO, AI-powered automation, and content-driven growth. From leading high-performing SEO teams to building automation systems that streamline technical and content workflows, I've worked across fintech, SaaS, D2C, and B2B sectors. On LinkedIn, I share real-world SEO strategies, behind-the-scenes systems that save time and boost performance, leadership insights, and mental models that help marketers and founders grow smarter — not just harder.

    Write a deeply insightful and professional LinkedIn post based on the following inputs:
    - Topic: {topic}
    - Tone: {tone}
    - Audience: {persona}
    - Post Type: {post_type or 'Value-Driven'}
    - Style: {style_note or 'Insightful, punchy, and bold'}
    - Real Life: {real_life_note or 'Incorporate a relevant personal or client example'}

    Structure:
    1. Open with a bold hook — no label, no emoji. Just grab attention.
    2. Present a sharp, relatable problem.
    3. Deliver a clear, expert-level insight or solution — show, don’t tell.
    4. End with a smart, reflective CTA that invites discussion.

    Additional rules:
    - DO NOT use emojis.
    - Do NOT label sections (e.g., “Hook:”, “Problem:”, etc.)
    - Avoid generic SEO or marketing clichés — write like someone who's done the work, not selling advice.
    - Make it feel like a snapshot from your day-to-day thinking or real projects.
    - Prioritize clarity, boldness, and flow.
    - Aim for 12–16 lines of high-impact writing.
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
