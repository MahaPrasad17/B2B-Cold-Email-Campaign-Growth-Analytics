"""
Page 6: Optimization Insights & AI Recommendation Engine
B2B Cold Email Campaign & Growth Analytics Platform
"""

import os
import sys
import streamlit as st
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))
from src.recommendation_engine import GrowthRecommendationEngine
from src.deliverability import DELIVERABILITY_FRAMEWORK

st.set_page_config(page_title="Optimization Insights | GoodSpace AI", layout="wide")

st.title("💡 Growth Optimization Engine & Audit")
st.caption("Algorithmic growth marketer recommendations, deliverability health audit, and underperforming campaign alerts.")

engine = GrowthRecommendationEngine()
recs = engine.generate_recommendations()
deliv = engine.deliverability

# Row 1: Technical Deliverability Health Scorecard
st.subheader("1. Technical Domain Health & Deliverability Audit")
d1, d2, d3, d4 = st.columns(4)

d1.metric("Domain Health Score", f"{deliv['Domain_Health_Score']}/100", deliv["Domain_Health_Status"])
d2.metric("Global Delivery Rate", f"{deliv['Delivery_Rate']}%")
d3.metric("Bounce Rate", f"{deliv['Bounce_Rate']}%", delta="-0.05%" if deliv["Bounce_Rate"] <= 2.0 else "High")
d4.metric("Unsubscribe Rate", f"{deliv['Unsubscribe_Rate']}%")

# Deliverability protocol cards
with st.expander("🛡️ Technical Email Authentication Protocols (SPF, DKIM, DMARC, Tracking)"):
    for key, item in DELIVERABILITY_FRAMEWORK.items():
        st.markdown(f"**{item['Name']}** ({item['Type']})")
        st.markdown(f"- *Purpose:* {item['Purpose']}")
        st.markdown(f"- *Example Record:* `{item['Example']}`")
        st.markdown(f"- *Risk if Missing:* {item['Risk_If_Missing']}")
        st.markdown("---")

st.markdown("---")

# Row 2: Prioritized Action Items
st.subheader("2. Prioritized Algorithmic Growth Recommendations")

df_recs = pd.DataFrame(recs)

# Priority filter
priority_filter = st.radio("Filter by Priority Level:", ["All Priorities", "HIGH", "MEDIUM", "LOW"], horizontal=True)

if priority_filter != "All Priorities":
    display_recs = df_recs[df_recs["Priority"] == priority_filter]
else:
    display_recs = df_recs

for _, r in display_recs.iterrows():
    p_color = "🔴" if r["Priority"] == "HIGH" else ("🟡" if r["Priority"] == "MEDIUM" else "🟢")
    with st.container():
        st.markdown(f"#### {p_color} [{r['Priority']}] {r['Category']}")
        st.markdown(f"**Observed Metric:** `{r['Observed_Metric']}`")
        st.markdown(f"**Diagnostic Finding:** {r['Finding']}")
        st.info(f"**Prescribed Action:** {r['Actionable_Recommendation']}")
        st.caption(f"**Expected Business Impact:** {r['Expected_Impact']}")
        st.markdown("---")

# Download Recommendations
csv_recs = df_recs.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Download Growth Recommendations Plan (CSV)",
    data=csv_recs,
    file_name="goodspace_growth_recommendations.csv",
    mime="text/csv"
)

# Row 3: Suppression List Inspector
st.subheader("3. Compliance Suppression List (Opt-Outs & Bounces)")
supp_path = "data/processed/suppression_list.csv"
if os.path.exists(supp_path):
    df_supp = pd.read_csv(supp_path)
    st.markdown(f"Currently managing **{len(df_supp)}** suppressed leads to comply with CAN-SPAM, GDPR, and protect sender reputation.")
    st.dataframe(df_supp.head(20), use_container_width=True)
    st.caption("Showing first 20 suppressed contacts.")

