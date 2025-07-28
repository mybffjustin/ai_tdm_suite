# file: ai_tdm_suite/modules/revenue_models.py

import streamlit as st
import pandas as pd

# === FULL CATALOG OF REVENUE MODELS (Reference/Source-of-Truth) ===
ALL_REVENUE_MODELS = [
    {"grade": "A",   "category": "Recurring Revenue",        "name": "Subscription",           "desc": "Ongoing access fee (e.g., Netflix, Salesforce)", "rationale": "High predictability, 70-90% margins, infinite scalability."},
    {"grade": "A",   "category": "Recurring Revenue",        "name": "Membership Site",        "desc": "Community, perks (e.g., Patreon, h Club)", "rationale": "Predictable, scalable, high LTV."},
    {"grade": "A",   "category": "Licensing/Franchising",    "name": "Licensing IP",           "desc": "License IP or patents (e.g., IBM)", "rationale": "Passive, scalable, recurring, low risk."},
    {"grade": "A",   "category": "Licensing/Franchising",    "name": "Franchising",            "desc": "Expand via brand license (e.g., McDonald's, Subway)", "rationale": "Leverage others’ capital, scalable."},
    {"grade": "A",   "category": "Data Sales",               "name": "DaaS/Data Monetization", "desc": "Sell insights/aggregates (e.g., G2, CB Insights)", "rationale": "High value, 100% margins, scalable, privacy risk."},
    {"grade": "A",   "category": "Digital Products",         "name": "Online Courses/eBooks",  "desc": "Sell digital content (e.g., Udemy)", "rationale": "90%+ margins, passive, top profitability."},
    {"grade": "A",   "category": "Marketplaces/Aggregator",  "name": "Marketplace/Aggregator", "desc": "Connect buyers/sellers (e.g., Amazon, Yelp)", "rationale": "Network effects, high profitability."},
    {"grade": "A",   "category": "Fintech",                  "name": "Financial Tools",        "desc": "Fees/interest (e.g., Robinhood)", "rationale": "Recurring, digital, high returns, regulatory risk."},
    {"grade": "A-",  "category": "Freemium",                 "name": "Freemium",               "desc": "Free tier + paid upgrades (e.g., Spotify)", "rationale": "Low acquisition cost, high conversion potential."},
    {"grade": "A-",  "category": "Affiliate Marketing",      "name": "Affiliate Marketing",    "desc": "Promote for commission (e.g., Amazon Assoc)", "rationale": "Zero inventory, 20-50% commission, passive."},
    {"grade": "B+",  "category": "Transaction-Based",        "name": "Commission/Fees",        "desc": "Fee per sale (e.g., eBay, Stripe)", "rationale": "Scalable, 10-30% fees."},
    {"grade": "B+",  "category": "Usage-Based",              "name": "Pay-Per-Use",            "desc": "Charge by consumption (e.g., AWS, car rentals)", "rationale": "Aligns value, 40-70% margin."},
    {"grade": "B+",  "category": "Circular Economy",         "name": "Reuse/Recycle",          "desc": "Resell/repair (e.g., Patagonia, Vinted)", "rationale": "Sustainable, moderate margin."},
    {"grade": "B+",  "category": "Integrator/Layer Player",  "name": "Layer Player",           "desc": "Control value chain (e.g., Apple HW/SW)", "rationale": "Cost savings, complex ops."},
    {"grade": "B+",  "category": "Guaranteed Availability",  "name": "Zero-Downtime",          "desc": "Premium reliability (e.g., backup services)", "rationale": "Builds trust, recurring."},
    {"grade": "B",   "category": "Advertising-Based",        "name": "Ads/Sponsorship",        "desc": "Earn from ads/views (e.g., Google, LinkedIn)", "rationale": "Scalable with traffic, 20-50% margin."},
    {"grade": "B",   "category": "Product Sales",            "name": "Physical/Digital Sales", "desc": "E-commerce (e.g., Shopify, DTC)", "rationale": "Direct revenue, inventory risk."},
    {"grade": "B",   "category": "Service-Based",            "name": "Consulting/Agency",      "desc": "Sell expertise/time (e.g., Upwork, McKinsey)", "rationale": "High margin, time-limited."},
    {"grade": "B",   "category": "Buy Now Pay Later",        "name": "BNPL/Interest",          "desc": "Financing/installments (e.g., Klarna, Affirm)", "rationale": "20-40% returns, default risk."},
    {"grade": "B",   "category": "Content Creation",         "name": "Blogging/YouTube",       "desc": "Monetize via ads/affiliates (e.g., MrBeast)", "rationale": "Viral, slow start, 30-60% margin."},
    {"grade": "B",   "category": "App Development",          "name": "App Sales",              "desc": "Build/sell apps", "rationale": "Demand, dev cost."},
    {"grade": "B",   "category": "Local Services",           "name": "Per-Job Services",       "desc": "Task-based (e.g., TaskRabbit)", "rationale": "Steady, location-limited."},
    {"grade": "B",   "category": "Flat Rate",                "name": "Membership/Flat Rate",   "desc": "Fixed fee (e.g., gym, SaaS)", "rationale": "Predictable, overuse risk."},
    {"grade": "B",   "category": "Experience Selling",       "name": "Experiences",            "desc": "Premium events/experiences (e.g., Disney)", "rationale": "Loyalty, high delivery cost."},
    {"grade": "B",   "category": "From Push to Pull",        "name": "Customer-Driven",        "desc": "Custom orders (e.g., Dell PCs)", "rationale": "Reduces waste, scalable with data."},
    {"grade": "B",   "category": "Customer Loyalty",         "name": "Loyalty/Rewards",        "desc": "Incentivize repeats (e.g., Starbucks app)", "rationale": "Retention, scalable digital."},
    {"grade": "B-",  "category": "Cost Leadership",          "name": "Low-Price Volume",       "desc": "High volume, low margin (e.g., Walmart)", "rationale": "Profitable at scale, razor margins."},
    {"grade": "B-",  "category": "Ingredient Branding",      "name": "Co-Branding",            "desc": "Promote component (e.g., Intel Inside)", "rationale": "Boost perception, partner-dependent."},
    {"grade": "B-",  "category": "Cash Machine",             "name": "Pre-Payment",            "desc": "Advance bookings", "rationale": "Funds growth, refund risk."},
]

# === MODULE TO REVENUE MODELS MAP ===
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
    """
    Return the list of revenue model dicts for a given module.
    """
    names = MODULE_REVENUE_MODELS.get(module_name, [])
    return [m for m in ALL_REVENUE_MODELS if m["name"] in names]

def show_revenue_model_reference():
    """
    Display a full reference table of all available revenue models.
    """
    df = pd.DataFrame(ALL_REVENUE_MODELS)
    st.dataframe(df[["grade", "category", "name", "desc", "rationale"]], use_container_width=True)

def show_revenue_badges(module_name):
    """
    Show visually distinctive badges for all enabled revenue models in the current module.
    """
    enabled = get_enabled_models(module_name)
    if not enabled:
        st.info("No revenue models configured for this module.")
        return
    st.markdown("**Active Revenue Models:**", unsafe_allow_html=True)
    badge_html = ""
    for m in enabled:
        badge_html += (
            f"<span class='h-badge' title='{m['desc']} | {m['rationale']}'>"
            f"{m['name']} ({m['grade']})</span> "
        )
    st.markdown(badge_html, unsafe_allow_html=True)
