# Fraud Detection & Risk Dashboard

An end-to-end fraud analytics project covering data generation, SQL investigation,
machine learning risk scoring, and dashboard-ready output — built to mirror the
workflow of a real fraud/risk analyst.

## Pipeline

| Step | File | What it does |
|---|---|---|
| 1 | `01_generate_data.py` | Generates 20,000 synthetic e-commerce transactions with realistic fraud patterns (high-risk countries, gift cards, new accounts, odd-hour purchases) |
| 2 | `02_load_to_sqlite.py` | Loads the transactions into a SQLite database (`fraud.db`) |
| 3 | `03_fraud_queries.sql` | Six SQL investigation queries: fraud rate by channel/country/payment method, a monthly trend using window functions, a CTE-based risk-tier flag, and repeat-offender detection |
| 4 | `04_model_and_score.py` | Trains a Gradient Boosting classifier, evaluates it (precision/recall/ROC-AUC), and scores every transaction with a `fraud_risk_score` and `risk_band` (Low/Medium/High) |

Final output: **`transactions_scored.csv`** — ready to plug straight into Tableau or Power BI.

## Suggested dashboard tiles (Tableau/Power BI)

- KPI cards: total transactions, overall fraud rate, £ value flagged
- Fraud rate by country (map or bar chart)
- Fraud rate by channel and payment method
- Monthly fraud trend line with running total
- Risk-band breakdown (Low/Medium/High) as a donut or stacked bar
- Table of top 20 highest-risk transactions for manual review

## Model results

- Precision: 0.984 | Recall: 0.977 | ROC-AUC: 1.000
- Top predictive feature: transaction amount, followed by account age and new-account flag

**Interview talking point:** the near-perfect ROC-AUC is a sign the synthetic
data has a strong, clean signal (amount is highly separable between classes).
Real-world fraud data is messier — a good way to show interviewers you understand
model evaluation is to explain *why* this score is unrealistically high, and how
you'd sanity-check that on a real dataset (e.g. checking for data leakage,
using time-based train/test splits, monitoring for concept drift).

## CV bullet template

> Built an end-to-end fraud detection pipeline (SQL, Python, Tableau) processing
> 20,000 synthetic transactions; engineered risk features and trained a Gradient
> Boosting model achieving 98% precision, then published an interactive dashboard
> surfacing fraud trends by channel, country, and payment method for risk triage.

Adjust the numbers once you've run it against your own scored output, and swap
in a screenshot link once the Tableau dashboard is published.
