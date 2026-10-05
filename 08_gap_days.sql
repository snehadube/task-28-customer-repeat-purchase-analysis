-- Days between consecutive orders of repeat customers
WITH r AS (SELECT customer_id, order_date,
  LAG(order_date) OVER (PARTITION BY customer_id ORDER BY order_date) prev FROM orders)
SELECT customer_id, julianday(order_date)-julianday(prev) AS gap_days FROM r WHERE prev IS NOT NULL;
