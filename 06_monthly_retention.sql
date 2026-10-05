-- Monthly cohorts: % of cohort customers who ordered again in later months
WITH f AS (SELECT customer_id, substr(first_order,1,7) cohort FROM customer_summary),
m AS (SELECT DISTINCT customer_id, substr(order_date,1,7) ym FROM orders)
SELECT f.cohort, COUNT(DISTINCT f.customer_id) AS cohort_size,
       COUNT(DISTINCT CASE WHEN m.ym>f.cohort THEN m.customer_id END) AS returned_later,
       ROUND(100.0*COUNT(DISTINCT CASE WHEN m.ym>f.cohort THEN m.customer_id END)/COUNT(DISTINCT f.customer_id),1) AS pct_returned
FROM f JOIN m USING(customer_id) GROUP BY f.cohort ORDER BY f.cohort;
