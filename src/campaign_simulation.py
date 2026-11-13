"""
B2B Cold Email Campaign & Growth Analytics Platform
Module: src/campaign_simulation.py

Campaign management engine and cold email copywriting sequences
for fictional AI recruitment company GoodSpace AI.

Disclaimer: All campaign data, metrics, and activities are synthetic simulations
designed for portfolio and growth analytics evaluation.
"""

from typing import Dict, List, Any


# Full sequence copy templates for GoodSpace AI campaigns
CAMPAIGN_COPY_CATALOG: Dict[str, Dict[str, Any]] = {
    "CMP-001": {
        "Campaign_ID": "CMP-001",
        "Campaign_Name": "IT Tech Hiring Velocity Q1",
        "Target_Industry": "Information Technology",
        "Target_Audience": "VP of Talent Acquisition, Head of Engineering Recruitment, Technical Sourcing Leads",
        "Objective": "Engage IT talent acquisition leaders to automate preliminary technical screening and cut time-to-hire by 60% with GoodSpace AI.",
        "Sequence": {
            "Step_1_Variant_A": {
                "Step_Number": 1,
                "Timing": "Day 0 (Initial Outreach)",
                "Variant_Label": "Variant A - Direct Benefit",
                "Subject": "Reduce technical screening time by 60% at {{Company_Name}}",
                "Body": (
                    "Hi {{First_Name}},\n\n"
                    "Most tech recruitment leaders I speak with tell me their engineering managers spend "
                    "15+ hours weekly screening candidate resumes that don't pass the first technical screen.\n\n"
                    "At GoodSpace AI, our autonomous screening agents conduct interactive 15-minute "
                    "coding & architecture pre-assessments, delivering pre-vetted top 5% shortlists to your inbox.\n\n"
                    "We recently helped an enterprise software team cut their time-to-hire from 38 days to 14 days.\n\n"
                    "Would you be open to a 7-minute introductory chat this Thursday to see how this works for {{Company_Name}}?\n\n"
                    "Best regards,\n"
                    "Alex Rivera\n"
                    "Growth Marketing & Solutions Lead | GoodSpace AI"
                ),
                "CTA": "Would you be open to a 7-minute introductory chat this Thursday?"
            },
            "Step_1_Variant_B": {
                "Step_Number": 1,
                "Timing": "Day 0 (Initial Outreach)",
                "Variant_Label": "Variant B - Curiosity & Problem Question",
                "Subject": "Quick question regarding your Q3 tech hiring targets, {{First_Name}}",
                "Body": (
                    "Hi {{First_Name}},\n\n"
                    "Saw that {{Company_Name}} is currently scaling its technical and engineering team.\n\n"
                    "How is your recruiting team currently filtering through high volumes of applicants without "
                    "pulling senior engineers into first-round screening calls?\n\n"
                    "GoodSpace AI automates preliminary technical evaluations via adaptive conversational assessments—ranking "
                    "candidates on real problem-solving ability before human interviews.\n\n"
                    "Open to seeing a 2-minute interactive demo video of how it screens software engineers?\n\n"
                    "Best regards,\n"
                    "Alex Rivera\n"
                    "Growth Marketing & Solutions Lead | GoodSpace AI"
                ),
                "CTA": "Open to seeing a 2-minute interactive demo video of how it screens software engineers?"
            },
            "Step_2": {
                "Step_Number": 2,
                "Timing": "Day 3 (Follow-Up #1 - Value Proof)",
                "Subject": "Re: Quick follow-up regarding {{Company_Name}}'s recruitment speed",
                "Body": (
                    "Hi {{First_Name}},\n\n"
                    "Following up on my previous note. Thought you might find this benchmark study interesting:\n\n"
                    "Teams using AI-driven pre-screening report a 40% reduction in interview drop-off and "
                    "a 3.2x increase in candidate-to-offer acceptance ratios.\n\n"
                    "Here is a short case summary of how another technology leader eliminated interview scheduling bottlenecks: "
                    "https://goodspace.ai/case-study/tech-velocity\n\n"
                    "Do you have 10 minutes next Tuesday to explore if this is a fit for {{Company_Name}}?\n\n"
                    "Best,\n"
                    "Alex"
                ),
                "CTA": "Do you have 10 minutes next Tuesday to explore if this is a fit for {{Company_Name}}?"
            },
            "Step_3": {
                "Step_Number": 3,
                "Timing": "Day 8 (Follow-Up #2 - Breakup & Permission)",
                "Subject": "Permission to close your file, {{First_Name}}?",
                "Body": (
                    "Hi {{First_Name}},\n\n"
                    "I haven't heard back, which usually means either you're completely satisfied with your current "
                    "recruiting workflow at {{Company_Name}}, or tech hiring isn't an immediate priority right now.\n\n"
                    "Either way, I won't continue cluttering your inbox.\n\n"
                    "If automating candidate evaluations ever becomes top-of-mind down the road, feel free to bookmark "
                    "GoodSpace AI (https://goodspace.ai).\n\n"
                    "Wishing you and the team continued success!\n\n"
                    "Cheers,\n"
                    "Alex Rivera"
                ),
                "CTA": "Feel free to bookmark GoodSpace AI or reply if priorities shift."
            }
        }
    },
    "CMP-002": {
        "Campaign_ID": "CMP-002",
        "Campaign_Name": "Manufacturing Plant & Eng Talent Pipeline",
        "Target_Industry": "Manufacturing",
        "Target_Audience": "Talent Acquisition Directors, VP Human Resources, Plant Operations Recruiters",
        "Objective": "Source and pre-qualify specialized plant operations, electrical, and quality assurance engineers with zero recruiter fatigue.",
        "Sequence": {
            "Step_1_Variant_A": {
                "Step_Number": 1,
                "Timing": "Day 0 (Initial Outreach)",
                "Variant_Label": "Variant A - Direct Calendar Call",
                "Subject": "Sourcing plant & manufacturing talent for {{Company_Name}}",
                "Body": (
                    "Hi {{First_Name}},\n\n"
                    "Finding qualified plant supervisors, reliability engineers, and precision technicians in manufacturing "
                    "has become one of the toughest challenges of 2026.\n\n"
                    "GoodSpace AI enables industrial manufacturers to autonomously verify certifications, "
                    "safety protocols, and mechanical competencies within 24 hours of application submission.\n\n"
                    "Grab a quick 10-minute slot on my calendar here to discuss your open requisitions: "
                    "https://calendly.com/goodspace-ai/10min\n\n"
                    "Best regards,\n"
                    "Elena Vance\n"
                    "Industry Practice Lead | GoodSpace AI"
                ),
                "CTA": "Grab a quick 10-minute slot on my calendar here to discuss your open requisitions."
            },
            "Step_1_Variant_B": {
                "Step_Number": 1,
                "Timing": "Day 0 (Initial Outreach)",
                "Variant_Label": "Variant B - Low-Friction Video Permission",
                "Subject": "Solving specialized technician shortages at {{Company_Name}}",
                "Body": (
                    "Hi {{First_Name}},\n\n"
                    "Are your plant recruiters struggling to source and verify licensed manufacturing engineers?\n\n"
                    "GoodSpace AI acts as a 24/7 technical screening assistant that automatically checks trade certifications, "
                    "shift availability, and hands-on diagnostic abilities before you review a single profile.\n\n"
                    "Would you be opposed to seeing a 2-minute workflow video showing how it cut manufacturing time-to-fill by 50%?\n\n"
                    "Best regards,\n"
                    "Elena Vance\n"
                    "Industry Practice Lead | GoodSpace AI"
                ),
                "CTA": "Would you be opposed to seeing a 2-minute workflow video?"
            },
            "Step_2": {
                "Step_Number": 2,
                "Timing": "Day 3 (Follow-Up #1)",
                "Subject": "Re: Sourcing plant & manufacturing talent for {{Company_Name}}",
                "Body": (
                    "Hi {{First_Name}},\n\n"
                    "Checking back in. Our manufacturing partners typically reduce candidate ghosting by 55% "
                    "because candidates receive instant feedback on their qualifications instead of waiting weeks for recruiter calls.\n\n"
                    "Happy to send over our Industrial Hiring Playbook if you'd like to take a look.\n\n"
                    "Best,\n"
                    "Elena"
                ),
                "CTA": "Happy to send over our Industrial Hiring Playbook if you'd like to take a look."
            },
            "Step_3": {
                "Step_Number": 3,
                "Timing": "Day 8 (Follow-Up #2)",
                "Subject": "Closing the loop on plant recruiting at {{Company_Name}}",
                "Body": (
                    "Hi {{First_Name}},\n\n"
                    "Assuming manufacturing hiring is running smoothly right now. I will step back and not follow up further.\n\n"
                    "If plant expansion or technician shortages become an obstacle next quarter, we're always here to help.\n\n"
                    "Best of luck with your hiring goals!\n\n"
                    "Elena Vance"
                ),
                "CTA": "Reply if priorities shift next quarter."
            }
        }
    },
    "CMP-003": {
        "Campaign_ID": "CMP-003",
        "Campaign_Name": "Consulting Executive Search & Onboarding",
        "Target_Industry": "Consulting",
        "Target_Audience": "Recruitment Heads, Managing Directors, People & Culture Executives in Management Consulting",
        "Objective": "Partner with professional services firms to accelerate partner-track and specialized practice recruitment.",
        "Sequence": {
            "Step_1_Variant_A": {
                "Step_Number": 1,
                "Timing": "Day 0 (Initial Outreach)",
                "Variant_Label": "Variant A - Peer Benchmark Insight",
                "Subject": "How Tier-1 consulting firms cut candidate drop-off by 40%",
                "Body": (
                    "Hi {{First_Name}},\n\n"
                    "In management consulting, losing elite lateral hires to competing advisory firms during "
                    "prolonged 6-week case study interview cycles costs upwards of $120k in lost billable hours.\n\n"
                    "GoodSpace AI deploys generative AI case simulation agents that evaluate candidates on structured logic, "
                    "financial modeling, and strategic presentation in a single weekend.\n\n"
                    "Would you be open to reviewing a 1-page benchmark sheet showing how peer firms streamlined their case assessments?\n\n"
                    "Best regards,\n"
                    "Marcus Sterling\n"
                    "VP Strategic Accounts | GoodSpace AI"
                ),
                "CTA": "Would you be open to reviewing a 1-page benchmark sheet?"
            },
            "Step_1_Variant_B": {
                "Step_Number": 1,
                "Timing": "Day 0 (Initial Outreach)",
                "Variant_Label": "Variant B - Headcount Expansion Hook",
                "Subject": "Noticed {{Company_Name}} is expanding client consulting headcount",
                "Body": (
                    "Hi {{First_Name}},\n\n"
                    "Saw that {{Company_Name}} has recently taken on new client engagements and is scaling its consulting roster.\n\n"
                    "Our AI assessment suite automates preliminary case interviews and competency benchmarking, ensuring "
                    "only the sharpest analytical talent reaches your Partner interview rounds.\n\n"
                    "Do you have 10 minutes next Wednesday to explore how this could accelerate your practice's recruitment?\n\n"
                    "Best regards,\n"
                    "Marcus Sterling\n"
                    "VP Strategic Accounts | GoodSpace AI"
                ),
                "CTA": "Do you have 10 minutes next Wednesday to explore how this could accelerate your practice's recruitment?"
            },
            "Step_2": {
                "Step_Number": 2,
                "Timing": "Day 3 (Follow-Up #1)",
                "Subject": "Re: Accelerating case interviews at {{Company_Name}}",
                "Body": (
                    "Hi {{First_Name}},\n\n"
                    "Quick follow-up on my note regarding lateral consultant hiring.\n\n"
                    "One mid-sized strategy boutique we partnered with reduced candidate evaluation turnaround from 24 days to 5 days, "
                    "winning 88% of competitive candidate offers.\n\n"
                    "Would a brief 8-minute walkthrough be worth your time next week?\n\n"
                    "Best,\n"
                    "Marcus"
                ),
                "CTA": "Would a brief 8-minute walkthrough be worth your time next week?"
            },
            "Step_3": {
                "Step_Number": 3,
                "Timing": "Day 8 (Follow-Up #2)",
                "Subject": "Final thought on consulting talent acquisition for {{Company_Name}}",
                "Body": (
                    "Hi {{First_Name}},\n\n"
                    "I realize partner schedules and client deliverables keep consulting leaders exceptionally busy.\n\n"
                    "I'll mark this as low priority on my side. If you ever want to benchmark your candidate assessment flow, "
                    "feel free to reach out anytime.\n\n"
                    "Best regards,\n"
                    "Marcus Sterling"
                ),
                "CTA": "Feel free to reach out anytime."
            }
        }
    },
    "CMP-004": {
        "Campaign_ID": "CMP-004",
        "Campaign_Name": "Fintech & Banking Compliance Hiring",
        "Target_Industry": "Banking and Finance",
        "Target_Audience": "HR Directors, Chief People Officers, Compliance Talent Acquisition Leads",
        "Objective": "Assist financial institutions in sourcing pre-vetted compliance, AML/KYC, and quantitative risk talent.",
        "Sequence": {
            "Step_1_Variant_A": {
                "Step_Number": 1,
                "Timing": "Day 0 (Initial Outreach)",
                "Variant_Label": "Variant A - Short & Punchy (under 75 words)",
                "Subject": "Compliance & Risk talent for {{Company_Name}}",
                "Body": (
                    "Hi {{First_Name}},\n\n"
                    "Hiring certified AML, BSA, and financial risk analysts takes an average of 52 days in banking.\n\n"
                    "GoodSpace AI instantly pre-screens and audits regulatory competencies against SEC, FINRA, and OCC frameworks—delivering pre-validated talent in 48 hours.\n\n"
                    "Worth a 5-minute conversation to see how {{Company_Name}} could accelerate compliance staffing?\n\n"
                    "Best,\n"
                    "Kavita Patel\n"
                    "Financial Services Lead | GoodSpace AI"
                ),
                "CTA": "Worth a 5-minute conversation to see how {{Company_Name}} could accelerate compliance staffing?"
            },
            "Step_1_Variant_B": {
                "Step_Number": 1,
                "Timing": "Day 0 (Initial Outreach)",
                "Variant_Label": "Variant B - Case Study & Metric Story (150 words)",
                "Subject": "How leading financial institutions solve compliance talent shortages",
                "Body": (
                    "Hi {{First_Name}},\n\n"
                    "With tightening financial regulations and strict AML/KYC scrutiny, financial institutions are facing a 35% shortfall in experienced compliance officers.\n\n"
                    "When a regional banking group partnered with GoodSpace AI, they automated background regulatory knowledge evaluations and situational judgment tests.\n\n"
                    "The outcome? Their compliance team cut screening backlog from 4 weeks to 3 days while boosting new hire 1-year retention to 94%.\n\n"
                    "We'd love to share the full regulatory staffing case study with {{Company_Name}}.\n\n"
                    "Do you have a few minutes for a quick introductory discussion next week?\n\n"
                    "Warm regards,\n"
                    "Kavita Patel\n"
                    "Financial Services Lead | GoodSpace AI"
                ),
                "CTA": "Do you have a few minutes for a quick introductory discussion next week?"
            },
            "Step_2": {
                "Step_Number": 2,
                "Timing": "Day 3 (Follow-Up #1)",
                "Subject": "Re: Compliance & Risk talent for {{Company_Name}}",
                "Body": (
                    "Hi {{First_Name}},\n\n"
                    "Reaching back out on compliance recruitment at {{Company_Name}}.\n\n"
                    "Because our evaluations are SOC2 Type II and GDPR compliant, bank risk committees approve our screening environment in under 48 hours.\n\n"
                    "Happy to share our compliance security whitepaper if helpful.\n\n"
                    "Best,\n"
                    "Kavita"
                ),
                "CTA": "Happy to share our compliance security whitepaper if helpful."
            },
            "Step_3": {
                "Step_Number": 3,
                "Timing": "Day 8 (Follow-Up #2)",
                "Subject": "Closing the loop on risk hiring at {{Company_Name}}",
                "Body": (
                    "Hi {{First_Name}},\n\n"
                    "I assume your regulatory and risk recruitment pipeline is fully covered for now.\n\n"
                    "I won't follow up again, but please don't hesitate to reach out if staffing needs surge ahead of audit season.\n\n"
                    "Best regards,\n"
                    "Kavita Patel"
                ),
                "CTA": "Reach out if staffing needs surge ahead of audit season."
            }
        }
    }
}


