import streamlit as st
import google.generativeai as genai
import PIL.Image
import time

# --- 1. API CONNECTION (NAYI KEY SET HAI) ---
API_KEY = "AIzaSyDP5xs3w2rwHd7AaaDVO-3VEffHwY82Ys0"

def get_ai_response(prompt_text, image_file=None):
    try:
        genai.configure(api_key=API_KEY)
        model = genai.GenerativeModel('gemini-1.5-flash')
        if image_file:
            img = PIL.Image.open(image_file)
            response = model.generate_content([prompt_text, img])
        else:
            response = model.generate_content(f"You are Mihir AI, a friendly and smart boy. Reply in Hinglish. Help the user: {prompt_text}")
        return response.text
    except Exception:
        return "Dost, server thoda busy hai, ek baar phir se koshish karo!"

st.set_page_config(page_title="Mihir AI", layout="centered")

# --- 2. SAKT PROFESSIONAL CSS (No Patti, No Error Boxes) ---
st.markdown("""
    <style>
    /* Sabhi faltu patti aur branding hide karo */
    header, footer, .stDeployButton, #MainMenu, #stDecoration {visibility: hidden !important; display: none !important;}
    [data-testid="stStatusWidget"], [data-testid="stToolbar"] {display: none !important;}
    div[class*="st-emotion-cache-1wb59as"], div[class*="st-emotion-cache-80989f"] {display: none !important;}
    [data-testid="stFileUploader"] section { display: none !important; }

    /* Pure Black Theme */
    body, .main { background-color: #000000 !important; color: white !important; }
    [data-testid="stChatMessageAvatarUser"], [data-testid="stChatMessageAvatarAssistant"] {display: none !important;}
    [data-testid="stChatMessage"] { background-color: transparent !important; border: none !important; }

    /* Input & Plus Button Positioning */
    .stChatInputContainer { border-radius: 30px !important; background: #1E1F20 !important; border: 1px solid #333 !important; }
    [data-testid="stFileUploader"] { position: fixed !important; bottom: 35px !important; left: 20px !important; width: 45px !important; z-index: 1001; }
    [data-testid="stFileUploader"]::before { content: "＋"; font-size: 26px; color: #888; display: flex; align-items: center; justify-content: center; }
    
    /* 4-Grid Buttons */
    .stButton button { background-color: #1E1F20; color: white; border: 1px solid #333; border-radius: 15px; height: 85px; width: 100%; text-align: left; padding: 15px; }
    
    /* Banner Ad Box (Bottom) */
    .banner-ads { position: fixed; bottom: 0; left: 0; width: 100%; background: #000; text-align: center; z-index: 999; }
    </style>
    """, unsafe_allow_html=True)

# Banner Ad niche
st.markdown('<div class="banner-ads"><script>if(window.AppCreator24){window.AppCreator24.showBanner();}</script></div>', unsafe_allow_html=True)

# --- 3. SESSION STATE ---
if "user_name" not in st.session_state: st.session_state.user_name = "Praveen pratap mishra"
if "messages" not in st.session_state: st.session_state.messages = []
if "photo_count" not in st.session_state: st.session_state.photo_count = 0

# --- 4. 4-OPTION UI ---
if not st.session_state.messages:
    st.markdown(f"<h1>Hi {st.session_state.user_name}</h1>", unsafe_allow_html=True)
    st.markdown("<h3 style='color:#888;'>Main Mihir AI hoon. Kya madad karun?</h3>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎨 Create Photo"): st.session_state.temp = "Create art: "
        if st.button("🚀 Boost My Day"): st.session_state.temp = "Mihir dost, kuch mast sunao!"
    with c2:
        if st.button("🧠 Solve Anything"): st.session_state.temp = "Help me solve: "
        if st.button("☸️ Kundali Reading"): st.session_state.temp = "Analyze my kundali."

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "img" in m: st.image(m["img"])
        st.markdown(m["content"])

# --- 5. RESPONSE LOGIC (Jawab Dega 100%) ---
up_file = st.file_uploader("", type=['png', 'jpg', 'jpeg'])
prompt = st.chat_input("Ask Mihir AI...")

if "temp" in st.session_state: prompt = st.session_state.pop("temp")

if prompt or up_file:
    u_input = prompt if prompt else "Analyze this image"
    st.session_state.messages.append({"role": "user", "content": u_input})
    
    with st.chat_message("assistant"):
        # Reward Ads Trigger (5 photos ke baad 2 ads)
        is_photo = any(x in u_input.lower() for x in ["create", "photo", "art", "banao"])
        if is_photo and st.session_state.photo_count >= 5:
            st.warning("Reward ads loading...")
            st.markdown("<script>if(window.AppCreator24){window.AppCreator24.showRewardVideo(); window.AppCreator24.showRewardVideo();}</script>", unsafe_allow_html=True)
            st.session_state.photo_count = 0
            st.stop()

        if is_photo:
            url = f"https://pollinations.ai/p/{u_input.replace(' ', '%20')}?width=1024&height=1024&seed=42&model=flux"
            st.image(url)
            st.session_state.photo_count += 1
            st.session_state.messages.append({"role": "assistant", "content": "Aapki photo taiyar hai!", "img": url})
        else:
            # AI Jawab Dega
            response_text = get_ai_response(u_input, up_file)
            st.markdown(response_text)
            st.session_state.messages.append({"role": "assistant", "content": response_text})

st.markdown("<br><br>", unsafe_allow_html=True)
