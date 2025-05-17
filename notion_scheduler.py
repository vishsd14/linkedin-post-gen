import openai
import datetime
import requests
import os

# === SETUP ===
NOTION_API_KEY = "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"
DATABASE_ID = "1bec9f98bd1280908e1ed09503a1fa4c"

openai.api_key = "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"

headers = {
    "Authorization": f"Bearer {NOTION_API_KEY}",
    "Content-Type": "application/json",
    "Notion-Version": "2022-06-28"
}

def generate_post(topic, tone, persona, post_type, style_note, real_life_note):
    prompt = f"""
    You are Jayati — a seasoned SEO strategist and content marketing expert with 10+ years of experience.
    Write a {post_type or 'high-quality'} LinkedIn post for the target audience: {persona}.

    Use storytelling frameworks (PAS, analogy, emotion).
    Style: {style_note or 'bold and insightful'}
    Tone: {tone}

    Format: Hook → Story → Takeaway → CTA
    {f"Include this real-life context: {real_life_note}" if real_life_note else ""}
    Topic: {topic}
    """

    response = openai.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7
    )
    return response.choices[0].message.content.strip()

def add_to_notion(topic, post, tone, persona, post_type):
    today = datetime.datetime.now().isoformat()

    data = {
        "parent": {"database_id": DATABASE_ID},
        "properties": {
            "Name": {"title": [{"text": {"content": topic}}]},
            "Date": {"date": {"start": today}},
            "Topic": {"rich_text": [{"text": {"content": topic}}]},
            "Post Content": {"rich_text": [{"text": {"content": post}}]},
            "Tone": {"select": {"name": tone}},
            "Persona": {"select": {"name": persona}},
            "Post Type": {"select": {"name": post_type}},
            "Status": {"select": {"name": "Draft"}}
        }
    }

    response = requests.post("https://api.notion.com/v1/pages", json=data, headers=headers)
    if response.status_code == 200:
        print("✅ Post added to Notion!")
    else:
        print(f"❌ Failed to add post: {response.text}")

if __name__ == "__main__":
    print("=== LinkedIn Post Scheduler to Notion ===")
    topic = input("Enter topic: ")
    tone = input("Tone (Motivational / Informative / Candid / Relatable): ")
    persona = input("Audience (Freelance Client / Founder / SEO / etc.): ")
    post_type = input("Post Type (Case Study / Mindset / Hot Take / etc.): ")
    style_note = input("Writing style (optional): ")
    real_life_note = input("Add real-life scenario (optional): ")

    post = generate_post(topic, tone, persona, post_type, style_note, real_life_note)
    print("\nGenerated Post:\n")
    print(post)

    add_to_notion(topic, post, tone, persona, post_type)
