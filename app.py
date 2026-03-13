import streamlit as st
import google.generativeai as genai
import PIL.Image

# API Key jo aapne di thi
API_KEY = "AIzaSyDP5xs3w2rwHd7AaaDVO-3VEffHwY82Ys0"

try:
    genai.configure(api_key=API_KEY)
    model = genai.GenerativeModel('gemini-1.5-flash')
except:
    pass

st.set_page_config(page_title="Mihir AI", layout="centered")

# Branding & CSS (No Patti)
st.markdown("""
    <style>
    header, footer, .stDeployButton, #MainMenu {visibility: hidden !important; display: none !important;}
    [data-testid="stStatusWidget"], [data-testid="stToolbar"] {display: none !important;}
    body, .main { background-color: #000000 !important; color: white !important; }
    .brand-title { color: white; font-size: 38px; font-weight: bold; text-align: center; margin-top: -30px; }
    .stChatInputContainer { border-radius: 30px !important; background: #1E1F20 !important; border: 1px solid #333 !important; }
    .stButton button { background-color: #1E1F20; color: white; border: 1px solid #333; border-radius: 15px; height: 80px; width: 100%; text-align: left; }
    </style>
    """, unsafe_allow_html=True)

st.markdown('<div class="brand-title">Mihir AI</div>', unsafe_allow_html=True)

if "messages" not in st.session_state: st.session_state.messages = []

# 4 Buttons Display
if not st.session_state.messages:
    st.markdown("<h2 style='text-align:center;'>Hi Praveen</h2>", unsafe_allow_html=True)
    c1, c2 = st.columns(2)
    with c1:
        if st.button("🎨 Create Photo"): st.session_state.temp = "Create art: "
        if st.button("🚀 Boost My Day"): st.session_state.temp = "Kuch mast sunao!"
    with c2:
        if st.button("🧠 Solve Anything"): st.session_state.temp = "Help me solve: "
        if st.button("☸️ Kundali Reading"): st.session_state.temp = "Analyze my kundali."

for m in st.session_state.messages:
    with st.chat_message(m["role"]):
        if "img" in m: st.image(m["img"])
        st.markdown(m["content"])

prompt = st.chat_input("Ask Mihir AI...")
if "temp" in st.session_state: prompt = st.session_state.pop("temp")

if prompt:
    st.session_state.messages.append({"role": "user", "content": prompt})
    with st.chat_message("assistant"):
        try:
            if "Create" in prompt:
                url = f"https://pollinations.ai/p/{prompt.replace(' ', '%20')}?width=1024&height=1024"
                st.image(url)
                st.session_state.messages.append({"role": "assistant", "content": "Done!", "img": url})
            else:
                # Direct call bina kisi extra instruction ke (Fastest)
                response = model.generate_content(prompt)
                st.markdown(response.text)
                st.session_state.messages.append({"role": "assistant", "content": response.text})
        except:
            st.markdown("Dost, ek baar page Refresh karein aur phir se puchiye!")
