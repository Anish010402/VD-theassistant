import streamlit as st
import google.generativeai as genai

# -- Page config
st.set_page_config(page_title="Legal Assistant", layout="wide")

# -- API key setup (replace this with env var for production)
genai.configure(api_key="AIzaSyA_z5f-qrOlSkIcKTk0T_AZoFJ1Ii1UfR0")

# -- Session state init
if "view" not in st.session_state:
    st.session_state.view = "home"
if "chat_history" not in st.session_state:
    st.session_state.chat_history = []

# --- HOME PAGE ---
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
    
    if st.button("👉 Get Started", use_container_width=True):
        st.session_state.view = "chat"
        st.rerun()

# --- CHAT PAGE ---
elif st.session_state.view == "chat":
    st.title("💬 VD - Compliance Chat Assistant")

    if st.button("🗑 Reset Chat"):
        st.session_state.view = "home"
        st.session_state.chat_history = []
        st.rerun()

    user_input = st.text_input("💬 Type your message:")

    if st.button("Send") and user_input.strip() != "":
        st.session_state.chat_history.append({"role": "user", "content": user_input})

        try:
            model = genai.GenerativeModel("gemini-pro")
            chat = model.start_chat(history=st.session_state.chat_history)
            response = chat.send_message(user_input)
            st.session_state.chat_history.append({"role": "model", "content": response.text})
        except Exception as e:
            st.error(f"❌ Error from Gemini: {e}")

    # Display conversation history
    for msg in st.session_state.chat_history:
        if msg["role"] == "user":
            st.write(f"👤 **You:** {msg['content']}")
        else:
            st.write(f"🤖 **Bot:** {msg['content']}")
