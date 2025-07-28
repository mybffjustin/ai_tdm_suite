# file: ai_tdm_suite/modules/label_anr_heatmap.py
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import random

def main():
    st.header("🔥 A&R Artist Heatmap (Demo)")
    st.markdown("Detect fast-rising artists or tracks from social, streaming, and ticket signals.")
    uploaded = st.file_uploader("Upload A&R Data (CSV: artist, city, streams, tiktok_views, ticket_sales, growth)", type=["csv"])
    if uploaded:
        df = pd.read_csv(uploaded)
        st.dataframe(df.head(), use_container_width=True)
        st.metric("Artists Tracked", df['artist'].nunique())
        top_growth = df.sort_values('growth', ascending=False).head(5)
        st.write("### 🚀 Top Trending Artists:")
        st.table(top_growth[['artist', 'city', 'growth']])
        # Heatmap
        st.markdown("#### Regional Growth Heatmap")
        pivot = df.pivot_table(values='growth', index='city', columns='artist', fill_value=0)
        fig, ax = plt.subplots(figsize=(8,3))
        ax.imshow(pivot, aspect='auto', cmap='YlOrRd')
        ax.set_yticks(range(len(pivot.index)))
        ax.set_yticklabels(pivot.index)
        ax.set_xticks(range(len(pivot.columns)))
        ax.set_xticklabels(pivot.columns, rotation=90)
        st.pyplot(fig)
        st.caption("Spot the next big thing, region by region.")
    else:
        st.info("Upload your A&R or talent scouting data to view this heatmap.")
