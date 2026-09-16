import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.ensemble import GradientBoostingClassifier
from sklearn.metrics import precision_score, recall_score, roc_auc_score, classification_report

df = pd.read_csv("transactions.csv", parse_dates=["transaction_date"])

# --- Feature engineering ---
df["hour"] = df["transaction_date"].dt.hour
df["is_night"] = df["hour"].isin([0, 1, 2, 3, 4]).astype(int)
df["is_new_account"] = (df["account_age_days"] < 15).astype(int)
df["is_high_value"] = (df["amount_gbp"] > 500).astype(int)
df["is_gift_card"] = (df["payment_method"] == "gift_card").astype(int)

df_model = pd.get_dummies(
    df,
    columns=["country", "channel", "payment_method"],
    drop_first=True
)

feature_cols = [c for c in df_model.columns if c not in [
    "transaction_id", "customer_id", "transaction_date", "is_fraud"
]]

X = df_model[feature_cols]
y = df_model["is_fraud"]

X_train, X_test, y_train, y_test = train_test_split(
    X, y, test_size=0.25, random_state=42, stratify=y
)

model = GradientBoostingClassifier(random_state=42)
model.fit(X_train, y_train)

# --- Evaluate ---
y_pred = model.predict(X_test)
y_proba = model.predict_proba(X_test)[:, 1]

precision = precision_score(y_test, y_pred)
recall = recall_score(y_test, y_pred)
roc_auc = roc_auc_score(y_test, y_proba)

print("=== Model Evaluation ===")
print(f"Precision: {precision:.3f}")
print(f"Recall:    {recall:.3f}")
print(f"ROC-AUC:   {roc_auc:.3f}")
print()
print(classification_report(y_test, y_pred, target_names=["Legit", "Fraud"]))

# --- Score the full dataset for the dashboard ---
df["fraud_risk_score"] = model.predict_proba(X)[:, 1]

def risk_band(score):
    if score >= 0.7:
        return "High"
    elif score >= 0.3:
        return "Medium"
    else:
        return "Low"

df["risk_band"] = df["fraud_risk_score"].apply(risk_band)

output_cols = [
    "transaction_id", "customer_id", "transaction_date", "amount_gbp",
    "country", "channel", "payment_method", "account_age_days", "num_items",
    "is_fraud", "fraud_risk_score", "risk_band"
]
df[output_cols].to_csv("transactions_scored.csv", index=False)

print("\nSaved transactions_scored.csv")
print(df["risk_band"].value_counts())

# --- Feature importance (useful for interview talking points) ---
importances = pd.Series(model.feature_importances_, index=feature_cols).sort_values(ascending=False)
print("\nTop 10 most important features:")
print(importances.head(10))
