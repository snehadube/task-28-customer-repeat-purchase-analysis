SELECT CASE WHEN country='United Kingdom' THEN 'UK' ELSE 'Non-UK' END AS region,
       COUNT(DISTINCT customer_id) AS customers,
       ROUND(100.0*COUNT(DISTINCT CASE WHEN customer_type='Repeat' THEN customer_id END)/COUNT(DISTINCT customer_id),1) AS repeat_rate_pct
FROM (SELECT DISTINCT o.customer_id, o.country, c.customer_type FROM orders o JOIN customer_summary c USING(customer_id))
GROUP BY 1;
