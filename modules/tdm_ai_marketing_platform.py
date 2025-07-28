# file: ai_tdm_suite/modules/tdm_ai_marketing_platform.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random
from datetime import datetime

# --- Inline Revenue Model Badges (copy-paste ready for modular import later) ---
ALL_REVENUE_MODELS = [
    {"grade": "A", "category": "Licensing/Franchising", "name": "Licensing IP", "desc": "License IP or patents", "rationale": "Passive, scalable, recurring."},
    {"grade": "B", "category": "App Development", "name": "App Sales", "desc": "Build/sell apps", "rationale": "Demand, dev cost."},
    {"grade": "B", "category": "Service-Based", "name": "Consulting/Agency", "desc": "Sell expertise/time", "rationale": "High margin, time-limited."},
    {"grade": "A", "category": "Marketplaces/Aggregator", "name": "Marketplace/Aggregator", "desc": "Connect buyers/sellers", "rationale": "Network effects."},
    {"grade": "B", "category": "Content Creation", "name": "Content Creation", "desc": "Content for marketing", "rationale": "Builds authority."},
    {"grade": "B+", "category": "Integrator/Layer Player", "name": "Layer Player", "desc": "Control value chain", "rationale": "Cost savings."},
    {"grade": "B", "category": "From Push to Pull", "name": "Customer-Driven", "desc": "Custom orders", "rationale": "Reduces waste, scalable with data."}
]
MODULE_REVENUE_MODELS = {
    "TDM AI Marketing Platform": [
        "Licensing IP", "App Sales", "Consulting/Agency", "Marketplace/Aggregator",
        "Content Creation", "Layer Player", "Customer-Driven"
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

# --- Helpers ---
def audit_log(action, user="anon"):
    print(f"[AUDIT] {datetime.now()} | {user}: {action}")

def explainability_box(explanation):
    with st.expander("Why did I see this?", expanded=False):
        st.info(explanation)

def simulate_live_analytics():
    st.subheader("📊 Live Campaign Analytics (Simulated)")
    col1, col2, col3, col4 = st.columns(4)
    col1.metric("Impressions", f"{random.randint(5000, 20000):,}")
    col2.metric("Clicks", f"{random.randint(300, 3000):,}")
    col3.metric("Conversion Rate", f"{random.uniform(0.02, 0.11):.2%}")
    col4.metric("Social Shares", f"{random.randint(50, 500)}")
    progress = st.progress(0)
    for percent_complete in range(0, 100, 10):
        st.sleep(0.035)
        progress.progress(percent_complete + 10)
    st.success("Analytics updated (simulated data for MVP).")

def generate_heatmap(promo_text):
    words = promo_text.lower().split()
    word_freq = pd.Series(words).value_counts().head(10)
    fig, ax = plt.subplots(figsize=(5, 2.8))
    ax.barh(word_freq.index[::-1], word_freq.values[::-1], color='#23244d')
    ax.set_title("Top Words by Frequency", fontsize=14, color="#111")
    ax.set_xlabel("Count", fontsize=12, color="#111")
    ax.tick_params(colors="#111", labelsize=11)
    fig.tight_layout()
    return fig

def main():
    st.header("📢 TDM AI Marketing Platform (MVP Demo)")
    show_revenue_badges("TDM AI Marketing Platform")

    # --- License/Franchise Partner Block ---
    with st.expander("🎓 Become a Licensee/Franchise Partner"):
        st.write("Want to license our AI or brand/IP for your venue, agency, or product?")
        name = st.text_input("Your Name / Organization")
        email = st.text_input("Contact Email")
        biz = st.text_area("Describe your business/interest:")
        if st.button("Request Info / Start Application"):
            st.success("Thank you! We'll reach out to you within 2 business days.")
            audit_log("Requested licensing info", st.session_state.get("user_id", "anon"))

    # --- Tabs for Core Marketing Tools ---
    tab1, tab2, tab3, tab4 = st.tabs([
        "Copy Optimizer", "Copy Heatmap", "Campaign Builder", "Distribution & Analytics"
    ])
    # --- Copy Optimizer ---
    with tab1:
        st.markdown("**Neuroscience-driven Copy Optimization & A/B Generator**")
        promo_copy = st.text_area("Paste your show promo copy below:", height=120)
        if promo_copy:
            st.write("**AI-Powered Suggestions:**")
            st.markdown("- *Add an action verb at the start for urgency.*")
            st.markdown("- *Highlight exclusive/limited seats for FOMO effect.*")
            st.markdown("- *Swap passive phrases for more emotional language.*")
            st.markdown("- *Suggest audience benefit or transformation ('Feel the magic live!').*")
            st.subheader("A/B Test Variant Generator (Demo)")
            st.markdown("**A:** " + promo_copy)
            st.markdown("**B:** " + "Don't miss out – " + promo_copy.replace(".", "!") + " (Now with added urgency)")
            audit_log("Ran copy optimizer", st.session_state.get("user_id", "anon"))

    # --- Copy Heatmap ---
    with tab2:
        st.markdown("**Copy Heatmap** (Top words by frequency in your copy)")
        promo_copy_heatmap = st.text_area("Paste your promo copy here for heatmap analysis:", height=80)
        if promo_copy_heatmap:
            fig = generate_heatmap(promo_copy_heatmap)
            st.pyplot(fig)
            st.caption("Shows most repeated/emphasized words; advanced: use eye tracking or click maps.")
            audit_log("Generated copy heatmap", st.session_state.get("user_id", "anon"))

    # --- Campaign Builder ---
    with tab3:
        st.markdown("**Campaign Builder** (Draft, preview, and save campaigns)")
        with st.form("build_campaign"):
            campaign_name = st.text_input("Campaign Name")
            target_audience = st.text_input("Target Audience (e.g., '18-34, New York')")
            campaign_copy = st.text_area("Campaign Message", height=100)
            campaign_channel = st.multiselect(
                "Channels", ["Email", "Instagram", "Facebook", "X/Twitter", "YouTube", "Web Push", "SMS"]
            )
            submitted = st.form_submit_button("Save Campaign")
            if submitted:
                if campaign_name and campaign_copy and campaign_channel:
                    st.success(f"Campaign '{campaign_name}' saved! (Demo only; persistence not implemented)")
                    audit_log("Saved campaign", st.session_state.get("user_id", "anon"))
                else:
                    st.warning("Please complete all campaign fields.")

    # --- Distribution & Analytics ---
    with tab4:
        st.markdown("**Automatic Distribution & Live Analytics**")
        st.info("Simulated: In production, would use APIs (Meta, X/Twitter, Mailchimp, etc).")
        if st.button("Distribute to All Selected Channels"):
            st.success("Campaign distributed! (Simulated for MVP.)")
            simulate_live_analytics()

