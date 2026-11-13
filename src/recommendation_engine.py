"""
B2B Cold Email Campaign & Growth Analytics Platform
Module: src/recommendation_engine.py

Rule-Based Marketing Recommendation Engine.
Analyzes computed campaign KPIs, A/B test significance, deliverability trends,
and audience segments against B2B industry benchmarks to generate actionable,
data-backed growth optimization recommendations.
"""

import os
import sys
from typing import List, Dict, Any

# Ensure parent directory is in sys.path for direct execution
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

import pandas as pd
from src.analytics import GrowthMarketingAnalytics
from src.ab_testing import analyze_ab_tests
from src.deliverability import DeliverabilityAuditor


class GrowthRecommendationEngine:
    """Algorithmic growth marketer recommendation generator."""

    def __init__(self):
        self.analytics = GrowthMarketingAnalytics()
        self.kpis = self.analytics.get_overall_executive_kpis()
        self.camp_df = self.analytics.get_campaign_performance_summary()
        self.ind_df = self.analytics.get_industry_performance()
        self.src_df = self.analytics.get_lead_source_performance()
        self.step_df = self.analytics.get_sequence_step_performance()
        self.ab_df = analyze_ab_tests()
        self.deliverability = DeliverabilityAuditor().generate_deliverability_report()

    def generate_recommendations(self) -> List[Dict[str, Any]]:
        """
        Evaluates data points and applies deterministic growth marketing heuristics.
        """
        recs = []

        # 1. Deliverability & Bounce Rate Rules
        bounce_rate = self.deliverability["Bounce_Rate"]
        if bounce_rate > 2.0:
            recs.append({
                "Category": "Deliverability & Technical Setup",
                "Priority": "HIGH",
                "Observed_Metric": f"Bounce Rate = {bounce_rate}% (Exceeds 2.0% threshold)",
                "Finding": "Email bounce rate is elevated above safe ISP limits. This threatens domain reputation.",
                "Actionable_Recommendation": (
                    "Immediately enforce real-time SMTP handshake verification (e.g., ZeroBounce/NeverBounce) "
                    "before importing leads into outbound sequencing. Suppress all invalid corporate domains."
                ),
                "Expected_Impact": "Protects sender score, keeps primary domain off Spamhaus/Barracuda blacklists."
            })
        else:
            recs.append({
                "Category": "Deliverability & Technical Setup",
                "Priority": "LOW",
                "Observed_Metric": f"Bounce Rate = {bounce_rate}% (Healthy <= 2.0%)",
                "Finding": "Bounce rate is within industry best practice range.",
                "Actionable_Recommendation": (
                    "Maintain current hygiene standards. Ensure suppression list of 250+ bounced contacts is synced "
                    "to CRM to prevent accidental re-engagement."
                ),
                "Expected_Impact": "Sustains 98%+ delivery inbox placement."
            })

        # 2. Campaign Reply Rate & Underperformance Rules
        for _, camp in self.camp_df.iterrows():
            cid = camp["Campaign_ID"]
            cname = camp["Campaign_Name"]
            reply_rate = camp["Reply_Rate"]
            open_rate = camp["Open_Rate"]

            if reply_rate < 3.0:
                recs.append({
                    "Category": "Campaign Performance",
                    "Priority": "HIGH",
                    "Observed_Metric": f"{cname} Reply Rate = {reply_rate}% (Benchmark: >= 3.5%)",
                    "Finding": f"Campaign {cid} is underperforming in response generation despite {open_rate}% open rate.",
                    "Actionable_Recommendation": (
                        f"Refactor email body copy for '{cname}'. Replace generic pitch with low-friction permission-based CTA "
                        f"(e.g., 'Open to a 2-min interactive video?') and shorten body text under 80 words."
                    ),
                    "Expected_Impact": "Expected 25-40% increase in reply volume."
                })

        # 3. A/B Testing Winning Variations Rollout
        for _, ab in self.ab_df.iterrows():
            cid = ab["Campaign_ID"]
            var_name = ab["Test_Variable"]
            winner = ab["Reply_Winner"]
            lift = ab["Reply_Lift_Pct"]
            pval = ab["Reply_P_Value"]

            if "Variant" in winner:
                win_desc = ab["Variant_B_Description"] if winner == "Variant B" else ab["Variant_A_Description"]
                recs.append({
                    "Category": "A/B Testing Optimization",
                    "Priority": "HIGH",
                    "Observed_Metric": f"{cid} {var_name}: {winner} won with {lift:+.1f}% lift (p={pval:.4f})",
                    "Finding": f"Statistical hypothesis test confirmed {winner} significantly outperforms the alternative.",
                    "Actionable_Recommendation": (
                        f"Promote winning variation to 100% traffic across {cid}: '{win_desc}'. "
                        f"Deprecate losing variation immediately."
                    ),
                    "Expected_Impact": f"Locks in {abs(lift):.1f}% ongoing response lift across remaining sequence sends."
                })

        # 4. Audience & Industry Segmentation Rules
        top_industry = self.ind_df.iloc[0]
        bottom_industry = self.ind_df.iloc[-1]
        
        recs.append({
            "Category": "Audience Prioritization",
            "Priority": "MEDIUM",
            "Observed_Metric": f"Top Industry: {top_industry['Industry']} (Reply Rate: {top_industry['Reply_Rate']}%, Positive: {top_industry['Positive_Reply_Rate']}%)",
            "Finding": f"{top_industry['Industry']} demonstrates the strongest market resonance and intent for GoodSpace AI.",
            "Actionable_Recommendation": (
                f"Allocate 60% of Q3 outbound SDR capacity and prospecting budget to {top_industry['Industry']}. "
                f"Develop industry-tailored ROI calculator and customer proof points."
            ),
            "Expected_Impact": "Maximizes pipeline generation per 1,000 emails sent."
        })

        if bottom_industry["Reply_Rate"] < 2.5:
            recs.append({
                "Category": "Audience Prioritization",
                "Priority": "MEDIUM",
                "Observed_Metric": f"Lowest Industry: {bottom_industry['Industry']} (Reply Rate: {bottom_industry['Reply_Rate']}%)",
                "Finding": f"Underwhelming engagement from {bottom_industry['Industry']}.",
                "Actionable_Recommendation": (
                    f"Pause outbound volume to {bottom_industry['Industry']} temporarily. Conduct 5 customer discovery interviews "
                    f"with HR leaders in this sector to identify tailored pain points before relaunching."
                ),
                "Expected_Impact": "Prevents domain fatigue and reallocates resources to higher ROI segments."
            })

        # 5. Lead Source Performance
        top_src = self.src_df.iloc[0]
        recs.append({
            "Category": "Channel Allocation",
            "Priority": "MEDIUM",
            "Observed_Metric": f"Highest Quality Source: {top_src['Lead_Source']} (Positive Reply Rate: {top_src['Positive_Reply_Rate']}%)",
            "Finding": f"{top_src['Lead_Source']} produces the highest intent prospects.",
            "Actionable_Recommendation": (
                f"Double prospecting list size from {top_src['Lead_Source']}. Build automated lead enrichment workflows "
                f"to ingest newly active prospects within 24 hours of intent signals."
            ),
            "Expected_Impact": "Accelerates sales cycle and conversion from lead to demo."
        })

        # 6. Sequence Follow-up Optimization
        if len(self.step_df) >= 2:
            step2 = self.step_df[self.step_df["Sequence_Step"].str.contains("Step 2")]
            if len(step2) > 0 and step2["Reply_Rate"].values[0] >= 3.0:
                recs.append({
                    "Category": "Sequence Architecture",
                    "Priority": "LOW",
                    "Observed_Metric": f"Follow-up Step 2 Reply Rate: {step2['Reply_Rate'].values[0]}%",
                    "Finding": "First follow-up email generates substantial reply volume, proving multi-touch cadence is essential.",
                    "Actionable_Recommendation": (
                        "Test shortening follow-up gap from 3 days to 2 business days for prospects who opened Step 1, "
                        "capitalizing on immediate brand recall while the problem is fresh."
                    ),
                    "Expected_Impact": "Shortens average time-to-first-response by 24 hours."
                })

        return recs


def export_recommendations(output_path: str = "data/processed/growth_recommendations.csv") -> pd.DataFrame:
    """Exports structured recommendations to CSV and prints summary."""
    engine = GrowthRecommendationEngine()
    recs = engine.generate_recommendations()
    df_recs = pd.DataFrame(recs)
    df_recs.to_csv(output_path, index=False)
    print(f"[Recommendation Engine] Generated {len(df_recs)} data-backed growth recommendations.")
    print(f"                        Saved -> {output_path}")
    return df_recs


if __name__ == "__main__":
    export_recommendations()
