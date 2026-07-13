# 🏫 School X — CRM Operational Analytics Dashboard

A 10-page interactive analytics dashboard built with Python (Dash/Plotly)
to clean, analyze, and extract actionable business recommendations from
an online school's CRM data.

🔗 **Live demo:** _link to be added after deployment_

## 📌 Project Overview
**Scenario:** analyze a full year (Jan–Dec 2024) of CRM data — leads,
deals, ad spend, and call logs — for an online school, to identify data
quality issues, understand what drives revenue and conversion, and
provide the management team with concrete, actionable recommendations
to improve operational efficiency.

**Data sources:** 4 CRM exports (Deals, Ad Spend, Calls, Contacts),
including both the original raw exports and the cleaned versions, so the
cleaning process itself can be inspected and compared.

## 🎯 Dashboard Pages
1. **Intro** — project scope, dataset period, and tools used
2. **Data Hygiene** — technical data audit comparing raw vs. cleaned
   data across all 4 source tables, surfacing duplicates, inconsistent
   values, and formatting issues
3. **Descriptive Stats** — distribution of initial payments across all
   deals (strip/box plots), category breakdowns
4. **Time Dynamics** — dual-axis chart tracking deal volume against
   call activity over time, to reveal operational trends
5. **Campaign Analysis** — marketing campaign performance and unit
   economics (ROMI %) broken down by traffic source
6. **Unit Economics** — business metrics hierarchy, growth points, and
   explicit hypotheses with proposed validation methods
7. **Performance Analysis** — sales manager efficiency, using violin
   plots (talk time distribution) and box plots (calls-per-deal
   efficiency) to compare individual performance
8. **Growth & Experience** — dual-axis analysis of revenue vs. staff
   count over time, and conversion rate vs. sales tenure (experience
   curve)
9. **Team Analysis** — team composition (donut chart) and a
   multi-dimensional radar chart for resource allocation, with a
   strategic insight callout
10. **Conclusion** — summary of findings and strategic recommendations
    for the management team

## 💡 Key Business Recommendations
- **CRM Data Integrity**: replace manual text-entry fields with dropdown
  selection to prevent data duplication and ensure accurate reporting
- **Rebalance lead distribution** across sales tiers to maximize
  high-performer ROI
- **Invest in onboarding and retention** to build a more experienced,
  senior sales core over time
- **Track monthly**: "team size vs. revenue" and "tenure vs. conversion"
  as ongoing KPIs
- **A/B-test** delay/threshold rules for automated lead reassignment in
  the CRM

## 🛠️ Tech Stack
- Python
- Dash & Plotly (interactive multi-page web app, not a static notebook)
- Pandas / NumPy (data cleaning and transformation)
- Deployed on Render.com

## 📂 Project Structure
```
school-crm-analytics-dash/
├── app.py                    # main Dash app: layout, routing, tab navigation
├── finalizernew.py           # DataFinalizer class: shared data-cleaning logic
├── data_hygiene.py           # Tab 2
├── descriptive_stats.py      # Tab 3
├── time_analysis.py          # Tab 4
├── campaign_analysis.py      # Tab 5
├── unit_economics.py         # Tab 6
├── performance_analysis.py   # Tab 7
├── growth_analysis.py        # Tab 8
├── team_analysis.py          # Tab 9
├── intro_tab.py               # Tab 1
├── conclusion_tab.py          # Tab 10
├── styles.py                  # shared colors and style constants
├── data_utils.py
├── *.xlsx                     # raw and cleaned CRM data exports
├── requirements.txt
└── Procfile                   # deployment config (Render.com)
```

## 🚀 How to Run Locally
1. Clone the repository
   ```
   git clone https://github.com/yourusername/school-crm-analytics-dash.git
   cd school-crm-analytics-dash
   ```
2. Install dependencies
   ```
   pip install -r requirements.txt
   ```
3. Run the app
   ```
   python app.py
   ```
4. Open `http://127.0.0.1:8051` in your browser
   *(note: the app loads several Excel files on startup, including a
   ~96,000-row call log, so the first load can take ~20–30 seconds)*

## 🔒 Data Note
All names in this dataset (sales reps, deal owners) are synthetic
training data, not real individuals. Contact identifiers are anonymized
numeric IDs.

## 💡 What I Learned
- Structuring a multi-page Dash application with shared data-processing
  logic across tabs
- Comparing raw vs. cleaned data explicitly, to make the data-cleaning
  process itself visible and auditable
- Building varied statistical visualizations (violin plots, box plots,
  dual-axis charts, radar charts) matched to the specific question each
  one answers
- Turning descriptive analysis into concrete, testable business
  hypotheses with proposed validation methods
- Deploying a Python web app (not just a notebook) to a live hosting
  service

## 📸 Preview
**Intro**
![Intro tab](screenshot.png)

**Data Hygiene** — completeness audit across all source columns
![Data Hygiene tab](screenshot2.png)

**Time Dynamics** — deal volume vs. calling activity over time
![Time Dynamics tab](screenshot3.png)