def render_email_copy(
    campaign_id: str,
    step_key: str,
    lead_info: Dict[str, str]
) -> Dict[str, str]:
    """
    Renders personalized email subject and body by populating merge tags.
    """
    if campaign_id not in CAMPAIGN_COPY_CATALOG:
        raise ValueError(f"Campaign {campaign_id} not found in catalog.")
    
    seq = CAMPAIGN_COPY_CATALOG[campaign_id]["Sequence"]
    if step_key not in seq:
        raise ValueError(f"Step {step_key} not found for campaign {campaign_id}.")
    
    template = seq[step_key]
    first_name = lead_info.get("First_Name", "Colleague")
    company_name = lead_info.get("Company_Name", "your team")
    job_title = lead_info.get("Job_Title", "Recruitment Leader")
    industry = lead_info.get("Company_Industry", "your industry")

    rendered_subject = (
        template["Subject"]
        .replace("{{First_Name}}", first_name)
        .replace("{{Company_Name}}", company_name)
        .replace("{{Job_Title}}", job_title)
        .replace("{{Target_Industry}}", industry)
    )

    rendered_body = (
        template["Body"]
        .replace("{{First_Name}}", first_name)
        .replace("{{Company_Name}}", company_name)
        .replace("{{Job_Title}}", job_title)
        .replace("{{Target_Industry}}", industry)
    )

    return {
        "Campaign_ID": campaign_id,
        "Step_Key": step_key,
        "Timing": template.get("Timing", ""),
        "Subject": rendered_subject,
        "Body": rendered_body,
        "CTA": template.get("CTA", "")
    }


