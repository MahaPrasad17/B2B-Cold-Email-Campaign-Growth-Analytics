"""
B2B Cold Email Campaign & Growth Analytics Platform
Module: src/deliverability.py

Dedicated Email Deliverability, Domain Health & Inbox Placement Engine.
Analyzes delivery rates, bounce trends, domain-level health, suppression lists,
and provides educational guidance on SPF, DKIM, DMARC, and sender reputation.

Disclaimer: Measures are computed on simulated campaign data. Real-world deliverability
requires live mailbox testing, seed lists, and ESP webhook telemetry.
"""

import os
from typing import Dict, Any
import pandas as pd


# Deliverability Educational Knowledge Base
DELIVERABILITY_FRAMEWORK = {
    "SPF": {
        "Name": "Sender Policy Framework (SPF)",
        "Type": "DNS TXT Record",
        "Purpose": "Specifies which mail servers (IP addresses) are authorized to send email on behalf of your domain.",
        "Example": "v=spf1 include:_spf.google.com include:sendgrid.net ~all",
        "Risk_If_Missing": "Receiving mail servers flag emails as potential spoofing/phishing, routing them straight to Spam."
    },
    "DKIM": {
        "Name": "DomainKeys Identified Mail (DKIM)",
        "Type": "DNS TXT Record (Public Key Cryptography)",
        "Purpose": "Cryptographically signs the email header and body to ensure email has not been tampered with in transit.",
        "Example": "k=rsa; p=MIGfMA0GCSqGSIb3DQEBAQUAA4GNADCBiQ...",
        "Risk_If_Missing": "Cannot verify authenticity; high likelihood of junk filtering by Google Workspace and Outlook 365."
    },
    "DMARC": {
        "Name": "Domain-based Message Authentication, Reporting & Conformance (DMARC)",
        "Type": "DNS Policy Record",
        "Purpose": "Instructs receiving servers what to do if SPF or DKIM fails (none, quarantine, or reject) and sends XML reports.",
        "Example": "v=DMARC1; p=quarantine; rua=mailto:dmarc-reports@goodspace.ai; pct=100",
        "Risk_If_Missing": "Vulnerable to domain impersonation and fails mandatory 2024+ Yahoo/Google bulk sender requirements."
    },
    "Custom_Tracking_Domain": {
        "Name": "Custom Domain Tracking (CNAME)",
        "Type": "CNAME Record",
        "Purpose": "Replaces third-party ESP tracking links (e.g., link.esp.com) with a branded subdomain (e.g., track.goodspace.ai).",
        "Example": "track.goodspace.ai CNAME mailgun.org",
        "Risk_If_Missing": "Shared ESP domains shared with spammers can cause your emails to be blacklisted."
    }
}


