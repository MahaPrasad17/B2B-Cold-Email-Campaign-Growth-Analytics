"""
B2B Cold Email Campaign & Growth Analytics Platform
Module: src/data_generation.py

Generates realistic synthetic B2B lead data, cold email campaigns,
email activity logs with strict email funnel logic, A/B test experiments,
and conversion records.

Simulated Company: GoodSpace AI (B2B AI-powered recruitment platform)
"""

import os
import random
import datetime
import numpy as np
import pandas as pd

# Set deterministic seed for reproducibility
RANDOM_SEED = 42
random.seed(RANDOM_SEED)
np.random.seed(RANDOM_SEED)

# Reference pools for realistic B2B attributes
FIRST_NAMES = [
    "Alexander", "Emily", "Michael", "Sarah", "David", "Jessica", "James", "Sophia",
    "Daniel", "Olivia", "Robert", "Emma", "William", "Ava", "Joseph", "Isabella",
    "Matthew", "Mia", "Andrew", "Charlotte", "Ethan", "Amelia", "Benjamin", "Harper",
    "Arjun", "Priya", "Rahul", "Ananya", "Rohan", "Sneha", "Vikram", "Neha",
    "Marcus", "Elena", "Stefan", "Katja", "Lukas", "Sophie", "Jean", "Camille"
]

LAST_NAMES = [
    "Smith", "Johnson", "Williams", "Brown", "Jones", "Garcia", "Miller", "Davis",
    "Rodriguez", "Martinez", "Hernandez", "Lopez", "Gonzalez", "Wilson", "Anderson",
    "Taylor", "Thomas", "Moore", "Jackson", "Martin", "Sharma", "Patel", "Verma",
    "Kapoor", "Gupta", "Nair", "Schneider", "Mueller", "Fischer", "Weber", "Dubois"
]

INDUSTRIES = [
    "Information Technology",
    "Banking and Finance",
    "Healthcare",
    "Education",
    "Manufacturing",
    "Retail",
    "Consulting",
    "E-commerce"
]

COMPANY_PREFIXES = [
    "Apex", "Nexus", "Vertex", "Quantum", "Synergy", "Beacon", "Pinnacle", "Acro",
    "Vanguard", "Catalyst", "Nova", "Starlight", "Crestview", "Summit", "Horizon",
    "Infinitum", "Optima", "Paramount", "Sterling", "Kore", "Aegis", "Centurion"
]

COMPANY_SUFFIXES = [
    "Technologies", "Solutions", "Global", "Systems", "Health", "Capital", "Logistics",
    "Consulting", "Ventures", "Partners", "Digital", "Industries", "Group", "Analytics"
]

COMPANY_SIZES = [
    "1-10",
    "11-50",
    "51-200",
    "201-500",
    "501-1000",
    "1000+"
]

JOB_TITLES = [
    "VP of Talent Acquisition",
    "Head of Recruitment",
    "Director of Human Resources",
    "Chief People Officer",
    "Technical Recruitment Lead",
    "Senior Talent Sourcing Manager",
    "HR Operations Director",
    "People & Culture Lead",
    "Head of Global Sourcing",
    "HR Business Partner"
]

GEOGRAPHIES = [
    {"Country": "United States", "Cities": ["San Francisco", "New York", "Austin", "Chicago", "Seattle", "Boston"]},
    {"Country": "United Kingdom", "Cities": ["London", "Manchester", "Birmingham", "Edinburgh"]},
    {"Country": "Canada", "Cities": ["Toronto", "Vancouver", "Montreal", "Calgary"]},
    {"Country": "Germany", "Cities": ["Berlin", "Munich", "Frankfurt", "Hamburg"]},
    {"Country": "India", "Cities": ["Bengaluru", "Mumbai", "Gurugram", "Hyderabad", "Pune"]},
    {"Country": "Singapore", "Cities": ["Singapore"]},
    {"Country": "Australia", "Cities": ["Sydney", "Melbourne", "Brisbane"]}
]

LEAD_SOURCES = [
    "LinkedIn Outreach",
    "Apollo Database",
    "Webinar Attendee",
    "Inbound Content Download",
    "Conference & Expo",
    "G2 Reviewer Lead"
]

