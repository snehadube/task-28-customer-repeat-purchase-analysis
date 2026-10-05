-- One row per order (invoice)
DROP VIEW IF EXISTS orders;
CREATE VIEW orders AS
SELECT invoice, customer_id, country, MIN(invoice_date) AS order_date,
       SUM(revenue) AS order_value
FROM transactions GROUP BY invoice, customer_id, country;

-- One row per customer; repeat customer = 2+ distinct orders
DROP VIEW IF EXISTS customer_summary;
CREATE VIEW customer_summary AS
SELECT customer_id, COUNT(*) AS n_orders, SUM(order_value) AS revenue,
       MIN(order_date) AS first_order, MAX(order_date) AS last_order,
       CASE WHEN COUNT(*)>=2 THEN 'Repeat' ELSE 'One-time' END AS customer_type,
       CASE WHEN COUNT(*)=1 THEN '1. One-time (1 order)'
            WHEN COUNT(*)<=3 THEN '2. Occasional (2-3)'
            WHEN COUNT(*)<=9 THEN '3. Regular (4-9)'
            ELSE '4. Loyal (10+)' END AS segment
FROM orders GROUP BY customer_id;
