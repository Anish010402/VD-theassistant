import streamlit as st
from PIL import Image
import random

st.set_page_config(page_title="Legal Assistant", layout="wide")

# --- Session state initialization ---
if "view" not in st.session_state:
    st.session_state.view = "home"

# --- Helper: Carousel-like tips ---
tips = [
    "📌 Tip: Use this assistant to quickly understand complex laws like GDPR or HIPAA!",
    "📄 Tip: Draft professional NDAs, Privacy Policies, and more in seconds.",
    "🧠 Tip: Ask compliance questions in plain English — we simplify legal jargon for you.",
    "📂 Tip: Upload and summarize lengthy legal PDF documents instantly.",
]
current_tip = random.choice(tips)

# --- Home Page ---
if st.session_state.view == "home":
    col1, col2 = st.columns([2, 1])
    with col1:
        st.markdown("# 📚 VD - Compliance & Legal Assistant")
        st.markdown("#### Simplifying Regulations, One Chat at a Time.")
        st.markdown("Welcome to **VD Compliance & Legal Assistant** – your AI-powered helper for navigating U.S. corporate regulations, drafting legal documents, and summarizing compliance materials.")
        st.markdown("##### 💡 Key Features:")
        st.markdown("""
        - 📄 Summarize regulations like **GDPR, HIPAA, SOX, PCI DSS**
        - 🧾 Draft **NDAs**, **Privacy Policies**, and **Terms of Service**
        - 🧠 Answer compliance questions in a U.S. legal context
        - 📂 Analyze and preview PDF documents
        - ✅ Get non-binding legal insights – fast and simple
        """)
        st.success(current_tip)
        if st.button("👉 Get Started", use_container_width=True):
            st.session_state.view = "chat"
            st.experimental_rerun()

    with col2:
        st.image("https://cdn-icons-png.flaticon.com/512/1973/1973808.png", width=250, caption="Your AI Legal Guide")

# --- Chat Page ---
elif st.session_state.view == "chat":
    st.markdown("## 💬 VD - Compliance Chat Assistant")
    st.markdown("Ask questions or get help drafting documents in real-time.")

    # Top controls
    col1, col2 = st.columns([1, 4])
    with col1:
        if st.button("🔄 Reset"):
            st.session_state.view = "home"
            st.experimental_rerun()

    st.markdown("---")

    # Chat area
    with st.container():
        st.markdown("### 💬 Start a conversation")
        st.markdown("Ask about compliance rules, draft documents, or upload a legal PDF.")

        user_input = st.text_input("Your message")
        if st.button("Send"):
            st.write(f"🧑 You: {user_input}")
            st.write("🤖 Bot: _(Response will appear here)_")

    st.markdown("---")
    st.info("Need to upload a document? That feature is coming soon!")