CAMPAIGN_CONFIGS = [
    {
        "Campaign_ID": "CMP-001",
        "Campaign_Name": "IT Tech Hiring Velocity Q1",
        "Campaign_Type": "Outbound Cold Outreach",
        "Target_Industry": "Information Technology",
        "Campaign_Start_Date": "2026-06-01",
        "Campaign_End_Date": "2026-07-15",
        "Objective": "Engage IT HR and TA leaders to automate engineering screening with GoodSpace AI",
        "Test_Variable": "Subject Line",
        "Variant_A_Desc": "Direct Benefit: 'Reduce technical screening time by 60% with AI'",
        "Variant_B_Desc": "Curiosity Question: 'Quick question regarding your Q3 tech hiring targets'",
        "Base_Open_Rate": 0.42,
        "Base_Reply_Rate": 0.075,
        "Base_Positive_Rate": 0.45,
        "Base_Bounce_Rate": 0.024
    },
    {
        "Campaign_ID": "CMP-002",
        "Campaign_Name": "Manufacturing Plant & Eng Talent Pipeline",
        "Campaign_Type": "Outbound Cold Outreach",
        "Target_Industry": "Manufacturing",
        "Campaign_Start_Date": "2026-06-15",
        "Campaign_End_Date": "2026-07-31",
        "Objective": "Assist manufacturing talent teams in sourcing plant engineers and supply chain specialists",
        "Test_Variable": "Call To Action",
        "Variant_A_Desc": "Direct Calendar Invite: 'Grab a quick 10-min calendar slot here'",
        "Variant_B_Desc": "Low-friction Permission: 'Would you be opposed to seeing a 2-min workflow video?'",
        "Base_Open_Rate": 0.35,
        "Base_Reply_Rate": 0.048,
        "Base_Positive_Rate": 0.38,
        "Base_Bounce_Rate": 0.038
    },
    {
        "Campaign_ID": "CMP-003",
        "Campaign_Name": "Consulting Executive Search & Onboarding",
        "Campaign_Type": "Outbound Cold Outreach",
        "Target_Industry": "Consulting",
        "Campaign_Start_Date": "2026-07-01",
        "Campaign_End_Date": "2026-08-20",
        "Objective": "Partner with consulting firm recruitment directors to accelerate partner-track talent acquisition",
        "Test_Variable": "Personalization Hook",
        "Variant_A_Desc": "Peer Benchmark Hook: 'How Tier-1 consulting firms cut candidate drop-off by 40%'",
        "Variant_B_Desc": "Headcount Growth Hook: 'Noticed your team is expanding client consulting headcount'",
        "Base_Open_Rate": 0.48,
        "Base_Reply_Rate": 0.092,
        "Base_Positive_Rate": 0.52,
        "Base_Bounce_Rate": 0.019
    },
    {
        "Campaign_ID": "CMP-004",
        "Campaign_Name": "Fintech & Banking Compliance Hiring",
        "Campaign_Type": "Outbound Cold Outreach",
        "Target_Industry": "Banking and Finance",
        "Campaign_Start_Date": "2026-07-15",
        "Campaign_End_Date": "2026-09-05",
        "Objective": "Help financial institutions source pre-vetted compliance, risk, and quantitative talent",
        "Test_Variable": "Email Body Length",
        "Variant_A_Desc": "Short & Punchy (under 75 words): Value proposition + metric proof",
        "Variant_B_Desc": "Case Study Format (150 words): Customer narrative and quotes",
        "Base_Open_Rate": 0.38,
        "Base_Reply_Rate": 0.055,
        "Base_Positive_Rate": 0.40,
        "Base_Bounce_Rate": 0.031
    }
]


def generate_company_name(industry: str) -> str:
    """Generate a realistic synthetic B2B company name."""
    p = random.choice(COMPANY_PREFIXES)
    s = random.choice(COMPANY_SUFFIXES)
    return f"{p} {s}"


