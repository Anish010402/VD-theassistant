import streamlit as st

# --- State Initialization ---
if "page" not in st.session_state:
    st.session_state.page = "home"  # Default to home page

# --- Home Page ---
if st.session_state.page == "home":
    # Home page UI
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
    
    # Button to navigate to Chat Assistant page
    if st.button("👉 Get Started", use_container_width=True):
        st.session_state.page = "chat"  # Change page state to "chat"
        st.experimental_rerun()  # Trigger rerun to reload and switch to chat page

# --- Chat Page ---
elif st.session_state.page == "chat":
    # Chat Assistant Page UI
    st.title("💬 VD - Compliance Chat Assistant")

    # Reset chat button
    if st.button("🗑 Reset Chat"):
        st.session_state.page = "home"  # Reset back to home page
        st.experimental_rerun()  # Trigger rerun to go back to home page
    
    st.write("This is the chat assistant view.")
    
    # Example chat interface (this can be replaced with actual chat logic)
    user_input = st.text_input("💬 Type your message")
    if st.button("Send"):
        st.write(f"You said: {user_input}")
        st.write("Bot response: (This is where the bot response would appear)")

    # You can implement your actual chat functionality here as needed
