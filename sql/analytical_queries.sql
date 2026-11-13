-- =====================================================================
-- B2B Cold Email Campaign & Growth Analytics Platform
-- 20 Production Analytical SQL Queries
-- Designed for Growth Marketing Analysts & Marketing Data Engineers
-- Compatible with SQLite and Microsoft SQL Server (T-SQL)
-- =====================================================================

-- ---------------------------------------------------------------------
-- QUERY 1: Total Number of Leads & Overall Database Health
-- Business Objective: Determine top-of-funnel database capacity and regional distribution.
-- ---------------------------------------------------------------------
SELECT 
    COUNT(*) AS Total_Leads,
    COUNT(DISTINCT Company_Name) AS Unique_Companies,
    COUNT(DISTINCT Business_Email) AS Unique_Verified_Emails,
    ROUND(AVG(Hiring_Intent_Score), 1) AS Avg_Hiring_Intent_Score,
    ROUND(AVG(Estimated_Revenue_M), 2) AS Avg_Company_Revenue_M
FROM Leads;


-- ---------------------------------------------------------------------
-- QUERY 2: Industry-Wise Lead Distribution & Market Penetration
-- Business Objective: Identify which B2B verticals form the largest prospecting pool.
-- ---------------------------------------------------------------------
SELECT 
    Company_Industry,
    COUNT(Lead_ID) AS Lead_Count,
    ROUND(COUNT(Lead_ID) * 100.0 / (SELECT COUNT(*) FROM Leads), 2) AS Pct_Of_Total_Database,
    ROUND(AVG(Hiring_Intent_Score), 1) AS Avg_Intent_Score
FROM Leads
GROUP BY Company_Industry
ORDER BY Lead_Count DESC;


-- ---------------------------------------------------------------------
-- QUERY 3: Campaign-Wise Email Performance & Delivery Metrics
-- Business Objective: Assess end-to-end volumetric throughput for every outbound campaign.
-- ---------------------------------------------------------------------
SELECT 
    c.Campaign_ID,
    c.Campaign_Name,
    c.Target_Industry,
    COUNT(a.Email_ID) AS Emails_Sent,
    SUM(a.Delivery_Status) AS Emails_Delivered,
    ROUND(CAST(SUM(a.Delivery_Status) AS FLOAT) / COUNT(a.Email_ID) * 100, 2) AS Delivery_Rate,
    SUM(a.Open_Status) AS Opens,
    ROUND(CAST(SUM(a.Open_Status) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) * 100, 2) AS Open_Rate,
    SUM(a.Reply_Status) AS Replies,
    ROUND(CAST(SUM(a.Reply_Status) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) * 100, 2) AS Reply_Rate
FROM Campaigns c
LEFT JOIN Email_Activities a ON c.Campaign_ID = a.Campaign_ID
GROUP BY c.Campaign_ID, c.Campaign_Name, c.Target_Industry
ORDER BY Emails_Sent DESC;


-- ---------------------------------------------------------------------
-- QUERY 4: Highest Reply-Rate Campaigns (Ranked by Engagement)
-- Business Objective: Identify which campaigns generate the highest prospect conversations.
-- ---------------------------------------------------------------------
SELECT 
    c.Campaign_ID,
    c.Campaign_Name,
    SUM(a.Delivery_Status) AS Emails_Delivered,
    SUM(a.Reply_Status) AS Total_Replies,
    ROUND(CAST(SUM(a.Reply_Status) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) * 100, 2) AS Reply_Rate,
    RANK() OVER (ORDER BY CAST(SUM(a.Reply_Status) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) DESC) AS Reply_Rate_Rank
FROM Campaigns c
JOIN Email_Activities a ON c.Campaign_ID = a.Campaign_ID
GROUP BY c.Campaign_ID, c.Campaign_Name
ORDER BY Reply_Rate_Rank;


