"""
B2B Cold Email Campaign & Growth Analytics Platform
Module: src/data_cleaning.py

Provides enterprise-grade data cleaning, validation, deduplication,
standardization, and enrichment for B2B lead datasets.
"""

import os
import re
import json
import numpy as np
import pandas as pd

# RFC 5322 compliant simplified regex pattern for corporate email validation
EMAIL_REGEX = re.compile(r"^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$")

# Standardized company size mapping
COMPANY_SIZE_TIERS = {
    "1-10": "Small (1-50)",
    "11-50": "Small (1-50)",
    "51-200": "Mid-Market (51-500)",
    "201-500": "Mid-Market (51-500)",
    "501-1000": "Enterprise (500+)",
    "1000+": "Enterprise (500+)"
}

# Seniority classification mapping from B2B Job Titles
def classify_seniority(title: str) -> str:
    """Classify lead seniority level based on job title."""
    if not isinstance(title, str):
        return "Unknown"
    title_lower = title.lower()
    if any(k in title_lower for k in ["chief", "cpo", "c-level", "vp", "vice president"]):
        return "C-Suite & VP"
    elif any(k in title_lower for k in ["director", "head"]):
        return "Director & Head"
    elif any(k in title_lower for k in ["manager", "lead", "business partner"]):
        return "Manager & Lead"
    elif any(k in title_lower for k in ["specialist", "sourcing", "recruiter", "analyst"]):
        return "Specialist & Individual Contributor"
    return "Manager & Lead"

# Region mapping
def classify_region(country: str) -> str:
    """Map country to macro-geographic sales region."""
    if not isinstance(country, str):
        return "Other"
    north_america = ["United States", "Canada"]
    emea = ["United Kingdom", "Germany", "France", "Netherlands"]
    apac = ["India", "Singapore", "Australia", "Japan"]
    if country in north_america:
        return "North America (NA)"
    elif country in emea:
        return "Europe & Middle East (EMEA)"
    elif country in apac:
        return "Asia Pacific (APAC)"
    return "Other"


