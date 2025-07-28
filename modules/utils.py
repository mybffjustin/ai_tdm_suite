# file: ai_tdm_suite/modules/utils.py

import streamlit as st
import pandas as pd
import random
from collections import OrderedDict
from modules.revenue_models import ALL_REVENUE_MODELS

MODULES = [
    "Audience Insights Dashboard",
    "Accessible Streaming Platform",
    "TDM AI Marketing Platform",
    "Creator-to-Fan AI CRM",
    "Digital Merch & NFT Platform",
    "Live Experience Marketplace",
    "TDM Digital Publishing Studio",
    "Smart Merch & Print-on-Demand Hub"
]

# ---- Revenue Models Reference ----

def show_revenue_model_reference():
    """Display all revenue models in a Streamlit DataFrame."""
    df = pd.DataFrame(ALL_REVENUE_MODELS)
    st.dataframe(df[["grade", "category", "name", "desc", "rationale"]], use_container_width=True)

# ---- User Session/State ----

def check_session():
    """Ensure session state is properly initialized."""
    if "pro_user" not in st.session_state:
        st.session_state["pro_user"] = False
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = f"user_{random.randint(10000,99999)}"

def is_pro():
    """Return True if current session is Pro."""
    return st.session_state.get("pro_user", False)

def subscribe():
    """Upgrade to Pro."""
    st.session_state["pro_user"] = True

def logout():
    """Downgrade to Free."""
    st.session_state["pro_user"] = False

# ---- Revenue Model Enablement ----

# Map modules to their active revenue models
MODULE_REVENUE_MODELS = {
    "Audience Insights Dashboard": [
        "Subscription", "DaaS/Data Monetization", "BNPL/Interest", "Freemium", "Loyalty/Rewards", "Commission/Fees", "Ads/Sponsorship"
    ],
    "Accessible Streaming Platform": [
        "Freemium", "Subscription", "BNPL/Interest", "Ads/Sponsorship", "Pay-Per-Use", "Experiences", "Online Courses/eBooks", "Affiliate Marketing"
    ],
    "TDM AI Marketing Platform": [
        "Licensing IP", "App Sales", "Consulting/Agency", "Marketplace/Aggregator", "Content Creation", "Layer Player", "Customer-Driven"
    ],
    "Creator-to-Fan AI CRM": [
        "Membership Site", "Marketplace/Aggregator", "Commission/Fees", "Affiliate Marketing", "Loyalty/Rewards"
    ],
    "Digital Merch & NFT Platform": [
        "Marketplace/Aggregator", "Online Courses/eBooks", "Co-Branding", "Commission/Fees", "Freemium", "Ads/Sponsorship", "Pre-Payment"
    ],
    "Live Experience Marketplace": [
        "Marketplace/Aggregator", "Experiences", "Affiliate Marketing"
    ],
    "TDM Digital Publishing Studio": [
        "Online Courses/eBooks", "Licensing IP", "Affiliate Marketing", "Commission/Fees"
    ],
    "Smart Merch & Print-on-Demand Hub": [
        "Physical/Digital Sales", "Freemium", "Commission/Fees", "Loyalty/Rewards"
    ]
}

def get_enabled_models(module_name):
    """Return enabled revenue models (full dicts) for a given module name."""
    enabled_names = MODULE_REVENUE_MODELS.get(module_name, [])
    return [m for m in ALL_REVENUE_MODELS if m["name"] in enabled_names]

def show_revenue_badges(module_name):
    """Render active revenue model badges for a module in Streamlit."""
    enabled = get_enabled_models(module_name)
    st.markdown("**Active Revenue Models:**", unsafe_allow_html=True)
    badge_html = ""
    for m in enabled:
        badge_html += (
            f"<span class='h-badge' title='{m.get('desc', '')} | {m.get('rationale', '')}'>"
            f"{m.get('name', '')} ({m.get('grade', '')})</span>"
        )
    st.markdown(badge_html, unsafe_allow_html=True)

# ---- Pricing Plans ----

pricing_plans = OrderedDict([
    ("Freemium", {
        "price_month": 0,
        "features": [
            "Basic analytics dashboard",
            "Access 1 module",
            "Community support"
        ],
        "badge": "Free Forever",
        "color": "#ececec",
        "transaction_fee": 0.15,
    }),
    ("Pro", {
        "price_month": 29,
        "price_annual": 290,  # 2 months free
        "features": [
            "All 8 modules unlocked",
            "Export/Download analytics",
            "Advanced AI features",
            "Marketplace selling enabled",
            "Email/chat support"
        ],
        "badge": "Most Popular",
        "color": "#A51C30",
        "transaction_fee": 0.08,
    }),
    ("Enterprise", {
        "price_month": 199,
        "price_annual": 1900,  # 2 months free
        "features": [
            "White-label platform",
            "Custom AI model tuning",
            "API access/integrations",
            "Bulk/team seats (10+)",
            "SLA support"
        ],
        "badge": "Best Value",
        "color": "#003366",
        "transaction_fee": 0.05,
    }),
    ("Pay-per-Use", {
        "price_per_action": 1.99,
        "features": [
            "No subscription required",
            "Pay only for usage (API call, export, etc.)"
        ],
        "badge": "Flexible",
        "color": "#2a826d",
        "transaction_fee": 0.12,
    }),
])

# -- END OF FILE --
