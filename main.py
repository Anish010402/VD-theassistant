import streamlit as st
import google.generativeai as genai
from PyPDF2 import PdfReader
import os

# Configure Gemini with Streamlit secret
genai.configure(api_key=st.secrets["GEMINI_API_KEY"])

# Load the Gemini model
model = genai.GenerativeModel("gemini-pro")

# Set page config
st.set_page_config(page_title="Legal Assistant", layout="wide")

# Initialize session state
if "view" not in st.session_state:
    st.session_state.view = "home"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- Function to send message to Gemini ---
def send_message_to_gemini(user_message):
    chat = model.start_chat(history=st.session_state.chat_history)
    response = chat.send_message(user_message)
    return response.text

# --- Function to summarize PDF ---
def summarize_pdf(uploaded_file):
    try:
        pdf_reader = PdfReader(uploaded_file)
        text = ""
        for page in pdf_reader.pages:
            text += page.extract_text()
        
        # Send extracted text to Gemini for summarization
        return send_message_to_gemini(f"Summarize the following compliance document:\n\n{text[:1000]}")  # Limiting to 1000 chars
    except Exception as e:
        return f"Error processing PDF: {e}"

# --- Home Page ---
if st.session_state.view == "home":
    st.title("📚 VD - Compliance & Legal Assistant")
    st.markdown("#### Simplifying Regulations, One Chat at a Time.")

    st.markdown("""
    Welcome to VD Compliance & Legal Assistant – your AI-powered helper for navigating U.S. corporate regulations, drafting legal documents, and summarizing compliance materials.

    ---

    ### 💡 Key Features:
    - 📄 Summarize regulations like GDPR, HIPAA, SOX, PCI DSS
    - 🧾 Draft NDAs, Privacy Policies, and Terms of Service
    - 🧠 Answer compliance questions with U.S. legal context
    - 📂 Analyze and preview PDF documents
    - ✅ Provide clear, non-binding legal insights
    """)

    # PDF Upload
    uploaded_file = st.file_uploader("Upload a PDF document for summarization", type="pdf")
    if uploaded_file is not None:
        summary = summarize_pdf(uploaded_file)
        st.write(summary)

    if st.button("👉 Get Started", use_container_width=True):
        st.session_state.view = "chat"
        st.rerun()

# --- Chat Page ---
elif st.session_state.view == "chat":
    st.title("💬 VD - Compliance Chat Assistant")

    # Reset button
    if st.button("🗑 Reset Chat"):
        st.session_state.view = "home"
        st.session_state.chat_history = []
        st.rerun()

    # Display chat history
    for user, bot in st.session_state.chat_history:
        st.markdown(f"**You:** {user}")
        st.markdown(f"**Assistant:** {bot}")

    # Input and send
    user_input = st.text_input("💬 Type your message", key="chat_input")
    if st.button("Send") and user_input.strip():
        bot_reply = send_message_to_gemini(user_input)
        st.session_state.chat_history.append((user_input, bot_reply))
        st.rerun()

