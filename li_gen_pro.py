import openai
import streamlit as st

openai.api_key = st.secrets["OPENAI_API_KEY"]

def generate_post(custom_bio, topic, tone, persona, mode="full", real_life_note="", style_note="", post_type=""):
    prompt = f"""
You are {custom_bio}.

Your role is to craft high-authority, insight-driven LinkedIn posts that:
- Establish trust and expertise
- Address critical challenges faced by the target audience
- Offer sharp, valuable perspectives — without sounding preachy
- Invite professional dialogue, not just reactions

---
Task:
Write a clear, professional LinkedIn post based on:
- Topic: {topic}
- Tone: {tone}
- Target Audience: {persona}
- Writing Style: {style_note or 'Concise, insightful, thought-provoking'}
- Real-Life Experience (Optional): {real_life_note}
- Post Type: {post_type}
- Post Length Mode: {mode}

---
Post Structure:

1. **Hook**:
   - Start with a bold, sharp observation or challenge.
   - No labels like \"Problem\" — just real, provocative statements.
   - 1–2 lines max, designed to make the reader stop and think.

2. **Context**:
   - Present the real-world scenario or industry situation.
   - Grounded, relatable — no jargon, no fluff.
   - Crisp broken sentences for mobile readability.

3. **Analysis**:
   - Dissect the issue intelligently.
   - Share ONE strong insight or unconventional POV (Point of View).

4. **Solution / Shift**:
   - Offer ONE professional advice, framework, or strategic shift.
   - Keep it lean, powerful, not tutorial-style.

5. **Call to Reflection**:
   - End with a thought-provoking, reflective question.
   - Example: \"What’s one shift you’ve made that changed everything?\"

---
Style Instructions:
- NO emojis, hashtags, section titles.
- Focus on credibility, authority, and smart simplicity.
- Max 12–18 lines for full mode, 4–6 lines for quick mode.

---
Important:
Your goal is to educate, inspire trust, and spark meaningful conversations among professionals — not sell or motivate artificially.
"""
    try:
        response = openai.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            temperature=0.7
        )
        return response.choices[0].message.content.strip()
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
