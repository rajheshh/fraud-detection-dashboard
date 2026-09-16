import sqlite3
import pandas as pd

df = pd.read_csv("transactions.csv")

conn = sqlite3.connect("fraud.db")
df.to_sql("transactions", conn, if_exists="replace", index=False)

# quick sanity check
cur = conn.cursor()
cur.execute("SELECT COUNT(*), SUM(is_fraud) FROM transactions")
total, fraud_count = cur.fetchone()
print(f"Loaded {total} rows into fraud.db, {fraud_count} flagged as fraud")

conn.close()
