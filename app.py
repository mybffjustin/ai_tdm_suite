# file: ai_tdm_suite/app.py

import streamlit as st
import os

# === Module Imports ===
from modules.audience_insights_dashboard import main as audience_insights_dashboard_main
from modules.accessible_streaming_platform import main as accessible_streaming_platform_main
from modules.tdm_ai_marketing_platform import main as tdm_ai_marketing_platform_main
from modules.creator_to_fan_crm import main as creator_to_fan_crm_main
from modules.digital_merch_nft_platform import main as digital_merch_nft_platform_main
from modules.live_experience_marketplace import main as live_experience_marketplace_main
from modules.tdm_digital_publishing_studio import main as tdm_digital_publishing_studio_main
from modules.smart_merch_print_hub import main as smart_merch_print_hub_main

from modules.utils import (
    MODULES, show_revenue_model_reference, check_session, is_pro, pricing_plans,
    subscribe, logout
)

# === SIDEBAR CONFIG ===
with st.sidebar:
    st.markdown("#### 🎼 Label & Enterprise Tools")
    label_mode = st.toggle("Label/Enterprise Mode", key="label_mode")
    if label_mode:
        label_tool = st.radio(
            "Label Dashboard",
            ["Catalog Analytics", "A&R Heatmap", "Royalty & Finance", "White-label Settings"],
            key="label_nav"
        )
    st.markdown("---")

# === PAGE CONFIG & CSS ===
st.set_page_config(
    page_title="AI TDM Suite: Theater, Dance & Music AI",
    layout="wide",
    page_icon="🎭",
    initial_sidebar_state="expanded"
)
# Load CSS
if os.path.exists(os.path.join("assets", "style.css")):
    with open(os.path.join("assets", "style.css")) as f:
        st.markdown(f"<style>{f.read()}</style>", unsafe_allow_html=True)

# === SESSION INIT ===
check_session()

# === SIDEBAR NAVIGATION ===
with st.sidebar:
    st.markdown("<h3 style='color:#fff;font-weight:700;'>AI TDM Suite</h3>", unsafe_allow_html=True)
    st.markdown("<span style='color:#ffb87c;font-weight:700;'>Smarter insights, bigger audiences.</span>", unsafe_allow_html=True)
    st.markdown("---")
    # Onboarding for first-time users
    if st.session_state.get("first_run", True):
        with st.expander("👋 Welcome to AI TDM Suite! Start here."):
            st.markdown("""
- **Upload your first CSV for analytics.**
- Or [download a sample](https://raw.githubusercontent.com/youruser/ai_tdm_suite/main/data/sample_ticket_data.csv).
- Try all 8 modules from the menu below.
""")
        st.session_state["first_run"] = False
    # Navigation
    app_mode = st.radio(
        "🔎 Choose Platform",
        MODULES,
        index=0,
        key="nav_platform"
    )
    with st.expander("📖 Revenue Model Reference (A/B grades)", expanded=False):
        show_revenue_model_reference()
    st.markdown("---")
    st.markdown("#### 🤝 Partner Offers / Affiliate")
    st.markdown("""
- 🎫 [Buy Show Tickets](#)
- 👕 [Merch Store](#)
- 📚 [Theater Courses](#)
""")
    st.markdown("##### Your Account")
    if st.session_state.get("pro_user", False):
        st.success("🌟 Pro User (Subscribed)")
        if st.button("Log Out / Switch to Free"):
            logout()
    else:
        st.info("🚀 Free Tier: Upgrade for full access.")
        if st.button("Upgrade to Pro ($29/mo)"):
            subscribe()
    st.markdown("---")
    with st.expander("🔐 Data & Privacy"):
        st.write("Your data is stored securely, processed for analytics, never resold. Delete at any time via support@tdmsuite.com.")
        st.button("Request Data Deletion", key="reqdel")
    st.markdown("💡 [Give Feedback](mailto:support@tdmsuite.com?subject=AI%20TDM%20Suite%20Feedback)")
    st.markdown("[Privacy Policy](https://yourdomain.com/privacy) | [Terms of Service](https://yourdomain.com/tos)")

# === MAIN ROUTER: Regular Modules ===
if app_mode == "Audience Insights Dashboard":
    audience_insights_dashboard_main()
elif app_mode == "Accessible Streaming Platform":
    accessible_streaming_platform_main()
elif app_mode == "TDM AI Marketing Platform":
    tdm_ai_marketing_platform_main()
elif app_mode == "Creator-to-Fan AI CRM":
    creator_to_fan_crm_main()
elif app_mode == "Digital Merch & NFT Platform":
    digital_merch_nft_platform_main()
elif app_mode == "Live Experience Marketplace":
    live_experience_marketplace_main()
elif app_mode == "TDM Digital Publishing Studio":
    tdm_digital_publishing_studio_main()
elif app_mode == "Smart Merch & Print-on-Demand Hub":
    smart_merch_print_hub_main()

