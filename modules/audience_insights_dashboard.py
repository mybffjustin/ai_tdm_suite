# file: ai_tdm_suite/modules/audience_insights_dashboard.py

import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
from sklearn.linear_model import LinearRegression
from datetime import datetime
import random
import hashlib

# --- Revenue model badge logic ---
ALL_REVENUE_MODELS = [
    {"grade": "A",  "category": "Recurring Revenue", "name": "Subscription",         "desc": "Ongoing access fee (e.g., Netflix, Salesforce)", "rationale": "High predictability, 70-90% margins, infinite scalability."},
    {"grade": "A",  "category": "Data Sales",        "name": "DaaS/Data Monetization","desc": "Sell insights/aggregates",                       "rationale": "High value, 100% margins, scalable."},
    {"grade": "A-", "category": "Freemium",          "name": "Freemium",              "desc": "Free tier + paid upgrades",                      "rationale": "Low acquisition cost, high conversion potential."},
    {"grade": "B+", "category": "Transaction-Based", "name": "Commission/Fees",       "desc": "Fee per sale",                                   "rationale": "Scalable, 10-30% fees."},
    {"grade": "B",  "category": "Advertising-Based", "name": "Ads/Sponsorship",       "desc": "Earn from ads/views",                            "rationale": "Scalable with traffic, 20-50% margin."},
]
MODULE_REVENUE_MODELS = {
    "Audience Insights Dashboard": [
        "Subscription", "DaaS/Data Monetization", "Freemium", "Commission/Fees", "Ads/Sponsorship"
    ]
}

def show_revenue_badges(module):
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
def consent_checkbox(label):
    """Show a consent checkbox with custom label."""
    return st.checkbox(f"☑️ I consent to {label}")

def watermark_csv(df, user_id="anon"):
    """Add a watermark to a DataFrame export."""
    df["_watermark"] = hashlib.sha256(f"{user_id}_{datetime.now()}".encode()).hexdigest()[:16]
    return df

def audit_log(action, user="anon"):
    """Print simple audit log (swap for persistent logging in prod)."""
    print(f"[AUDIT] {datetime.now()} | {user}: {action}")

def explainability_box(explanation):
    """Show an expandable box explaining analytics."""
    with st.expander("Why did I see this?", expanded=False):
        st.info(explanation)

def is_pro():
    return st.session_state.get("pro_user", False)

def pro_paywall(msg="Upgrade to Pro to access this feature."):
    """Stop execution if not Pro."""
    if not is_pro():
        st.error("🌟 " + msg)
        st.stop()

def check_session():
    if "pro_user" not in st.session_state:
        st.session_state["pro_user"] = False
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = f"user_{random.randint(10000, 99999)}"

def load_data(uploaded_file):
    try:
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Failed to load file: {e}")
        return None

def safe_parse_date(df):
    """Ensure 'date' column is present and parsed to datetime, drop invalid rows."""
    if 'date' not in df.columns:
        st.error("Your CSV is missing a required 'date' column.")
        return None
    try:
        df['date'] = pd.to_datetime(df['date'], format='%Y-%m-%d', errors='coerce')
    except Exception:
        df['date'] = pd.to_datetime(df['date'], errors='coerce')
    df = df.dropna(subset=['date'])
    if df.empty:
        st.error("No valid date entries found in your data.")
        return None
    return df

# --- Main App ---
def main():
    check_session()
    st.header("🎯 Audience Insights for Live Arts")
    show_revenue_badges("Audience Insights Dashboard")
    uploaded_file = st.file_uploader("📤 Upload Ticket Sales Data (CSV)", type=["csv"])
    if uploaded_file:
        with st.spinner("Analyzing your data..."):
            if not consent_checkbox("use of data for analytics and model improvement."):
                st.warning("Consent required to proceed.")
                st.stop()
            df = load_data(uploaded_file)
            if df is not None:
                df = safe_parse_date(df)
                if df is not None and not df.empty:
                    audit_log("Uploaded sales data", st.session_state.get("user_id", "anon"))
                    st.success("✅ Data uploaded!")
                    st.dataframe(df.head(), use_container_width=True)
                    # --- Audience Age & Sales Analysis ---
                    c1, c2 = st.columns([1, 1])
                    with c1:
                        if 'age_group' in df.columns:
                            st.markdown("#### 👥 Audience Age Distribution")
                            age_counts = df['age_group'].value_counts()
                            st.bar_chart(age_counts)
                            explainability_box("Shows the age group breakdown from your ticket data.")
                    with c2:
                        sales_by_date = df.groupby('date', as_index=False)['tickets_sold'].sum()
                        st.markdown("#### 📅 Tickets Sold Over Time")
                        fig, ax = plt.subplots()
                        ax.plot(sales_by_date['date'], sales_by_date['tickets_sold'], marker='o', linewidth=2, color='#23244d')
                        ax.set_xlabel('Date')
                        ax.set_ylabel('Tickets Sold')
                        fig.tight_layout()
                        st.pyplot(fig)
                    # --- AI Demand Prediction ---
                    st.markdown("#### 🤖 AI-Powered Demand Prediction")
                    sales_by_date['ordinal_date'] = sales_by_date['date'].apply(lambda d: d.toordinal())
                    X = sales_by_date[['ordinal_date']]
                    y = sales_by_date['tickets_sold']
                    model = LinearRegression()
                    model.fit(X, y)
                    future_dates = [sales_by_date['date'].max() + pd.Timedelta(days=i) for i in range(1, 8)]
                    future_ordinals_df = pd.DataFrame({'ordinal_date': [d.toordinal() for d in future_dates]})
                    predicted_sales = model.predict(future_ordinals_df)
                    future_df = pd.DataFrame({
                        "date": future_dates,
                        "predicted_tickets_sold": predicted_sales.astype(int)
                    })
                    st.write("##### 🗓️ Next 7 Days: Ticket Sales Forecast")
                    st.dataframe(future_df, use_container_width=True)
                    explainability_box("AI uses past ticket sales to predict demand. For entertainment only.")
                    if not future_df.empty:
                        best_day = future_df.loc[future_df['predicted_tickets_sold'].idxmax()]['date']
                        st.success(f"📢 Best day for marketing push: <b>{best_day.strftime('%A, %b %d')}</b>", icon="📢")
                    # --- Channel, Top Show, Export ---
                    exp1, exp2 = st.columns([1.4, 1])
                    with exp1:
                        if 'channel' in df.columns:
                            st.markdown("##### 📈 Sales Channel Breakdown")
                            channel_counts = df.groupby('channel')['tickets_sold'].sum()
                            st.bar_chart(channel_counts)
                        if 'show' in df.columns:
                            st.markdown("##### 🎟️ Top Performing Shows")
                            st.write(df.groupby('show')['tickets_sold'].sum().sort_values(ascending=False).head(5))
                    with exp2:
                        st.markdown("##### ⬇️ Export Insights")
                        if is_pro():
                            exp_df = watermark_csv(df, st.session_state.get("user_id", "anon"))
                            st.download_button("Download Analytics (CSV)", exp_df.to_csv(index=False), file_name="insights_watermarked.csv")
                        else:
                            st.info("Upgrade to Pro to export analytics.")
                        st.markdown("##### 💰 Revenue Dashboard")
                        st.metric("Total Earnings", f"${random.randint(1000,3000)}")
                        st.metric("Pending Payouts", f"${random.randint(50,200)}")
    else:
        st.info("Please upload a ticket sales CSV to begin. Sample CSV shown in the sidebar.")
