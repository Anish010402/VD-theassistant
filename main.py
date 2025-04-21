import streamlit as st

# Set up the page configuration
st.set_page_config(page_title="Legal Assistant", layout="wide")

# Initialize session state if not already initialized
if "view" not in st.session_state:
    st.session_state.view = "home"  # Default view

# --- Home Page ---
if st.session_state.view == "home":
    # Home page UI
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

    # Button to navigate to Chat Assistant page
    if st.button("👉 Get Started", use_container_width=True):
        st.session_state.view = "chat"  # Switch to chat view
        st.experimental_rerun()  # Trigger rerun to reload the app and switch the view

# --- Chat Page ---
elif st.session_state.view == "chat":
    # Chat Assistant Page UI
    st.title("💬 VD - Compliance Chat Assistant")

    # Reset chat button (to go back to home page)
    if st.button("🗑 Reset Chat"):
        st.session_state.view = "home"  # Reset to home view
        st.experimental_rerun()  # Trigger rerun to go back to home page
    
    st.write("This is the chat assistant view.")
    
    # Example chat interface (you can replace this with your actual chat logic)
    user_input = st.text_input("💬 Type your message")
    if st.button("Send"):
        st.write(f"You said: {user_input}")
        st.write("Bot response: (This is where the bot response would appear)")

    # You can implement the actual chat functionality here as needed
