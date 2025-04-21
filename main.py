import streamlit as st
from PIL import Image
import time

st.set_page_config(page_title="Legal Assistant", layout="wide", page_icon="📚")

# Background color and style tweaks using markdown
def set_background():
    st.markdown("""
        <style>
            .main {
                background-color: #f4f6f9;
            }
            .block-container {
                padding-top: 2rem;
                padding-bottom: 2rem;
            }
            .stButton button {
                border-radius: 8px;
                font-weight: 600;
                background-color: #0055A5;
                color: white;
                padding: 10px 20px;
            }
            .stButton button:hover {
                background-color: #004080;
            }
        </style>
    """, unsafe_allow_html=True)

set_background()

# Initialize view
if "view" not in st.session_state:
    st.session_state.view = "home"

# --- Home Page ---
if st.session_state.view == "home":
    col1, col2 = st.columns([2, 3])
    with col1:
        st.image("https://images.unsplash.com/photo-1554224154-22dec7ec8818", caption="Your Legal AI Partner", use_column_width=True)
    with col2:
        st.title("📚 VD - Compliance & Legal Assistant")
        st.subheader("Simplifying Regulations, One Chat at a Time.")
        st.write("""
        Welcome to **VD Compliance & Legal Assistant** – your AI-powered partner for navigating U.S. corporate regulations, drafting legal documents, and understanding compliance materials.
        """)

        st.markdown("### 💡 Key Features:")
        st.markdown("""
        - 📄 Summarize regulations like **GDPR, HIPAA, SOX, PCI DSS**
        - 🧾 Draft **NDAs, Privacy Policies, Terms of Service**
        - 🧠 Answer compliance questions with **U.S. legal context**
        - 📂 Analyze and preview **PDF documents**
        - ✅ Provide clear, **non-binding legal insights**
        """)

        if st.button("👉 Get Started", use_container_width=True):
            st.session_state.view = "chat"
            st.rerun()

    # Image carousel simulation
    st.markdown("### 🔄 Our Assistant in Action:")
    img_urls = [
        "https://images.unsplash.com/photo-1581091870632-7f63b2120baf",
        "https://images.unsplash.com/photo-1573164713347-df1e007f11e3",
        "https://images.unsplash.com/photo-1559027615-cd1a0f73946e"
    ]
    carousel_col = st.columns(len(img_urls))
    for i, img_url in enumerate(img_urls):
        with carousel_col[i]:
            st.image(img_url, use_column_width=True)

# --- Chat Page ---
elif st.session_state.view == "chat":
    st.title("💬 VD - Compliance Chat Assistant")

    col1, col2 = st.columns([8, 2])
    with col2:
        if st.button("🔄 Reset"):
            st.session_state.view = "home"
            st.rerun()

    st.markdown("###### Ask me anything about legal compliance, policies, or regulations:")

    user_input = st.text_input("💬 Your Message")
    if st.button("Send"):
        st.markdown(f"**You:** {user_input}")
        # Simulated bot response
        with st.spinner("VD Assistant is typing..."):
            time.sleep(1)
        st.markdown(f"**VD Assistant:** This is a placeholder response. (Actual model response will be here.)")