-- ---------------------------------------------------------------------
-- QUERY 5: Highest Conversion-Rate Campaigns & Pipeline Value Generated
-- Business Objective: Measure bottom-of-funnel ROI and revenue impact per campaign.
-- ---------------------------------------------------------------------
SELECT 
    c.Campaign_ID,
    c.Campaign_Name,
    SUM(a.Delivery_Status) AS Delivered_Volume,
    COUNT(DISTINCT cv.Conversion_ID) AS Total_Conversions,
    ROUND(CAST(COUNT(DISTINCT cv.Conversion_ID) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) * 100, 2) AS Conversion_Rate,
    COALESCE(SUM(cv.Opportunity_Value), 0.0) AS Total_Pipeline_Value,
    ROUND(COALESCE(AVG(cv.Opportunity_Value), 0.0), 2) AS Avg_Deal_Size
FROM Campaigns c
JOIN Email_Activities a ON c.Campaign_ID = a.Campaign_ID
LEFT JOIN Conversions cv ON c.Campaign_ID = cv.Campaign_ID
GROUP BY c.Campaign_ID, c.Campaign_Name
ORDER BY Conversion_Rate DESC;


-- ---------------------------------------------------------------------
-- QUERY 6: Bounce-Rate Analysis & Technical Risk Assessment
-- Business Objective: Monitor hard bounces against the 2.0% industry risk threshold.
-- ---------------------------------------------------------------------
SELECT 
    c.Campaign_ID,
    c.Campaign_Name,
    COUNT(a.Email_ID) AS Total_Sent,
    SUM(a.Bounce_Status) AS Total_Bounces,
    ROUND(CAST(SUM(a.Bounce_Status) AS FLOAT) / COUNT(a.Email_ID) * 100, 2) AS Bounce_Rate,
    CASE 
        WHEN (CAST(SUM(a.Bounce_Status) AS FLOAT) / COUNT(a.Email_ID) * 100) > 2.0 
        THEN 'Action Required: High Risk (>2%)'
        ELSE 'Healthy (<=2%)'
    END AS Technical_Deliverability_Status
FROM Campaigns c
JOIN Email_Activities a ON c.Campaign_ID = a.Campaign_ID
GROUP BY c.Campaign_ID, c.Campaign_Name
ORDER BY Bounce_Rate DESC;


-- ---------------------------------------------------------------------
-- QUERY 7: Unsubscribe & Opt-Out Analysis
-- Business Objective: Ensure compliance with CAN-SPAM / GDPR opt-out thresholds (target < 0.5%).
-- ---------------------------------------------------------------------
SELECT 
    c.Campaign_ID,
    c.Campaign_Name,
    SUM(a.Delivery_Status) AS Delivered_Emails,
    SUM(a.Unsubscribe_Status) AS Total_Unsubscribes,
    ROUND(CAST(SUM(a.Unsubscribe_Status) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) * 100, 2) AS Unsubscribe_Rate,
    CASE 
        WHEN (CAST(SUM(a.Unsubscribe_Status) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) * 100) > 0.5 
        THEN 'Caution: Fatigue Detected (>0.5%)'
        ELSE 'Safe (<0.5%)'
    END AS Audience_Fatigue_Alert
FROM Campaigns c
JOIN Email_Activities a ON c.Campaign_ID = a.Campaign_ID
GROUP BY c.Campaign_ID, c.Campaign_Name
ORDER BY Unsubscribe_Rate DESC;


-- ---------------------------------------------------------------------
-- QUERY 8: Lead Acquisition Source Performance
-- Business Objective: Evaluate lead quality by channel to optimize marketing CAC.
-- ---------------------------------------------------------------------
SELECT 
    l.Lead_Source,
    COUNT(DISTINCT l.Lead_ID) AS Leads_Contacted,
    COUNT(a.Email_ID) AS Emails_Sent,
    SUM(a.Delivery_Status) AS Emails_Delivered,
    SUM(a.Open_Status) AS Opens,
    ROUND(CAST(SUM(a.Open_Status) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) * 100, 2) AS Open_Rate,
    SUM(CASE WHEN a.Reply_Type = 'Positive' THEN 1 ELSE 0 END) AS Positive_Replies,
    ROUND(CAST(SUM(CASE WHEN a.Reply_Type = 'Positive' THEN 1 ELSE 0 END) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) * 100, 2) AS Positive_Reply_Rate
FROM Leads l
JOIN Email_Activities a ON l.Lead_ID = a.Lead_ID
GROUP BY l.Lead_Source
ORDER BY Positive_Reply_Rate DESC;


