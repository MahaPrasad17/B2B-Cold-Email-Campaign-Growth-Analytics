"""
B2B Cold Email Campaign & Growth Analytics Platform
Module: src/analytics.py

Enterprise Marketing Analytics Engine.
Calculates core growth KPIs with strictly documented mathematical formulas
and explicit denominators across campaigns, industries, lead sources, and sequence steps.
"""

from typing import Dict, Any
import pandas as pd


# Explicit KPI Definition Registry with Formula & Denominator documentation
KPI_DEFINITIONS = {
    "Delivery_Rate": {
        "Formula": "(Emails_Delivered / Emails_Sent) * 100",
        "Numerator": "Count of successfully delivered emails (Bounce_Status = 0)",
        "Denominator": "Total emails dispatched by email service provider (Emails_Sent)",
        "Benchmark": ">= 97.0%",
        "Unit": "%"
    },
    "Bounce_Rate": {
        "Formula": "(Bounced_Emails / Emails_Sent) * 100",
        "Numerator": "Count of emails rejected by recipient mail server (Bounce_Status = 1)",
        "Denominator": "Total emails dispatched (Emails_Sent)",
        "Benchmark": "<= 2.0%",
        "Unit": "%"
    },
    "Open_Rate": {
        "Formula": "(Unique_Opens / Delivered_Emails) * 100",
        "Numerator": "Count of delivered emails opened by recipient (Open_Status = 1)",
        "Denominator": "Delivered emails (Delivery_Status = 1)",
        "Benchmark": ">= 30.0%",
        "Unit": "%"
    },
    "Click_Rate": {
        "Formula": "(Unique_Clicks / Delivered_Emails) * 100",
        "Numerator": "Count of delivered emails with link clicks (Click_Status = 1)",
        "Denominator": "Delivered emails (Delivery_Status = 1)",
        "Benchmark": ">= 3.0%",
        "Unit": "%"
    },
    "Reply_Rate": {
        "Formula": "(Unique_Replies / Delivered_Emails) * 100",
        "Numerator": "Count of delivered emails receiving any reply (Reply_Status = 1)",
        "Denominator": "Delivered emails (Delivery_Status = 1)",
        "Benchmark": ">= 3.5%",
        "Unit": "%"
    },
    "Positive_Reply_Rate": {
        "Formula": "(Positive_Replies / Delivered_Emails) * 100",
        "Numerator": "Count of replies classified as interested / positive intent",
        "Denominator": "Delivered emails (Delivery_Status = 1)",
        "Benchmark": ">= 1.5%",
        "Unit": "%"
    },
    "Unsubscribe_Rate": {
        "Formula": "(Unsubscribes / Delivered_Emails) * 100",
        "Numerator": "Count of delivered emails where recipient opted out (Unsubscribe_Status = 1)",
        "Denominator": "Delivered emails (Delivery_Status = 1)",
        "Benchmark": "<= 0.5%",
        "Unit": "%"
    },
    "Conversion_Rate": {
        "Formula": "(Conversions / Delivered_Emails) * 100",
        "Numerator": "Count of qualified opportunities / deals generated",
        "Denominator": "Delivered emails (Delivery_Status = 1)",
        "Benchmark": ">= 0.8%",
        "Unit": "%"
    }
}


