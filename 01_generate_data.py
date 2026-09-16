

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

np.random.seed(42)

N_TRANSACTIONS = 20000
FRAUD_RATE = 0.03  # ~3% of transactions are fraudulent

countries = ["UK", "US", "Germany", "France", "Nigeria", "Romania", "India", "Brazil"]
country_fraud_weight = {
    "UK": 0.01, "US": 0.015, "Germany": 0.01, "France": 0.01,
    "Nigeria": 0.08, "Romania": 0.07, "India": 0.03, "Brazil": 0.04
}

channels = ["web", "mobile_app", "in_store"]
channel_fraud_weight = {"web": 0.04, "mobile_app": 0.02, "in_store": 0.005}

payment_methods = ["credit_card", "debit_card", "paypal", "gift_card", "bank_transfer"]
payment_fraud_weight = {
    "credit_card": 0.03, "debit_card": 0.015, "paypal": 0.02,
    "gift_card": 0.09, "bank_transfer": 0.01
}

start_date = datetime(2025, 1, 1)
end_date = datetime(2025, 12, 31)
date_range_days = (end_date - start_date).days

rows = []
for i in range(N_TRANSACTIONS):
    country = np.random.choice(countries, p=[0.30, 0.20, 0.10, 0.10, 0.08, 0.07, 0.08, 0.07])
    channel = np.random.choice(channels, p=[0.55, 0.35, 0.10])
    payment = np.random.choice(payment_methods, p=[0.35, 0.25, 0.20, 0.10, 0.10])

    # base fraud probability blends country/channel/payment risk
    base_prob = (country_fraud_weight[country] + channel_fraud_weight[channel] + payment_fraud_weight[payment]) / 3
    is_fraud = np.random.rand() < base_prob

    # transaction amount: fraud tends to cluster at high or oddly precise amounts
    if is_fraud:
        amount = round(np.random.choice([
            np.random.uniform(200, 900),
            np.random.uniform(900, 3000)
        ]), 2)
    else:
        amount = round(np.random.gamma(shape=2.0, scale=25.0), 2)

    txn_date = start_date + timedelta(
        days=np.random.randint(0, date_range_days),
        hours=np.random.randint(0, 24),
        minutes=np.random.randint(0, 60)
    )

    # fraud is more common late at night
    if is_fraud and np.random.rand() < 0.4:
        txn_date = txn_date.replace(hour=np.random.choice([0, 1, 2, 3, 4]))

    customer_id = np.random.randint(1000, 6000)
    account_age_days = np.random.randint(1, 2000)
    if is_fraud and np.random.rand() < 0.5:
        account_age_days = np.random.randint(0, 15)  # new accounts riskier

    num_items = np.random.randint(1, 8)

    rows.append({
        "transaction_id": f"TXN{100000 + i}",
        "customer_id": customer_id,
        "transaction_date": txn_date.strftime("%Y-%m-%d %H:%M:%S"),
        "amount_gbp": amount,
        "country": country,
        "channel": channel,
        "payment_method": payment,
        "account_age_days": account_age_days,
        "num_items": num_items,
        "is_fraud": int(is_fraud)
    })

df = pd.DataFrame(rows)
df = df.sort_values("transaction_date").reset_index(drop=True)
df.to_csv("transactions.csv", index=False)

print(f"Generated {len(df)} transactions")
print(f"Fraud rate: {df['is_fraud'].mean():.2%}")
print(df.head())