-- ---------------------------------------------------------------------
-- QUERY 9: Job-Title-Wise Engagement & Persona Resonance
-- Business Objective: Determine which HR & Talent Acquisition personas respond best.
-- ---------------------------------------------------------------------
SELECT 
    l.Job_Title,
    l.Seniority_Level,
    COUNT(DISTINCT l.Lead_ID) AS Contacted_Leads,
    SUM(a.Delivery_Status) AS Delivered_Emails,
    SUM(a.Open_Status) AS Opens,
    ROUND(CAST(SUM(a.Open_Status) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) * 100, 2) AS Open_Rate,
    SUM(a.Reply_Status) AS Replies,
    ROUND(CAST(SUM(a.Reply_Status) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) * 100, 2) AS Reply_Rate,
    SUM(CASE WHEN a.Reply_Type = 'Positive' THEN 1 ELSE 0 END) AS Positive_Replies
FROM Leads l
JOIN Email_Activities a ON l.Lead_ID = a.Lead_ID
GROUP BY l.Job_Title, l.Seniority_Level
ORDER BY Reply_Rate DESC;


-- ---------------------------------------------------------------------
-- QUERY 10: Company-Size-Wise Response Rates & Deal Size Potential
-- Business Objective: Understand whether SMB, Mid-Market, or Enterprise responds best.
-- ---------------------------------------------------------------------
SELECT 
    l.Company_Size,
    COUNT(DISTINCT l.Lead_ID) AS Total_Leads,
    SUM(a.Delivery_Status) AS Delivered_Volume,
    ROUND(CAST(SUM(a.Open_Status) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) * 100, 2) AS Open_Rate,
    ROUND(CAST(SUM(a.Reply_Status) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) * 100, 2) AS Reply_Rate,
    ROUND(CAST(SUM(CASE WHEN a.Reply_Type = 'Positive' THEN 1 ELSE 0 END) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) * 100, 2) AS Positive_Reply_Rate,
    COUNT(DISTINCT cv.Conversion_ID) AS Total_Conversions,
    COALESCE(SUM(cv.Opportunity_Value), 0.0) AS Total_Opportunity_Pipeline
FROM Leads l
JOIN Email_Activities a ON l.Lead_ID = a.Lead_ID
LEFT JOIN Conversions cv ON l.Lead_ID = cv.Lead_ID
GROUP BY l.Company_Size
ORDER BY Total_Opportunity_Pipeline DESC;


-- ---------------------------------------------------------------------
-- QUERY 11: Campaign-Wise Positive Reply Distribution & Sentiment Share
-- Business Objective: Categorize prospect replies (Positive vs Neutral vs Negative vs OOO).
-- ---------------------------------------------------------------------
SELECT 
    c.Campaign_Name,
    SUM(a.Reply_Status) AS Total_Replies,
    SUM(CASE WHEN a.Reply_Type = 'Positive' THEN 1 ELSE 0 END) AS Positive_Replies,
    SUM(CASE WHEN a.Reply_Type = 'Neutral' THEN 1 ELSE 0 END) AS Neutral_Replies,
    SUM(CASE WHEN a.Reply_Type = 'Negative' THEN 1 ELSE 0 END) AS Negative_Replies,
    SUM(CASE WHEN a.Reply_Type = 'Out of Office' THEN 1 ELSE 0 END) AS OOO_Replies,
    ROUND(CAST(SUM(CASE WHEN a.Reply_Type = 'Positive' THEN 1 ELSE 0 END) AS FLOAT) / NULLIF(SUM(a.Reply_Status), 0) * 100, 2) AS Positive_Sentiment_Share_Pct
FROM Campaigns c
JOIN Email_Activities a ON c.Campaign_ID = a.Campaign_ID
WHERE a.Reply_Status = 1
GROUP BY c.Campaign_Name
ORDER BY Positive_Sentiment_Share_Pct DESC;