def calculate_kpis_from_subset(df_sub: pd.DataFrame, df_conv: pd.DataFrame = None) -> Dict[str, Any]:
    """
    Computes all standard marketing KPIs dynamically from a slice of email activities.
    """
    sent = len(df_sub)
    if sent == 0:
        return {k: 0.0 for k in KPI_DEFINITIONS} | {"Total_Sent": 0, "Total_Delivered": 0}

    delivered = int(df_sub["Delivery_Status"].sum())
    bounces = int(df_sub["Bounce_Status"].sum())
    opens = int(df_sub["Open_Status"].sum())
    clicks = int(df_sub["Click_Status"].sum())
    replies = int(df_sub["Reply_Status"].sum())
    positive_replies = int((df_sub["Reply_Type"] == "Positive").sum())
    neutral_replies = int((df_sub["Reply_Type"] == "Neutral").sum())
    negative_replies = int((df_sub["Reply_Type"] == "Negative").sum())
    unsubscribes = int(df_sub["Unsubscribe_Status"].sum())

    # Count conversions matching lead IDs in this activity slice
    lead_ids = set(df_sub["Lead_ID"].unique())
    if df_conv is not None and len(df_conv) > 0 and len(lead_ids) > 0:
        conv_slice = df_conv[df_conv["Lead_ID"].isin(lead_ids)]
        conversions = len(conv_slice)
        opportunity_value = float(conv_slice["Opportunity_Value"].sum())
    else:
        conversions = 0
        opportunity_value = 0.0

    # Rates calculations with exact denominators
    delivery_rate = round((delivered / sent * 100), 2) if sent > 0 else 0.0
    bounce_rate = round((bounces / sent * 100), 2) if sent > 0 else 0.0
    open_rate = round((opens / delivered * 100), 2) if delivered > 0 else 0.0
    click_rate = round((clicks / delivered * 100), 2) if delivered > 0 else 0.0
    reply_rate = round((replies / delivered * 100), 2) if delivered > 0 else 0.0
    positive_reply_rate = round((positive_replies / delivered * 100), 2) if delivered > 0 else 0.0
    unsubscribe_rate = round((unsubscribes / delivered * 100), 2) if delivered > 0 else 0.0
    conversion_rate = round((conversions / delivered * 100), 2) if delivered > 0 else 0.0

    return {
        "Total_Leads_Contacted": len(lead_ids),
        "Total_Emails_Sent": sent,
        "Total_Emails_Delivered": delivered,
        "Total_Bounces": bounces,
        "Total_Opens": opens,
        "Total_Clicks": clicks,
        "Total_Replies": replies,
        "Total_Positive_Replies": positive_replies,
        "Total_Neutral_Replies": neutral_replies,
        "Total_Negative_Replies": negative_replies,
        "Total_Unsubscribes": unsubscribes,
        "Total_Conversions": conversions,
        "Total_Opportunity_Value": opportunity_value,
        "Delivery_Rate": delivery_rate,
        "Bounce_Rate": bounce_rate,
        "Open_Rate": open_rate,
        "Click_Rate": click_rate,
        "Reply_Rate": reply_rate,
        "Positive_Reply_Rate": positive_reply_rate,
        "Unsubscribe_Rate": unsubscribe_rate,
        "Conversion_Rate": conversion_rate
    }


