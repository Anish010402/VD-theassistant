import streamlit as st

st.set_page_config(page_title="Legal Assistant", layout="wide")

st.title("📚 VD - Compliance & Legal Assistant")
st.markdown("#### Simplifying Regulations, One Chat at a Time.")

st.markdown("""
Welcome to *VD Compliance & Legal Assistant* – your AI-powered helper for navigating U.S. corporate regulations, drafting legal documents, and summarizing compliance materials.

---

### 💡 Key Features:
- 📄 Summarize regulations like GDPR, HIPAA, SOX, PCI DSS
- 🧾 Draft NDAs, Privacy Policies, and Terms of Service
- 🧠 Answer compliance questions with U.S. legal context
- 📂 Analyze and preview PDF documents
- ✅ Provide clear, non-binding legal insights
""")

# ✅ Switch page on button click (must be run as multipage app)
if st.button("👉 Get Started", use_container_width=True):
    st.session_state.view = "chat"
    st.rerun()
