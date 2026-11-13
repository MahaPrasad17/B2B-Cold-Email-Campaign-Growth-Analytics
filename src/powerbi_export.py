"""
B2B Cold Email Campaign & Growth Analytics Platform
Module: src/powerbi_export.py

Generates production-grade, star-schema ready CSV exports for Microsoft Power BI.
Exports Fact and Dimension tables along with pre-calculated KPI summaries.
"""

import os
import pandas as pd


def generate_powerbi_exports():
    """Extract, format, and save Power BI tables into data/exports/."""
    export_dir = "data/exports"
    os.makedirs(export_dir, exist_ok=True)
    print(f"[Power BI Export] Preparing star-schema datasets for Power BI in {export_dir}/...")

    # 1. Dim_Leads
    df_leads = pd.read_csv("data/processed/clean_leads.csv")
    leads_export_cols = [
        "Lead_ID", "Full_Name", "First_Name", "Last_Name", "Company_Name",
        "Company_Industry", "Company_Size", "Company_Size_Tier", "Job_Title",
        "Seniority_Level", "Business_Email", "Country", "City", "Sales_Region",
        "Lead_Source", "Lead_Created_Date", "Campaign_ID",
        "Estimated_Revenue_M", "Hiring_Intent_Score", "Deliverability_Score"
    ]
    df_leads_export = df_leads[[c for c in leads_export_cols if c in df_leads.columns]]
    df_leads_export.to_csv(f"{export_dir}/PowerBI_Leads.csv", index=False)
    print(f"  * Exported Dim_Leads: {len(df_leads_export):,} rows -> PowerBI_Leads.csv")

    # 2. Dim_Campaigns
    df_campaigns = pd.read_csv("data/raw/campaigns.csv")
    df_campaigns.to_csv(f"{export_dir}/PowerBI_Campaigns.csv", index=False)
    print(f"  * Exported Dim_Campaigns: {len(df_campaigns):,} rows -> PowerBI_Campaigns.csv")

    # 3. Fact_Email_Activities
    df_activities = pd.read_csv("data/raw/email_activities.csv")
    df_activities.to_csv(f"{export_dir}/PowerBI_Email_Activities.csv", index=False)
    print(f"  * Exported Fact_Email_Activities: {len(df_activities):,} rows -> PowerBI_Email_Activities.csv")

    # 4. Fact_AB_Testing
    df_ab = pd.read_csv("data/raw/ab_testing.csv")
    df_ab.to_csv(f"{export_dir}/PowerBI_AB_Testing.csv", index=False)
    print(f"  * Exported Fact_AB_Testing: {len(df_ab):,} rows -> PowerBI_AB_Testing.csv")

    # 5. Fact_Conversions
    df_conv = pd.read_csv("data/raw/conversions.csv")
    df_conv.to_csv(f"{export_dir}/PowerBI_Conversions.csv", index=False)
    print(f"  * Exported Fact_Conversions: {len(df_conv):,} rows -> PowerBI_Conversions.csv")

    # 6. Summary_Campaign_KPIs
    df_summary = pd.read_csv("data/processed/campaign_kpi_summary.csv")
    df_summary.to_csv(f"{export_dir}/PowerBI_Campaign_KPI_Summary.csv", index=False)
    print(f"  * Exported Summary_Campaign_KPIs: {len(df_summary):,} rows -> PowerBI_Campaign_KPI_Summary.csv")

    print("[Power BI Export] All 6 CSV exports generated successfully!\n")


if __name__ == "__main__":
    generate_powerbi_exports()

