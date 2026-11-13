"""
B2B Cold Email Campaign & Growth Analytics Platform
Main Streamlit Application
Simulated Company: GoodSpace AI (B2B Recruitment Tech)
"""

import os
import sys
import streamlit as st

# Configure sys.path so modules can be imported
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

st.set_page_config(
    page_title="GoodSpace AI | B2B Cold Email & Growth Analytics",
    page_icon="🚀",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom SaaS-styled CSS
st.markdown("""
<style>
    .main {
        background-color: #0E1117;
    }
    .metric-card {
        background-color: #1E232F;
        border: 1px solid #2D3748;
        border-radius: 8px;
        padding: 18px;
        box-shadow: 0 4px 6px -1px rgba(0, 0, 0, 0.1);
    }
    .metric-title {
        color: #A0AEC0;
        font-size: 0.85rem;
        font-weight: 600;
        text-transform: uppercase;
        letter-spacing: 0.05em;
    }
    .metric-value {
        color: #F7FAFC;
        font-size: 1.85rem;
        font-weight: 700;
        margin-top: 4px;
    }
    .metric-sub {
        color: #68D391;
        font-size: 0.8rem;
        font-weight: 500;
        margin-top: 4px;
    }
    .badge-sim {
        display: inline-block;
        padding: 4px 10px;
        background-color: rgba(99, 102, 241, 0.15);
        color: #818CF8;
        border: 1px solid #4F46E5;
        border-radius: 12px;
        font-size: 0.75rem;
        font-weight: 600;
    }
</style>
""", unsafe_allow_html=True)

# Sidebar
with st.sidebar:
    st.markdown("## 🚀 GoodSpace AI")
    st.markdown("<span class='badge-sim'>SIMULATED CAMPAIGN SUITE</span>", unsafe_allow_html=True)
    st.markdown("---")
    st.markdown("**Growth Marketing & Analytics Platform**")
    st.caption("Outbound B2B Outreach & A/B Experimentation Engine for AI-Powered Recruitment Technology.")
    st.markdown("---")
    st.markdown("### Navigation")
    st.markdown(
        """
        - **Page 1:** Executive Overview
        - **Page 2:** Campaign Analytics
        - **Page 3:** Lead Management
        - **Page 4:** A/B Testing Lab
        - **Page 5:** Audience Insights
        - **Page 6:** Optimization & AI Engine
        """
    )
    st.markdown("---")
    st.caption("Portfolio Project: Growth Marketer Internship (GoodSpace AI Simulation)")

# Main Landing Router
st.title("B2B Cold Email Campaign & Growth Analytics Platform")
st.markdown(
    "Welcome to the **GoodSpace AI** outbound growth intelligence console. "
    "Select a module from the left sidebar or explore the pages below."
)

col1, col2, col3 = st.columns(3)

with col1:
    st.info("### 📊 Executive Overview\nHigh-level growth KPIs, funnel drop-off analysis, timeline trajectories, and overall response metrics.")
    st.success("### 🎯 Campaign Analytics\nSide-by-side performance comparison across all 4 targeted B2B industry campaigns and 3-step sequence pacing.")

with col2:
    st.warning("### 👥 Lead Management\nCleaned database of 5,900+ verified B2B prospects with multi-attribute filtering, search, and CSV export.")
    st.info("### 🔬 A/B Testing Engine\nRigorous hypothesis testing, two-proportion z-tests, p-values, 95% confidence intervals, and statistical lift.")

with col3:
    st.success("### 🌐 Audience Insights\nSegmentation across industries, company size tiers, executive job titles, and inbound/outbound channels.")
    st.error("### 💡 Optimization Engine\nAlgorithmic growth marketer recommendations, underperforming campaign alerts, and deliverability audit.")

