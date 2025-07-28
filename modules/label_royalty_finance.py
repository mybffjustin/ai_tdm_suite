# file: ai_tdm_suite/modules/label_royalty_finance.py
import streamlit as st
import pandas as pd
import random

def main():
    st.header("💸 Label Royalty & Finance (Demo)")
    st.markdown("Aggregate label-wide, artist-level, and rights-holder payouts for all revenue streams. Simulated for MVP.")
    uploaded = st.file_uploader("Upload Royalty Data (CSV: artist, rightsholder, stream_revenue, merch_revenue, payout)", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        st.dataframe(df.head(), use_container_width=True)
        st.metric("Artists Paid", df['artist'].nunique())
        st.metric("Total Royalties Owed", f"${df['payout'].sum():,.2f}")
        st.bar_chart(df.groupby('artist')['payout'].sum())
        st.write("Recent Payouts:")
        st.table(df.sort_values('payout', ascending=False).head(10))
        st.download_button("Export Payout Report", df.to_csv(index=False), file_name="label_royalty_report.csv")
    else:
        st.info("Upload a royalty/payout CSV to use this dashboard.")
