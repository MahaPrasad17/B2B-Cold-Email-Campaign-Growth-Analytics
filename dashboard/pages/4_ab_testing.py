"""
Page 4: A/B Testing Engine & Statistical Lab
B2B Cold Email Campaign & Growth Analytics Platform
"""

import os
import sys
import streamlit as st
import plotly.graph_objects as go
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.ab_testing import analyze_ab_tests
from src.campaign_simulation import CAMPAIGN_COPY_CATALOG

st.set_page_config(page_title="A/B Testing Lab | GoodSpace AI", layout="wide")

st.title("🔬 A/B Testing & Statistical Lift Lab")
st.caption("Hypothesis testing engine evaluating subject lines, CTAs, personalization hooks, and email copy.")

df_ab_results = analyze_ab_tests()

# Campaign Selector
campaign_opts = list(df_ab_results["Campaign_ID"].unique())
selected_cid = st.selectbox("Select Experiment / Campaign:", campaign_opts)

exp_row = df_ab_results[df_ab_results["Campaign_ID"] == selected_cid].iloc[0]
copy_meta = CAMPAIGN_COPY_CATALOG.get(selected_cid, {})

st.subheader(f"Experiment: {exp_row['Test_ID']} - Variable: {exp_row['Test_Variable']}")
st.markdown(f"**Campaign:** {selected_cid} | **Target Audience:** {copy_meta.get('Target_Audience', 'B2B Leaders')}")

# Winning Badge Banner
winner = exp_row["Primary_Winning_Variant"]
if "Variant B" in winner:
    st.success(f"🏆 **WINNER: {winner}** | Relative Lift: **{exp_row['Reply_Lift_Pct']:+.2f}%** | p-value = **{exp_row['Reply_P_Value']:.4f}** (Statistically Significant)")
elif "Variant A" in winner:
    st.info(f"🏆 **WINNER: {winner} (Control)** | Relative Lift: **{exp_row['Reply_Lift_Pct']:+.2f}%** | p-value = **{exp_row['Reply_P_Value']:.4f}** (Statistically Significant)")
else:
    st.warning(f"⚖️ **{winner}** | p-value = **{exp_row['Reply_P_Value']:.4f}**")

st.markdown(f"> *{exp_row['Executive_Summary']}*")

st.markdown("---")

# Variant A vs Variant B Side-by-Side Comparison
colA, colB = st.columns(2)

with colA:
    st.markdown("### 🅰️ Variant A (Control)")
    st.info(f"**Description:** {exp_row['Variant_A_Description']}")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Delivered", f"{exp_row['Delivered_A']:,}")
    m2.metric("Open Rate", f"{exp_row['Open_Rate_A']}%")
    m3.metric("Reply Rate", f"{exp_row['Reply_Rate_A']}%")
    m4.metric("Conv. Rate", f"{exp_row['Conversion_Rate_A']}%")

    if copy_meta:
        step1_a = copy_meta["Sequence"]["Step_1_Variant_A"]
        with st.expander("📄 View Variant A Copy"):
            st.markdown(f"**Subject:** `{step1_a['Subject']}`")
            st.markdown(f"**CTA:** *{step1_a['CTA']}*")
            st.text_area("Body Copy:", step1_a["Body"], height=180, disabled=True)

with colB:
    st.markdown("### 🅱️ Variant B (Challenger)")
    st.info(f"**Description:** {exp_row['Variant_B_Description']}")
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Delivered", f"{exp_row['Delivered_B']:,}")
    m2.metric("Open Rate", f"{exp_row['Open_Rate_B']}%", delta=f"{exp_row['Open_Lift_Pct']:+.1f}%")
    m3.metric("Reply Rate", f"{exp_row['Reply_Rate_B']}%", delta=f"{exp_row['Reply_Lift_Pct']:+.1f}%")
    m4.metric("Conv. Rate", f"{exp_row['Conversion_Rate_B']}%", delta=f"{exp_row['Conversion_Lift_Pct']:+.1f}%")

    if copy_meta:
        step1_b = copy_meta["Sequence"]["Step_1_Variant_B"]
        with st.expander("📄 View Variant B Copy"):
            st.markdown(f"**Subject:** `{step1_b['Subject']}`")
            st.markdown(f"**CTA:** *{step1_b['CTA']}*")
            st.text_area("Body Copy:", step1_b["Body"], height=180, disabled=True)

# Comparison Bar Chart
st.markdown("---")
st.subheader("Conversion Metrics Comparison (Variant A vs Variant B)")

metrics = ["Open Rate (%)", "Reply Rate (%)", "Positive Reply Rate (%)", "Conversion Rate (%)"]
vals_a = [exp_row["Open_Rate_A"], exp_row["Reply_Rate_A"], exp_row["Positive_Rate_A"], exp_row["Conversion_Rate_A"]]
vals_b = [exp_row["Open_Rate_B"], exp_row["Reply_Rate_B"], exp_row["Positive_Rate_B"], exp_row["Conversion_Rate_B"]]

fig_ab = go.Figure(data=[
    go.Bar(name="Variant A", x=metrics, y=vals_a, marker_color="#3B82F6", text=vals_a, textposition="auto"),
    go.Bar(name="Variant B", x=metrics, y=vals_b, marker_color="#10B981", text=vals_b, textposition="auto")
])
fig_ab.update_layout(barmode="group", height=350, template="plotly_dark", margin=dict(l=20, r=20, t=20, b=20))
st.plotly_chart(fig_ab, use_container_width=True)

# Master All-Experiments Summary Table
st.markdown("---")
st.subheader("All A/B Experiments Summary Table")
st.dataframe(
    df_ab_results[[
        "Test_ID", "Campaign_ID", "Test_Variable",
        "Open_Rate_A", "Open_Rate_B", "Open_Lift_Pct", "Open_P_Value",
        "Reply_Rate_A", "Reply_Rate_B", "Reply_Lift_Pct", "Reply_P_Value",
        "Primary_Winning_Variant"
    ]].style.format({
        "Open_Rate_A": "{:.2f}%",
        "Open_Rate_B": "{:.2f}%",
        "Open_Lift_Pct": "{:+.2f}%",
        "Open_P_Value": "{:.4f}",
        "Reply_Rate_A": "{:.2f}%",
        "Reply_Rate_B": "{:.2f}%",
        "Reply_Lift_Pct": "{:+.2f}%",
        "Reply_P_Value": "{:.4f}"
    }),
    use_container_width=True
)

