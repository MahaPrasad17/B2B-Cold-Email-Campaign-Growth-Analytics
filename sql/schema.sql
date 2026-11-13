-- =====================================================================
-- B2B Cold Email Campaign & Growth Analytics Platform
-- Relational Database Schema DDL
-- Compatible with SQLite and Microsoft SQL Server (T-SQL)
-- =====================================================================

DROP VIEW IF EXISTS vw_funnel_summary;
DROP VIEW IF EXISTS vw_industry_performance;
DROP VIEW IF EXISTS vw_campaign_kpis;

DROP TABLE IF EXISTS Conversions;
DROP TABLE IF EXISTS AB_Tests;
DROP TABLE IF EXISTS Email_Activities;
DROP TABLE IF EXISTS Leads;
DROP TABLE IF EXISTS Campaigns;

CREATE TABLE Campaigns (
    Campaign_ID VARCHAR(20) PRIMARY KEY,
    Campaign_Name VARCHAR(100) NOT NULL,
    Campaign_Type VARCHAR(50) NOT NULL,
    Target_Industry VARCHAR(50) NOT NULL,
    Campaign_Start_Date DATE NOT NULL,
    Campaign_End_Date DATE NOT NULL,
    Total_Leads INTEGER NOT NULL DEFAULT 0,
    Campaign_Status VARCHAR(20) NOT NULL DEFAULT 'Active',
    Objective TEXT
);

CREATE TABLE Leads (
    Lead_ID VARCHAR(20) PRIMARY KEY,
    First_Name VARCHAR(50),
    Last_Name VARCHAR(50),
    Company_Name VARCHAR(100) NOT NULL,
    Company_Industry VARCHAR(50) NOT NULL,
    Company_Size VARCHAR(20),
    Job_Title VARCHAR(100) NOT NULL,
    Business_Email VARCHAR(150) NOT NULL UNIQUE,
    Country VARCHAR(50) NOT NULL,
    City VARCHAR(50),
    Lead_Source VARCHAR(50) NOT NULL,
    Lead_Created_Date DATE NOT NULL,
    Lead_Status VARCHAR(30) NOT NULL DEFAULT 'New',
    Campaign_ID VARCHAR(20),
    Seniority_Level VARCHAR(50),
    Sales_Region VARCHAR(50),
    Estimated_Revenue_M NUMERIC(10, 2),
    Hiring_Intent_Score INTEGER,
    CONSTRAINT FK_Leads_Campaign FOREIGN KEY (Campaign_ID) REFERENCES Campaigns(Campaign_ID)
);

CREATE TABLE Email_Activities (
    Email_ID VARCHAR(30) PRIMARY KEY,
    Lead_ID VARCHAR(20) NOT NULL,
    Campaign_ID VARCHAR(20) NOT NULL,
    Email_Variant VARCHAR(20) NOT NULL,
    Email_Subject VARCHAR(255) NOT NULL,
    Sent_Date DATE NOT NULL,
    Delivery_Status INTEGER NOT NULL DEFAULT 1 CHECK (Delivery_Status IN (0, 1)),
    Open_Status INTEGER NOT NULL DEFAULT 0 CHECK (Open_Status IN (0, 1)),
    Click_Status INTEGER NOT NULL DEFAULT 0 CHECK (Click_Status IN (0, 1)),
    Reply_Status INTEGER NOT NULL DEFAULT 0 CHECK (Reply_Status IN (0, 1)),
    Reply_Type VARCHAR(30),
    Bounce_Status INTEGER NOT NULL DEFAULT 0 CHECK (Bounce_Status IN (0, 1)),
    Unsubscribe_Status INTEGER NOT NULL DEFAULT 0 CHECK (Unsubscribe_Status IN (0, 1)),
    CONSTRAINT FK_Activity_Lead FOREIGN KEY (Lead_ID) REFERENCES Leads(Lead_ID),
    CONSTRAINT FK_Activity_Campaign FOREIGN KEY (Campaign_ID) REFERENCES Campaigns(Campaign_ID)
);