def generate_leads_dataset(num_leads: int = 6000) -> pd.DataFrame:
    """
    Generate synthetic B2B leads dataset with industry-grade realism.
    Includes controlled data quality anomalies (duplicates, missing values,
    untrimmed whitespace, malformed emails) to demonstrate data cleaning.
    """
    leads = []
    base_date = datetime.date(2026, 5, 1)

    for i in range(1, num_leads + 1):
        lead_id = f"LEAD-{i:05d}"
        first_name = random.choice(FIRST_NAMES)
        last_name = random.choice(LAST_NAMES)
        
        # Select geography
        geo = random.choice(GEOGRAPHIES)
        country = geo["Country"]
        city = random.choice(geo["Cities"])

        # Select industry and company
        industry = random.choice(INDUSTRIES)
        company_name = generate_company_name(industry)
        company_size = random.choice(COMPANY_SIZES)
        job_title = random.choice(JOB_TITLES)
        lead_source = random.choice(LEAD_SOURCES)
        
        # Email generation with corporate domain
        domain_clean = company_name.lower().replace(" ", "").replace("&", "") + ".com"
        business_email = f"{first_name.lower()}.{last_name.lower()}@{domain_clean}"

        # Creation date spread across May to July 2026
        days_offset = random.randint(0, 90)
        created_date = base_date + datetime.timedelta(days=days_offset)

        # Assign Campaign based on target industry or general distribution
        if industry == "Information Technology":
            campaign_id = "CMP-001"
        elif industry == "Manufacturing":
            campaign_id = "CMP-002"
        elif industry == "Consulting":
            campaign_id = "CMP-003"
        elif industry == "Banking and Finance":
            campaign_id = "CMP-004"
        else:
            # Distribute remaining industries (Healthcare, Education, Retail, E-commerce) across campaigns
            campaign_id = random.choice(["CMP-001", "CMP-002", "CMP-003", "CMP-004"])

        lead_status = "New"

        leads.append({
            "Lead_ID": lead_id,
            "First_Name": first_name,
            "Last_Name": last_name,
            "Company_Name": company_name,
            "Company_Industry": industry,
            "Company_Size": company_size,
            "Job_Title": job_title,
            "Business_Email": business_email,
            "Country": country,
            "City": city,
            "Lead_Source": lead_source,
            "Lead_Created_Date": created_date.strftime("%Y-%m-%d"),
            "Lead_Status": lead_status,
            "Campaign_ID": campaign_id
        })

    df_leads = pd.DataFrame(leads)

    # Inject realistic data anomalies into ~4% of rows to test Data Cleaning module
    # 1. Duplicate rows
    num_dupes = 85
    dupe_indices = np.random.choice(df_leads.index, size=num_dupes, replace=False)
    dupe_rows = df_leads.loc[dupe_indices].copy()
    # give them duplicate emails / person info with different Lead_IDs to mimic re-import
    for idx, row_idx in enumerate(dupe_rows.index):
        dupe_rows.loc[row_idx, "Lead_ID"] = f"LEAD-DUP-{idx+1:04d}"
    df_leads = pd.concat([df_leads, dupe_rows], ignore_index=True)

    # 2. Missing/Empty values in First_Name or Company_Size
    missing_name_idx = np.random.choice(df_leads.index, size=40, replace=False)
    df_leads.loc[missing_name_idx, "First_Name"] = None

    missing_size_idx = np.random.choice(df_leads.index, size=35, replace=False)
    df_leads.loc[missing_size_idx, "Company_Size"] = None

    # 3. Malformed email addresses (missing '@', missing TLD, or space)
    bad_email_idx = np.random.choice(df_leads.index, size=50, replace=False)
    for b_idx in bad_email_idx:
        original_email = df_leads.loc[b_idx, "Business_Email"]
        if original_email and "@" in original_email:
            defect_type = random.choice(["no_at", "no_domain", "spaces", "invalid_char"])
            if defect_type == "no_at":
                df_leads.loc[b_idx, "Business_Email"] = original_email.replace("@", "")
            elif defect_type == "no_domain":
                df_leads.loc[b_idx, "Business_Email"] = original_email.split("@")[0] + "@"
            elif defect_type == "spaces":
                df_leads.loc[b_idx, "Business_Email"] = " " + original_email + " "
            elif defect_type == "invalid_char":
                df_leads.loc[b_idx, "Business_Email"] = original_email.replace("@", "@@")

    # 4. Untrimmed whitespace in text fields
    whitespace_idx = np.random.choice(df_leads.index, size=60, replace=False)
    for w_idx in whitespace_idx:
        if df_leads.loc[w_idx, "Company_Name"]:
            df_leads.loc[w_idx, "Company_Name"] = f"  {df_leads.loc[w_idx, 'Company_Name']}  "

    return df_leads


