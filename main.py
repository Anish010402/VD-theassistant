import streamlit as st

st.set_page_config(page_title="Legal Assistant", layout="wide")

# --- HOME PAGE UI ---
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

# --- GET STARTED ---
st.markdown("### 🚀 Ready to Chat?")
if st.button("👉 Get Started", use_container_width=True):
    st.switch_page("💬 Chat Assistant")  # Use the sidebar label here

