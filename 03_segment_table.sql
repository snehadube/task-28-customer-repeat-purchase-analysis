SELECT segment, COUNT(*) AS customers,
       ROUND(100.0*COUNT(*)/(SELECT COUNT(*) FROM customer_summary),1) AS pct_customers,
       SUM(n_orders) AS orders, ROUND(SUM(revenue),0) AS revenue,
       ROUND(100.0*SUM(revenue)/(SELECT SUM(revenue) FROM customer_summary),1) AS pct_revenue,
       ROUND(SUM(revenue)/SUM(n_orders),2) AS aov,
       ROUND(AVG(n_orders),2) AS avg_orders_per_cust
FROM customer_summary GROUP BY segment ORDER BY segment;
