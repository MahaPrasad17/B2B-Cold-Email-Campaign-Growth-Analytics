"""
Page 1: Executive Overview
B2B Cold Email Campaign & Growth Analytics Platform
"""

import os
import sys
import streamlit as st
import plotly.express as px
import plotly.graph_objects as go
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.analytics import GrowthMarketingAnalytics

st.set_page_config(page_title="Executive Overview | GoodSpace AI", layout="wide")

st.title("📊 Executive Growth Overview")
st.caption("GoodSpace AI Outbound Cold Outreach & Conversion Telemetry (Simulated Campaign Suite)")

analytics = GrowthMarketingAnalytics()
kpis = analytics.get_overall_executive_kpis()
df_camp = analytics.get_campaign_performance_summary()
df_trends = analytics.get_daily_engagement_trends()

# Row 1: KPI Metric Cards
c1, c2, c3, c4, c5, c6, c7 = st.columns(7)

with c1:
    st.metric("Total Leads", f"{kpis['Total_Leads_Database']:,}")
with c2:
    st.metric("Emails Sent", f"{kpis['Total_Emails_Sent']:,}")
with c3:
    st.metric("Delivery Rate", f"{kpis['Delivery_Rate']}%")
with c4:
    st.metric("Open Rate", f"{kpis['Open_Rate']}%")
with c5:
    st.metric("Reply Rate", f"{kpis['Reply_Rate']}%")
with c6:
    st.metric("Bounce Rate", f"{kpis['Bounce_Rate']}%")
with c7:
    st.metric("Conversion Rate", f"{kpis['Conversion_Rate']}%", delta=f"${kpis['Total_Opportunity_Value']:,.0f} Pipe")

st.markdown("---")

# Row 2: Charts
col_left, col_right = st.columns([1.2, 1])

with col_left:
    st.subheader("Email Engagement Funnel")
    funnel_stages = [
        "Emails Sent",
        "Delivered",
        "Opened",
        "Clicked",
        "Replied",
        "Positive Reply",
        "Pipeline Opps"
    ]
    funnel_values = [
        kpis["Total_Emails_Sent"],
        kpis["Total_Emails_Delivered"],
        kpis["Total_Opens"],
        kpis["Total_Clicks"],
        kpis["Total_Replies"],
        kpis["Total_Positive_Replies"],
        kpis["Total_Conversions"]
    ]
    fig_funnel = go.Figure(go.Funnel(
        y=funnel_stages,
        x=funnel_values,
        textinfo="value+percent initial",
        marker={"color": ["#6366F1", "#3B82F6", "#0EA5E9", "#10B981", "#F59E0B", "#EC4899", "#8B5CF6"]}
    ))
    fig_funnel.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=380, template="plotly_dark")
    st.plotly_chart(fig_funnel, use_container_width=True)

with col_right:
    st.subheader("Campaign-Wise Reply Rate (%)")
    fig_bar = px.bar(
        df_camp,
        x="Reply_Rate",
        y="Campaign_Name",
        orientation="h",
        color="Reply_Rate",
        color_continuous_scale="Viridis",
        text="Reply_Rate",
        labels={"Reply_Rate": "Reply Rate (%)", "Campaign_Name": "Campaign"}
    )
    fig_bar.update_layout(margin=dict(l=20, r=20, t=20, b=20), height=380, template="plotly_dark")
    fig_bar.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    st.plotly_chart(fig_bar, use_container_width=True)

# Row 3: Daily Timeline
st.subheader("Campaign Performance Over Time")
fig_time = px.line(
    df_trends,
    x="Sent_Date",
    y=["Delivered", "Opens", "Replies", "Positive_Replies"],
    markers=True,
    labels={"value": "Daily Volume", "Sent_Date": "Send Date", "variable": "Event"},
    color_discrete_map={
        "Delivered": "#3B82F6",
        "Opens": "#10B981",
        "Replies": "#F59E0B",
        "Positive_Replies": "#EC4899"
    }
)
fig_time.update_layout(height=350, margin=dict(l=20, r=20, t=20, b=20), template="plotly_dark")
st.plotly_chart(fig_time, use_container_width=True)

# Row 4: Summary Table
st.subheader("Overall Campaign Performance Summary")
st.dataframe(
    df_camp[[
        "Campaign_ID", "Campaign_Name", "Target_Industry", "Total_Emails_Sent",
        "Total_Emails_Delivered", "Delivery_Rate", "Open_Rate", "Reply_Rate",
        "Positive_Reply_Rate", "Total_Conversions", "Total_Opportunity_Value"
    ]].style.format({
        "Delivery_Rate": "{:.2f}%",
        "Open_Rate": "{:.2f}%",
        "Reply_Rate": "{:.2f}%",
        "Positive_Reply_Rate": "{:.2f}%",
        "Total_Opportunity_Value": "${:,.2f}"
    }),
    use_container_width=True
)

