import streamlit as st
import uuid
import os
from PyPDF2 import PdfReader
import google.generativeai as genai

# --- Set page config ---
st.set_page_config(page_title="VD Assistant", layout="wide")

# --- Init Session State ---
if "view" not in st.session_state:
    st.session_state.view = "home"
if "user_id" not in st.session_state:
    st.session_state["user_id"] = str(uuid.uuid4())
if "messages" not in st.session_state:
    st.session_state["messages"] = [{
        "role": "user",
        "parts": """
You are a Compliance and Legal Assistant expert, purpose-built to support legal professionals, compliance officers, and corporate teams in the United States.
You possess deep knowledge of GDPR, HIPAA, SOX, CCPA, PCI DSS, and related laws. Default to U.S. jurisdiction unless otherwise specified.

Always provide clear, professional, and non-binding legal information.
"""
    }]
if "uploaded_docs" not in st.session_state:
    st.session_state["uploaded_docs"] = []
if "uploaded_texts" not in st.session_state:
    st.session_state["uploaded_texts"] = {}

# --- View Switcher ---
def go_to_chat():
    st.session_state.view = "chat"

# --- HOME VIEW ---
if st.session_state.view == "home":
    st.title("📚 VD - Compliance & Legal Assistant")
    st.markdown("#### Simplifying Regulations, One Chat at a Time.")

    st.markdown("""
Welcome to *VD Compliance & Legal Assistant* – your AI-powered helper for navigating U.S. corporate regulations, drafting legal documents, and summarizing compliance materials.

### 🔍 What It Can Do:
- Summarize policies, contracts, and regulations
- Draft NDAs, Privacy Policies, and Terms of Service
- Help with U.S. regulatory frameworks (GDPR, HIPAA, SOX, PCI DSS, etc.)
- Extract and preview PDF documents
- Provide intelligent compliance guidance

---

💡 Whether you're a lawyer, compliance officer, or startup founder — this tool streamlines legal interpretation and document analysis in plain English.
    """)

    st.markdown("### 🚀 Ready to Chat?")
    if st.button("👉 Get Started", use_container_width=True):
        go_to_chat()

# --- CHAT VIEW ---
elif st.session_state.view == "chat":
    genai.configure(api_key=st.secrets["API_KEY"])
    model = genai.GenerativeModel("gemini-1.5-pro")

    with st.sidebar:
        if st.button("🏠 Back to Home"):
            st.session_state.view = "home"
        st.markdown("### 📄 Uploaded Docs")
        for doc in st.session_state["uploaded_docs"]:
            preview = st.session_state["uploaded_texts"].get(doc, "")[:3000]
            st.markdown(f"**{doc}**\n\n```text\n{preview}```")

    st.title("💬 VD - Compliance Chat Assistant")

    if st.button("🗑 Reset Chat"):
        st.session_state["messages"] = [st.session_state["messages"][0]]
        st.session_state["uploaded_docs"] = []
        st.session_state["uploaded_texts"] = {}
        st.rerun()

    for msg in st.session_state["messages"][1:]:
        bubble_class = "chat-bubble-user" if msg["role"] == "user" else "chat-bubble-bot"
        st.markdown(f"<div class='{bubble_class}'>{msg['parts']}</div>", unsafe_allow_html=True)

    with st.form("chat_form", clear_on_submit=True):
        user_input = st.text_input("💬 Type your message", key=f"chat_input_{len(st.session_state['messages'])}")
        if st.form_submit_button("Send") and user_input:
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

# --- CSS Chat Styling ---
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
</style>
""", unsafe_allow_html=True)



# import streamlit as st

# st.set_page_config(page_title="Legal Assistant", layout="wide")

# st.title("📚 VD - Compliance & Legal Assistant")
# st.markdown("#### Simplifying Regulations, One Chat at a Time.")

# st.markdown("""
# Welcome to *VD Compliance & Legal Assistant* – your AI-powered helper for navigating U.S. corporate regulations, drafting legal documents, and summarizing compliance materials.

# ---

# ### 💡 Key Features:
# - 📄 Summarize regulations like GDPR, HIPAA, SOX, PCI DSS
# - 🧾 Draft NDAs, Privacy Policies, and Terms of Service
# - 🧠 Answer compliance questions with U.S. legal context
# - 📂 Analyze and preview PDF documents
# - ✅ Provide clear, non-binding legal insights
# """)

# # ✅ Switch page on button click (must be run as multipage app)
# if st.button("👉 Get Started", use_container_width=True):
#     st.session_state.view = "chat"
#     st.rerun()