-- ---------------------------------------------------------------------
-- QUERY 12: Monthly Campaign Performance & Trend Progression
-- Business Objective: Track pacing, volume, and engagement progression over time.
-- ---------------------------------------------------------------------
SELECT 
    SUBSTR(Sent_Date, 1, 7) AS Sent_Month,
    COUNT(Email_ID) AS Dispatched_Emails,
    SUM(Delivery_Status) AS Delivered_Emails,
    SUM(Open_Status) AS Opens,
    SUM(Reply_Status) AS Replies,
    SUM(CASE WHEN Reply_Type = 'Positive' THEN 1 ELSE 0 END) AS Positive_Replies,
    ROUND(CAST(SUM(Open_Status) AS FLOAT) / NULLIF(SUM(Delivery_Status), 0) * 100, 2) AS Monthly_Open_Rate,
    ROUND(CAST(SUM(Reply_Status) AS FLOAT) / NULLIF(SUM(Delivery_Status), 0) * 100, 2) AS Monthly_Reply_Rate
FROM Email_Activities
GROUP BY SUBSTR(Sent_Date, 1, 7)
ORDER BY Sent_Month ASC;


-- ---------------------------------------------------------------------
-- QUERY 13: Follow-Up Email Sequence Performance (Step 1 vs 2 vs 3)
-- Business Objective: Quantify lift generated by follow-up sequence touches.
-- ---------------------------------------------------------------------
SELECT 
    CASE 
        WHEN Email_Subject LIKE 'Re:%' THEN 'Step 2: Follow-Up (+3 Days)'
        WHEN Email_Subject LIKE 'Permission%' OR Email_Subject LIKE 'Closing%' OR Email_Subject LIKE 'Final%' 
        THEN 'Step 3: Breakup (+8 Days)'
        ELSE 'Step 1: Initial Outreach (Day 0)'
    END AS Sequence_Touchpoint,
    COUNT(Email_ID) AS Dispatched_Volume,
    SUM(Delivery_Status) AS Delivered_Volume,
    SUM(Open_Status) AS Opens,
    ROUND(CAST(SUM(Open_Status) AS FLOAT) / NULLIF(SUM(Delivery_Status), 0) * 100, 2) AS Open_Rate,
    SUM(Reply_Status) AS Replies,
    ROUND(CAST(SUM(Reply_Status) AS FLOAT) / NULLIF(SUM(Delivery_Status), 0) * 100, 2) AS Reply_Rate,
    SUM(CASE WHEN Reply_Type = 'Positive' THEN 1 ELSE 0 END) AS Positive_Replies
FROM Email_Activities
GROUP BY Sequence_Touchpoint
ORDER BY Dispatched_Volume DESC;


-- ---------------------------------------------------------------------
-- QUERY 14: A/B Testing Direct Statistical Head-to-Head Comparison
-- Business Objective: Compare control (Variant A) vs test (Variant B) across all experiments.
-- ---------------------------------------------------------------------
SELECT 
    Test_ID,
    Campaign_ID,
    Test_Variable,
    Emails_Delivered_A,
    Emails_Delivered_B,
    Opens_A,
    Opens_B,
    ROUND(CAST(Opens_A AS FLOAT) / Emails_Delivered_A * 100, 2) AS Open_Rate_A,
    ROUND(CAST(Opens_B AS FLOAT) / Emails_Delivered_B * 100, 2) AS Open_Rate_B,
    Replies_A,
    Replies_B,
    ROUND(CAST(Replies_A AS FLOAT) / Emails_Delivered_A * 100, 2) AS Reply_Rate_A,
    ROUND(CAST(Replies_B AS FLOAT) / Emails_Delivered_B * 100, 2) AS Reply_Rate_B,
    ROUND((CAST(Replies_B AS FLOAT) / Emails_Delivered_B - CAST(Replies_A AS FLOAT) / Emails_Delivered_A) / (CAST(Replies_A AS FLOAT) / Emails_Delivered_A) * 100, 2) AS Reply_Lift_Pct
FROM AB_Tests;


