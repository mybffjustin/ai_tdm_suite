# file: ai_tdm_suite/modules/smart_merch_print_hub.py

import streamlit as st
import random
from datetime import datetime

# --- Inline Revenue Badges for this module ---
ALL_REVENUE_MODELS = [
    {"grade": "B",   "category": "Product Sales",        "name": "Physical/Digital Sales", "desc": "E-commerce",                     "rationale": "Direct revenue, inventory risk."},
    {"grade": "A-",  "category": "Freemium",             "name": "Freemium",               "desc": "Free tier + paid upgrades",      "rationale": "Low acquisition cost, high conversion potential."},
    {"grade": "B+",  "category": "Transaction-Based",    "name": "Commission/Fees",        "desc": "Fee per sale",                   "rationale": "Scalable, 10-30% fees."},
    {"grade": "B",   "category": "Customer Loyalty",     "name": "Loyalty/Rewards",        "desc": "Incentivize repeats",            "rationale": "Retention, scalable digital."},
]
MODULE_REVENUE_MODELS = {
    "Smart Merch & Print-on-Demand Hub": [
        "Physical/Digital Sales", "Freemium", "Commission/Fees", "Loyalty/Rewards"
    ]
}

def show_revenue_badges(module):
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

# --- Inline audit log for demo (robust for prod) ---
def audit_log(action, user="anon"):
    print(f"[AUDIT] {datetime.now()} | {user}: {action}")

def main():
    st.header("👕 Smart Merch & Print-on-Demand Hub (MVP Demo)")
    show_revenue_badges("Smart Merch & Print-on-Demand Hub")
    st.markdown("""
Design and launch physical merch (apparel, posters, collectibles) and hybrid/AR merch with zero inventory risk.
    """)

    # --- Merch Product Creator ---
    with st.expander("Create New Merch Product"):
        merch_title = st.text_input("Product Name", key="merch_title")
        merch_type = st.selectbox(
            "Type", ["T-Shirt", "Poster", "Sticker", "AR Collectible", "Other"], key="merch_type"
        )
        designer = st.text_input("Designer/Creator", key="merch_designer")
        merch_file = st.file_uploader(
            "Upload Artwork (jpg/png/pdf)", type=["jpg", "png", "pdf"], key="merch_file"
        )
        merch_price = st.number_input("Set Price ($)", min_value=5, value=20, key="merch_price")
        loyalty = st.checkbox("Enable loyalty/rewards on this product?", value=True, key="merch_loyalty")
        if st.button("List Product", key="merch_list"):
            if merch_title and designer and merch_file:
                st.success(f"Product '{merch_title}' by {designer} listed at ${merch_price}. (Demo only)")
                if loyalty:
                    st.info("Loyalty/Rewards enabled: Customers will earn points for this purchase.")
                audit_log("Listed merch product", st.session_state.get("user_id", "anon"))
            else:
                st.warning("Product name, designer, and artwork required to list.")

    # --- Featured Merch / Marketplace Demo ---
    st.subheader("Featured Merch (Demo)")
    for i in range(3):
        merch_type = ["T-Shirt", "Poster", "Sticker"][i % 3]
        merch_price = random.randint(19, 39)
        merch_designer = f"Designer {chr(66 + i)}"
        st.info(
            f"**Exclusive {merch_type} #{i+1}** by {merch_designer} — "
            f"Price: ${merch_price} (Demo)"
        )
        if st.button(f"Order #{i+1} (Simulated)"):
            st.success("Order placed! (Simulated for MVP)")
            audit_log("Ordered merch", st.session_state.get("user_id", "anon"))

    # --- Loyalty/Rewards Callout ---
    st.markdown("---")
    st.markdown("#### 🎁 Loyalty & Rewards Program")
    st.info("Earn points on every purchase! Unlock free merch, discounts, and exclusive AR collectibles. (Demo program for MVP.)")

    # --- Commission/Fees Callout ---
    st.markdown("#### 💸 Commissions & Marketplace Fees")
    st.caption("Marketplace sellers are charged a small commission per sale (see your plan for details).")

    st.markdown("---")
    st.caption("Print-on-demand fulfillment, AR integrations, and bulk ordering are available for enterprise partners (demo only).")
