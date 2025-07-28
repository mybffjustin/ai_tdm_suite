# file: modules/b2b_network.py
import streamlit as st
import pandas as pd
from datetime import datetime

# --- In-memory "database" for MVP ---
if "user_profiles" not in st.session_state:
    st.session_state.user_profiles = []

if "messages" not in st.session_state:
    st.session_state.messages = []

# --- User Profile Creation ---
st.header("🌐 B2B Founder/Exec Network")
st.markdown("Connect with entrepreneurs, investors, and creative leaders.")

with st.expander("Create/Update Your Profile"):
    name = st.text_input("Your Name")
    company = st.text_input("Your Company or Project")
    role = st.text_input("Your Role")
    sector = st.text_input("Industry/Sector")
    needs = st.text_area("Looking for...", placeholder="e.g. investors, advisors, co-founders, tech, clients")
    offers = st.text_area("I can offer...", placeholder="e.g. funding, mentorship, marketing, dev, talent")
    linkedin = st.text_input("LinkedIn URL (optional)")
    update_profile = st.button("Save Profile")
    if update_profile and name and company:
        st.session_state.user_profiles.append({
            "name": name, "company": company, "role": role, "sector": sector,
            "needs": needs, "offers": offers, "linkedin": linkedin,
            "timestamp": datetime.now().isoformat()
        })
        st.success("Profile updated!")

# --- Browse/Search Network ---
st.subheader("🔎 Find Founders & Companies")
search = st.text_input("Search by name, company, sector, or keyword")
profiles = pd.DataFrame(st.session_state.user_profiles)
if not profiles.empty:
    filtered = profiles[
        profiles.apply(lambda row: search.lower() in str(row).lower(), axis=1) if search else slice(None)
    ]
    st.dataframe(filtered[["name", "company", "role", "sector", "needs", "offers", "linkedin"]], use_container_width=True)
else:
    st.info("No profiles found yet. Be the first to join!")

# --- Simple Messaging (MVP only; not persistent) ---
st.subheader("💬 Direct Message (MVP)")
if not profiles.empty:
    target_name = st.selectbox("Who do you want to message?", profiles["name"].unique())
    msg = st.text_area("Your message", height=60)
    if st.button("Send Message"):
        st.session_state.messages.append({
            "from": st.session_state.get("user_id", "anon"),
            "to": target_name,
            "body": msg,
            "timestamp": datetime.now().isoformat()
        })
        st.success("Message sent (demo only; not persistent)")

# --- Inbox ---
st.subheader("📥 Your Inbox (Demo)")
my_msgs = [m for m in st.session_state.messages if m["to"] == name]
for m in my_msgs:
    st.info(f"From: {m['from']} | {m['timestamp']}\n\n{m['body']}")
