-- A) AOV by customer type
SELECT c.customer_type, COUNT(*) AS orders, ROUND(AVG(o.order_value),2) AS aov
FROM orders o JOIN customer_summary c USING(customer_id) GROUP BY c.customer_type;