-- ---------------------------------------------------------------------
-- QUERY 15: Full Conversion Funnel Analysis (Drop-off Analysis)
-- Business Objective: Calculate stage-by-stage progression from sent to deal creation.
-- ---------------------------------------------------------------------
WITH FunnelMetrics AS (
    SELECT 
        COUNT(a.Email_ID) AS Stage_1_Sent,
        SUM(a.Delivery_Status) AS Stage_2_Delivered,
        SUM(a.Open_Status) AS Stage_3_Opened,
        SUM(a.Click_Status) AS Stage_4_Clicked,
        SUM(a.Reply_Status) AS Stage_5_Replied,
        SUM(CASE WHEN a.Reply_Type = 'Positive' THEN 1 ELSE 0 END) AS Stage_6_Positive_Replied,
        (SELECT COUNT(*) FROM Conversions) AS Stage_7_Converted
    FROM Email_Activities a
)
SELECT 
    Stage_1_Sent,
    Stage_2_Delivered,
    ROUND(CAST(Stage_2_Delivered AS FLOAT) / Stage_1_Sent * 100, 2) AS Delivery_Retention_Pct,
    Stage_3_Opened,
    ROUND(CAST(Stage_3_Opened AS FLOAT) / Stage_2_Delivered * 100, 2) AS Open_Retention_Pct,
    Stage_4_Clicked,
    ROUND(CAST(Stage_4_Clicked AS FLOAT) / Stage_3_Opened * 100, 2) AS Click_Retention_Pct,
    Stage_5_Replied,
    ROUND(CAST(Stage_5_Replied AS FLOAT) / Stage_2_Delivered * 100, 2) AS Reply_Retention_Pct,
    Stage_6_Positive_Replied,
    ROUND(CAST(Stage_6_Positive_Replied AS FLOAT) / Stage_5_Replied * 100, 2) AS Positive_Intent_Pct,
    Stage_7_Converted,
    ROUND(CAST(Stage_7_Converted AS FLOAT) / Stage_6_Positive_Replied * 100, 2) AS Lead_To_Opportunity_Close_Pct
FROM FunnelMetrics;


-- ---------------------------------------------------------------------
-- QUERY 16: Customer Engagement Segmentation & Multi-Touch Heat
-- Business Objective: Group leads into engagement tiers based on interaction frequency.
-- ---------------------------------------------------------------------
SELECT 
    CASE 
        WHEN cv.Conversion_ID IS NOT NULL THEN 'Champion: Converted Deal'
        WHEN pos.Positive_Count > 0 THEN 'Hot: Positive Intent Replier'
        WHEN act.Total_Replies > 0 THEN 'Warm: Replied (Neutral/Objection)'
        WHEN act.Total_Opens >= 2 THEN 'Interested: High Open Engagement'
        WHEN act.Total_Opens = 1 THEN 'Lukewarm: Single Open'
        ELSE 'Cold: Unresponsive'
    END AS Prospect_Engagement_Segment,
    COUNT(DISTINCT l.Lead_ID) AS Lead_Count,
    ROUND(COUNT(DISTINCT l.Lead_ID) * 100.0 / (SELECT COUNT(*) FROM Leads), 2) AS Segment_Share_Pct
FROM Leads l
LEFT JOIN (
    SELECT Lead_ID, SUM(Open_Status) AS Total_Opens, SUM(Reply_Status) AS Total_Replies
    FROM Email_Activities
    GROUP BY Lead_ID
) act ON l.Lead_ID = act.Lead_ID
LEFT JOIN (
    SELECT Lead_ID, COUNT(*) AS Positive_Count
    FROM Email_Activities
    WHERE Reply_Type = 'Positive'
    GROUP BY Lead_ID
) pos ON l.Lead_ID = pos.Lead_ID
LEFT JOIN Conversions cv ON l.Lead_ID = cv.Lead_ID
GROUP BY Prospect_Engagement_Segment
ORDER BY Lead_Count DESC;


