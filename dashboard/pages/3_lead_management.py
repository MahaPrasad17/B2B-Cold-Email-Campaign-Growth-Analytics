"""
Page 3: Lead Management
B2B Cold Email Campaign & Growth Analytics Platform
"""

import os
import sys
import streamlit as st
import pandas as pd

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "../..")))

st.set_page_config(page_title="Lead Management | GoodSpace AI", layout="wide")

st.title("👥 B2B Lead Management & Intelligence")
st.caption("Search, filter, and inspect verified B2B prospect profiles with behavioral engagement data.")

# Load segmented leads
data_path = "data/processed/segmented_leads.csv"
if not os.path.exists(data_path):
    st.error("Segmented leads dataset not found. Please run the data pipeline.")
    st.stop()

df = pd.read_csv(data_path)

# Top Bar Filters
col_search, col_ind, col_size, col_seg = st.columns([1.5, 1, 1, 1])

with col_search:
    search_query = st.text_input("🔍 Search Leads (Name, Company, Email, Title):", "")

with col_ind:
    industries = ["All Industries"] + sorted(list(df["Company_Industry"].dropna().unique()))
    selected_ind = st.selectbox("Industry:", industries)

with col_size:
    sizes = ["All Sizes"] + sorted(list(df["Company_Size"].dropna().unique()))
    selected_size = st.selectbox("Company Size:", sizes)

with col_seg:
    segments = ["All Segments"] + sorted(list(df["Engagement_Segment"].dropna().unique()))
    selected_seg = st.selectbox("Engagement Tier:", segments)

# Filter Logic
filtered_df = df.copy()

if search_query:
    q = search_query.lower()
    filtered_df = filtered_df[
        filtered_df["Full_Name"].str.lower().str.contains(q, na=False) |
        filtered_df["Company_Name"].str.lower().str.contains(q, na=False) |
        filtered_df["Business_Email"].str.lower().str.contains(q, na=False) |
        filtered_df["Job_Title"].str.lower().str.contains(q, na=False)
    ]

if selected_ind != "All Industries":
    filtered_df = filtered_df[filtered_df["Company_Industry"] == selected_ind]

if selected_size != "All Sizes":
    filtered_df = filtered_df[filtered_df["Company_Size"] == selected_size]

if selected_seg != "All Segments":
    filtered_df = filtered_df[filtered_df["Engagement_Segment"] == selected_seg]

# Metrics banner
m1, m2, m3, m4 = st.columns(4)
m1.metric("Matching Leads", f"{len(filtered_df):,}")
m2.metric("Positive Repliers", f"{(filtered_df['Positive_Replies'] > 0).sum():,}")
m3.metric("Qualified Deals", f"{(filtered_df['Conversion_Count'] > 0).sum():,}")
m4.metric("Pipeline Value", f"${filtered_df['Total_Opportunity_Value'].sum():,.2f}")

st.markdown("---")

# Leads Table View
display_cols = [
    "Lead_ID", "Full_Name", "Company_Name", "Company_Industry", "Company_Size",
    "Job_Title", "Seniority_Level", "Business_Email", "Country",
    "Engagement_Segment", "Marketing_Lead_Score", "Total_Opportunity_Value"
]
st.dataframe(
    filtered_df[display_cols].head(100).style.format({
        "Total_Opportunity_Value": "${:,.2f}",
        "Marketing_Lead_Score": "{:d}"
    }),
    use_container_width=True
)

st.caption(f"Showing top 100 of {len(filtered_df):,} matching leads.")

# CSV Download
csv_data = filtered_df.to_csv(index=False).encode("utf-8")
st.download_button(
    label="📥 Export Filtered Leads to CSV",
    data=csv_data,
    file_name="goodspace_filtered_leads.csv",
    mime="text/csv"
)

# Lead Inspector Expander
st.markdown("---")
st.subheader("🔍 Individual Lead Profile Inspector")
lead_ids = list(filtered_df["Lead_ID"].head(50))

if lead_ids:
    selected_lead_id = st.selectbox("Select a Lead ID to Inspect:", lead_ids)
    lead_row = filtered_df[filtered_df["Lead_ID"] == selected_lead_id].iloc[0]

    p1, p2, p3 = st.columns(3)
    with p1:
        st.markdown(f"**Name:** {lead_row['Full_Name']}")
        st.markdown(f"**Email:** `{lead_row['Business_Email']}`")
        st.markdown(f"**Job Title:** {lead_row['Job_Title']} ({lead_row['Seniority_Level']})")
        st.markdown(f"**Location:** {lead_row['City']}, {lead_row['Country']}")

    with p2:
        st.markdown(f"**Company:** {lead_row['Company_Name']}")
        st.markdown(f"**Industry:** {lead_row['Company_Industry']}")
        st.markdown(f"**Company Size:** {lead_row['Company_Size']} ({lead_row['Company_Size_Tier']})")
        st.markdown(f"**Est. Revenue:** ${lead_row.get('Estimated_Revenue_M', 0)}M")
        st.markdown(f"**ATS / HRIS:** {lead_row.get('Current_ATS_HRIS', 'Unknown')}")

    with p3:
        st.markdown(f"**Engagement Tier:** `{lead_row['Engagement_Segment']}`")
        st.markdown(f"**Marketing Lead Score:** `{lead_row['Marketing_Lead_Score']}/100`")
        st.markdown(f"**Emails Delivered:** {lead_row['Total_Emails_Delivered']} | **Opens:** {lead_row['Total_Opens']}")
        st.markdown(f"**Replies:** {lead_row['Total_Replies']} (Positive: {lead_row['Positive_Replies']})")
        st.markdown(f"**Pipeline Deal Value:** ${lead_row['Total_Opportunity_Value']:,.2f} ({lead_row['Latest_Conversion_Status']})")

