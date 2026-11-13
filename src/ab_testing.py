"""
B2B Cold Email Campaign & Growth Analytics Platform
Module: src/ab_testing.py

Enterprise A/B Testing & Hypothesis Testing Engine for B2B Growth Marketing.
Implements Two-Proportion Z-Tests, 95% Confidence Intervals, Relative Lift,
Statistical Power / Sample Size Sufficiency, and Evidence-Based Decision Rules.
Uses pure Python standard library statistics for maximum portability and zero DLL dependency.
"""

import math
import statistics
from typing import Dict, Any, List
import pandas as pd

# Standard Normal Distribution helper from standard library
_NORMAL_DIST = statistics.NormalDist(mu=0.0, sigma=1.0)


def calculate_two_proportion_z_test(
    count_a: int,
    n_a: int,
    count_b: int,
    n_b: int,
    alpha: float = 0.05,
    min_success_threshold: int = 15
) -> Dict[str, Any]:
    """
    Computes rigorous statistical comparison between two conversion proportions.
    
    Parameters:
      count_a: Successes in control (Variant A)
      n_a: Total sample size in control (Variant A)
      count_b: Successes in test (Variant B)
      n_b: Total sample size in test (Variant B)
      alpha: Significance level (default 0.05 for 95% confidence)
      min_success_threshold: Minimum successes required to ensure normal approximation validity
    
    Returns:
      Dictionary of statistical metrics including p-value, z-score, confidence interval,
      observed lift, sample size sufficiency flag, and winning conclusion.
    """
    if n_a <= 0 or n_b <= 0:
        return {
            "Rate_A": 0.0, "Rate_B": 0.0, "Abs_Diff": 0.0, "Relative_Lift_Pct": 0.0,
            "Z_Score": 0.0, "P_Value": 1.0, "Significant": False,
            "Sample_Size_Sufficient": False, "Winner": "Insufficient Data",
            "CI_Lower": 0.0, "CI_Upper": 0.0, "Verdict_Description": "No data available."
        }

    rate_a = count_a / n_a
    rate_b = count_b / n_b
    abs_diff = rate_b - rate_a
    rel_lift = (abs_diff / rate_a * 100.0) if rate_a > 0 else 0.0

    # Check sample size sufficiency (rule of thumb: count >= threshold and n - count >= threshold)
    sample_sufficient = (
        count_a >= min_success_threshold and
        count_b >= min_success_threshold and
        (n_a - count_a) >= min_success_threshold and
        (n_b - count_b) >= min_success_threshold
    )

    # Pooled proportion for standard error under null hypothesis
    p_pool = (count_a + count_b) / (n_a + n_b)
    
    if p_pool == 0 or p_pool == 1:
        z_score = 0.0
        p_val = 1.0
        se_pool = 0.0
    else:
        se_pool = math.sqrt(p_pool * (1 - p_pool) * (1 / n_a + 1 / n_b))
        z_score = (rate_b - rate_a) / se_pool if se_pool > 0 else 0.0
        # Two-tailed p-value
        p_val = 2.0 * (1.0 - _NORMAL_DIST.cdf(abs(z_score)))

    # Unpooled Standard Error for Confidence Interval of difference (rate_b - rate_a)
    se_diff = math.sqrt((rate_a * (1 - rate_a) / n_a) + (rate_b * (1 - rate_b) / n_b))
    z_crit = _NORMAL_DIST.inv_cdf(1.0 - alpha / 2.0)  # ~1.96 for 95% CI
    ci_lower = abs_diff - z_crit * se_diff
    ci_upper = abs_diff + z_crit * se_diff

    # Determine significance and winner
    is_significant = (p_val < alpha) and sample_sufficient

    if not sample_sufficient:
        winner = "Inconclusive (Underpowered Sample)"
        verdict_desc = (
            f"Sample size insufficient (success counts: A={count_a}, B={count_b}; threshold={min_success_threshold}). "
            f"Continue running test to reach statistical power."
        )
    elif is_significant:
        if rate_b > rate_a:
            winner = "Variant B"
            verdict_desc = (
                f"Variant B is the statistically significant winner (p={p_val:.4f} < {alpha}, "
                f"Relative Lift = {rel_lift:+.2f}%, 95% CI: [{ci_lower*100:.2f}%, {ci_upper*100:.2f}%])."
            )
        else:
            winner = "Variant A"
            verdict_desc = (
                f"Variant A (Control) is the statistically significant winner (p={p_val:.4f} < {alpha}, "
                f"Relative Lift = {rel_lift:+.2f}%, 95% CI: [{ci_lower*100:.2f}%, {ci_upper*100:.2f}%])."
            )
    else:
        winner = "No Significant Difference"
        verdict_desc = (
            f"No statistically significant difference observed (p={p_val:.4f} >= {alpha}). "
            f"Observed difference is likely due to random variance."
        )

    return {
        "Rate_A": round(rate_a * 100, 2),
        "Rate_B": round(rate_b * 100, 2),
        "Abs_Diff": round(abs_diff * 100, 2),
        "Relative_Lift_Pct": round(rel_lift, 2),
        "Z_Score": round(z_score, 4),
        "P_Value": round(p_val, 4),
        "Significant": is_significant,
        "Sample_Size_Sufficient": sample_sufficient,
        "CI_Lower": round(ci_lower * 100, 2),
        "CI_Upper": round(ci_upper * 100, 2),
        "Winner": winner,
        "Verdict_Description": verdict_desc
    }


