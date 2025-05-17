import openai
import gspread
from datetime import datetime
from google.oauth2.service_account import Credentials

# === CONFIG ===
openai.api_key = "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"

SERVICE_ACCOUNT_FILE = "seo-agents-452809-a76c4931190d.json"
CALENDAR_SHEET_ID = "16Oj8gCZhOJv7hAGyHj5-aO6gb0F-N83tsPvk22vfEg4"
POST_OUTPUT_SHEET_ID = "14st8t45SC9EfqY5Pv4buZ_xA9mdCs6X1xAxGvL3_Y0Q"

SCOPES = ["https://www.googleapis.com/auth/spreadsheets", "https://www.googleapis.com/auth/drive"]
creds = Credentials.from_service_account_file(SERVICE_ACCOUNT_FILE, scopes=SCOPES)
client = gspread.authorize(creds)

calendar_sheet = client.open_by_key(CALENDAR_SHEET_ID).sheet1
output_sheet = client.open_by_key(POST_OUTPUT_SHEET_ID).sheet1

def generate_post(topic, tone, persona, post_type, style_note, real_life_note):
    prompt = f"""
    You are Jayati — a seasoned SEO and content expert with 10+ years of experience.
    Topic: {topic}
    Tone: {tone}
    Audience: {persona}
    Type: {post_type}
    Style: {style_note or 'Bold and conversational'}
    Real life: {real_life_note or 'Make it relatable'}

    Write a high-quality LinkedIn post in this format:
    Hook → Story/Insight → Takeaway → CTA
    Length: 8-12 lines, short sentences, powerful voice.
    """

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def process_calendar():
    rows = calendar_sheet.get_all_records()
    today_str = datetime.now().strftime("%Y-%m-%d")

    for i, row in enumerate(rows, start=2):  # start=2 to account for header row
        if row.get("Status", "").strip().lower() == "done":
            continue

        date_str = row.get("Date")
        if not date_str or date_str != today_str:
            continue

        topic = row.get("Topic")
        tone = row.get("Tone")
        persona = row.get("Persona")
        post_type = row.get("Post Type")
        style = row.get("Style")
        real_life = row.get("Real Life Insight")

        post = generate_post(topic, tone, persona, post_type, style, real_life)

        # Save to output sheet
        output_sheet.append_row([topic, tone, persona, post])

        # Mark as Done in calendar
        calendar_sheet.update_cell(i, 8, "Done ✅")  # Column H is 'Status'

        print(f"✅ Post for '{topic}' added and marked as done.")

if __name__ == "__main__":
    print("=== Batch LinkedIn Post Generator ===")
    process_calendar()
