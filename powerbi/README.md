# Power BI Integration & Data Modeling Guide
## B2B Cold Email Campaign & Growth Analytics Platform

This document describes how to connect, model, and visualize the B2B Growth Marketing datasets in **Microsoft Power BI**.

---

## 1. Data Source Files
All export files are located in `data/exports/`:

| File Name | Role in Model | Description | Record Count |
|---|---|---|---|
| `PowerBI_Leads.csv` | Dimension Table (`Dim_Leads`) | Master database of B2B prospect attributes | 5,920 rows |
| `PowerBI_Campaigns.csv` | Dimension Table (`Dim_Campaigns`) | Campaign metadata, objectives & target verticals | 4 rows |
| `PowerBI_Email_Activities.csv` | Fact Table (`Fact_Email_Activities`) | Granular touchpoint activity log across 3-step sequences | 16,765 rows |
| `PowerBI_AB_Testing.csv` | Fact Table (`Fact_AB_Testing`) | Aggregated A/B experiment data by campaign | 4 rows |
| `PowerBI_Conversions.csv` | Fact Table (`Fact_Conversions`) | Qualified pipeline opportunities & deal values | 165 rows |
| `PowerBI_Campaign_KPI_Summary.csv` | Summary Table (`Summary_KPIs`) | Pre-aggregated KPI summary table | 4 rows |

---

## 2. Star Schema Data Model Architecture

The data model follows an industry-standard **Star Schema** pattern optimized for high-performance Power BI in-memory VertiPaq engine:

```
          +------------------------+
          |      Dim_Campaigns     |
          |------------------------|
          | Campaign_ID (PK)       |
          | Campaign_Name          |
          | Target_Industry        |
          +------------------------+
                      | 1
                      |
                      | *
          +----------------------------+             +------------------------+
          |    Fact_Email_Activities   | *         1 |        Dim_Leads       |
          |----------------------------|-------------|------------------------|
          | Email_ID (PK)              |             | Lead_ID (PK)           |
          | Lead_ID (FK)               |             | First_Name, Last_Name  |
          | Campaign_ID (FK)           |             | Company_Name           |
          | Sent_Date (Date)           |             | Company_Industry       |
          | Delivery_Status (0/1)      |             | Company_Size_Tier      |
          | Open_Status (0/1)          |             | Seniority_Level        |
          | Click_Status (0/1)         |             | Sales_Region           |
          | Reply_Status (0/1)         |             | Lead_Source            |
          | Reply_Type (Sentiment)     |             +------------------------+
          | Bounce_Status (0/1)        |                         | 1
          | Unsubscribe_Status (0/1)   |                         |
          +----------------------------+                         |
                      |                                          | *
                      | 1                            +------------------------+
                      |                              |    Fact_Conversions    |
                      | *                            |------------------------|
          +------------------------+                 | Conversion_ID (PK)     |
          |     Fact_AB_Testing    |                 | Lead_ID (FK)           |
          |------------------------|                 | Campaign_ID (FK)       |
          | Test_ID (PK)           |                 | Conversion_Date        |
          | Campaign_ID (FK)       |                 | Conversion_Status      |
          | Test_Variable          |                 | Opportunity_Value ($)  |
          | Variant_A, Variant_B   |                 +------------------------+
          +------------------------+
```

### Table Relationships Configuration:
1. **`Dim_Campaigns[Campaign_ID]` (1) -> `Fact_Email_Activities[Campaign_ID]` (\*)**
   - Cardinality: One-to-Many (1:\*)
   - Cross-filter direction: Single
2. **`Dim_Leads[Lead_ID]` (1) -> `Fact_Email_Activities[Lead_ID]` (\*)**
   - Cardinality: One-to-Many (1:\*)
   - Cross-filter direction: Single
3. **`Dim_Leads[Lead_ID]` (1) -> `Fact_Conversions[Lead_ID]` (\*)**
   - Cardinality: One-to-Many (1:\*)
   - Cross-filter direction: Both (or Single)
4. **`Dim_Campaigns[Campaign_ID]` (1) -> `Fact_Conversions[Campaign_ID]` (\*)**
   - Cardinality: One-to-Many (1:\*)
   - Cross-filter direction: Single
5. **`Dim_Campaigns[Campaign_ID]` (1) -> `Fact_AB_Testing[Campaign_ID]` (\*)**
   - Cardinality: One-to-Many (1:\*)
   - Cross-filter direction: Single

---

## 3. Recommended Power BI Report Pages & Visual Layout

### Page 1: Executive Growth Overview
- **Header Card KPIs**: Total Emails Sent (`[Total Emails Sent]`), Delivery Rate (`[Delivery Rate %]`), Open Rate (`[Open Rate %]`), Reply Rate (`[Reply Rate %]`), Total Pipeline (`[Total Pipeline Value]`).
- **Funnel Visual**: Stages from Sent -> Delivered -> Opened -> Clicked -> Replied -> Positive -> Converted.
- **Line & Clustered Column Chart**: X-axis: `Sent_Date (Month)`, Columns: `Delivered`, Line: `Reply Rate %`.
- **Donut Chart**: Reply Sentiment distribution (`Reply_Type`: Positive, Neutral, Negative, OOO).

### Page 2: Campaign Deep-Dive & Sequences
- **Matrix Visual**: Rows: `Campaign_Name`, Columns: KPIs (`Delivered`, `Open Rate %`, `Reply Rate %`, `Positive Reply Rate %`, `Pipeline Value`).
- **Bar Chart**: Sequence touchpoint performance (Step 1 vs Step 2 vs Step 3).
- **Slicers**: `Target_Industry`, `Campaign_Status`, `Sales_Region`.

### Page 3: A/B Testing & Lift Lab
- **Clustered Bar Chart**: Comparing Variant A vs Variant B open rates and reply rates per campaign.
- **Table / KPI Cards**: Displaying `[AB Relative Lift %]`, Test Variable, and Primary Winner tag.

### Page 4: Audience & TAM Segmentation
- **Treemap Visual**: Category: `Company_Industry`, Details: `Company_Size_Tier`, Values: `Total Positive Replies`.
- **Heatmap / Matrix**: Rows: `Job_Title` / `Seniority_Level`, Columns: `Company_Industry`, Values: `Reply Rate %`.
- **Scatter Plot**: X-axis: `Open Rate %`, Y-axis: `Reply Rate %`, Size: `Pipeline Value`, Legend: `Lead_Source`.

---

## 4. How to Import into Power BI Desktop
1. Open **Power BI Desktop**.
2. Click **Get Data** -> **Text/CSV**.
3. Select the 6 CSV files from `data/exports/`.
4. In the Power Query editor, verify data types:
   - `Sent_Date`, `Conversion_Date` -> Date
   - `Delivery_Status`, `Open_Status`, `Click_Status`, `Reply_Status`, `Bounce_Status` -> Whole Number (0 or 1)
   - `Opportunity_Value` -> Fixed Decimal / Currency
5. Click **Close & Apply**.
6. Switch to the **Model View** and confirm relationships match Section 2.
7. Create a dedicated `_Measures` table and copy the formulas from `powerbi/dax_measures.md`.