def get_all_campaign_metadata() -> List[Dict[str, Any]]:
    """Returns metadata for all simulated campaigns."""
    result = []
    for cid, data in CAMPAIGN_COPY_CATALOG.items():
        result.append({
            "Campaign_ID": cid,
            "Campaign_Name": data["Campaign_Name"],
            "Target_Industry": data["Target_Industry"],
            "Target_Audience": data["Target_Audience"],
            "Objective": data["Objective"],
            "Total_Sequence_Steps": len(data["Sequence"])
        })
    return result


if __name__ == "__main__":
    print("[Campaign Management] GoodSpace AI Outreach Sequences Loaded.")
    for meta in get_all_campaign_metadata():
        print(f" -> {meta['Campaign_ID']}: {meta['Campaign_Name']} ({meta['Target_Industry']})")
    
    # Test sample rendering
    test_lead = {
        "First_Name": "Sarah",
        "Company_Name": "Pinnacle Technologies",
        "Job_Title": "VP of Talent Acquisition",
        "Company_Industry": "Information Technology"
    }
    rendered = render_email_copy("CMP-001", "Step_1_Variant_B", test_lead)
    print("\n--- SAMPLE PERSONALIZED EMAIL (Step 1, Variant B) ---")
    print(f"Subject: {rendered['Subject']}")
    print(f"Body:\n{rendered['Body']}")

