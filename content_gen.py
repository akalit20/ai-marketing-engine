import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI Agency Engine Pro", page_icon="🚀", layout="wide")
st.title("🚀 E-commerce AI Marketing Agency Engine")

# --- HARD PASSCODE LOCK ON MAIN SCREEN ---
secret_passcode = st.secrets.get("APP_PASSCODE", "vip2026")
user_pass = st.text_input("🔒 Enter VIP Passcode to Unlock App:", type="password")

if user_pass != secret_passcode:
    st.warning("⛔ App-ti lock kora ache! Sothik passcode diye Enter chapun.")
    st.stop()

st.success("✅ Access Granted! Welcome back.")
st.divider()

# Load API key
api_key = st.secrets.get("GROQ_API_KEY", None)

with st.sidebar:
    st.header("🧠 AI Settings")
    if not api_key:
        api_key = st.text_input("Groq API Key Din:", type="password")
    
    selected_model = None
    if api_key:
        try:
            client = Groq(api_key=api_key)
            models = client.models.list()
            text_models = [
                m.id for m in models.data 
                if not any(x in m.id.lower() for x in ["whisper", "guard", "tts", "orpheus"])
            ]
            default_ix = 0
            for i, m in enumerate(text_models):
                if "120b" in m or "70b" in m or "qwen" in m:
                    default_ix = i
                    break
            selected_model = st.selectbox("AI Brain:", text_models, index=default_ix)
        except Exception:
            st.error("Invalid API Key!")

col1, col2 = st.columns(2)
with col1:
    product_name = st.text_input("📦 Product-er Nam:", placeholder="e.g. Hydrating Lip Gloss")
    language = st.selectbox("🌍 Language / Bhasha:", ["English", "Italian", "Bengali (Banglish)"])
with col2:
    brand_tone = st.selectbox("🎭 Brand Tone / Vibe:", ["Luxury & Aesthetic ✨", "Trendy & Gen-Z 🔥", "Warm & Friendly 😊", "Direct & High-Converting 🎯"])
    target_audience = st.text_input("👥 Target Audience:", placeholder="e.g. Women 18-35, beauty lovers")

key_features = st.text_area("📝 Key Benefits / Details:", placeholder="e.g. Non-sticky, mirror shine, vitamin E infused, lasts 8 hours")

if st.button("✨ Generate Full Agency Package 🚀", use_container_width=True):
    if not product_name:
        st.error("Product-er nam likhun!")
        st.stop()

    prompt = f"""
    You are an elite digital marketing agency director.
    Create a complete 5-in-1 marketing campaign for:
    - Product: {product_name}
    - Benefits: {key_features}
    - Target Audience: {target_audience}
    - Brand Tone: {brand_tone}
    - Language: {language}

    Provide the output clearly structured with Markdown:
    ### 🎥 1. INSTAGRAM / TIKTOK REEL SCRIPT
    Table with columns: [Time/Segment, Visual Scene, On-Screen Text, Voiceover/SFX]. Include a 3-sec viral hook.
    ### 📱 2. VIRAL CAPTION & 15 HASHTAGS
    Engaging hook, bullet points, CTA, and 15 niche hashtags.
    ### 🎯 3. FACEBOOK / IG AD COPY (2 Variations)
    1 Problem-Solution style and 1 Aesthetic/Storytelling style.
    ### 🎨 4. AI PRODUCT PHOTOGRAPHY PROMPTS
    2 detailed prompts (in English) for Midjourney/DALL-E to generate luxury product shoot images.
    ### 📩 5. CLIENT PITCH DM
    A short, high-converting Instagram DM pitching this campaign to a brand owner in {language}.
    """

    with st.spinner("Generating 5-in-1 Agency Package..."):
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=selected_model,
        )
        result = chat_completion.choices[0].message.content
        st.success("✅ Full 5-in-1 Agency Package Ready!")
        st.markdown(result)
        st.download_button(
            label="📥 Download Client Package (.txt)",
            data=result,
            file_name=f"{product_name.replace(' ', '_')}_agency_package.txt",
            mime="text/plain"
        )
