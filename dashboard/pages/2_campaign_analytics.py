"""
Page 2: Campaign Analytics
B2B Cold Email Campaign & Growth Analytics Platform
"""

import os
import sys
import streamlit as st
import plotly.express as px
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.analytics import GrowthMarketingAnalytics

st.set_page_config(page_title="Campaign Analytics | GoodSpace AI", layout="wide")

st.title("🎯 Campaign Analytics & Sequence Deep Dive")
st.caption("Cross-campaign comparisons, industry performance, and multi-step sequence velocity.")

analytics = GrowthMarketingAnalytics()
df_camp = analytics.get_campaign_performance_summary()
df_ind = analytics.get_industry_performance()
df_steps = analytics.get_sequence_step_performance()
df_trends = analytics.get_daily_engagement_trends()

# Campaign Selector
campaign_names = ["All Campaigns"] + list(df_camp["Campaign_Name"].unique())
selected_camp = st.selectbox("Filter by Campaign:", campaign_names)

if selected_camp != "All Campaigns":
    df_camp_view = df_camp[df_camp["Campaign_Name"] == selected_camp]
else:
    df_camp_view = df_camp

# Top Row: Side-by-side comparison charts
col1, col2 = st.columns(2)

with col1:
    st.subheader("Industry-Wise Performance (Open & Reply Rates)")
    fig_ind = px.bar(
        df_ind,
        x="Industry",
        y=["Open_Rate", "Reply_Rate"],
        barmode="group",
        labels={"value": "Rate (%)", "variable": "Metric"},
        color_discrete_map={"Open_Rate": "#3B82F6", "Reply_Rate": "#10B981"}
    )
    fig_ind.update_layout(height=380, template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20))
    st.plotly_chart(fig_ind, use_container_width=True)

with col2:
    st.subheader("Multi-Touch Sequence Performance (Step 1 vs 2 vs 3)")
    fig_step = px.bar(
        df_steps,
        x="Sequence_Step",
        y="Reply_Rate",
        color="Positive_Reply_Rate",
        color_continuous_scale="Purples",
        text="Reply_Rate",
        labels={"Reply_Rate": "Reply Rate (%)", "Sequence_Step": "Sequence Touchpoint"}
    )
    fig_step.update_layout(height=380, template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20))
    fig_step.update_traces(texttemplate="%{text:.2f}%", textposition="outside")
    st.plotly_chart(fig_step, use_container_width=True)

# Middle Row: Reply and Bounce Daily Trends
st.subheader("Daily Engagement & Deliverability Trends")
fig_daily = px.line(
    df_trends,
    x="Sent_Date",
    y=["Opens", "Replies", "Bounces"],
    labels={"value": "Count", "Sent_Date": "Date", "variable": "Event"},
    color_discrete_map={"Opens": "#10B981", "Replies": "#6366F1", "Bounces": "#EF4444"}
)
fig_daily.update_layout(height=320, template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig_daily, use_container_width=True)

# Bottom Row: Best-Performing Campaigns Ranked
st.subheader("Best-Performing Campaigns Ranked by Reply Rate")
ranked_df = df_camp_view.sort_values("Reply_Rate", ascending=False).reset_index(drop=True)
ranked_df["Rank"] = ranked_df.index + 1

st.dataframe(
    ranked_df[[
        "Rank", "Campaign_Name", "Target_Industry", "Total_Emails_Delivered",
        "Open_Rate", "Reply_Rate", "Positive_Reply_Rate", "Total_Conversions", "Total_Opportunity_Value"
    ]].style.format({
        "Open_Rate": "{:.2f}%",
        "Reply_Rate": "{:.2f}%",
        "Positive_Reply_Rate": "{:.2f}%",
        "Total_Opportunity_Value": "${:,.2f}"
    }),
    use_container_width=True
)

