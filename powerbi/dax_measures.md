# Power BI DAX Measures Reference Guide
## B2B Cold Email Campaign & Growth Analytics Platform

This guide provides **25+ industry-standard DAX (Data Analysis Expressions) measures** optimized for Power BI Desktop and Power BI Service. Every formula specifies the exact calculation logic, format string, and business rationale.

---

## 1. Volume & Activity Measures

### `[Total Emails Sent]`
Calculates the gross volume of emails dispatched by the email infrastructure.
```dax
Total Emails Sent = 
COUNTROWS('PowerBI_Email_Activities')
```

### `[Total Emails Delivered]`
Calculates total emails successfully accepted by recipient mail transfer agents (MTAs).
```dax
Total Emails Delivered = 
CALCULATE(
    COUNTROWS('PowerBI_Email_Activities'),
    'PowerBI_Email_Activities'[Delivery_Status] = 1
)
```

### `[Total Bounces]`
Count of hard/soft delivery rejections.
```dax
Total Bounces = 
CALCULATE(
    COUNTROWS('PowerBI_Email_Activities'),
    'PowerBI_Email_Activities'[Bounce_Status] = 1
)
```

### `[Total Opens]`
Count of unique email open events.
```dax
Total Opens = 
CALCULATE(
    COUNTROWS('PowerBI_Email_Activities'),
    'PowerBI_Email_Activities'[Open_Status] = 1
)
```

### `[Total Clicks]`
Count of unique click-through interactions on links/CTAs.
```dax
Total Clicks = 
CALCULATE(
    COUNTROWS('PowerBI_Email_Activities'),
    'PowerBI_Email_Activities'[Click_Status] = 1
)
```

### `[Total Replies]`
Total responses received from recipients.
```dax
Total Replies = 
CALCULATE(
    COUNTROWS('PowerBI_Email_Activities'),
    'PowerBI_Email_Activities'[Reply_Status] = 1
)
```

### `[Total Positive Replies]`
High-intent responses classified as interested or requesting next steps.
```dax
Total Positive Replies = 
CALCULATE(
    COUNTROWS('PowerBI_Email_Activities'),
    'PowerBI_Email_Activities'[Reply_Type] = "Positive"
)
```

### `[Total Unsubscribes]`
Total opt-outs and suppression requests.
```dax
Total Unsubscribes = 
CALCULATE(
    COUNTROWS('PowerBI_Email_Activities'),
    'PowerBI_Email_Activities'[Unsubscribe_Status] = 1
)
```

---

## 2. Marketing KPI Rates (Percentages)

### `[Delivery Rate %]`
Evaluates mail server reputation and email list health.
```dax
Delivery Rate % = 
DIVIDE(
    [Total Emails Delivered],
    [Total Emails Sent],
    0
)
```
*Format: `0.0%` (Target: >= 98.0%)*

### `[Bounce Rate %]`
Technical deliverability health indicator.
```dax
Bounce Rate % = 
DIVIDE(
    [Total Bounces],
    [Total Emails Sent],
    0
)
```
*Format: `0.0%` (Target: <= 2.0%)*

### `[Open Rate %]`
Measures subject line effectiveness, brand recognition, and inbox placement.
```dax
Open Rate % = 
DIVIDE(
    [Total Opens],
    [Total Emails Delivered],
    0
)
```
*Format: `0.0%` (Target: >= 30.0%)*

### `[Click-Through Rate (CTR) %]`
Link click interest relative to delivered outreach.
```dax
Click-Through Rate % = 
DIVIDE(
    [Total Clicks],
    [Total Emails Delivered],
    0
)
```
*Format: `0.0%` (Target: >= 3.0%)*

### `[Click-To-Open Rate (CTOR) %]`
Content resonance among recipients who actually opened the email.
```dax
Click-To-Open Rate % = 
DIVIDE(
    [Total Clicks],
    [Total Opens],
    0
)
```
*Format: `0.0%` (Target: >= 10.0%)*

### `[Reply Rate %]`
Conversation conversion efficiency.
```dax
Reply Rate % = 
DIVIDE(
    [Total Replies],
    [Total Emails Delivered],
    0
)
```
*Format: `0.0%` (Target: >= 3.5%)*

