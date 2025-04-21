import streamlit as st
import os
import uuid
import google.generativeai as genai
from PyPDF2 import PdfReader

# --- Configure Gemini API ---
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-pro")

# --- Page Config ---
st.set_page_config(page_title="VD - Legal Assistant", layout="wide")

# --- CSS Styling ---
st.markdown("""
<style>
.hero {
    text-align: center;
    padding: 3rem 2rem;
    background-color: #f8f9fa;
    border-radius: 20px;
    box-shadow: 0px 0px 20px rgba(0,0,0,0.05);
}
.hero h1 {
    font-size: 3rem;
    margin-bottom: 0.5rem;
}
.hero p {
    font-size: 1.2rem;
    color: #555;
}
.feature-box {
    padding: 1.5rem;
    background-color: #ffffff;
    border-radius: 15px;
    text-align: center;
    box-shadow: 0px 0px 15px rgba(0,0,0,0.05);
    transition: all 0.3s ease-in-out;
}
.feature-box:hover {
    box-shadow: 0px 0px 25px rgba(0,0,0,0.1);
}
img {
    max-width: 100%;
    border-radius: 10px;
}
.chat-bubble-user {
    background-color: #DCF8C6;
    padding: 10px 15px;
    border-radius: 15px;
    margin-bottom: 10px;
    max-width: 80%;
    align-self: flex-end;
    margin-left: auto;
}
.chat-bubble-bot {
    background-color: #F1F0F0;
    padding: 10px 15px;
    border-radius: 15px;
    margin-bottom: 10px;
    max-width: 80%;
    align-self: flex-start;
    margin-right: auto;
}
</style>
""", unsafe_allow_html=True)

# --- Session State Init ---
if "view" not in st.session_state:
    st.session_state.view = "home"
if "user_id" not in st.session_state:
    st.session_state.user_id = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state.messages = [{
        "role": "user",
        "parts": """
You are a Compliance and Legal Assistant expert, purpose-built to support legal professionals, compliance officers, and corporate teams in the United States.
You possess deep knowledge of GDPR, HIPAA, SOX, CCPA, PCI DSS, and related laws. Default to U.S. jurisdiction unless otherwise specified.

Always provide clear, professional, and non-binding legal information.
"""
    }]
if "uploaded_docs" not in st.session_state:
    st.session_state.uploaded_docs = []
if "uploaded_texts" not in st.session_state:
    st.session_state.uploaded_texts = {}

# --- Home Page ---
if st.session_state.view == "home":
    with st.container():
        st.markdown('<div class="hero">', unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/6698/6698127.png", width=120)
        st.markdown("<h1>VD Compliance & Legal Assistant</h1>", unsafe_allow_html=True)
        st.markdown("<p>Simplifying Regulations, One Chat at a Time.</p>", unsafe_allow_html=True)
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("### 💡 What can I help you with?")

    col1, col2, col3 = st.columns(3)
    with col1:
        st.markdown('<div class="feature-box">', unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/206/206865.png", width=60)
        st.markdown("#### 📘 Regulatory Insights")
        st.write("Summarize GDPR, HIPAA, SOX, CCPA, PCI DSS, and more.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col2:
        st.markdown('<div class="feature-box">', unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/1250/1250615.png", width=60)
        st.markdown("#### 📄 Draft Legal Docs")
        st.write("Generate NDAs, Privacy Policies, and TOS tailored for the U.S.")
        st.markdown('</div>', unsafe_allow_html=True)

    with col3:
        st.markdown('<div class="feature-box">', unsafe_allow_html=True)
        st.image("https://cdn-icons-png.flaticon.com/512/337/337946.png", width=60)
        st.markdown("#### 📂 Analyze PDFs")
        st.write("Upload and analyze contracts, policies, and legal forms.")
        st.markdown('</div>', unsafe_allow_html=True)

    st.markdown("---")

    if st.button("👉 Launch Chat Assistant", use_container_width=True):
        st.session_state.view = "chat"
        st.experimental_rerun()

# --- Chat Page ---
elif st.session_state.view == "chat":
    st.title("💬 VD - Compliance Chat Assistant")

    if st.button("⬅️ Back to Home"):
        st.session_state.view = "home"
        st.experimental_rerun()

    if st.button("🗑 Reset Chat"):
        st.session_state.messages = [st.session_state.messages[0]]
        st.session_state.uploaded_docs = []
        st.session_state.uploaded_texts = {}
        st.rerun()

    for msg in st.session_state.messages[1:]:
        bubble = "chat-bubble-user" if msg["role"] == "user" else "chat-bubble-bot"
        st.markdown(f"<div class='{bubble}'>{msg['parts']}</div>", unsafe_allow_html=True)

    with st.form(key="chat_form", clear_on_submit=True):
        user_input = st.text_input("💬 Type your message", key=f"chat_input_{len(st.session_state['messages'])}")
        submitted = st.form_submit_button("Send")

        if submitted and user_input:
            st.session_state.messages.append({"role": "user", "parts": user_input})
            try:
                response = model.generate_content(st.session_state.messages)
                st.session_state.messages.append({"role": "model", "parts": response.text})
                os.makedirs("logs", exist_ok=True)
                with open(f"logs/{st.session_state.user_id}.txt", "a", encoding="utf-8") as f:
                    f.write(f"\nUser: {user_input}\nBot: {response.text}\n")
                st.rerun()
            except Exception as e:
                st.error(f"Error: {str(e)}")

    uploaded_file = st.file_uploader("📄 Upload a PDF", type=["pdf"])
    if uploaded_file:
        file_name = uploaded_file.name
        if file_name not in st.session_state.uploaded_docs:
            reader = PdfReader(uploaded_file)
            extracted = "\n\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
            short_text = extracted[:3000]
            st.session_state.messages.append({
                "role": "user",
                "parts": f"Extracted from uploaded PDF '{file_name}':\n{short_text}"
            })
            st.session_state.uploaded_docs.append(file_name)
            st.session_state.uploaded_texts[file_name] = extracted
            st.rerun()

    if st.session_state.uploaded_docs:
        st.markdown("---")
        st.markdown("### 📄 Uploaded Documents Preview")
        for doc in st.session_state.uploaded_docs:
            st.markdown(f"**{doc}**")
            st.text_area("Preview", value=st.session_state.uploaded_texts[doc][:3000], height=200, disabled=True)
