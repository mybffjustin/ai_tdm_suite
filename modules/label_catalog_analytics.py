# file: ai_tdm_suite/modules/label_catalog_analytics.py
import streamlit as st
import pandas as pd
import random

def main():
    st.header("📊 Label Catalog Analytics (Demo)")
    st.markdown("Upload multiple artist data CSVs for a combined catalog view. (Artist, Album, Track, Streams, Tickets, Merch, Region...)")
    uploaded_files = st.file_uploader("Upload Catalog Data (multiple CSVs)", type=["csv"], accept_multiple_files=True)
    if uploaded_files:
        dfs = [pd.read_csv(f) for f in uploaded_files]
        catalog = pd.concat(dfs, ignore_index=True)
        st.dataframe(catalog.head(20), use_container_width=True)
        st.metric("Unique Artists", catalog['artist'].nunique())
        st.metric("Total Streams", f"{catalog['streams'].sum():,}")
        st.metric("Total Tickets Sold", f"{catalog['tickets_sold'].sum():,}")
        st.metric("Total Merch Revenue", f"${catalog['merch_revenue'].sum():,.2f}")
        st.bar_chart(catalog.groupby('artist')['streams'].sum().sort_values(ascending=False).head(10))
        st.caption("View performance by artist, genre, geography. Export catalog-wide insights for exec meetings.")
        st.download_button("Export Full Analytics (CSV)", catalog.to_csv(index=False), file_name="label_catalog_analytics.csv")
    else:
        st.info("Upload at least one artist or catalog data CSV to start.")
