import streamlit as st
from groq import Groq

st.set_page_config(page_title="AI E-commerce Engine Pro", page_icon="🚀", layout="wide")
st.title("🚀 5-in-1 E-commerce AI Marketing Engine")
st.caption("Instant Reel Scripts, Viral Captions, FB/IG Ads, 8K Studio Photo Prompts & SEO Descriptions!")

#Hidden Passcodes
admin_passcode = st.secrets.get("APP_PASSCODE", None)
customer_passcode = st.secrets.get("CUSTOMER_PASSCODE", None)

# Gumroad link 
PAYMENT_LINK = "https://nishya0.gumroad.com/l/vlxxe"

# LOCK SCREEN & MONETIZATION UI 
col_lock1, col_lock2 = st.columns([2, 1])

with col_lock1:
    user_pass = st.text_input(
        "🔒 Enter VIP Passcode to Unlock Engine:", 
        type="password", 
        placeholder="Type your passcode and press Enter..."
    )

with col_lock2:
    st.write("")
    st.write("")
    st.link_button("💳 Get 6-Month VIP Pass (€5.99)", PAYMENT_LINK, use_container_width=True)

if not user_pass or user_pass not in [admin_passcode, customer_passcode]:
    st.info("💡 **Want instant marketing campaigns for your store?** Click **'Get 6-Month VIP Pass (€5.99)'** above to unlock all 5-in-1 E-commerce tools!")
    st.stop()

# --- API KEY ROUTING (ADMIN VS CUSTOMER) ---
api_key = None

if user_pass == admin_passcode:
    api_key = st.secrets.get("GROQ_API_KEY", None)
    st.success("👑 **Admin Mode Active!** Using your personal Vault API Key.")
elif user_pass == customer_passcode:
    st.success("🎉 **6-Month VIP Access Granted!**")
    with st.expander("🔑 Step 1: Connect Your Free Groq AI Key (Takes 30 Seconds)", expanded=True):
        st.markdown("""
        To enjoy **unlimited generations for 6 months** with zero extra cost, paste your free personal Groq key below:
        1. Go to **[GroqCloud Console](https://console.groq.com/keys)** and sign in with Google (100% Free).
        2. Click **Create API Key** and copy the key (`gsk_...`).
        3. Paste it in the box below!
        """)
        api_key = st.text_input("Paste Your Groq API Key (`gsk_...`):", type="password")

if not api_key:
    st.warning("👆 Please enter your Groq API Key above to start generating.")
    st.stop()

# Auto-Select Best Text Model
selected_model = None
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
    with st.sidebar:
        st.header("🧠 AI Engine Settings")
        selected_model = st.selectbox("Select AI Model:", text_models, index=default_ix)
except Exception:
    st.error("❌ Invalid API Key! Please check your `gsk_...` key and try again.")
    st.stop()

st.divider()

# --- MAIN GENERATOR UI ---
col1, col2 = st.columns(2)
with col1:
    product_name = st.text_input("📦 Product Name:", placeholder="e.g. Hydrating Lip Gloss")
    language = st.selectbox("🌍 Output Language:", ["English", "Italian", "Bengali (Banglish)"])
with col2:
    brand_tone = st.selectbox("🎭 Brand Tone / Vibe:", ["Luxury & Aesthetic ✨", "Trendy & Gen-Z 🔥", "Warm & Friendly 😊", "Direct & High-Converting 🎯"])
    target_audience = st.text_input("👥 Target Audience:", placeholder="e.g. Women 18-35, beauty lovers")

key_features = st.text_area("📝 Key Benefits / Details:", placeholder="e.g. Non-sticky, mirror shine, vitamin E infused, lasts 8 hours")

if st.button("✨ Generate Complete 5-in-1 E-commerce Campaign 🚀", use_container_width=True):
    if not product_name:
        st.error("Please enter a product name!")
        st.stop()

    prompt = f"""
    You are an elite e-commerce marketing director.
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

    ### 🎨 4. 8K AI PRODUCT PHOTOGRAPHY PROMPTS
    2 detailed prompts (in English) for Midjourney/DALL-E to generate luxury studio product shoot images.

    ### 🛍️ 5. SEO WEBSITE DESCRIPTION & PROMO EMAIL
    1 high-converting Shopify/Amazon product description with bullet points, plus 1 short promotional/abandoned-cart email to customers in {language}.
    """

    with st.spinner("Generating your 5-in-1 E-commerce Package..."):
        chat_completion = client.chat.completions.create(
            messages=[{"role": "user", "content": prompt}],
            model=selected_model,
        )
        result = chat_completion.choices[0].message.content
        st.success("✅ Full 5-in-1 E-commerce Package Ready!")
        st.markdown(result)
        st.download_button(
            label="📥 Download Campaign (.txt)",
            data=result,
            file_name=f"{product_name.replace(' ', '_')}_campaign.txt",
            mime="text/plain"
        )
