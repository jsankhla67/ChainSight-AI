-- 10_views.sql
-- Views → Customer → Sales → Seller → Category → Delivery → Payment → Dashboard

USE ecommerce_supply_chain;

-- Purane views hatao
DROP VIEW IF EXISTS customer_summary;
DROP VIEW IF EXISTS monthly_sales;
DROP VIEW IF EXISTS seller_performance;
DROP VIEW IF EXISTS category_sales;
DROP VIEW IF EXISTS delivery_summary;
DROP VIEW IF EXISTS payment_summary;
DROP VIEW IF EXISTS product_sales;
DROP VIEW IF EXISTS executive_dashboard;

-- Customer summary
CREATE VIEW customer_summary AS
SELECT
    c.customer_unique_id,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(p.payment_value), 2) AS total_spent,
    ROUND(AVG(p.payment_value), 2) AS avg_order_value,
    MAX(o.order_purchase_timestamp) AS last_purchase
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN payments p
    ON o.order_id = p.order_id
GROUP BY c.customer_unique_id;

-- Monthly sales
CREATE VIEW monthly_sales AS
SELECT
    YEAR(o.order_purchase_timestamp) AS sales_year,
    MONTH(o.order_purchase_timestamp) AS sales_month,
    COUNT(DISTINCT o.order_id) AS total_orders,
    ROUND(SUM(p.payment_value), 2) AS revenue
FROM orders o
JOIN payments p
    ON o.order_id = p.order_id
GROUP BY sales_year, sales_month;

-- Seller performance
CREATE VIEW seller_performance AS
SELECT
    oi.seller_id,
    COUNT(DISTINCT oi.order_id) AS total_orders,
    COUNT(oi.product_id) AS products_sold,
    ROUND(SUM(oi.price), 2) AS revenue,
    ROUND(AVG(oi.price), 2) AS avg_product_price
FROM order_items oi
GROUP BY oi.seller_id;

-- Category sales
CREATE VIEW category_sales AS
SELECT
    ct.product_category_name_english,
    COUNT(oi.order_id) AS total_orders,
    ROUND(SUM(oi.price), 2) AS revenue,
    ROUND(AVG(oi.price), 2) AS average_price
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
LEFT JOIN category_translation ct
    ON p.product_category_name = ct.product_category_name
GROUP BY ct.product_category_name_english;

-- Delivery summary
CREATE VIEW delivery_summary AS
SELECT
    order_id,
    order_purchase_timestamp,
    order_delivered_customer_date,
    order_estimated_delivery_date,
    DATEDIFF(
        order_delivered_customer_date,
        order_purchase_timestamp
    ) AS delivery_days,
    CASE
        WHEN order_delivered_customer_date <= order_estimated_delivery_date
        THEN 'On Time'
        ELSE 'Late'
    END AS delivery_status
FROM orders
WHERE order_delivered_customer_date IS NOT NULL;

-- Payment summary
CREATE VIEW payment_summary AS
SELECT
    payment_type,
    COUNT(*) AS transactions,
    ROUND(SUM(payment_value), 2) AS revenue,
    ROUND(AVG(payment_value), 2) AS average_payment
FROM payments
GROUP BY payment_type;

-- Product sales
CREATE VIEW product_sales AS
SELECT
    oi.product_id,
    COUNT(*) AS quantity_sold,
    ROUND(SUM(oi.price), 2) AS revenue,
    ROUND(AVG(oi.price), 2) AS average_price
FROM order_items oi
GROUP BY oi.product_id;

-- Executive dashboard
CREATE VIEW executive_dashboard AS
SELECT
    COUNT(DISTINCT c.customer_unique_id) AS total_customers,
    COUNT(DISTINCT o.order_id) AS total_orders,
    COUNT(DISTINCT oi.product_id) AS total_products,
    COUNT(DISTINCT oi.seller_id) AS total_sellers,
    ROUND(SUM(p.payment_value), 2) AS total_revenue,
    ROUND(AVG(p.payment_value), 2) AS average_order_value
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN payments p
    ON o.order_id = p.order_id
JOIN order_items oi
    ON o.order_id = oi.order_id;

-- Views check
SHOW FULL TABLES
WHERE TABLE_TYPE = 'VIEW';

-- Sample data check
SELECT *
FROM customer_summary
LIMIT 10;

SELECT *
FROM monthly_sales;

SELECT *
FROM seller_performance
ORDER BY revenue DESC
LIMIT 10;

SELECT *
FROM category_sales
ORDER BY revenue DESC
LIMIT 10;

SELECT *
FROM delivery_summary
LIMIT 10;

SELECT *
FROM payment_summary;

SELECT *
FROM product_sales
ORDER BY revenue DESC
LIMIT 10;

SELECT *
FROM executive_dashboard;