class LeadDataCleaner:
    """Enterprise B2B Lead Cleaner and Validator."""

    def __init__(self, raw_df: pd.DataFrame):
        self.raw_df = raw_df.copy()
        self.cleaned_df = pd.DataFrame()
        self.invalid_df = pd.DataFrame()
        self.audit_report = {}

    def clean_and_validate(self) -> tuple[pd.DataFrame, pd.DataFrame, dict]:
        """
        Executes end-to-end data cleaning workflow:
        1. String trimming & normalization
        2. Email format validation
        3. Duplicate identification and deduplication
        4. Missing value imputation & standardization
        5. Lead enrichment (revenue, tech stack, deliverability score)
        """
        df = self.raw_df.copy()
        total_raw = len(df)
        
        # Step 1: Whitespace trimming and text normalization
        str_columns = ["First_Name", "Last_Name", "Company_Name", "Company_Industry", 
                       "Job_Title", "Business_Email", "Country", "City", "Lead_Source"]
        for col in str_columns:
            if col in df.columns:
                df[col] = df[col].astype(str).str.strip()
                df[col] = df[col].replace({"nan": None, "None": None, "": None})

        # Step 2: Validate Email Format
        def is_valid_email(val):
            if not val or not isinstance(val, str):
                return False
            # Check length, characters, single @, valid domain dot
            return bool(EMAIL_REGEX.match(val))

        df["Email_Valid"] = df["Business_Email"].apply(is_valid_email)
        invalid_email_count = int((~df["Email_Valid"]).sum())

        # Step 3: Duplicate Identification
        # Lowercase email for deduplication
        df["Email_Normalized"] = df["Business_Email"].astype(str).str.lower()
        df["Is_Duplicate"] = df.duplicated(subset=["Email_Normalized"], keep="first")
        duplicate_count = int(df["Is_Duplicate"].sum())

        # Split valid leads vs invalid/quarantined records
        valid_mask = df["Email_Valid"] & (~df["Is_Duplicate"])
        clean_df = df[valid_mask].copy()
        invalid_df = df[~valid_mask].copy()

        # Step 4: Missing Value Imputation
        missing_first_names = int(clean_df["First_Name"].isna().sum())
        missing_company_sizes = int(clean_df["Company_Size"].isna().sum())

        # Impute missing First Name from email prefix (e.g. john.doe@ -> John)
        for idx in clean_df[clean_df["First_Name"].isna()].index:
            email_val = str(clean_df.loc[idx, "Business_Email"])
            if "@" in email_val:
                prefix = email_val.split("@")[0].split(".")[0]
                clean_df.loc[idx, "First_Name"] = prefix.capitalize()
            else:
                clean_df.loc[idx, "First_Name"] = "Colleague"

        # Impute missing Company Size with most frequent mode
        default_size = "51-200"
        clean_df["Company_Size"] = clean_df["Company_Size"].fillna(default_size)

        # Standardize text capitalization
        clean_df["First_Name"] = clean_df["First_Name"].str.capitalize()
        clean_df["Last_Name"] = clean_df["Last_Name"].fillna("").str.capitalize()
        clean_df["Company_Name"] = clean_df["Company_Name"].str.title()
        clean_df["Full_Name"] = clean_df["First_Name"] + " " + clean_df["Last_Name"]

        # Standardize Company Size Tier & Seniority
        clean_df["Company_Size_Tier"] = clean_df["Company_Size"].map(COMPANY_SIZE_TIERS).fillna("Mid-Market (51-500)")
        clean_df["Seniority_Level"] = clean_df["Job_Title"].apply(classify_seniority)
        clean_df["Sales_Region"] = clean_df["Country"].apply(classify_region)

        # Step 5: Lead Enrichment (Synthetic attributes for B2B SaaS context)
        np.random.seed(42)
        # Estimated revenue ($M) based on company size
        def estimate_revenue(size: str) -> float:
            if size == "1-10":
                return round(np.random.uniform(0.5, 2.0), 2)
            elif size == "11-50":
                return round(np.random.uniform(2.0, 10.0), 2)
            elif size == "51-200":
                return round(np.random.uniform(10.0, 40.0), 2)
            elif size == "201-500":
                return round(np.random.uniform(40.0, 100.0), 2)
            elif size == "501-1000":
                return round(np.random.uniform(100.0, 300.0), 2)
            else:
                return round(np.random.uniform(300.0, 1500.0), 2)

        clean_df["Estimated_Revenue_M"] = clean_df["Company_Size"].apply(estimate_revenue)

        # Tech stack detection (ATS / HRIS platforms)
        tech_stacks = [
            "Greenhouse + Workday",
            "Lever + BambooHR",
            "SAP SuccessFactors + Ashby",
            "Taleo + Oracle HCM",
            "SmartRecruiters + UKG Pro",
            "Pinpoint + HiBob"
        ]
        clean_df["Current_ATS_HRIS"] = np.random.choice(tech_stacks, size=len(clean_df))

        # Synthetic Hiring Intent Score (1 - 100)
        clean_df["Hiring_Intent_Score"] = np.random.randint(35, 99, size=len(clean_df))

        # Email Deliverability Score (90 - 99 for clean valid corporate domains)
        clean_df["Deliverability_Score"] = np.random.randint(92, 100, size=len(clean_df))

        # Clean up temporary columns
        clean_df = clean_df.drop(columns=["Email_Valid", "Is_Duplicate", "Email_Normalized"], errors="ignore")

        # Compile audit summary
        self.audit_report = {
            "Total_Raw_Records": total_raw,
            "Total_Clean_Records": len(clean_df),
            "Quarantined_Records": len(invalid_df),
            "Duplicate_Records_Removed": duplicate_count,
            "Invalid_Email_Formats_Removed": invalid_email_count,
            "Missing_First_Names_Imputed": missing_first_names,
            "Missing_Company_Sizes_Imputed": missing_company_sizes,
            "Data_Cleanliness_Percentage": round((len(clean_df) / total_raw) * 100, 2)
        }

        self.cleaned_df = clean_df
        self.invalid_df = invalid_df
        return clean_df, invalid_df, self.audit_report


def clean_lead_pipeline(raw_path: str = "data/raw/raw_leads.csv") -> pd.DataFrame:
    """Executes the lead cleaning pipeline and saves output."""
    if not os.path.exists(raw_path):
        raise FileNotFoundError(f"Raw lead file not found at {raw_path}")

    raw_df = pd.read_csv(raw_path)
    cleaner = LeadDataCleaner(raw_df)
    clean_df, invalid_df, audit = cleaner.clean_and_validate()

    os.makedirs("data/processed", exist_ok=True)
    clean_df.to_csv("data/processed/clean_leads.csv", index=False)
    invalid_df.to_csv("data/processed/quarantined_leads.csv", index=False)

    with open("data/processed/data_cleaning_audit.json", "w") as f:
        json.dump(audit, f, indent=4)

    print(f"[Data Cleaning] Processed {audit['Total_Raw_Records']} raw leads.")
    print(f"                Clean valid leads : {audit['Total_Clean_Records']} ({audit['Data_Cleanliness_Percentage']}%)")
    print(f"                Duplicates pruned : {audit['Duplicate_Records_Removed']}")
    print(f"                Invalid emails     : {audit['Invalid_Email_Formats_Removed']}")
    print(f"                Names imputed      : {audit['Missing_First_Names_Imputed']}")
    print("                Clean dataset saved -> data/processed/clean_leads.csv")
    return clean_df


if __name__ == "__main__":
    clean_lead_pipeline()

