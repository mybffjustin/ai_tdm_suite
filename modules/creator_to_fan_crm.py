# file: ai_tdm_suite/modules/creator_to_fan_crm.py

import streamlit as st
import pandas as pd
import random
from datetime import datetime

# ==== Revenue Model Badges (configurable per module) ====
ALL_REVENUE_MODELS = [
    {"grade": "A",   "category": "Membership",            "name": "Membership Site",      "desc": "Community, perks",            "rationale": "Predictable, scalable, high LTV."},
    {"grade": "A",   "category": "Marketplaces/Aggregator","name": "Marketplace/Aggregator","desc": "Connect buyers/sellers",    "rationale": "Network effects, high profitability."},
    {"grade": "B+",  "category": "Transaction-Based",     "name": "Commission/Fees",       "desc": "Fee per sale",                "rationale": "Scalable, 10-30% fees."},
    {"grade": "A-",  "category": "Affiliate Marketing",   "name": "Affiliate Marketing",   "desc": "Promote for commission",      "rationale": "Zero inventory, passive."},
    {"grade": "B",   "category": "Customer Loyalty",      "name": "Loyalty/Rewards",       "desc": "Incentivize repeats",         "rationale": "Retention, scalable digital."},
]
MODULE_REVENUE_MODELS = {
    "Creator-to-Fan AI CRM": [
        "Membership Site", "Marketplace/Aggregator", "Commission/Fees", "Affiliate Marketing", "Loyalty/Rewards"
    ]
}

def show_revenue_badges(module):
    """Display all revenue models enabled for this module as stylish badges."""
    enabled = [m for m in ALL_REVENUE_MODELS if m["name"] in MODULE_REVENUE_MODELS.get(module, [])]
    st.markdown("**Active Revenue Models:**", unsafe_allow_html=True)
    badge_html = ""
    for m in enabled:
        badge_html += (
            f"<span style='background:#A51C30;color:#fff;padding:6px 14px 7px 14px;"
            f"border-radius:9px;font-weight:900;margin-right:7px;margin-bottom:7px;display:inline-block;'>"
            f"{m['name']} ({m['grade']})</span>"
        )
    st.markdown(badge_html, unsafe_allow_html=True)

# ==== Helpers ====
def consent_checkbox(label):
    """Show a checkbox and return True if checked."""
    return st.checkbox(f"☑️ I consent to {label}")

def audit_log(action, user="anon"):
    """Simple audit log for MVP (stdout), swap for persistent logging in prod."""
    print(f"[AUDIT] {datetime.now()} | {user}: {action}")

def is_pro():
    """Detect if user is on Pro plan."""
    return st.session_state.get("pro_user", False)

# ==== Main App ====
def main():
    st.header("🧑‍🎤 Creator-to-Fan AI CRM (MVP Demo)")
    show_revenue_badges("Creator-to-Fan AI CRM")
    st.markdown("""
**Features:**  
- Import/upload your fan list  
- AI-powered audience segmentation  
- Smart messaging  
- Engagement scores for each fan (simulated)  
- Marketplace for 3rd-party sellers/fans
    """)

    # --- Fan List Upload & Segmentation Demo ---
    uploaded_fans = st.file_uploader("Upload Fan List (CSV: name,email,city,interests)", type=["csv"])
    if uploaded_fans:
        if not consent_checkbox("use of uploaded fan data for segmentation and messaging."):
            st.warning("Consent required to proceed.")
            st.stop()
        fans_df = pd.read_csv(uploaded_fans)
        st.dataframe(fans_df.head(), use_container_width=True)
        st.subheader("Fan Segments (Simulated)")
        st.write("Superfans:", random.randint(20, 100))
        st.write("Active Fans:", random.randint(100, 500))
        st.write("At-Risk/Lapsed:", random.randint(10, 100))
        st.caption("⚡ In production, use real AI clustering for segmentation.")
        audit_log("Uploaded fan data", st.session_state.get("user_id", "anon"))

    # --- Smart Messaging ---
    st.text_area("Write a message to your fans (AI can auto-personalize in production):", height=80)
    st.button("Send (Simulated)")

    # --- Marketplace for 3rd-party Sellers/Fans ---
    st.subheader("Marketplace: Become a Seller")
    if is_pro():
        st.info("You're a Pro Seller! List unlimited products.")
    else:
        st.warning("Upgrade to Pro to unlock unlimited listings.")
    seller_name = st.text_input("Seller Name")
    seller_product = st.text_input("Product Name")
    seller_file = st.file_uploader("Upload Product File (jpg/pdf/mp4)", type=["jpg", "pdf", "mp4"])
    if st.button("List Product for Sale"):
        if seller_product and seller_file:
            st.success(f"{seller_product} listed in the marketplace! (Demo only)")
            audit_log("Listed product for sale", st.session_state.get("user_id", "anon"))
        else:
            st.error("Please provide a product name and upload a file to list your product.")

    # --- Optionally: Simulated Marketplace Listing Display (MVP) ---
    st.subheader("Featured Seller Listings (Demo)")
    for i in range(2):
        st.info(f"**Demo Product #{i+1}** by Seller {chr(65+i)} — ${random.randint(12,40)}")
        if st.button(f"Buy #{i+1} (Simulated)"):
            st.success("Purchase complete! (Simulated for MVP)")
            audit_log("Purchased seller product", st.session_state.get("user_id", "anon"))