# === LABEL FEATURES ROUTER ===
if st.session_state.get("label_mode"):
    if label_tool == "Catalog Analytics":
        from modules.label_catalog_analytics import main as label_catalog_analytics_main
        label_catalog_analytics_main()
    elif label_tool == "A&R Heatmap":
        from modules.label_anr_heatmap import main as label_anr_heatmap_main
        label_anr_heatmap_main()
    elif label_tool == "Royalty & Finance":
        from modules.label_royalty_finance import main as label_royalty_finance_main
        label_royalty_finance_main()
    elif label_tool == "White-label Settings":
        from modules.label_whitelabel_settings import main as label_whitelabel_settings_main
        label_whitelabel_settings_main()

# === PRICING PLANS & SIMULATION ===
st.markdown("## 🏷️ Pricing Plans & Strategy")
toggle_annual = st.toggle("Annual billing (save ~17%)", value=True)
selected_plan = st.selectbox(
    "Select a Plan to Simulate Revenue Impact:",
    options=list(pricing_plans.keys()),
    index=1  # Pro as default
)
plan = pricing_plans[selected_plan]
plan_price = (
    plan.get("price_annual", plan["price_month"]*12) / 12 if toggle_annual and "price_annual" in plan
    else plan.get("price_month", 0)
)
# Plan cards
st.markdown("<div style='display:flex;gap:24px;flex-wrap:wrap;'>", unsafe_allow_html=True)
for name, info in pricing_plans.items():
    badge_html = f"<span style='background:{info['color']};color:#fff;padding:4px 12px;border-radius:8px;font-size:0.92em;margin-right:9px;'>{info['badge']}</span>" if "badge" in info else ""
    price = (
        f"${info.get('price_annual', info.get('price_month', 0)*12)//12:.0f}/mo <span style='font-size:0.95em;'>(annual)</span>"
        if toggle_annual and "price_annual" in info else
        f"${info.get('price_month', info.get('price_per_action', 0)):.2f}/mo" if "price_month" in info else
        f"${info.get('price_per_action', 0):.2f}/action"
    )
    features = "".join(f"<li>{f}</li>" for f in info['features'])
    box_shadow = "0 0 0 2.5px #003366" if name == selected_plan else "0 1px 8px #999"
    st.markdown(f"""
    <div style='flex:1;min-width:220px;background:#fff;padding:18px 14px 15px 14px;border-radius:17px;
                box-shadow:{box_shadow};border:1.5px solid #f3f3f3;margin-bottom:10px;'>
        <div style='margin-bottom:7px;'>{badge_html}</div>
        <span style='font-size:2.1em;font-weight:700;color:{info['color']}'>{price}</span>
        <ul style='margin-top:9px;font-size:1.03em;padding-left:18px;color:#232326;'>
            {features}
        </ul>
        <span style='color:#888;font-size:0.98em;'>Marketplace Fee: <b>{int(info.get('transaction_fee',0)*100)}%</b></span>
    </div>
    """, unsafe_allow_html=True)
st.markdown("</div>", unsafe_allow_html=True)

# Scenario modeling
st.markdown("#### 💰 Revenue Impact Simulation")
colu1, colu2 = st.columns([2, 1])
with colu1:
    n_customers = st.slider("How many customers on this plan?", 10, 5000, 200, step=10)
    avg_gmv = st.number_input("Avg. Gross Marketplace Volume (per user, per month)", min_value=0, value=500)
    saas_revenue = n_customers * plan_price if selected_plan != "Pay-per-Use" else 0
    tx_fee = plan.get("transaction_fee", 0)
    marketplace_revenue = n_customers * avg_gmv * tx_fee
    ppu_revenue = n_customers * plan.get("price_per_action", 0) * 10 if selected_plan == "Pay-per-Use" else 0
    monthly_revenue = saas_revenue + marketplace_revenue + ppu_revenue
    st.metric("Simulated Monthly Revenue", f"${monthly_revenue:,.0f}")
    st.metric("Simulated Annual Revenue", f"${monthly_revenue*12:,.0f}")
with colu2:
    st.markdown("""
- **Anchoring:** Highlight best value and most popular.
- **Value Ladder:** Freemium → Pro → Enterprise.
- **Psychology:** Use .99, “2 months free,” scarcity badges.
- **Experiment:** Change pricing at any time, test revenue instantly.
- **Conversion Triggers:** Upgrade prompts and in-app nudges.
""")
    st.info("💡 Top pricing psychology built-in: anchor, ladder, urgency, choice simplification.")

if not is_pro():
    if st.button(f"🚀 Upgrade to {selected_plan} Now"):
        st.session_state['pro_user'] = True
        st.success(f"You're now on the {selected_plan} plan! Enjoy full access.")

# === FOOTER ===
st.markdown("---")
colL, colC, colR = st.columns([1,2,1])
with colC:
    st.caption("AI TDM Suite | All Revenue Models + 8 MVP Feature Apps | Powered by Mocha, Streamlit, GPT-4")
st.markdown(
    "<center><span style='color:#23244d;font-size:1.01em'>"
    "© 2024 Justin Hoang & AI TDM Suite. All rights reserved.</span></center>",
    unsafe_allow_html=True
)
