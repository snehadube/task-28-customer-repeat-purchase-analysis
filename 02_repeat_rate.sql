SELECT COUNT(*) AS total_customers,
       SUM(customer_type='Repeat') AS repeat_customers,
       ROUND(100.0*SUM(customer_type='Repeat')/COUNT(*),2) AS repeat_rate_pct
FROM customer_summary;