class DeliverabilityAuditor:
    """Audits email deliverability, bounces, and domain health."""

    def __init__(
        self,
        activities_path: str = "data/raw/email_activities.csv",
        leads_path: str = "data/processed/clean_leads.csv"
    ):
        self.df_activities = pd.read_csv(activities_path)
        self.df_leads = pd.read_csv(leads_path)

        # Merge email and company attributes
        self.df_merged = pd.merge(
            self.df_activities,
            self.df_leads[["Lead_ID", "Business_Email", "Company_Name", "Company_Industry"]],
            on="Lead_ID",
            how="left"
        )
        self.df_merged["Email_Domain"] = self.df_merged["Business_Email"].astype(str).apply(
            lambda x: x.split("@")[1] if "@" in x else "unknown.com"
        )

    def generate_deliverability_report(self) -> Dict[str, Any]:
        """Calculates global deliverability metrics."""
        total_sent = len(self.df_activities)
        total_delivered = int(self.df_activities["Delivery_Status"].sum())
        total_bounces = int(self.df_activities["Bounce_Status"].sum())
        total_unsub = int(self.df_activities["Unsubscribe_Status"].sum())

        delivery_rate = round(total_delivered / total_sent * 100, 2) if total_sent > 0 else 0.0
        bounce_rate = round(total_bounces / total_sent * 100, 2) if total_sent > 0 else 0.0
        unsubscribe_rate = round(total_unsub / total_delivered * 100, 2) if total_delivered > 0 else 0.0

        # Health status evaluation
        if bounce_rate <= 1.5 and delivery_rate >= 98.0:
            health_status = "Excellent (Green)"
            health_score = 96
        elif bounce_rate <= 3.0:
            health_status = "Good / Monitor (Yellow)"
            health_score = 84
        else:
            health_status = "Critical Risk (Red - Pause Campaigns)"
            health_score = 62

        return {
            "Total_Sent": total_sent,
            "Total_Delivered": total_delivered,
            "Total_Bounces": total_bounces,
            "Total_Unsubscribes": total_unsub,
            "Delivery_Rate": delivery_rate,
            "Bounce_Rate": bounce_rate,
            "Unsubscribe_Rate": unsubscribe_rate,
            "Domain_Health_Score": health_score,
            "Domain_Health_Status": health_status
        }

    def analyze_domain_level_health(self, min_emails: int = 5) -> pd.DataFrame:
        """
        Groups deliverability performance by recipient corporate domain
        to identify domain-level blocking or spam filtering.
        """
        domain_grp = self.df_merged.groupby("Email_Domain").agg(
            Sent=("Email_ID", "count"),
            Delivered=("Delivery_Status", "sum"),
            Bounced=("Bounce_Status", "sum"),
            Unsubscribes=("Unsubscribe_Status", "sum")
        ).reset_index()

        domain_grp = domain_grp[domain_grp["Sent"] >= min_emails].copy()
        domain_grp["Delivery_Rate"] = (domain_grp["Delivered"] / domain_grp["Sent"] * 100).round(2)
        domain_grp["Bounce_Rate"] = (domain_grp["Bounced"] / domain_grp["Sent"] * 100).round(2)

        def assign_domain_status(r):
            if r["Bounce_Rate"] > 5.0:
                return "High Bounce (Investigate Domain)"
            elif r["Bounce_Rate"] > 2.0:
                return "Moderate Risk"
            return "Healthy"

        domain_grp["Domain_Reputation_Risk"] = domain_grp.apply(assign_domain_status, axis=1)
        return domain_grp.sort_values("Bounce_Rate", ascending=False)

    def export_suppression_list(self, output_path: str = "data/processed/suppression_list.csv") -> pd.DataFrame:
        """
        Extracts all leads that resulted in hard bounces or unsubscribes
        to generate an automated compliance suppression list.
        """
        bounced_lead_ids = set(self.df_activities[self.df_activities["Bounce_Status"] == 1]["Lead_ID"])
        unsub_lead_ids = set(self.df_activities[self.df_activities["Unsubscribe_Status"] == 1]["Lead_ID"])

        suppressed_ids = bounced_lead_ids.union(unsub_lead_ids)

        supp_leads = self.df_leads[self.df_leads["Lead_ID"].isin(suppressed_ids)].copy()
        
        def assign_reason(lid):
            if lid in bounced_lead_ids and lid in unsub_lead_ids:
                return "Bounced and Unsubscribed"
            elif lid in bounced_lead_ids:
                return "Hard Bounce (Delivery Failure)"
            else:
                return "Recipient Opt-Out (Unsubscribed)"

        supp_leads["Suppression_Reason"] = supp_leads["Lead_ID"].apply(assign_reason)
        supp_leads["Suppression_Date"] = "2026-09-10"

        export_cols = [
            "Lead_ID", "First_Name", "Last_Name", "Company_Name",
            "Business_Email", "Suppression_Reason", "Suppression_Date"
        ]
        export_df = supp_leads[export_cols]

        os.makedirs(os.path.dirname(output_path), exist_ok=True)
        export_df.to_csv(output_path, index=False)
        print(f"[Deliverability Engine] Exported {len(export_df)} leads to suppression list -> {output_path}")
        return export_df


if __name__ == "__main__":
    auditor = DeliverabilityAuditor()
    report = auditor.generate_deliverability_report()
    print("[Email Deliverability Audit]")
    print(f"  * Delivery Rate   : {report['Delivery_Rate']}%")
    print(f"  * Bounce Rate     : {report['Bounce_Rate']}% (Benchmark: <= 2.0%)")
    print(f"  * Unsubscribe Rate: {report['Unsubscribe_Rate']}% (Benchmark: <= 0.5%)")
    print(f"  * Health Score    : {report['Domain_Health_Score']}/100 ({report['Domain_Health_Status']})")

    supp = auditor.export_suppression_list()

