# file: ai_tdm_suite/modules/tdm_digital_publishing_studio.py

import streamlit as st
import random
from datetime import datetime

# --- Inline Revenue Model Badges (can be replaced with global import if desired) ---
ALL_REVENUE_MODELS = [
    {
        "grade": "A", "category": "Digital Products", "name": "Online Courses/eBooks",
        "desc": "Sell digital content", "rationale": "90%+ margins, passive, top profitability."
    },
    {
        "grade": "A", "category": "Licensing/Franchising", "name": "Licensing IP",
        "desc": "License IP or patents", "rationale": "Passive, scalable, recurring, low risk."
    },
    {
        "grade": "A-", "category": "Affiliate Marketing", "name": "Affiliate Marketing",
        "desc": "Promote for commission", "rationale": "Zero inventory, 20-50% commission, passive."
    },
    {
        "grade": "B+", "category": "Transaction-Based", "name": "Commission/Fees",
        "desc": "Fee per sale", "rationale": "Scalable, 10-30% fees."
    },
]
MODULE_REVENUE_MODELS = {
    "TDM Digital Publishing Studio": [
        "Online Courses/eBooks", "Licensing IP", "Affiliate Marketing", "Commission/Fees"
    ]
}

def show_revenue_badges(module):
    """Display revenue model badges for this module."""
    enabled = [m for m in ALL_REVENUE_MODELS if m["name"] in MODULE_REVENUE_MODELS.get(module, [])]
    if enabled:
        st.markdown("**Active Revenue Models:**", unsafe_allow_html=True)
        badge_html = ""
        for m in enabled:
            badge_html += (
                f"<span style='background:#A51C30;color:#fff;padding:6px 14px 7px 14px;"
                f"border-radius:9px;font-weight:900;margin-right:7px;margin-bottom:7px;display:inline-block;'>"
                f"{m['name']} ({m['grade']})</span>"
            )
        st.markdown(badge_html, unsafe_allow_html=True)

def audit_log(action, user="anon"):
    """Print audit action to backend/console for traceability (MVP demo)."""
    print(f"[AUDIT] {datetime.now()} | {user}: {action}")

def main():
    st.header("📚 TDM Digital Publishing Studio (MVP Demo)")
    show_revenue_badges("TDM Digital Publishing Studio")
    st.markdown("""
Publish eBooks, scripts, sheet music, and courses. License and syndicate your digital work worldwide.
""")

    with st.expander("Upload & Publish New Work", expanded=False):
        work_title = st.text_input("Work Title", key="pub_title")
        work_type = st.selectbox("Type", ["eBook", "Script", "Sheet Music", "Video Course", "Other"], key="pub_type")
        author = st.text_input("Author/Creator", key="pub_author")
        pub_file = st.file_uploader("Upload File (pdf/mp4/zip)", type=["pdf", "mp4", "zip"], key="pub_file")
        pub_price = st.number_input("Set Price ($)", min_value=1, value=15, key="pub_price")
        if st.button("Publish Work", key="pub_list"):
            if work_title and author and pub_file:
                st.success(f"Published '{work_title}' by {author} at ${pub_price}. (Demo only)")
                audit_log("Published digital work", st.session_state.get("user_id", "anon"))
            else:
                st.error("All fields and file upload are required.")

    st.subheader("Published Works (Demo)")
    for i in range(2):
        st.info(
            f"**eBook Example #{i+1}** by Author {chr(65+i)} — "
            f"Price: ${random.randint(9,30)} (Demo)"
        )
        if st.button(f"Buy #{i+1} (Simulated)", key=f"buy_{i}"):
            st.success("Purchase complete! (Simulated for MVP)")
            audit_log("Purchased published work", st.session_state.get("user_id", "anon"))