-- ---------------------------------------------------------------------
-- QUERY 17: Underperforming Campaign Identification
-- Business Objective: Programmatically flag campaigns failing both open & reply benchmarks.
-- ---------------------------------------------------------------------
SELECT 
    c.Campaign_ID,
    c.Campaign_Name,
    ROUND(CAST(SUM(a.Open_Status) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) * 100, 2) AS Open_Rate,
    ROUND(CAST(SUM(a.Reply_Status) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) * 100, 2) AS Reply_Rate,
    ROUND(CAST(SUM(a.Bounce_Status) AS FLOAT) / COUNT(a.Email_ID) * 100, 2) AS Bounce_Rate,
    CASE 
        WHEN (CAST(SUM(a.Reply_Status) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) * 100) < 2.5 
        THEN 'Action Flag: Underperforming Reply Rate (<2.5%)'
        WHEN (CAST(SUM(a.Bounce_Status) AS FLOAT) / COUNT(a.Email_ID) * 100) > 2.0 
        THEN 'Action Flag: Critical Bounce Rate (>2.0%)'
        ELSE 'Performing within Target Threshold'
    END AS Performance_Audit_Verdict
FROM Campaigns c
JOIN Email_Activities a ON c.Campaign_ID = a.Campaign_ID
GROUP BY c.Campaign_ID, c.Campaign_Name
ORDER BY Reply_Rate ASC;


-- ---------------------------------------------------------------------
-- QUERY 18: Best-Performing Industry Segments Ranked by Positive Intent
-- Business Objective: Determine where marketing spend should be focused in next quarter.
-- ---------------------------------------------------------------------
SELECT 
    l.Company_Industry,
    COUNT(DISTINCT l.Lead_ID) AS Total_Prospects,
    SUM(a.Delivery_Status) AS Delivered_Emails,
    SUM(CASE WHEN a.Reply_Type = 'Positive' THEN 1 ELSE 0 END) AS Positive_Replies,
    ROUND(CAST(SUM(CASE WHEN a.Reply_Type = 'Positive' THEN 1 ELSE 0 END) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) * 100, 2) AS Positive_Reply_Rate,
    DENSE_RANK() OVER (ORDER BY CAST(SUM(CASE WHEN a.Reply_Type = 'Positive' THEN 1 ELSE 0 END) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) DESC) AS Industry_Intent_Rank
FROM Leads l
JOIN Email_Activities a ON l.Lead_ID = a.Lead_ID
GROUP BY l.Company_Industry
ORDER BY Industry_Intent_Rank;


-- ---------------------------------------------------------------------
-- QUERY 19: Lead-to-Conversion Pipeline Analysis & Sales Cycle
-- Business Objective: Track opportunity stages (Closed-Won, In Pipeline, Closed-Lost).
-- ---------------------------------------------------------------------
SELECT 
    cv.Conversion_Status,
    COUNT(cv.Conversion_ID) AS Total_Opportunities,
    ROUND(COUNT(cv.Conversion_ID) * 100.0 / (SELECT COUNT(*) FROM Conversions), 2) AS Pct_Of_All_Opportunities,
    SUM(cv.Opportunity_Value) AS Aggregate_Value,
    ROUND(AVG(cv.Opportunity_Value), 2) AS Average_Contract_Value_ACV
FROM Conversions cv
GROUP BY cv.Conversion_Status
ORDER BY Aggregate_Value DESC;


-- ---------------------------------------------------------------------
-- QUERY 20: Campaign Optimization Opportunities & Executive Takeaways
-- Business Objective: Synthesize high-yield optimization levers for executive leadership.
-- ---------------------------------------------------------------------
SELECT 
    c.Campaign_ID,
    c.Campaign_Name,
    c.Target_Industry,
    ROUND(CAST(SUM(a.Open_Status) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) * 100, 2) AS Open_Rate,
    ROUND(CAST(SUM(a.Reply_Status) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) * 100, 2) AS Reply_Rate,
    CASE 
        WHEN CAST(SUM(a.Open_Status) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) < 0.40 
        THEN 'Optimize Subject Line and Sender Identity to raise Top-of-Funnel Opens'
        WHEN CAST(SUM(a.Reply_Status) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) < 0.035 
        THEN 'Shorten Copy and Pivot CTA to Low-Friction Video/Asset'
        ELSE 'Scale Prospecting Volume - Content Resonance Confirmed'
    END AS Prescriptive_Optimization_Action
FROM Campaigns c
JOIN Email_Activities a ON c.Campaign_ID = a.Campaign_ID
GROUP BY c.Campaign_ID, c.Campaign_Name, c.Target_Industry
ORDER BY c.Campaign_ID ASC;
