-- 1. Fraud rate by channel
SELECT
    channel,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_count,
    ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct
FROM transactions
GROUP BY channel
ORDER BY fraud_rate_pct DESC;

-- 2. Fraud rate by country
SELECT
    country,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_count,
    ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct
FROM transactions
GROUP BY country
ORDER BY fraud_rate_pct DESC;

-- 3. Fraud rate by payment method
SELECT
    payment_method,
    COUNT(*) AS total_transactions,
    SUM(is_fraud) AS fraud_count,
    ROUND(100.0 * SUM(is_fraud) / COUNT(*), 2) AS fraud_rate_pct
FROM transactions
GROUP BY payment_method
ORDER BY fraud_rate_pct DESC;

-- 4. Monthly fraud trend with running total (window functions)
WITH monthly AS (
    SELECT
        strftime('%Y-%m', transaction_date) AS month,
        COUNT(*) AS total_transactions,
        SUM(is_fraud) AS fraud_count
    FROM transactions
    GROUP BY month
)
SELECT
    month,
    total_transactions,
    fraud_count,
    ROUND(100.0 * fraud_count / total_transactions, 2) AS fraud_rate_pct,
    SUM(fraud_count) OVER (ORDER BY month) AS running_fraud_total,
    LAG(fraud_count) OVER (ORDER BY month) AS prev_month_fraud_count
FROM monthly
ORDER BY month;

-- 5. Risk-tier flag using a CTE (buckets transactions by combined risk signals)
WITH risk_flags AS (
    SELECT
        transaction_id,
        customer_id,
        amount_gbp,
        country,
        channel,
        payment_method,
        account_age_days,
        is_fraud,
        CASE WHEN account_age_days < 15 THEN 1 ELSE 0 END AS new_account_flag,
        CASE WHEN payment_method = 'gift_card' THEN 1 ELSE 0 END AS gift_card_flag,
        CASE WHEN amount_gbp > 500 THEN 1 ELSE 0 END AS high_value_flag
    FROM transactions
)
SELECT
    transaction_id,
    customer_id,
    amount_gbp,
    country,
    payment_method,
    (new_account_flag + gift_card_flag + high_value_flag) AS risk_score,
    CASE
        WHEN (new_account_flag + gift_card_flag + high_value_flag) >= 2 THEN 'High'
        WHEN (new_account_flag + gift_card_flag + high_value_flag) = 1 THEN 'Medium'
        ELSE 'Low'
    END AS risk_tier,
    is_fraud
FROM risk_flags
ORDER BY risk_score DESC
LIMIT 100;

-- 6. Repeat-offender detection: customers with more than one fraudulent transaction
SELECT
    customer_id,
    COUNT(*) AS fraud_transaction_count,
    SUM(amount_gbp) AS total_fraud_amount_gbp
FROM transactions
WHERE is_fraud = 1
GROUP BY customer_id
HAVING COUNT(*) > 1
ORDER BY fraud_transaction_count DESC;
