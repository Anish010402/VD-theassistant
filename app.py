import streamlit as st
import google.generativeai as genai
import os
import uuid
from PyPDF2 import PdfReader

# --- Configure Gemini API ---
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-pro")

# --- Page Setup ---
st.set_page_config(page_title="Chat | Legal Assistant", layout="wide")

# --- Sidebar Navigation ---
with st.sidebar:
    st.page_link("main.py", label="🏠 Home")
    st.page_link("app.py", label="💬 Chat Assistant")

# --- System Prompt ---
system_prompt = {
    "role": "user",
    "parts": """
You are a Compliance and Legal Assistant expert, purpose-built to support legal professionals, compliance officers, and corporate teams in the United States.
You possess deep knowledge of GDPR, HIPAA, SOX, CCPA, PCI DSS, and related laws. Default to U.S. jurisdiction unless otherwise specified.

Always provide clear, professional, and non-binding legal information.
"""
}

# --- Session State Init ---
if "user_id" not in st.session_state:
    st.session_state["user_id"] = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state["messages"] = [system_prompt]
if "input_submitted" not in st.session_state:
    st.session_state["input_submitted"] = False
if "uploaded_docs" not in st.session_state:
    st.session_state["uploaded_docs"] = []
if "uploaded_texts" not in st.session_state:
    st.session_state["uploaded_texts"] = {}

# --- Custom CSS ---
st.markdown("""
<style>
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
#right-panel {
    position: fixed;
    top: 75px;
    right: 0;
    width: 320px;
    height: 90%;
    background-color: #ffffff;
    border-left: 1px solid #ccc;
    padding: 20px;
    overflow-y: auto;
    z-index: 998;
}
.pdf-preview {
    font-size: 0.85rem;
    white-space: pre-wrap;
    max-height: 200px;
    overflow-y: auto;
    border: 1px solid #eee;
    padding: 8px;
    margin-bottom: 15px;
    border-radius: 8px;
    background-color: #f8f8f8;
}
</style>
""", unsafe_allow_html=True)

# --- Title & Reset ---
st.title("💬 VD - Compliance Chat Assistant")
if st.button("🗑 Reset Chat"):
    st.session_state["messages"] = [system_prompt]
    st.session_state["uploaded_docs"] = []
    st.session_state["uploaded_texts"] = {}
    st.rerun()

# --- Chat History as Bubbles ---
for msg in st.session_state["messages"][1:]:
    bubble = "chat-bubble-user" if msg["role"] == "user" else "chat-bubble-bot"
    st.markdown(f"<div class='{bubble}'>{msg['parts']}</div>", unsafe_allow_html=True)

# --- Chat Input Form ---
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("💬 Type your message", key=f"chat_input_{len(st.session_state['messages'])}")
    submitted = st.form_submit_button("Send")

    if submitted and user_input:
        st.session_state["messages"].append({"role": "user", "parts": user_input})
        try:
            response = model.generate_content(st.session_state["messages"])
            st.session_state["messages"].append({"role": "model", "parts": response.text})
            os.makedirs("logs", exist_ok=True)
            with open(f"logs/{st.session_state['user_id']}.txt", "a", encoding="utf-8") as f:
                f.write(f"\nUser: {user_input}\nBot: {response.text}\n")
            st.rerun()
        except Exception as e:
            st.error(f"Error: {str(e)}")

# --- PDF Upload ---
uploaded_file = st.file_uploader("📄 Upload a PDF", type=["pdf"])
if uploaded_file:
    file_name = uploaded_file.name
    if file_name not in st.session_state["uploaded_docs"]:
        reader = PdfReader(uploaded_file)
        extracted = "\n\n".join([page.extract_text() for page in reader.pages if page.extract_text()])
        short_text = extracted[:3000]
        st.session_state["messages"].append({
            "role": "user",
            "parts": f"Extracted from uploaded PDF '{file_name}':\n{short_text}"
        })
        st.session_state["uploaded_docs"].append(file_name)
        st.session_state["uploaded_texts"][file_name] = extracted
        st.rerun()

# --- Right Margin PDF Preview Panel ---
if st.session_state["uploaded_docs"]:
    preview_html = "<div id='right-panel'><h4>📄 Uploaded Docs</h4>"
    for doc in st.session_state["uploaded_docs"]:
        preview_html += f"<b>📘 {doc}</b><div class='pdf-preview'>{st.session_state['uploaded_texts'][doc][:3000]}</div>"
    preview_html += "</div>"
    st.markdown(preview_html, unsafe_allow_html=True)