class GrowthMarketingAnalytics:
    """Consolidated Marketing Analytics Suite."""

    def __init__(
        self,
        leads_path: str = "data/processed/clean_leads.csv",
        activities_path: str = "data/raw/email_activities.csv",
        campaigns_path: str = "data/raw/campaigns.csv",
        conversions_path: str = "data/raw/conversions.csv"
    ):
        self.df_leads = pd.read_csv(leads_path)
        self.df_activities = pd.read_csv(activities_path)
        self.df_campaigns = pd.read_csv(campaigns_path)
        self.df_conversions = pd.read_csv(conversions_path)

        # Merge lead attributes onto activities for multi-dimensional aggregation
        self.df_full = pd.merge(
            self.df_activities,
            self.df_leads[["Lead_ID", "Company_Industry", "Company_Size", "Job_Title", "Country", "Lead_Source"]],
            on="Lead_ID",
            how="left"
        )

    def get_overall_executive_kpis(self) -> Dict[str, Any]:
        """Calculates global macro KPIs across all campaigns."""
        kpis = calculate_kpis_from_subset(self.df_activities, self.df_conversions)
        kpis["Total_Leads_Database"] = len(self.df_leads)
        return kpis

    def get_campaign_performance_summary(self) -> pd.DataFrame:
        """Campaign-level KPI aggregation."""
        records = []
        for cid, group in self.df_activities.groupby("Campaign_ID"):
            c_meta = self.df_campaigns[self.df_campaigns["Campaign_ID"] == cid]
            c_name = c_meta["Campaign_Name"].values[0] if len(c_meta) > 0 else cid
            t_ind = c_meta["Target_Industry"].values[0] if len(c_meta) > 0 else "All"
            
            # conversions for this campaign
            c_conv = self.df_conversions[self.df_conversions["Campaign_ID"] == cid]
            kpis = calculate_kpis_from_subset(group, c_conv)
            
            records.append({
                "Campaign_ID": cid,
                "Campaign_Name": c_name,
                "Target_Industry": t_ind,
                **kpis
            })
        
        df_summary = pd.DataFrame(records)
        df_summary.to_csv("data/processed/campaign_kpi_summary.csv", index=False)
        return df_summary

    def get_industry_performance(self) -> pd.DataFrame:
        """Industry-level KPI breakdown."""
        records = []
        for industry, group in self.df_full.groupby("Company_Industry"):
            kpis = calculate_kpis_from_subset(group, self.df_conversions)
            records.append({
                "Industry": industry,
                **kpis
            })
        df_ind = pd.DataFrame(records).sort_values("Reply_Rate", ascending=False)
        return df_ind

    def get_lead_source_performance(self) -> pd.DataFrame:
        """Lead acquisition channel breakdown."""
        records = []
        for source, group in self.df_full.groupby("Lead_Source"):
            kpis = calculate_kpis_from_subset(group, self.df_conversions)
            records.append({
                "Lead_Source": source,
                **kpis
            })
        df_src = pd.DataFrame(records).sort_values("Positive_Reply_Rate", ascending=False)
        return df_src

    def get_sequence_step_performance(self) -> pd.DataFrame:
        """Performance decay across sequence steps (Step 1 vs 2 vs 3)."""
        # Distinguish steps from subject line patterns
        def determine_step(subj: str) -> str:
            if "Re:" in subj:
                return "Step 2 (Day 3 Follow-Up)"
            elif "Permission" in subj or "Closing" in subj or "Final" in subj:
                return "Step 3 (Day 8 Breakup)"
            else:
                return "Step 1 (Day 0 Initial Outreach)"

        df_steps = self.df_activities.copy()
        df_steps["Sequence_Step"] = df_steps["Email_Subject"].apply(determine_step)

        records = []
        for step_name, group in df_steps.groupby("Sequence_Step"):
            kpis = calculate_kpis_from_subset(group, self.df_conversions)
            records.append({
                "Sequence_Step": step_name,
                **kpis
            })
        return pd.DataFrame(records).sort_values("Total_Emails_Sent", ascending=False)

    def get_daily_engagement_trends(self) -> pd.DataFrame:
        """Daily timeline of sent, delivered, opened, replied, and bounced emails."""
        daily = self.df_activities.groupby("Sent_Date").agg(
            Sent=("Email_ID", "count"),
            Delivered=("Delivery_Status", "sum"),
            Opens=("Open_Status", "sum"),
            Clicks=("Click_Status", "sum"),
            Replies=("Reply_Status", "sum"),
            Positive_Replies=("Reply_Type", lambda x: (x == "Positive").sum()),
            Bounces=("Bounce_Status", "sum")
        ).reset_index()
        return daily


if __name__ == "__main__":
    analytics = GrowthMarketingAnalytics()
    kpis = analytics.get_overall_executive_kpis()
    print("[Growth Analytics] Platform Executive KPI Summary:")
    print(f"  * Total Leads in DB       : {kpis['Total_Leads_Database']:,}")
    print(f"  * Total Emails Dispatched : {kpis['Total_Emails_Sent']:,}")
    print(f"  * Total Emails Delivered  : {kpis['Total_Emails_Delivered']:,} ({kpis['Delivery_Rate']}%)")
    print(f"  * Total Bounces           : {kpis['Total_Bounces']:,} ({kpis['Bounce_Rate']}%)")
    print(f"  * Total Opens             : {kpis['Total_Opens']:,} ({kpis['Open_Rate']}%)")
    print(f"  * Total Replies           : {kpis['Total_Replies']:,} ({kpis['Reply_Rate']}%)")
    print(f"  * Positive Replies        : {kpis['Total_Positive_Replies']:,} ({kpis['Positive_Reply_Rate']}%)")
    print(f"  * Qualified Opportunities : {kpis['Total_Conversions']:,} (${kpis['Total_Opportunity_Value']:,.2f})")
    print(f"  * Overall Conversion Rate : {kpis['Conversion_Rate']}%\n")

    camp_summary = analytics.get_campaign_performance_summary()
    print("[Campaign Summary Table Saved -> data/processed/campaign_kpi_summary.csv]")

