-- B) AOV of each customer's 1st order vs later orders (repeat customers only)
WITH ranked AS (
  SELECT o.*, ROW_NUMBER() OVER (PARTITION BY customer_id ORDER BY order_date) rn
  FROM orders o JOIN customer_summary c USING(customer_id) WHERE c.customer_type='Repeat')
SELECT CASE WHEN rn=1 THEN 'First order' ELSE 'Repeat orders (2nd+)' END AS order_type,
       COUNT(*) AS orders, ROUND(AVG(order_value),2) AS aov
FROM ranked GROUP BY 1;
