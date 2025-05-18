import streamlit as st
from li_gen_pro import generate_post

st.set_page_config(page_title="LinkedIn Post Generator", layout="centered")
st.title("🚀 LinkedIn Post Generator")
st.markdown("Create professional, high-authority LinkedIn posts tailored to your persona and goals.")

with st.form("post_form"):
    custom_bio = st.text_area("🧑‍💼 Your LinkedIn Persona/Bio", help="This will shape the tone, context, and authority of your post.")
    topic = st.text_input("📝 Topic")
    tone = st.selectbox("🎤 Tone", ["Motivational", "Informative", "Guiding", "Candid", "Relatable"])
    persona = st.text_input("🎯 Target Audience", help="E.g., Content Creator, Marketer, Agency Owner, Hiring Manager")
    post_type = st.selectbox("🧬 Post Type", ["Lesson Learned", "Framework Reveal", "Myth-Busting", "Hot Take", "Mindset", "Case Study", "Open Reflection"])
    mode = st.selectbox("📏 Post Length", ["quick", "full"])
    style_note = st.text_input("🎨 Writing Style (Optional)", help="E.g., witty, punchy, philosophical, tough love")
    real_life_note = st.text_area("🎯 Real-Life Insight (Optional)", help="Add a story, moment, or challenge you'd like the post to reflect")

    submitted = st.form_submit_button("Generate LinkedIn Post")

if submitted:
    st.markdown("⚙️ Generating your post...")
    post = generate_post(
        custom_bio=custom_bio,
        topic=topic,
        tone=tone,
        persona=persona,
        mode=mode,
        real_life_note=real_life_note,
        style_note=style_note,
        post_type=post_type
    )

    if post:
        st.success("✅ Post generated successfully!")
        st.text_area("Generated LinkedIn Post", value=post, height=450)
    else:
        st.error("❌ Failed to generate post. Please check your inputs or API connection.")