def generate_campaigns_dataset(df_clean_leads: pd.DataFrame) -> pd.DataFrame:
    """Generate campaign metadata and total lead counts."""
    campaign_records = []
    for cfg in CAMPAIGN_CONFIGS:
        cid = cfg["Campaign_ID"]
        total_leads = int((df_clean_leads["Campaign_ID"] == cid).sum())
        campaign_records.append({
            "Campaign_ID": cid,
            "Campaign_Name": cfg["Campaign_Name"],
            "Campaign_Type": cfg["Campaign_Type"],
            "Target_Industry": cfg["Target_Industry"],
            "Campaign_Start_Date": cfg["Campaign_Start_Date"],
            "Campaign_End_Date": cfg["Campaign_End_Date"],
            "Total_Leads": total_leads,
            "Campaign_Status": "Completed",
            "Objective": cfg["Objective"]
        })
    return pd.DataFrame(campaign_records)


def simulate_email_activities(df_clean_leads: pd.DataFrame) -> tuple[pd.DataFrame, pd.DataFrame, pd.DataFrame]:
    """
    Simulate cold email marketing outreach across a 3-step sequence:
      Step 1: Day 0 (Initial outreach)
      Step 2: Day 3 (Follow-up)
      Step 3: Day 8 (Final follow-up / Breakup email)
    
    Adheres strictly to the logical email funnel rules:
      - Bounced => Delivery=0, Open=0, Click=0, Reply=0, Unsub=0.
      - Delivered=0 => Open=0, Click=0, Reply=0.
      - Open=0 => Click=0, Reply=0.
      - Click=1 or Reply=1 => Delivery=1 and Open=1.
      - If lead replies to Step 1 or unsubscribes, sequence stops (no Step 2/3).
      - Converts only if reply is positive.
    
    Returns:
      (df_activities, df_ab_test, df_conversions)
    """
    activities = []
    conversions = []
    email_counter = 1
    conversion_counter = 1

    # Map campaign configs
    cfg_map = {c["Campaign_ID"]: c for c in CAMPAIGN_CONFIGS}

    # Tracking per-variant performance for A/B dataset
    ab_tracker = {
        cid: {
            "Delivered_A": 0, "Delivered_B": 0,
            "Opens_A": 0, "Opens_B": 0,
            "Clicks_A": 0, "Clicks_B": 0,
            "Replies_A": 0, "Replies_B": 0,
            "Positive_A": 0, "Positive_B": 0,
            "Conversions_A": 0, "Conversions_B": 0
        }
        for cid in cfg_map
    }

    # Iterate over every clean lead assigned to a campaign
    for _, lead in df_clean_leads.iterrows():
        lead_id = lead["Lead_ID"]
        cid = lead["Campaign_ID"]
        if cid not in cfg_map:
            continue
        cfg = cfg_map[cid]

        # Randomly assign A/B variant (50/50 split)
        variant = "Variant_A" if random.random() < 0.5 else "Variant_B"

        # Apply slight realistic performance lift depending on variant
        # In CMP-001 (Tech), Variant B (Curiosity) outperforms Variant A by ~14% relative
        # In CMP-002 (Mfg), Variant B (Low friction video) outperforms Variant A by ~22% relative
        # In CMP-003 (Consulting), Variant A (Benchmark data) outperforms Variant B by ~18% relative
        # In CMP-004 (Finance), Variant A (Short email) outperforms Variant B by ~16% relative
        open_rate = cfg["Base_Open_Rate"]
        reply_rate = cfg["Base_Reply_Rate"]
        positive_rate = cfg["Base_Positive_Rate"]
        bounce_rate = cfg["Base_Bounce_Rate"]

        if cid == "CMP-001":
            if variant == "Variant_B":
                open_rate *= 1.15
                reply_rate *= 1.25
        elif cid == "CMP-002":
            if variant == "Variant_B":
                open_rate *= 1.10
                reply_rate *= 1.35
        elif cid == "CMP-003":
            if variant == "Variant_A":
                open_rate *= 1.18
                reply_rate *= 1.30
        elif cid == "CMP-004":
            if variant == "Variant_A":
                open_rate *= 1.14
                reply_rate *= 1.28

        # Higher job titles (VP, Director, C-level) have slightly higher positive reply value
        job = str(lead.get("Job_Title", ""))
        if any(exec_word in job for exec_word in ["VP", "Chief", "Director"]):
            positive_rate *= 1.10

        # Start sequence: Step 1 (Day 0)
        start_date = datetime.datetime.strptime(cfg["Campaign_Start_Date"], "%Y-%m-%d").date()
        stagger_days = random.randint(0, 14)
        step1_date = start_date + datetime.timedelta(days=stagger_days)

        sequence_active = True
        lead_converted = False

        sequence_steps = [
            {"step": 1, "days": 0, "name": "Initial Outreach"},
            {"step": 2, "days": 3, "name": "Follow-Up #1 (Value & Proof)"},
            {"step": 3, "days": 8, "name": "Follow-Up #2 (Breakup & Resource)"}
        ]

        for s_info in sequence_steps:
            if not sequence_active:
                break

            step_num = s_info["step"]
            sent_date = step1_date + datetime.timedelta(days=s_info["days"])
            email_id = f"EML-{email_counter:07d}"
            email_counter += 1

            # Subject lines
            if step_num == 1:
                subj = (
                    f"{cfg['Variant_A_Desc'].split(':')[1].strip()}"
                    if variant == "Variant_A"
                    else f"{cfg['Variant_B_Desc'].split(':')[1].strip()}"
                )
            elif step_num == 2:
                subj = f"Re: Quick follow-up regarding {lead['Company_Name']}'s recruitment speed"
            else:
                subj = f"Permission to close your file, {lead['First_Name']}?"

            # Simulate Deliverability
            # Step 1 handles the initial bounce check; if bounced, lead never receives step 2 or 3
            is_bounced = 1 if (step_num == 1 and random.random() < bounce_rate) else 0
            is_delivered = 0 if is_bounced == 1 else 1
            is_unsubscribed = 0

            is_opened = 0
            is_clicked = 0
            is_replied = 0
            reply_type = None

            if is_delivered == 1:
                # Step 1 has base open rate; Follow-up 2 has higher opens due to thread bump (45%), Step 3 slightly lower
                step_open_multiplier = 1.0 if step_num == 1 else (1.12 if step_num == 2 else 0.85)
                effective_open = min(0.85, open_rate * step_open_multiplier)
                is_opened = 1 if random.random() < effective_open else 0

                if is_opened == 1:
                    # Click rate conditioned on open
                    click_prob = 0.18 if variant == "Variant_B" and cid == "CMP-002" else 0.12
                    is_clicked = 1 if random.random() < click_prob else 0

                    # Reply probability
                    step_reply_multiplier = 1.0 if step_num == 1 else (1.20 if step_num == 2 else 0.70)
                    effective_reply = min(0.60, reply_rate * step_reply_multiplier)
                    is_replied = 1 if random.random() < effective_reply else 0

                    if is_replied == 1:
                        # Determine sentiment of reply
                        rep_rand = random.random()
                        if rep_rand < positive_rate:
                            reply_type = "Positive"
                        elif rep_rand < positive_rate + 0.25:
                            reply_type = "Neutral"
                        elif rep_rand < positive_rate + 0.45:
                            reply_type = "Out of Office"
                        else:
                            reply_type = "Negative"

                        # If replied, sequence stops!
                        sequence_active = False

                # Unsubscribe check (only if delivered and not positive reply)
                if reply_type != "Positive" and random.random() < 0.006:
                    is_unsubscribed = 1
                    sequence_active = False

            # If bounced, sequence stops immediately
            if is_bounced == 1:
                sequence_active = False

            # Track A/B metrics
            v_key = "A" if variant == "Variant_A" else "B"
            if is_delivered == 1:
                ab_tracker[cid][f"Delivered_{v_key}"] += 1
            if is_opened == 1:
                ab_tracker[cid][f"Opens_{v_key}"] += 1
            if is_clicked == 1:
                ab_tracker[cid][f"Clicks_{v_key}"] += 1
            if is_replied == 1:
                ab_tracker[cid][f"Replies_{v_key}"] += 1
            if reply_type == "Positive":
                ab_tracker[cid][f"Positive_{v_key}"] += 1

            activities.append({
                "Email_ID": email_id,
                "Lead_ID": lead_id,
                "Campaign_ID": cid,
                "Email_Variant": variant,
                "Email_Subject": subj,
                "Sent_Date": sent_date.strftime("%Y-%m-%d"),
                "Delivery_Status": is_delivered,
                "Open_Status": is_opened,
                "Click_Status": is_clicked,
                "Reply_Status": is_replied,
                "Reply_Type": reply_type,
                "Bounce_Status": is_bounced,
                "Unsubscribe_Status": is_unsubscribed
            })

            # Check if positive reply turns into a Conversion
            if reply_type == "Positive" and not lead_converted:
                # 65% of positive replies qualify into pipeline opportunity
                if random.random() < 0.65:
                    lead_converted = True
                    conv_id = f"CNV-{conversion_counter:05d}"
                    conversion_counter += 1
                    conv_date = sent_date + datetime.timedelta(days=random.randint(1, 10))

                    # Opportunity Value based on company size
                    c_size = str(lead.get("Company_Size", "51-200"))
                    if c_size == "1000+":
                        val = random.randint(25000, 50000)
                    elif c_size in ["501-1000", "201-500"]:
                        val = random.randint(15000, 30000)
                    elif c_size in ["51-200", "11-50"]:
                        val = random.randint(7500, 15000)
                    else:
                        val = random.randint(3500, 7500)

                    c_status = random.choices(
                        ["Closed-Won", "In Pipeline", "Closed-Lost"],
                        weights=[0.35, 0.45, 0.20],
                        k=1
                    )[0]

                    conversions.append({
                        "Conversion_ID": conv_id,
                        "Lead_ID": lead_id,
                        "Campaign_ID": cid,
                        "Conversion_Date": conv_date.strftime("%Y-%m-%d"),
                        "Conversion_Status": c_status,
                        "Opportunity_Value": val
                    })
                    ab_tracker[cid][f"Conversions_{v_key}"] += 1

    df_activities = pd.DataFrame(activities)
    df_conversions = pd.DataFrame(conversions)

    # Build A/B Testing Dataset
    ab_rows = []
    test_num = 1
    for cid, data in ab_tracker.items():
        cfg = cfg_map[cid]
        ab_rows.append({
            "Test_ID": f"ABT-{test_num:03d}",
            "Campaign_ID": cid,
            "Test_Variable": cfg["Test_Variable"],
            "Variant_A": cfg["Variant_A_Desc"],
            "Variant_B": cfg["Variant_B_Desc"],
            "Emails_Delivered_A": data["Delivered_A"],
            "Emails_Delivered_B": data["Delivered_B"],
            "Opens_A": data["Opens_A"],
            "Opens_B": data["Opens_B"],
            "Replies_A": data["Replies_A"],
            "Replies_B": data["Replies_B"],
            "Clicks_A": data["Clicks_A"],
            "Clicks_B": data["Clicks_B"],
            "Positive_Replies_A": data["Positive_A"],
            "Positive_Replies_B": data["Positive_B"],
            "Conversions_A": data["Conversions_A"],
            "Conversions_B": data["Conversions_B"]
        })
        test_num += 1

    df_ab_test = pd.DataFrame(ab_rows)
    return df_activities, df_ab_test, df_conversions


