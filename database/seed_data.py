"""
B2B Cold Email Campaign & Growth Analytics Platform
Module: database/seed_data.py

Initializes SQLite relational database (b2b_growth.db), executes DDL schema,
and seeds verified datasets into relational tables.
"""

import os
import sqlite3
import pandas as pd


DB_PATH = "database/b2b_growth.db"
SCHEMA_PATH = "database/schema.sql"


def init_and_seed_database():
    """Build relational schema and populate database tables."""
    print(f"[Database Seed] Connecting to SQLite database at {DB_PATH}...")
    os.makedirs(os.path.dirname(DB_PATH), exist_ok=True)
    
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # 1. Execute Schema DDL
    print(f"[Database Seed] Executing DDL from {SCHEMA_PATH}...")
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    
    cursor.executescript(schema_sql)
    conn.commit()

    # 2. Seed Campaigns
    print("[Database Seed] Seeding Campaigns table...")
    df_campaigns = pd.read_csv("data/raw/campaigns.csv")
    campaign_cols = [
        "Campaign_ID", "Campaign_Name", "Campaign_Type", "Target_Industry",
        "Campaign_Start_Date", "Campaign_End_Date", "Total_Leads", "Campaign_Status", "Objective"
    ]
    df_campaigns[campaign_cols].to_sql("Campaigns", conn, if_exists="append", index=False)

    # 3. Seed Leads
    print("[Database Seed] Seeding Leads table...")
    df_leads = pd.read_csv("data/processed/clean_leads.csv")
    lead_cols = [
        "Lead_ID", "First_Name", "Last_Name", "Company_Name", "Company_Industry",
        "Company_Size", "Job_Title", "Business_Email", "Country", "City",
        "Lead_Source", "Lead_Created_Date", "Lead_Status", "Campaign_ID",
        "Seniority_Level", "Sales_Region", "Estimated_Revenue_M", "Hiring_Intent_Score"
    ]
    # Keep only columns defined in schema
    valid_lead_cols = [c for c in lead_cols if c in df_leads.columns]
    df_leads[valid_lead_cols].to_sql("Leads", conn, if_exists="append", index=False)

    # 4. Seed Email Activities
    print("[Database Seed] Seeding Email_Activities table...")
    df_activities = pd.read_csv("data/raw/email_activities.csv")
    df_activities.to_sql("Email_Activities", conn, if_exists="append", index=False)

    # 5. Seed A/B Tests
    print("[Database Seed] Seeding AB_Tests table...")
    df_ab = pd.read_csv("data/raw/ab_testing.csv")
    df_ab.to_sql("AB_Tests", conn, if_exists="append", index=False)

    # 6. Seed Conversions
    print("[Database Seed] Seeding Conversions table...")
    df_conv = pd.read_csv("data/raw/conversions.csv")
    df_conv.to_sql("Conversions", conn, if_exists="append", index=False)

    # Verify counts
    print("\n--- DATABASE SEED VERIFICATION ---")
    tables = ["Campaigns", "Leads", "Email_Activities", "AB_Tests", "Conversions"]
    for t in tables:
        cursor.execute(f"SELECT COUNT(*) FROM {t}")
        count = cursor.fetchone()[0]
        print(f"  * {t:18s}: {count:,} rows")

    # Test View execution
    cursor.execute("SELECT Campaign_ID, Campaign_Name, Total_Emails_Sent, Open_Rate, Reply_Rate FROM vw_campaign_kpis")
    rows = cursor.fetchall()
    print("\n--- VW_CAMPAIGN_KPIS VIEW PREVIEW ---")
    for r in rows:
        print(f"  [{r[0]}] {r[1]:40s} | Sent: {r[2]:5d} | Open: {r[3]}% | Reply: {r[4]}%")

    conn.close()
    print("\n[Database Seed] Completed successfully!")


if __name__ == "__main__":
    init_and_seed_database()

