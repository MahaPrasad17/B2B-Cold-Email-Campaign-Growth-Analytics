"""
Script to generate notebooks/exploratory_analysis.ipynb
"""

import json

def build_notebook():
    nb = {
        "cells": [],
        "metadata": {
            "language_info": {
                "name": "python",
                "version": "3.11.9"
            },
            "orig_nbformat": 4
        },
        "nbformat": 4,
        "nbformat_minor": 2
    }

    def add_md(source):
        nb["cells"].append({
            "cell_type": "markdown",
            "metadata": {},
            "source": [line + "\n" for line in source.split("\n")]
        })

    def add_code(source):
        nb["cells"].append({
            "cell_type": "code",
            "execution_count": None,
            "metadata": {},
            "outputs": [],
            "source": [line + "\n" for line in source.split("\n")]
        })

    # Cell 1: Markdown Title
    add_md(
        "# B2B Cold Email Campaign & Growth Analytics Platform\n"
        "### End-to-End Growth Marketing Analysis, SQL Modeling, A/B Testing & Deliverability Engine\n"
        "**Company Context:** GoodSpace AI (Simulated AI-Powered Recruitment SaaS)  \n"
        "**Role:** Growth Marketing Analyst & Marketing Data Engineer  \n"
        "**Author:** Candidate Portfolio Project  \n"
        "\n"
        "> **Notice:** All data, campaigns, prospect names, and performance figures in this project are synthetically generated for analytical demonstration. No actual unsolicited emails were sent."
    )

    # Cell 2: Markdown Section 1
    add_md(
        "## 1. Project Overview & Business Problem\n"
        "GoodSpace AI is an enterprise recruitment technology platform that automates preliminary candidate screening and technical evaluations.\n"
        "To acquire customer leads among HR and Talent Acquisition leaders, the growth marketing team executed four multi-step cold email campaigns across eight industries.\n"
        "\n"
        "### Key Objectives:\n"
        "1. Ingest, clean, deduplicate, and validate a database of 6,000 B2B leads.\n"
        "2. Segment leads across industry verticals, company size tiers, seniority levels, and acquisition channels.\n"
        "3. Simulate 3-step cold email sequence touchpoints (Day 0 Initial -> Day 3 Follow-Up -> Day 8 Breakup).\n"
        "4. Conduct rigorous A/B hypothesis testing using two-proportion z-tests and 95% confidence intervals.\n"
        "5. Execute 20 analytical SQL queries against a relational SQLite/SQL Server schema.\n"
        "6. Audit technical email deliverability (bounce trends, domain health, suppression lists, SPF/DKIM/DMARC).\n"
        "7. Generate data-driven, rule-based growth optimization recommendations."
    )

    # Cell 3: Code - Imports & Setup
    add_code(
        "import os\n"
        "import sys\n"
        "import sqlite3\n"
        "import math\n"
        "import statistics\n"
        "import pandas as pd\n"
        "import numpy as np\n"
        "import plotly.express as px\n"
        "import plotly.graph_objects as go\n"
        "\n"
        "# Add src to path\n"
        "sys.path.insert(0, os.path.abspath('..'))\n"
        "from src.analytics import GrowthMarketingAnalytics, calculate_kpis_from_subset, KPI_DEFINITIONS\n"
        "from src.ab_testing import calculate_two_proportion_z_test, analyze_ab_tests\n"
        "from src.deliverability import DeliverabilityAuditor\n"
        "from src.recommendation_engine import GrowthRecommendationEngine\n"
        "\n"
        "print('All libraries and analytical modules imported successfully!')"
    )

    # Cell 4: Markdown Section 2
    add_md(
        "## 2. Data Cleaning & Validation Audit\n"
        "We inspect the raw prospect records, identify data anomalies (duplicate emails, malformed addresses, missing values, untrimmed whitespace), and examine the cleaning audit report."
    )

    # Cell 5: Code - Cleaning Audit
    add_code(
        "# Load cleaning audit report and clean dataset\n"
        "with open('../data/processed/data_cleaning_audit.json', 'r') as f:\n"
        "    import json\n"
        "    audit = json.load(f)\n"
        "\n"
        "print('=== DATA QUALITY & CLEANING AUDIT REPORT ===')\n"
        "for k, v in audit.items():\n"
        "    print(f'  * {k:35s}: {v}')\n"
        "\n"
        "df_clean_leads = pd.read_csv('../data/processed/clean_leads.csv')\n"
        "df_clean_leads.head(5)"
    )

    # Cell 6: Markdown Section 3
    add_md(
        "## 3. Relational SQL Database Analytics\n"
        "We connect to `database/b2b_growth.db` and execute SQL queries to analyze top-of-funnel capacity, campaign throughput, and conversion metrics."
    )

    # Cell 7: Code - SQL Connection & Queries
    add_code(
        "db_conn = sqlite3.connect('../database/b2b_growth.db')\n"
        "\n"
        "# Query 1: Top-Level Database Overview\n"
        "q1 = '''\n"
        "SELECT \n"
        "    COUNT(*) AS Total_Leads,\n"
        "    COUNT(DISTINCT Company_Name) AS Unique_Companies,\n"
        "    COUNT(DISTINCT Business_Email) AS Unique_Verified_Emails,\n"
        "    ROUND(AVG(Hiring_Intent_Score), 1) AS Avg_Hiring_Intent_Score,\n"
        "    ROUND(AVG(Estimated_Revenue_M), 2) AS Avg_Company_Revenue_M\n"
        "FROM Leads;\n"
        "'''\n"
        "df_q1 = pd.read_sql(q1, db_conn)\n"
        "print('Database Capacity & Profile:')\n"
        "display(df_q1)\n"
        "\n"
        "# Query 3: Campaign Performance from SQL View\n"
        "q3 = 'SELECT * FROM vw_campaign_kpis;'\n"
        "df_q3 = pd.read_sql(q3, db_conn)\n"
        "print('\\nCampaign Performance (from vw_campaign_kpis):')\n"
        "display(df_q3)"
    )

    # Cell 8: Markdown Section 4
    add_md(
        "## 4. Full Conversion Funnel Analysis (Drop-Off Audit)\n"
        "Analyzing user progression across each stage of the outbound email lifecycle:\n"
        "**Sent -> Delivered -> Opened -> Clicked -> Replied -> Positive Reply -> Qualified Deal**"
    )

    # Cell 9: Code - Funnel Visualization
    add_code(
        "q15 = '''\n"
        "WITH FunnelMetrics AS (\n"
        "    SELECT \n"
        "        COUNT(a.Email_ID) AS Stage_1_Sent,\n"
        "        SUM(a.Delivery_Status) AS Stage_2_Delivered,\n"
        "        SUM(a.Open_Status) AS Stage_3_Opened,\n"
        "        SUM(a.Click_Status) AS Stage_4_Clicked,\n"
        "        SUM(a.Reply_Status) AS Stage_5_Replied,\n"
        "        SUM(CASE WHEN a.Reply_Type = 'Positive' THEN 1 ELSE 0 END) AS Stage_6_Positive_Replied,\n"
        "        (SELECT COUNT(*) FROM Conversions) AS Stage_7_Converted\n"
        "    FROM Email_Activities a\n"
        ")\n"
        "SELECT * FROM FunnelMetrics;\n"
        "'''\n"
        "df_funnel = pd.read_sql(q15, db_conn)\n"
        "\n"
        "stages = ['Sent', 'Delivered', 'Opened', 'Clicked', 'Replied', 'Positive Reply', 'Qualified Deal']\n"
        "counts = df_funnel.iloc[0].values\n"
        "\n"
        "fig_f = go.Figure(go.Funnel(\n"
        "    y=stages,\n"
        "    x=counts,\n"
        "    textinfo='value+percent initial',\n"
        "    marker={'color': ['#6366F1', '#3B82F6', '#0EA5E9', '#10B981', '#F59E0B', '#EC4899', '#8B5CF6']}\n"
        "))\n"
        "fig_f.update_layout(title='GoodSpace AI - Outbound Email Conversion Funnel', template='plotly_white', height=420)\n"
        "fig_f.show()"
    )

    # Cell 10: Markdown Section 5
    add_md(
        "## 5. Multi-Touch Sequence Pacing (Step 1 vs Step 2 vs Step 3)\n"
        "Evaluating reply generation across the 3-step cadence:\n"
        "- **Step 1:** Initial Outreach (Day 0)\n"
        "- **Step 2:** Value Proof & Case Benchmark (Day 3)\n"
        "- **Step 3:** Permission Breakup (Day 8)"
    )

    # Cell 11: Code - Sequence Performance
    add_code(
        "q13 = '''\n"
        "SELECT \n"
        "    CASE \n"
        "        WHEN Email_Subject LIKE 'Re:%' THEN 'Step 2: Follow-Up (+3 Days)'\n"
        "        WHEN Email_Subject LIKE 'Permission%' OR Email_Subject LIKE 'Closing%' OR Email_Subject LIKE 'Final%' \n"
        "        THEN 'Step 3: Breakup (+8 Days)'\n"
        "        ELSE 'Step 1: Initial Outreach (Day 0)'\n"
        "    END AS Sequence_Touchpoint,\n"
        "    COUNT(Email_ID) AS Dispatched_Volume,\n"
        "    SUM(Delivery_Status) AS Delivered_Volume,\n"
        "    SUM(Open_Status) AS Opens,\n"
        "    ROUND(CAST(SUM(Open_Status) AS FLOAT) / NULLIF(SUM(Delivery_Status), 0) * 100, 2) AS Open_Rate,\n"
        "    SUM(Reply_Status) AS Replies,\n"
        "    ROUND(CAST(SUM(Reply_Status) AS FLOAT) / NULLIF(SUM(Delivery_Status), 0) * 100, 2) AS Reply_Rate,\n"
        "    SUM(CASE WHEN Reply_Type = 'Positive' THEN 1 ELSE 0 END) AS Positive_Replies\n"
        "FROM Email_Activities\n"
        "GROUP BY Sequence_Touchpoint\n"
        "ORDER BY Dispatched_Volume DESC;\n"
        "'''\n"
        "df_seq = pd.read_sql(q13, db_conn)\n"
        "display(df_seq)\n"
        "\n"
        "fig_seq = px.bar(\n"
        "    df_seq,\n"
        "    x='Sequence_Touchpoint',\n"
        "    y='Reply_Rate',\n"
        "    color='Reply_Rate',\n"
        "    text='Reply_Rate',\n"
        "    title='Reply Rate by Sequence Step (%)',\n"
        "    color_continuous_scale='Blues'\n"
        ")\n"
        "fig_seq.update_traces(texttemplate='%{text:.2f}%', textposition='outside')\n"
        "fig_seq.show()"
    )

    # Cell 12: Markdown Section 6
    add_md(
        "## 6. A/B Testing & Statistical Hypothesis Testing Engine\n"
        "To rigorously evaluate email variations, we employ a **Two-Proportion Z-Test**:\n"
        "\n"
        "$$z = \\frac{\\hat{p}_B - \\hat{p}_A}{\\sqrt{p_{pool}(1 - p_{pool})\\left(\\frac{1}{n_A} + \\frac{1}{n_B}\\right)}}$$\n"
        "\n"
        "We calculate two-tailed p-values, 95% Confidence Intervals for difference in proportions, and evaluate sample size sufficiency before declaring a winner."
    )

    # Cell 13: Code - A/B Testing Execution
    add_code(
        "df_ab_analysis = analyze_ab_tests('../data/raw/ab_testing.csv')\n"
        "print('=== A/B TESTING STATISTICAL HYPOTHESIS EVALUATION ===\\n')\n"
        "\n"
        "for _, row in df_ab_analysis.iterrows():\n"
        "    print(f'Test {row[\"Test_ID\"]} ({row[\"Campaign_ID\"]}) - Variable: {row[\"Test_Variable\"]}')\n"
        "    print(f'  * Control (A): {row[\"Variant_A_Description\"]}')\n"
        "    print(f'  * Test    (B): {row[\"Variant_B_Description\"]}')\n"
        "    print(f'  * Open Rate  : A={row[\"Open_Rate_A\"]}% vs B={row[\"Open_Rate_B\"]}% (Lift: {row[\"Open_Lift_Pct\"]:+}%, p={row[\"Open_P_Value\"]})')\n"
        "    print(f'  * Reply Rate : A={row[\"Reply_Rate_A\"]}% vs B={row[\"Reply_Rate_B\"]}% (Lift: {row[\"Reply_Lift_Pct\"]:+}%, p={row[\"Reply_P_Value\"]})')\n"
        "    print(f'  * Winner     : {row[\"Primary_Winning_Variant\"]}')\n"
        "    print(f'  * Summary    : {row[\"Executive_Summary\"]}\\n')\n"
        "\n"
        "display(df_ab_analysis[[\n"
        "    'Test_ID', 'Campaign_ID', 'Test_Variable', \n"
        "    'Open_Rate_A', 'Open_Rate_B', 'Open_Lift_Pct', 'Open_P_Value',\n"
        "    'Reply_Rate_A', 'Reply_Rate_B', 'Reply_Lift_Pct', 'Reply_P_Value',\n"
        "    'Primary_Winning_Variant'\n"
        "]])"
    )

    # Cell 14: Markdown Section 7
    add_md(
        "## 7. Audience Insights: Industry & Seniority Matrix\n"
        "We evaluate how response and positive reply rates vary by target vertical and prospect seniority tier."
    )

    # Cell 15: Code - Audience Insights
    add_code(
        "q18 = '''\n"
        "SELECT \n"
        "    l.Company_Industry,\n"
        "    COUNT(DISTINCT l.Lead_ID) AS Total_Prospects,\n"
        "    SUM(a.Delivery_Status) AS Delivered_Emails,\n"
        "    SUM(CASE WHEN a.Reply_Type = 'Positive' THEN 1 ELSE 0 END) AS Positive_Replies,\n"
        "    ROUND(CAST(SUM(CASE WHEN a.Reply_Type = 'Positive' THEN 1 ELSE 0 END) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) * 100, 2) AS Positive_Reply_Rate\n"
        "FROM Leads l\n"
        "JOIN Email_Activities a ON l.Lead_ID = a.Lead_ID\n"
        "GROUP BY l.Company_Industry\n"
        "ORDER BY Positive_Reply_Rate DESC;\n"
        "'''\n"
        "df_ind_perf = pd.read_sql(q18, db_conn)\n"
        "\n"
        "fig_ind_p = px.bar(\n"
        "    df_ind_perf,\n"
        "    x='Company_Industry',\n"
        "    y='Positive_Reply_Rate',\n"
        "    color='Positive_Reply_Rate',\n"
        "    color_continuous_scale='Teal',\n"
        "    text='Positive_Reply_Rate',\n"
        "    title='Positive Reply Rate by Target Industry (%)'\n"
        ")\n"
        "fig_ind_p.update_traces(texttemplate='%{text:.2f}%', textposition='outside')\n"
        "fig_ind_p.show()"
    )

    # Cell 16: Markdown Section 8
    add_md(
        "## 8. Technical Email Deliverability & Suppression Audit\n"
        "We audit delivery rates, hard bounces, domain health, and extract the automated suppression list."
    )

    # Cell 17: Code - Deliverability Audit
    add_code(
        "auditor = DeliverabilityAuditor(\n"
        "    activities_path='../data/raw/email_activities.csv',\n"
        "    leads_path='../data/processed/clean_leads.csv'\n"
        ")\n"
        "deliv_report = auditor.generate_deliverability_report()\n"
        "\n"
        "print('=== TECHNICAL DELIVERABILITY HEALTH REPORT ===')\n"
        "for k, v in deliv_report.items():\n"
        "    print(f'  * {k:25s}: {v}')\n"
        "\n"
        "supp_df = auditor.export_suppression_list('../data/processed/suppression_list.csv')\n"
        "print(f'\\nSuppressed Contacts Count: {len(supp_df)}')\n"
        "display(supp_df.head(5))"
    )

    # Cell 18: Markdown Section 9
    add_md(
        "## 9. Algorithmic Growth Recommendations\n"
        "We execute the rule-based growth engine to produce prioritized strategic recommendations for executive leadership."
    )

    # Cell 19: Code - Recommendation Engine
    add_code(
        "engine = GrowthRecommendationEngine()\n"
        "recommendations = engine.generate_recommendations()\n"
        "df_rec = pd.DataFrame(recommendations)\n"
        "\n"
        "print(f'Generated {len(df_rec)} Prioritized Recommendations:\\n')\n"
        "for idx, r in df_rec.iterrows():\n"
        "    print(f'[{r[\"Priority\"]}] {r[\"Category\"]}: {r[\"Observed_Metric\"]}')\n"
        "    print(f'   Finding: {r[\"Finding\"]}')\n"
        "    print(f'   Action : {r[\"Actionable_Recommendation\"]}')\n"
        "    print(f'   Impact : {r[\"Expected_Impact\"]}\\n')\n"
        "\n"
        "display(df_rec[['Priority', 'Category', 'Observed_Metric', 'Actionable_Recommendation']])"
    )

    # Cell 20: Markdown Summary
    add_md(
        "## 10. Conclusion & Portfolio Impact\n"
        "This project establishes a complete, production-ready framework for B2B growth marketing:\n"
        "1. **Lead Hygiene:** Cleaned and enriched 5,900+ leads, eliminating duplicates and malformed records.\n"
        "2. **Data Modeling:** Structured a 5-table relational schema with ANSI SQL queries and Power BI star-schema exports.\n"
        "3. **Scientific Experimentation:** Validated statistically significant lifts in subject lines, CTAs, and copy length using two-proportion z-tests.\n"
        "4. **Deliverability & Compliance:** Maintained a 99.05% delivery rate and automated suppression list maintenance in compliance with CAN-SPAM and GDPR.\n"
        "5. **Revenue Alignment:** Tied top-of-funnel outbound engagement to $2.99M in qualified pipeline opportunity value."
    )

    # Save to disk
    with open("notebooks/exploratory_analysis.ipynb", "w", encoding="utf-8") as f:
        json.dump(nb, f, indent=2)
    print("Successfully built notebooks/exploratory_analysis.ipynb!")

if __name__ == "__main__":
    build_notebook()

