# GroundTruth-AI-Hackathon-Sanya

## GroundTruth H-001: Automated Insight Engine

This project implements an end-to-end **Automated Insight Engine** capable of ingesting one or multiple files (CSV, Excel, SQLite, PDF), performing automated data cleaning, transformation, KPI computation, visualization, LLM‑based insight generation, and exporting a formatted PDF or PowerPoint report.

## Approach

We are building a system that analyzes Facebook ad campaign data to generate insights or predictions (like campaign performance, audience engagement, or ROI). The approach can be summarized in the following steps:

### **1. Data Ingestion**
- Load the dataset (CSV, database, or API) containing campaign metrics.
- Handle missing values, inconsistent columns, and ensure proper formatting for analysis.

### **2. Exploratory Data Analysis (EDA)**
- Examine key metrics (impressions, clicks, conversions, spend).
- Visualize trends, correlations, and distributions to understand patterns and detect anomalies.

### **3. Feature Engineering**
- Derive new metrics if needed (e.g., CTR, conversion rate).
- Encode categorical variables and scale numeric features for modeling.


### **4. Analytics & Visualization Layer**
- Extracts top-level KPIs (impressions, clicks, spend, CTR, CPC, etc.).
- Generates meaningful visualizations like Time-series trends, Top-performing categories/campaigns, Correlation heatmaps (optional).
- Saves all plots to `outputs/figures/`.

### **5. Model Selection**
- Builds a structured prompt using KPIs, patterns, and extracted PDF text.
- Uses **Gemini** to generate concise, actionable insights.

### **6. Automated Report Builder (PPTX / PDF)**
- Creates an executive-style PowerPoint report that contains Title slide, KPI slide, Insights slide, Visuals slide(s).
- Optionally convert PPTX to PDF using system tools.

## Usage

1. Run this command:
   ```bash
   python main.py --inputs data.csv --out outputs/reports/report.pptx



