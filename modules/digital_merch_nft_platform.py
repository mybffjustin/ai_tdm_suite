# file: ai_tdm_suite/modules/digital_merch_nft_platform.py

import streamlit as st
import random
from datetime import datetime

# === Revenue Model Badges: For this module ===
ALL_REVENUE_MODELS = [
    {"grade": "A",   "category": "Marketplaces/Aggregator", "name": "Marketplace/Aggregator", "desc": "Connect buyers/sellers",        "rationale": "Network effects, high profitability."},
    {"grade": "A",   "category": "Digital Products",        "name": "Online Courses/eBooks",   "desc": "Sell digital content",         "rationale": "90%+ margins, passive, top profitability."},
    {"grade": "B-",  "category": "Ingredient Branding",     "name": "Co-Branding",             "desc": "Promote component",            "rationale": "Boost perception, partner-dependent."},
    {"grade": "B+",  "category": "Transaction-Based",       "name": "Commission/Fees",         "desc": "Fee per sale",                 "rationale": "Scalable, 10-30% fees."},
    {"grade": "A-",  "category": "Freemium",                "name": "Freemium",                "desc": "Free tier + paid upgrades",    "rationale": "Low acquisition cost, high conversion potential."},
    {"grade": "B",   "category": "Advertising-Based",       "name": "Ads/Sponsorship",         "desc": "Earn from ads/views",          "rationale": "Scalable with traffic, 20-50% margin."},
    {"grade": "B-",  "category": "Cash Machine",            "name": "Pre-Payment",             "desc": "Advance bookings",             "rationale": "Funds growth, refund risk."},
]
MODULE_REVENUE_MODELS = {
    "Digital Merch & NFT Platform": [
        "Marketplace/Aggregator", "Online Courses/eBooks", "Co-Branding",
        "Commission/Fees", "Freemium", "Ads/Sponsorship", "Pre-Payment"
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
    """Simple audit log for MVP, swap for persistent log in prod."""
    print(f"[AUDIT] {datetime.now()} | {user}: {action}")

def is_pro():
    return st.session_state.get("pro_user", False)

# --- Main MVP App ---
def main():
    """Streamlit UI for the Digital Merch & NFT Platform MVP."""
    st.header("🖼️ Digital Merch & NFT Platform for TDM (MVP Demo)")
    show_revenue_badges("Digital Merch & NFT Platform")
    st.markdown("""
**Features:**  
- Mint & list digital merchandise (posters, clips, backstage passes, NFTs)  
- Marketplace for fans to buy/support directly  
- Earnings dashboard (simulated)  
- Simple NFT minting for non-crypto users  
    """)

    # Licensee/Franchise Lead Form
    with st.expander("🎓 Become a Licensee/Franchise Partner"):
        st.write("Want to license digital merch or use our NFT platform tech?")
        name2 = st.text_input("Your Name / Organization", key="name2")
        email2 = st.text_input("Contact Email", key="email2")
        biz2 = st.text_area("Describe your business/interest:", key="biz2")
        if st.button("Request License Info", key="btn2"):
            st.success("Thank you! We'll reach out to you within 2 business days.")
            audit_log("Requested digital licensing info", st.session_state.get("user_id", "anon"))

    # NFT Minting Demo
    st.subheader("Mint a Digital Collectible (Demo)")
    item_name = st.text_input("Collectible Name")
    item_desc = st.text_area("Description", height=80)
    item_image = st.file_uploader("Upload Image (JPG/PNG)", type=["jpg", "png"])
    if st.button("Mint (Simulated)"):
        st.success(f"{item_name} minted! (Simulated NFT, not on-chain in MVP)")
        st.write(item_desc)
        if item_image:
            st.image(item_image, width=200)
        audit_log("Minted digital collectible", st.session_state.get("user_id", "anon"))

    # Demo Marketplace
    st.subheader("Marketplace (Demo)")
    st.info("In production, this connects to real blockchain/NFT APIs and payments.")
    st.write("Recent Collectibles (MVP):")
    for i in range(3):
        st.write(f"• Example Collectible #{i+1} - Sold: {random.randint(10,100)}")
    st.write("Fan purchases, royalties, and a real-time dashboard go here in a full build.")

    # Demo Revenue Dashboard
    st.subheader("Revenue Dashboard (Demo)")
    st.metric("Your Total Earnings", f"${random.randint(1000,5000)}")
    st.metric("Pending Payouts", f"${random.randint(50,400)}")

    # Tip Jar
    with st.expander("💸 Tip Jar / Support Artists"):
        st.write("Show your love with a quick tip! (Simulated payment for MVP.)")
        tip2 = st.select_slider("Tip Amount", options=[1, 2, 5, 8, 10, 20, 25, 40, 50, 80, 100], value=10, key="tip2")
        if st.button("Send Tip", key="send2"):
            st.success(f"Thank you for your ${tip2} tip! (Simulated)")
            audit_log("Sent tip via dashboard", st.session_state.get("user_id", "anon"))
