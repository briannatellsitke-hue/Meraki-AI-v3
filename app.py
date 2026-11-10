# MERAKI AI - v3 STRONG
# MERAKI AI - v3 STRONG BURGUNDY
# Run with: streamlit run app.py
# Needs: pip install streamlit google-generativeai
# Put logo.png in same folder
import streamlit as st
import google.generativeai as genai
import os, io, base64
from PIL import Image

st.set_page_config(page_title="MERAKI AI", page_icon="✨", layout="centered")

# --- BURGUNDY STRONG THEME ---
st.markdown("""
<style>
.stApp { background-color: #FFF8F3; }
h1, h2, h3 { color: #6B0F2A !important; font-weight: 800 !important; }
p, label, .stCaption { color: #2B0A14 !important; }
.stButton>button {
    background: linear-gradient(135deg, #6B0F2A 0%, #4A0A1E 100%) !important;
    color: white !important; border-radius: 12px !important;
    border: 2px solid #C9A227 !important; font-weight: 800 !important;
    font-size: 16px !important; padding: 12px 20px !important;
    text-transform: uppercase; letter-spacing: 1px;
    box-shadow: 0 4px 15px rgba(107,15,42,0.3);
}
.stButton>button:hover { background: #C9A227 !important; color: #4A0A1E !important; }
.stTextInput input, .stTextArea textarea { border: 2px solid #6B0F2A !important; border-radius: 12px !important; background: white !important; }
section[data-testid="stSidebar"] { background-color: #4A0A1E !important; }
section[data-testid="stSidebar"] h1, section[data-testid="stSidebar"] h2,
section[data-testid="stSidebar"] p, section[data-testid="stSidebar"] label,
section[data-testid="stSidebar"] span { color: white !important; }
.meraki-banner {
    background: linear-gradient(135deg, #6B0F2A, #4A0A1E);
    padding: 22px; border-radius: 16px; text-align: center;
    border: 2px solid #C9A227; margin-bottom: 16px;
}
.meraki-banner h1 { color: white !important; font-size: 38px !important; margin: 0; }
.meraki-banner p { color: #F5D67A !important; font-weight: 600; margin: 5px 0 0 0; letter-spacing: 2px; }
.gold-line { height: 4px; background: #C9A227; border-radius: 10px; margin: 10px 0 20px 0; }
.chat-you { background: #6B0F2A; color: white; padding: 12px; border-radius: 12px; margin: 5px 0; }
.chat-ai { background: white; border: 2px solid #C9A227; padding: 12px; border-radius: 12px; margin: 5px 0; }
</style>
""", unsafe_allow_html=True)

# --- LOGO + HEADER ---
if os.path.exists("logo.png"):
    c1, c2, c3 = st.columns([1,2,1])
    with c2:
        st.image("logo.png", width=220)

st.markdown("""
<div class="meraki-banner"><h1>MERAKI AI</h1><p>YOUR AI, WITH SOUL • KENYAN • PREMIUM</p></div>
<div class="gold-line"></div>
""", unsafe_allow_html=True)
st.caption("Professional English & Kiswahili | Strong. Bold. Meraki.")

# --- SIDEBAR ---
with st.sidebar:
    st.header("⚙️ Settings")
    language = st.selectbox("Language / Lugha", ["Auto - Detect", "English", "Kiswahili"])
    api_key = st.text_input("Gemini API Key", type="password")
    st.info("Get free key: aistudio.google.com")
    st.markdown("---")
    st.markdown("**MERAKI AI v3**\n\n✅ Real Images\n✅ Voice Input\n✅ Download Files")

if not api_key:
    st.warning("⚠️ Enter your Gemini API Key in sidebar to start.")
    st.stop()

genai.configure(api_key=api_key)
text_model = genai.GenerativeModel("gemini-2.5-flash")
# Real image model
image_model = genai.GenerativeModel("gemini-2.5-flash-preview-image-generation")

if "history" not in st.session_state:
    st.session_state.history = []
if "last_write" not in st.session_state:
    st.session_state.last_write = ""

MERAKI_PROMPT = """
You are MERAKI AI, a strong, professional, premium Kenyan AI assistant.
Style: Bold, clear, warm, respectful, confident. No slang unless asked.
Language: English = professional English. Kiswahili = professional Kiswahili. Auto = detect and match.
"""

def ask_meraki(user_input, mode_name):
    prompt = f"{MERAKI_PROMPT}\nLanguage: {language}\nMode: {mode_name}\nUser: {user_input}\nMeraki:"
    try:
        return text_model.generate_content(prompt).text
    except Exception as e:
        return f"Pole, kuna hitilafu: {e}"

def generate_real_image(prompt_text):
    try:
        # Enhance prompt for strong burgundy premium style if user wants
        full_prompt = f"Professional, high quality, detailed image: {prompt_text}. Vibrant, clean, realistic, premium Kenyan style."
        response = image_model.generate_content(full_prompt)
        for part in response.candidates[0].content.parts:
            if hasattr(part, 'inline_data') and part.inline_data:
                img_data = part.inline_data.data
                return Image.open(io.BytesIO(base64.b64decode(img_data) if isinstance(img_data, str) else img_data))
            if hasattr(part, 'text') and part.text:
                return part.text
        return "No image returned. Try again with simpler description."
    except Exception as e:
        return f"Image error: {e}. Tip: Check your API key has image generation enabled in Google AI Studio."

