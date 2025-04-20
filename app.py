import streamlit as st
import google.generativeai as genai
import os
import uuid
from PyPDF2 import PdfReader

# --- CONFIGURATION ---
genai.configure(api_key=st.secrets["API_KEY"])
model = genai.GenerativeModel("gemini-1.5-pro")

# --- SYSTEM PROMPT ---
system_prompt = {
    "role": "user",
    "parts": """
You are a Compliance and Legal Assistant expert, purpose-built to support legal professionals, compliance officers, and corporate teams...
(Default jurisdiction: United States unless otherwise specified.)
"""
}

# --- SESSION STATE INIT ---
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

# --- CUSTOM STYLES ---
st.markdown("""
<style>
/* Reset layout padding */
.block-container {
    padding: 1.5rem 2rem 1.5rem 2rem;
}

/* Chat layout styles */
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

/* Buttons */
button[kind="secondary"] {
    background-color: #f44336 !important;
    color: white !important;
    border: none;
    padding: 8px 14px;
    border-radius: 8px;
}

.stTextInput>div>div>input {
    padding: 10px !important;
}
</style>
""", unsafe_allow_html=True)

# --- TITLE + RESET ---
st.title("📚 VD - Compliance & Legal Assistant")

with st.container():
    if st.button("🗑 Reset Chat", use_container_width=True):
        st.session_state["messages"] = [system_prompt]
        st.session_state["uploaded_docs"] = []
        st.session_state["uploaded_texts"] = {}
        st.rerun()

# --- CHAT BUBBLES ---
with st.container():
    for msg in st.session_state["messages"][1:]:
        if msg["role"] == "user":
            st.markdown(f"<div class='chat-bubble-user'>{msg['parts']}</div>", unsafe_allow_html=True)
        else:
            st.markdown(f"<div class='chat-bubble-bot'>{msg['parts']}</div>", unsafe_allow_html=True)

# --- INPUT FORM WITH BUTTON ---
with st.form(key="chat_form", clear_on_submit=True):
    user_input = st.text_input("💬 Type your message", key="chat_input")
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

# --- FILE UPLOADER ---
uploaded_file = st.file_uploader("📄 Upload a PDF (e.g., contract, policy, legal doc)", type=["pdf"])

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

# --- FLOATING PREVIEW PANEL ---
if st.session_state["uploaded_docs"]:
    preview_html = "<div id='right-panel'><h4>📄 Uploaded Docs</h4>"
    for doc in st.session_state["uploaded_docs"]:
        preview_html += f"<b>📘 {doc}</b><div class='pdf-preview'>{st.session_state['uploaded_texts'][doc][:3000]}</div>"
    preview_html += "</div>"
    st.markdown(preview_html, unsafe_allow_html=True)
