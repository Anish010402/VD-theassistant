import streamlit as st

# --- Page Configuration ---
st.set_page_config(page_title="VD - Compliance & Legal Assistant", layout="centered")

# Initialize session state
if "view" not in st.session_state:
    st.session_state.view = "home"

# --- Home View ---
if st.session_state.view == "home":
    st.markdown("""
        <style>
            .big-title {
                font-size: 2.5rem;
                font-weight: 800;
                color: #2c3eeb;
                margin-bottom: 0.2rem;
            }
            .subtitle {
                font-size: 1.25rem;
                color: #5e6c84;
                margin-bottom: 2rem;
            }
            .feature-card {
                background-color: #f9f9f9;
                padding: 1rem 1.5rem;
                border-radius: 12px;
                margin-bottom: 1rem;
                border-left: 5px solid #2c3eeb;
            }
            .get-started {
                text-align: center;
                margin-top: 2rem;
            }
            .disclaimer {
                font-size: 0.85rem;
                color: gray;
                text-align: center;
                margin-top: 2rem;
            }
        </style>
    """, unsafe_allow_html=True)

    st.markdown('<div class="big-title">📖 VD - Compliance & Legal Assistant</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Simplifying Regulations, One Chat at a Time</div>', unsafe_allow_html=True)

    st.markdown("Welcome to VD Compliance & Legal Assistant – your AI-powered helper for navigating U.S. corporate regulations, drafting legal documents, and summarizing compliance materials.")
    st.markdown("---")

    st.markdown('<div class="feature-card">📄 <strong>Summarize regulations</strong> like GDPR, HIPAA, SOX, PCI DSS</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-card">🧾 <strong>Draft legal documents</strong> including NDAs, Privacy Policies, and Terms of Service</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-card">💬 <strong>Answer compliance questions</strong> with U.S. legal context</div>', unsafe_allow_html=True)
    st.markdown('<div class="feature-card">📂 <strong>Analyze and preview PDF documents</strong> for legal review</div>', unsafe_allow_html=True)

    with st.container():
        if st.button("🚀 Get Started", use_container_width=True):
            st.session_state.view = "chat"
            st.experimental_rerun()

    st.markdown('<div class="disclaimer">Advice provided is for informational purposes only and does not constitute legal advice.</div>', unsafe_allow_html=True)

# --- Chat View ---
elif st.session_state.view == "chat":
    st.title("💬 VD - Compliance Chat Assistant")

    if st.button("🔁 Reset to Home"):
        st.session_state.view = "home"
        st.experimental_rerun()

    st.write("This is the chat assistant view.")
    user_input = st.text_input("💬 Type your message")
    if st.button("Send"):
        st.write(f"You said: {user_input}")
        st.write("Bot response: (This is where the bot response would appear)")