### `[Positive Reply Rate %]`
The most critical B2B growth KPI: qualified prospect interest rate.
```dax
Positive Reply Rate % = 
DIVIDE(
    [Total Positive Replies],
    [Total Emails Delivered],
    0
)
```
*Format: `0.0%` (Target: >= 1.5%)*

### `[Positive Sentiment Share %]`
Percentage of replies that are positive.
```dax
Positive Sentiment Share % = 
DIVIDE(
    [Total Positive Replies],
    [Total Replies],
    0
)
```
*Format: `0.0%` (Target: >= 40.0%)*

### `[Unsubscribe Rate %]`
Audience fatigue and CAN-SPAM compliance metric.
```dax
Unsubscribe Rate % = 
DIVIDE(
    [Total Unsubscribes],
    [Total Emails Delivered],
    0
)
```
*Format: `0.0%` (Target: <= 0.5%)*

---

## 3. Pipeline & Conversion Measures

### `[Total Opportunities]`
Count of qualified sales opportunities created from campaigns.
```dax
Total Opportunities = 
COUNTROWS('PowerBI_Conversions')
```

### `[Total Pipeline Value]`
Total dollar value of sales opportunities in pipeline.
```dax
Total Pipeline Value = 
SUM('PowerBI_Conversions'[Opportunity_Value])
```
*Format: `$#,##0`*

### `[Closed-Won Pipeline Value]`
Won ARR generated from cold email initiatives.
```dax
Closed-Won Pipeline Value = 
CALCULATE(
    SUM('PowerBI_Conversions'[Opportunity_Value]),
    'PowerBI_Conversions'[Conversion_Status] = "Closed-Won"
)
```
*Format: `$#,##0`*

### `[Average Contract Value (ACV)]`
Mean opportunity value per qualified conversion.
```dax
Average Contract Value = 
DIVIDE(
    [Total Pipeline Value],
    [Total Opportunities],
    0
)
```
*Format: `$#,##0`*

### `[Lead Conversion Rate %]`
Percentage of contacted leads that generated a pipeline opportunity.
```dax
Lead Conversion Rate % = 
DIVIDE(
    [Total Opportunities],
    DISTINCTCOUNT('PowerBI_Email_Activities'[Lead_ID]),
    0
)
```
*Format: `0.00%`*

---

## 4. A/B Testing & Lift Measures

### `[Reply Rate Variant A]`
```dax
Reply Rate Variant A = 
DIVIDE(
    CALCULATE([Total Replies], 'PowerBI_Email_Activities'[Email_Variant] = "Variant_A"),
    CALCULATE([Total Emails Delivered], 'PowerBI_Email_Activities'[Email_Variant] = "Variant_A"),
    0
)
```

### `[Reply Rate Variant B]`
```dax
Reply Rate Variant B = 
DIVIDE(
    CALCULATE([Total Replies], 'PowerBI_Email_Activities'[Email_Variant] = "Variant_B"),
    CALCULATE([Total Emails Delivered], 'PowerBI_Email_Activities'[Email_Variant] = "Variant_B"),
    0
)
```

### `[A/B Relative Lift %]`
Percentage difference between Variant B and Variant A.
```dax
AB Relative Lift % = 
DIVIDE(
    [Reply Rate Variant B] - [Reply Rate Variant A],
    [Reply Rate Variant A],
    0
)
```
*Format: `+0.0%;-0.0%;0.0%`*

---

## 5. Time-Intelligence Measures

### `[Emails Sent Previous Month]`
```dax
Emails Sent Previous Month = 
CALCULATE(
    [Total Emails Sent],
    DATEADD('PowerBI_Email_Activities'[Sent_Date], -1, MONTH)
)
```

### `[MoM Volume Growth %]`
```dax
MoM Volume Growth % = 
DIVIDE(
    [Total Emails Sent] - [Emails Sent Previous Month],
    [Emails Sent Previous Month],
    0
)
```
*Format: `+0.0%;-0.0%;0.0%`*