def run_pipeline():
    """Execute synthetic data generation and export raw CSV files."""
    print("[1/4] Generating 6,000 synthetic B2B leads...")
    df_raw_leads = generate_leads_dataset(num_leads=6000)
    
    os.makedirs("data/raw", exist_ok=True)
    df_raw_leads.to_csv("data/raw/raw_leads.csv", index=False)
    print(f"      Saved raw leads: {len(df_raw_leads)} rows -> data/raw/raw_leads.csv")

    # Import clean lead logic temporarily or filter for baseline simulation
    # Full cleaning will be formalized in src/data_cleaning.py
    # Here we simulate with the valid leads
    valid_leads = df_raw_leads.dropna(subset=["Business_Email"]).copy()
    valid_leads = valid_leads[valid_leads["Business_Email"].str.contains("@", na=False)]
    valid_leads = valid_leads.drop_duplicates(subset=["Business_Email"])
    valid_leads["Company_Name"] = valid_leads["Company_Name"].astype(str).str.strip()

    print("[2/4] Generating Campaign dataset...")
    df_campaigns = generate_campaigns_dataset(valid_leads)
    df_campaigns.to_csv("data/raw/campaigns.csv", index=False)
    print(f"      Saved campaigns: {len(df_campaigns)} campaigns -> data/raw/campaigns.csv")

    print("[3/4] Simulating cold email activities across 3-step sequence...")
    df_activities, df_ab_test, df_conversions = simulate_email_activities(valid_leads)
    
    df_activities.to_csv("data/raw/email_activities.csv", index=False)
    df_ab_test.to_csv("data/raw/ab_testing.csv", index=False)
    df_conversions.to_csv("data/raw/conversions.csv", index=False)

    print(f"      Saved email activities: {len(df_activities)} records -> data/raw/email_activities.csv")
    print(f"      Saved A/B test experiments: {len(df_ab_test)} tests -> data/raw/ab_testing.csv")
    print(f"      Saved conversions: {len(df_conversions)} records -> data/raw/conversions.csv")
    print("[4/4] Data generation completed successfully!\n")


if __name__ == "__main__":
    run_pipeline()