# --- MODES ---
mode = st.radio("CHOOSE MODE / CHAGUA", ["💬 Chat", "✍️ Write", "🎨 Image", "📊 Predict", "🎤 Voice"], horizontal=True)

# CHAT
if mode == "💬 Chat":
    st.subheader("💬 Chat with Meraki")
    for msg in st.session_state.history:
        st.markdown(f'<div class="chat-you"><b>YOU:</b> {msg["q"]}</div>', unsafe_allow_html=True)
        st.markdown(f'<div class="chat-ai"><b>MERAKI:</b> {msg["a"]}</div>', unsafe_allow_html=True)
    user_q = st.text_input("Ask anything / Uliza chochote", key="chat_input")
    if st.button("ASK MERAKI ✨"):
        if user_q:
            with st.spinner("Meraki is thinking..."):
                ans = ask_meraki(user_q, "Chat")
                st.session_state.history.append({"q": user_q, "a": ans})
                st.rerun()
    if st.button("Clear Chat"):
        st.session_state.history = []
        st.rerun()

# WRITE + DOWNLOAD
elif mode == "✍️ Write":
    st.subheader("✍️ Write Mode")
    task = st.selectbox("What do you want to write?", ["CV", "Business Proposal", "Application Letter", "Business Plan", "Caption", "Sermon / Speech", "School Work", "WhatsApp Business Message"])
    details = st.text_area("Give details / Toa maelezo", placeholder="Example: CV for a driver with 5 years experience in Kibwezi, no KCSE certificate, good with customers...")
    if st.button("GENERATE ✍️"):
        if details:
            with st.spinner("Writing..."):
                result = ask_meraki(f"Write a {task}: {details}. Make it professional, ready to use, with headings.", "Write")
                st.session_state.last_write = result
                st.write(result)
    if st.session_state.last_write:
        st.markdown("---")
        st.download_button("⬇️ DOWNLOAD AS .TXT", data=st.session_state.last_write, file_name=f"Meraki_{task}.txt", mime="text/plain")
        st.caption("Tip: Open .txt in Word / Google Docs to save as PDF.")

# IMAGE - REAL
elif mode == "🎨 Image":
    st.subheader("🎨 Real Image Generation")
    st.info("This now creates a REAL picture, not just a prompt.")
    img_desc = st.text_input("Describe image / Eleza picha", placeholder="Example: Professional Kenyan woman selling mandazi in Kibwezi market, smiling, burgundy apron")
    col_a, col_b = st.columns(2)
    with col_a:
        if st.button("CREATE REAL IMAGE 🎨"):
            if img_desc:
                with st.spinner("Creating your image... this takes 10-20 seconds"):
                    result = generate_real_image(img_desc)
                    if isinstance(result, Image.Image):
                        st.image(result, caption="Made by MERAKI AI ✨", use_container_width=True)
                        # Download button
                        buf = io.BytesIO()
                        result.save(buf, format="PNG")
                        st.download_button("⬇️ DOWNLOAD IMAGE", data=buf.getvalue(), file_name="meraki_image.png", mime="image/png")
                    else:
                        st.write(result)
    with col_b:
        if st.button("CREATE PROMPT ONLY"):
            if img_desc:
                st.write(ask_meraki(img_desc, "Image - Create a very detailed image prompt"))

# PREDICT
elif mode == "📊 Predict":
    st.subheader("📊 Predict Mode")
    st.write("Upload your sales data or type your numbers")
    uploaded = st.file_uploader("Upload CSV (optional)", type=["csv", "txt"])
    data = st.text_area("Or paste your data", placeholder="Jan: 50,000, Feb: 65,000, Mar: 70,000. Predict April?")
    if uploaded:
        data = uploaded.read().decode("utf-8")[:3000]
        st.success("File uploaded!")
    if st.button("PREDICT 📊"):
        if data:
            with st.spinner("Analyzing..."):
                st.write(ask_meraki(data, "Predict - Explain trend simply, give prediction for next month, give 3 action tips for Kenyan small business"))

# VOICE - REAL INPUT
elif mode == "🎤 Voice":
    st.subheader("🎤 Voice Mode")
    st.write("Record your voice, or type. Meraki gives short answer perfect for speaking.")
    audio = st.audio_input("Record / Rekodi sauti yako")
    voice_text = st.text_input("Or type what you want to say", placeholder="Example: How do I price my mandazi business?")
    final_text = voice_text
    if audio:
        st.audio(audio)
        st.info("Voice recorded! For now, type what you said below to get answer. Full auto-transcription coming in v4.")
        # We keep audio for future, but use typed text
    if st.button("GET VOICE ANSWER 🎤"):
        if final_text:
            with st.spinner("Preparing..."):
                st.write(ask_meraki(final_text, "Voice - Give short, clear answer for speaking, max 3 sentences, simple words"))
        else:
            st.warning("Please type or record first.")

st.markdown("---")
st.markdown('<p style="text-align:center; color:#6B0F2A; font-weight:800;">MERAKI AI © 2026 • BUILT WITH SOUL IN KENYA 🇰🇪</p>', unsafe_allow_html=True)
st.markdown("---")
