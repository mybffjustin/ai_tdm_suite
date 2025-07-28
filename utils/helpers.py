# file: ai_tdm_suite/utils/helpers.py

import streamlit as st
import pandas as pd
from datetime import datetime
import random
import hashlib

def check_session():
    """Initialize session state for pro_user and user_id."""
    if "pro_user" not in st.session_state:
        st.session_state["pro_user"] = False
    if "user_id" not in st.session_state:
        st.session_state["user_id"] = f"user_{random.randint(10000,99999)}"

def is_pro():
    """Return True if current user is a Pro user."""
    return st.session_state.get("pro_user", False)

def pro_paywall(msg="Upgrade to Pro to access this feature."):
    """Show paywall if user is not Pro."""
    if not is_pro():
        st.error("🌟 " + msg)
        st.stop()

def consent_checkbox(label: str):
    """Reusable consent checkbox, returns True/False."""
    return st.checkbox(f"☑️ I consent to {label}")

def watermark_csv(df: pd.DataFrame, user_id="anon") -> pd.DataFrame:
    """Add a short unique watermark hash to each exported dataframe."""
    df = df.copy()
    df["_watermark"] = hashlib.sha256(f"{user_id}_{datetime.now()}".encode()).hexdigest()[:16]
    return df

def audit_log(action, user=None):
    """Simple stdout log for privacy/analytics events."""
    user = user or st.session_state.get("user_id", "anon")
    print(f"[AUDIT] {datetime.now()} | {user}: {action}")

def explainability_box(explanation):
    """Show an expandable explanation/info box."""
    with st.expander("Why did I see this?", expanded=False):
        st.info(explanation)

def load_data(uploaded_file):
    """Load user-uploaded CSV as DataFrame, with error handling."""
    try:
        df = pd.read_csv(uploaded_file)
        return df
    except Exception as e:
        st.error(f"Failed to load file: {e}")
        return None

def safe_parse_date(df: pd.DataFrame):
    """Parse a 'date' column in DataFrame, require at least 1 valid entry."""
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

def subscribe():
    """Upgrade session to Pro user."""
    st.session_state["pro_user"] = True

def logout():
    """Downgrade to Free user."""
    st.session_state["pro_user"] = False

# Visual badge renderer for active revenue models
def show_revenue_badges(module, get_enabled_models=None):
    """
    Render active revenue model badges for a module.
    get_enabled_models: function(module) -> list of models (should be set by importing module)
    """
    # Fallback: try to import get_enabled_models if not passed
    if get_enabled_models is None:
        try:
            from modules.utils import get_enabled_models  # circular ok for Streamlit runtime
        except Exception:
            st.warning("Revenue model lookup unavailable.")
            return
    enabled = get_enabled_models(module)
    st.markdown("**Active Revenue Models:**", unsafe_allow_html=True)
    badge_html = ""
    for m in enabled:
        badge_html += (
            f"<span class='h-badge' title='{m.get('desc','')} | {m.get('rationale','')}'>{m.get('name','')} ({m.get('grade','')})</span>"
        )
    st.markdown(badge_html, unsafe_allow_html=True)