def analyze_ab_tests(ab_csv_path: str = "data/raw/ab_testing.csv") -> pd.DataFrame:
    """
    Runs multi-metric A/B testing evaluation across all campaigns and test variables.
    Analyzes:
      1. Open Rate (Top of Funnel engagement)
      2. Reply Rate (Mid of Funnel engagement)
      3. Positive Reply Rate (High-intent engagement)
      4. Click Rate (Content engagement)
      5. Conversion Rate (Bottom of funnel pipeline opportunity)
    """
    df_ab = pd.read_csv(ab_csv_path)
    analysis_results = []

    for _, row in df_ab.iterrows():
        cid = row["Campaign_ID"]
        test_var = row["Test_Variable"]
        n_a = int(row["Emails_Delivered_A"])
        n_b = int(row["Emails_Delivered_B"])

        # 1. Open Rate Evaluation
        open_stats = calculate_two_proportion_z_test(
            count_a=int(row["Opens_A"]),
            n_a=n_a,
            count_b=int(row["Opens_B"]),
            n_b=n_b
        )

        # 2. Reply Rate Evaluation
        reply_stats = calculate_two_proportion_z_test(
            count_a=int(row["Replies_A"]),
            n_a=n_a,
            count_b=int(row["Replies_B"]),
            n_b=n_b
        )

        # 3. Positive Reply Rate Evaluation
        pos_stats = calculate_two_proportion_z_test(
            count_a=int(row.get("Positive_Replies_A", 0)),
            n_a=n_a,
            count_b=int(row.get("Positive_Replies_B", 0)),
            n_b=n_b
        )

        # 4. Conversion Rate Evaluation
        conv_stats = calculate_two_proportion_z_test(
            count_a=int(row["Conversions_A"]),
            n_a=n_a,
            count_b=int(row["Conversions_B"]),
            n_b=n_b,
            min_success_threshold=10  # conversions are lower volume
        )

        analysis_results.append({
            "Test_ID": row["Test_ID"],
            "Campaign_ID": cid,
            "Test_Variable": test_var,
            "Variant_A_Description": row["Variant_A"],
            "Variant_B_Description": row["Variant_B"],
            "Delivered_A": n_a,
            "Delivered_B": n_b,
            # Open rate
            "Open_Rate_A": open_stats["Rate_A"],
            "Open_Rate_B": open_stats["Rate_B"],
            "Open_Lift_Pct": open_stats["Relative_Lift_Pct"],
            "Open_P_Value": open_stats["P_Value"],
            "Open_Winner": open_stats["Winner"],
            # Reply rate
            "Reply_Rate_A": reply_stats["Rate_A"],
            "Reply_Rate_B": reply_stats["Rate_B"],
            "Reply_Lift_Pct": reply_stats["Relative_Lift_Pct"],
            "Reply_P_Value": reply_stats["P_Value"],
            "Reply_Winner": reply_stats["Winner"],
            # Positive Reply rate
            "Positive_Rate_A": pos_stats["Rate_A"],
            "Positive_Rate_B": pos_stats["Rate_B"],
            "Positive_Lift_Pct": pos_stats["Relative_Lift_Pct"],
            "Positive_P_Value": pos_stats["P_Value"],
            "Positive_Winner": pos_stats["Winner"],
            # Conversion rate
            "Conversion_Rate_A": conv_stats["Rate_A"],
            "Conversion_Rate_B": conv_stats["Rate_B"],
            "Conversion_Lift_Pct": conv_stats["Relative_Lift_Pct"],
            "Conversion_P_Value": conv_stats["P_Value"],
            "Conversion_Winner": conv_stats["Winner"],
            "Primary_Winning_Variant": reply_stats["Winner"],
            "Executive_Summary": reply_stats["Verdict_Description"]
        })

    df_out = pd.DataFrame(analysis_results)
    df_out.to_csv("data/processed/ab_test_analysis_results.csv", index=False)
    return df_out


if __name__ == "__main__":
    results = analyze_ab_tests()
    print("[A/B Testing Engine] Evaluated Experiments Across All 4 Campaigns:\n")
    for _, r in results.iterrows():
        print(f"Test: {r['Test_ID']} ({r['Campaign_ID']}) | Variable: {r['Test_Variable']}")
        print(f"  * Control (A): {r['Variant_A_Description']}")
        print(f"  * Test    (B): {r['Variant_B_Description']}")
        print(f"  * Open Rate  : A={r['Open_Rate_A']}% vs B={r['Open_Rate_B']}% (Lift: {r['Open_Lift_Pct']:+}%, p={r['Open_P_Value']}, Winner: {r['Open_Winner']})")
        print(f"  * Reply Rate : A={r['Reply_Rate_A']}% vs B={r['Reply_Rate_B']}% (Lift: {r['Reply_Lift_Pct']:+}%, p={r['Reply_P_Value']}, Winner: {r['Reply_Winner']})")
        print(f"  * Conclusion : {r['Executive_Summary']}\n")
