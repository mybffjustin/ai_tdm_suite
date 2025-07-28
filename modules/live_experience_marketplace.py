# file: ai_tdm_suite/modules/live_experience_marketplace.py

import streamlit as st
import random
from datetime import datetime

# === Revenue Model Badges: for this module only ===
ALL_REVENUE_MODELS = [
    {"grade": "A",   "category": "Marketplaces/Aggregator", "name": "Marketplace/Aggregator", "desc": "Connect buyers/sellers", "rationale": "Network effects, high profitability."},
    {"grade": "B+",  "category": "Experience Selling",      "name": "Experiences",            "desc": "Premium events/experiences", "rationale": "Loyalty, high delivery cost."},
    {"grade": "A-",  "category": "Affiliate Marketing",     "name": "Affiliate Marketing",    "desc": "Promote for commission", "rationale": "Zero inventory, 20-50% commission, passive."},
]
MODULE_REVENUE_MODELS = {
    "Live Experience Marketplace": [
        "Marketplace/Aggregator", "Experiences", "Affiliate Marketing"
    ]
}

def show_revenue_badges(module):
    """Show badges for all enabled revenue models in this module."""
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

# --- Helpers ---
def audit_log(action, user="anon"):
    """Print an audit log line (for MVP demonstration; replace with database in prod)."""
    print(f"[AUDIT] {datetime.now()} | {user}: {action}")

# --- Main MVP App ---
def main():
    """Streamlit UI for the Live Experience Marketplace MVP."""
    st.header("🎤 Live Experience Marketplace (MVP Demo)")
    show_revenue_badges("Live Experience Marketplace")
    st.markdown("""
Sell unique, premium, or interactive experiences for fans: backstage passes, meet-and-greets, or virtual artist Q&A.
    """)

    with st.expander("List a New Experience"):
        title = st.text_input("Experience Title", key="xp_title")
        xp_type = st.selectbox("Type", ["Backstage", "Meet & Greet", "Masterclass", "Virtual Q&A", "Other"], key="xp_type")
        price = st.number_input("Price ($)", min_value=5, value=30, key="xp_price")
        slots = st.number_input("Available Slots", min_value=1, value=10, key="xp_slots")
        if st.button("List Experience", key="xp_list"):
            st.success(f"Listed '{title}' with {slots} slots at ${price}. (Demo only)")
            audit_log("Listed live experience", st.session_state.get("user_id", "anon"))

    st.subheader("Browse/Book Experiences (Demo)")
    for i in range(3):
        st.info(f"**Backstage Pass with Star #{i+1}** — Type: Live, Price: ${random.randint(20, 100)} (Demo)")
        if st.button(f"Book #{i+1} (Simulated)"):
            st.success("Booking confirmed! (Simulated for MVP)")
            audit_log("Booked experience", st.session_state.get("user_id", "anon"))
