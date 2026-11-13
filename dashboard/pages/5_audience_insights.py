"""
Page 5: Audience Insights & Segmentation
B2B Cold Email Campaign & Growth Analytics Platform
"""

import os
import sys
import streamlit as st
import plotly.express as px
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.analytics import GrowthMarketingAnalytics

st.set_page_config(page_title="Audience Insights | GoodSpace AI", layout="wide")

st.title("🌐 Audience Insights & Segmentation Matrix")
st.caption("Deep-dive behavioral response analysis across B2B industries, job titles, company sizes, and acquisition channels.")

analytics = GrowthMarketingAnalytics()
df_ind = analytics.get_industry_performance()
df_src = analytics.get_lead_source_performance()

# Load full merged data for job title and size analysis
df_full = analytics.df_full

col1, col2 = st.columns(2)

with col1:
    st.subheader("Industry-Wise Response Rates")
    fig_ind = px.bar(
        df_ind,
        x="Industry",
        y=["Reply_Rate", "Positive_Reply_Rate"],
        barmode="group",
        labels={"value": "Rate (%)", "variable": "Metric"},
        color_discrete_map={"Reply_Rate": "#6366F1", "Positive_Reply_Rate": "#10B981"}
    )
    fig_ind.update_layout(height=360, template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_ind, use_container_width=True)

with col2:
    st.subheader("Lead Acquisition Source Performance")
    fig_src = px.bar(
        df_src,
        x="Lead_Source",
        y="Positive_Reply_Rate",
        color="Positive_Reply_Rate",
        color_continuous_scale="Tealgrn",
        text="Positive_Reply_Rate",
        labels={"Positive_Reply_Rate": "Positive Reply Rate (%)", "Lead_Source": "Source"}
    )
    fig_src.update_layout(height=360, template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20))
    fig_src.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    st.plotly_chart(fig_src, use_container_width=True)

st.markdown("---")

col3, col4 = st.columns(2)

with col3:
    st.subheader("Seniority Level Engagement")
    # Seniority aggregation
    seniority_grp = df_full.groupby("Seniority_Level", as_index=False).agg(
        Delivered=("Delivery_Status", "sum"),
        Opens=("Open_Status", "sum"),
        Replies=("Reply_Status", "sum"),
        Positive_Replies=("Reply_Type", lambda x: (x == "Positive").sum())
    )
    seniority_grp["Open_Rate"] = (seniority_grp["Opens"] / seniority_grp["Delivered"] * 100).round(2)
    seniority_grp["Reply_Rate"] = (seniority_grp["Replies"] / seniority_grp["Delivered"] * 100).round(2)
    
    fig_sen = px.bar(
        seniority_grp,
        x="Seniority_Level",
        y=["Open_Rate", "Reply_Rate"],
        barmode="group",
        labels={"value": "Rate (%)", "variable": "Metric"},
        color_discrete_map={"Open_Rate": "#38BDF8", "Reply_Rate": "#F59E0B"}
    )
    fig_sen.update_layout(height=340, template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_sen, use_container_width=True)

with col4:
    st.subheader("Company Size Tier Analysis")
    size_grp = df_full.groupby("Company_Size", as_index=False).agg(
        Delivered=("Delivery_Status", "sum"),
        Replies=("Reply_Status", "sum"),
        Positive=("Reply_Type", lambda x: (x == "Positive").sum())
    )
    size_grp["Reply_Rate"] = (size_grp["Replies"] / size_grp["Delivered"] * 100).round(2)

    fig_size = px.pie(
        size_grp,
        names="Company_Size",
        values="Delivered",
        hole=0.45,
        title="Outreach Volume by Company Size",
        color_discrete_sequence=px.colors.sequential.Plasma
    )
    fig_size.update_layout(height=340, template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_size, use_container_width=True)

st.markdown("---")
st.subheader("Audience Segmentation Data Table")
st.dataframe(
    df_ind[[
        "Industry", "Total_Emails_Sent", "Total_Emails_Delivered", "Open_Rate",
        "Reply_Rate", "Positive_Reply_Rate", "Total_Conversions"
    ]].style.format({
        "Open_Rate": "{:.2f}%",
        "Reply_Rate": "{:.2f}%",
        "Positive_Reply_Rate": "{:.2f}%"
    }),
    use_container_width=True
)