CREATE TABLE AB_Tests (
    Test_ID VARCHAR(20) PRIMARY KEY,
    Campaign_ID VARCHAR(20) NOT NULL,
    Test_Variable VARCHAR(50) NOT NULL,
    Variant_A TEXT NOT NULL,
    Variant_B TEXT NOT NULL,
    Emails_Delivered_A INTEGER NOT NULL DEFAULT 0,
    Emails_Delivered_B INTEGER NOT NULL DEFAULT 0,
    Opens_A INTEGER NOT NULL DEFAULT 0,
    Opens_B INTEGER NOT NULL DEFAULT 0,
    Replies_A INTEGER NOT NULL DEFAULT 0,
    Replies_B INTEGER NOT NULL DEFAULT 0,
    Clicks_A INTEGER NOT NULL DEFAULT 0,
    Clicks_B INTEGER NOT NULL DEFAULT 0,
    Positive_Replies_A INTEGER NOT NULL DEFAULT 0,
    Positive_Replies_B INTEGER NOT NULL DEFAULT 0,
    Conversions_A INTEGER NOT NULL DEFAULT 0,
    Conversions_B INTEGER NOT NULL DEFAULT 0,
    CONSTRAINT FK_ABTest_Campaign FOREIGN KEY (Campaign_ID) REFERENCES Campaigns(Campaign_ID)
);

CREATE TABLE Conversions (
    Conversion_ID VARCHAR(30) PRIMARY KEY,
    Lead_ID VARCHAR(20) NOT NULL,
    Campaign_ID VARCHAR(20) NOT NULL,
    Conversion_Date DATE NOT NULL,
    Conversion_Status VARCHAR(30) NOT NULL,
    Opportunity_Value NUMERIC(12, 2) NOT NULL DEFAULT 0.00,
    CONSTRAINT FK_Conversion_Lead FOREIGN KEY (Lead_ID) REFERENCES Leads(Lead_ID),
    CONSTRAINT FK_Conversion_Campaign FOREIGN KEY (Campaign_ID) REFERENCES Campaigns(Campaign_ID)
);

CREATE INDEX IDX_Leads_Industry ON Leads(Company_Industry);
CREATE INDEX IDX_Leads_Source ON Leads(Lead_Source);
CREATE INDEX IDX_Leads_Campaign ON Leads(Campaign_ID);
CREATE INDEX IDX_Activity_Lead ON Email_Activities(Lead_ID);
CREATE INDEX IDX_Activity_Campaign ON Email_Activities(Campaign_ID);
CREATE INDEX IDX_Activity_SentDate ON Email_Activities(Sent_Date);
CREATE INDEX IDX_Conversion_Lead ON Conversions(Lead_ID);

CREATE VIEW vw_campaign_kpis AS
SELECT 
    c.Campaign_ID,
    c.Campaign_Name,
    c.Target_Industry,
    COUNT(a.Email_ID) AS Total_Emails_Sent,
    SUM(a.Delivery_Status) AS Total_Delivered,
    SUM(a.Bounce_Status) AS Total_Bounces,
    SUM(a.Open_Status) AS Total_Opens,
    SUM(a.Click_Status) AS Total_Clicks,
    SUM(a.Reply_Status) AS Total_Replies,
    SUM(CASE WHEN a.Reply_Type = 'Positive' THEN 1 ELSE 0 END) AS Total_Positive_Replies,
    SUM(a.Unsubscribe_Status) AS Total_Unsubscribes,
    ROUND(CAST(SUM(a.Delivery_Status) AS FLOAT) / COUNT(a.Email_ID) * 100, 2) AS Delivery_Rate,
    ROUND(CAST(SUM(a.Bounce_Status) AS FLOAT) / COUNT(a.Email_ID) * 100, 2) AS Bounce_Rate,
    ROUND(CAST(SUM(a.Open_Status) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) * 100, 2) AS Open_Rate,
    ROUND(CAST(SUM(a.Reply_Status) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) * 100, 2) AS Reply_Rate,
    ROUND(CAST(SUM(CASE WHEN a.Reply_Type = 'Positive' THEN 1 ELSE 0 END) AS FLOAT) / NULLIF(SUM(a.Delivery_Status), 0) * 100, 2) AS Positive_Reply_Rate
FROM Campaigns c
LEFT JOIN Email_Activities a ON c.Campaign_ID = a.Campaign_ID
GROUP BY c.Campaign_ID, c.Campaign_Name, c.Target_Industry;

