"""
B2B Cold Email Campaign & Growth Analytics Platform
Module: src/lead_segmentation.py

Segments B2B leads across 6 foundational dimensions:
1. Industry
2. Company Size Tier
3. Job Designation / Seniority
4. Geography / Region
5. Lead Acquisition Source
6. Campaign Behavioral Engagement Tier
"""

import os
import pandas as pd


def segment_leads(
    leads_path: str = "data/processed/clean_leads.csv",
    activities_path: str = "data/raw/email_activities.csv",
    conversions_path: str = "data/raw/conversions.csv"
) -> pd.DataFrame:
    """
    Merge cleaned leads with behavioral email activity and conversion data
    to produce a multi-dimensional segmented lead intelligence table.
    """
    if not os.path.exists(leads_path):
        raise FileNotFoundError(f"Clean leads file missing at {leads_path}")
    if not os.path.exists(activities_path):
        raise FileNotFoundError(f"Email activities missing at {activities_path}")

    leads_df = pd.read_csv(leads_path)
    activities_df = pd.read_csv(activities_path)

    # Calculate lead-level behavioral aggregates
    lead_agg = activities_df.groupby("Lead_ID").agg(
        Total_Emails_Sent=("Email_ID", "count"),
        Total_Emails_Delivered=("Delivery_Status", "sum"),
        Total_Opens=("Open_Status", "sum"),
        Total_Clicks=("Click_Status", "sum"),
        Total_Replies=("Reply_Status", "sum"),
        Total_Bounces=("Bounce_Status", "sum"),
        Total_Unsubscribes=("Unsubscribe_Status", "sum"),
        Positive_Replies=("Reply_Type", lambda x: (x == "Positive").sum()),
        Neutral_Replies=("Reply_Type", lambda x: (x == "Neutral").sum()),
        Negative_Replies=("Reply_Type", lambda x: (x == "Negative").sum())
    ).reset_index()

    # Merge lead information with behavioral metrics
    merged = pd.merge(leads_df, lead_agg, on="Lead_ID", how="left")

    # Fill NA for uncontacted leads
    metric_cols = [
        "Total_Emails_Sent", "Total_Emails_Delivered", "Total_Opens",
        "Total_Clicks", "Total_Replies", "Total_Bounces",
        "Total_Unsubscribes", "Positive_Replies", "Neutral_Replies", "Negative_Replies"
    ]
    for col in metric_cols:
        merged[col] = merged[col].fillna(0).astype(int)

    # Incorporate Conversion Status
    if os.path.exists(conversions_path):
        conv_df = pd.read_csv(conversions_path)
        conv_summary = conv_df.groupby("Lead_ID").agg(
            Conversion_Count=("Conversion_ID", "count"),
            Total_Opportunity_Value=("Opportunity_Value", "sum"),
            Latest_Conversion_Status=("Conversion_Status", "last")
        ).reset_index()
        merged = pd.merge(merged, conv_summary, on="Lead_ID", how="left")
        merged["Conversion_Count"] = merged["Conversion_Count"].fillna(0).astype(int)
        merged["Total_Opportunity_Value"] = merged["Total_Opportunity_Value"].fillna(0.0)
        merged["Latest_Conversion_Status"] = merged["Latest_Conversion_Status"].fillna("Not Converted")
    else:
        merged["Conversion_Count"] = 0
        merged["Total_Opportunity_Value"] = 0.0
        merged["Latest_Conversion_Status"] = "Not Converted"

    # Behavioral Engagement Tiering
    def assign_engagement_tier(row) -> str:
        if row["Conversion_Count"] > 0 or row["Latest_Conversion_Status"] == "Closed-Won":
            return "Champion (Converted Deal)"
        elif row["Positive_Replies"] > 0:
            return "Hot (Positive Replier)"
        elif row["Total_Replies"] > 0:
            return "Warm (Replied Neutral/Obj)"
        elif row["Total_Clicks"] > 0 or row["Total_Opens"] >= 2:
            return "Interested (Multiple Opens/Clicks)"
        elif row["Total_Opens"] == 1:
            return "Lukewarm (Single Open)"
        elif row["Total_Bounces"] > 0:
            return "Bounced (Delivery Failure)"
        elif row["Total_Unsubscribes"] > 0:
            return "Opted-Out (Unsubscribed)"
        elif row["Total_Emails_Delivered"] > 0:
            return "Cold (Delivered, No Open)"
        return "Uncontacted"

    merged["Engagement_Segment"] = merged.apply(assign_engagement_tier, axis=1)

    # Lead Priority Tiering (Marketing Score based on Intent + Size + Seniority)
    def calculate_lead_score(row) -> int:
        score = 0
        # Intent score baseline (0-40 pts)
        score += int(row.get("Hiring_Intent_Score", 50) * 0.4)
        # Seniority tier (0-30 pts)
        sen = str(row.get("Seniority_Level", ""))
        if "C-Suite" in sen:
            score += 30
        elif "Director" in sen:
            score += 25
        elif "Manager" in sen:
            score += 15
        else:
            score += 10
        # Company size tier (0-20 pts)
        tier = str(row.get("Company_Size_Tier", ""))
        if "Enterprise" in tier:
            score += 20
        elif "Mid-Market" in tier:
            score += 15
        else:
            score += 10
        # Engagement bonus (0-10 pts)
        if "Hot" in row["Engagement_Segment"] or "Champion" in row["Engagement_Segment"]:
            score += 10
        elif "Interested" in row["Engagement_Segment"]:
            score += 5
        return min(100, score)

    merged["Marketing_Lead_Score"] = merged.apply(calculate_lead_score, axis=1)

    # Save segmented dataset
    os.makedirs("data/processed", exist_ok=True)
    merged.to_csv("data/processed/segmented_leads.csv", index=False)
    print(f"[Lead Segmentation] Successfully segmented {len(merged)} leads.")
    print("                    Breakdown by Engagement Segment:")
    for segment, count in merged["Engagement_Segment"].value_counts().items():
        print(f"                      * {segment:35s}: {count:5d} leads")
    print("                    Saved -> data/processed/segmented_leads.csv")
    return merged


if __name__ == "__main__":
    segment_leads()

