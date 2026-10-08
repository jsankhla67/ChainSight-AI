-- 07_sales_analytics.sql
-- Revenue → Time → Products → Customers → Payments → KPIs

USE ecommerce_supply_chain;

-- Total revenue
SELECT
    ROUND(SUM(payment_value), 2) AS Total_Revenue
FROM payments;

-- Average order value
SELECT
    ROUND(AVG(payment_value), 2) AS Average_Order_Value
FROM payments;

-- Highest order
SELECT
    MAX(payment_value) AS Highest_Order_Value
FROM payments;

-- Lowest order
SELECT
    MIN(payment_value) AS Lowest_Order_Value
FROM payments;

-- Month-wise sales
SELECT
    YEAR(o.order_purchase_timestamp) AS Year,
    MONTH(o.order_purchase_timestamp) AS Month,
    ROUND(SUM(p.payment_value), 2) AS Revenue
FROM orders o
JOIN payments p
    ON o.order_id = p.order_id
GROUP BY Year, Month
ORDER BY Year, Month;

-- Year-wise sales
SELECT
    YEAR(o.order_purchase_timestamp) AS Year,
    ROUND(SUM(p.payment_value), 2) AS Revenue
FROM orders o
JOIN payments p
    ON o.order_id = p.order_id
GROUP BY Year
ORDER BY Year;

-- Top sellers
SELECT
    oi.seller_id,
    ROUND(SUM(p.payment_value), 2) AS Revenue
FROM order_items oi
JOIN payments p
    ON oi.order_id = p.order_id
GROUP BY oi.seller_id
ORDER BY Revenue DESC
LIMIT 10;

-- Top product categories
SELECT
    ct.product_category_name_english,
    ROUND(SUM(oi.price), 2) AS Revenue
FROM order_items oi
JOIN products pr
    ON oi.product_id = pr.product_id
LEFT JOIN category_translation ct
    ON pr.product_category_name = ct.product_category_name
GROUP BY ct.product_category_name_english
ORDER BY Revenue DESC
LIMIT 10;

-- Top products
SELECT
    product_id,
    ROUND(SUM(price), 2) AS Revenue
FROM order_items
GROUP BY product_id
ORDER BY Revenue DESC
LIMIT 10;

-- Top states
SELECT
    c.customer_state,
    ROUND(SUM(p.payment_value), 2) AS Revenue
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN payments p
    ON o.order_id = p.order_id
GROUP BY customer_state
ORDER BY Revenue DESC
LIMIT 10;

-- Top cities
SELECT
    c.customer_city,
    ROUND(SUM(p.payment_value), 2) AS Revenue
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN payments p
    ON o.order_id = p.order_id
GROUP BY customer_city
ORDER BY Revenue DESC
LIMIT 10;

-- Payment type ke hisaab se sales
SELECT
    payment_type,
    ROUND(SUM(payment_value), 2) AS Revenue,
    COUNT(*) AS Transactions
FROM payments
GROUP BY payment_type
ORDER BY Revenue DESC;

-- Average product price
SELECT
    ROUND(AVG(price), 2) AS Average_Product_Price
FROM order_items;

-- Sabse expensive products
SELECT
    product_id,
    MAX(price) AS Highest_Price
FROM order_items
GROUP BY product_id
ORDER BY Highest_Price DESC
LIMIT 20;

-- Month-wise orders
SELECT
    YEAR(order_purchase_timestamp) AS Year,
    MONTH(order_purchase_timestamp) AS Month,
    COUNT(*) AS Orders
FROM orders
GROUP BY Year, Month
ORDER BY Year, Month;

-- Order status ke hisaab se revenue
SELECT
    o.order_status,
    ROUND(SUM(p.payment_value), 2) AS Revenue
FROM orders o
JOIN payments p
    ON o.order_id = p.order_id
GROUP BY o.order_status
ORDER BY Revenue DESC;

-- Average freight cost
SELECT
    ROUND(AVG(freight_value), 2) AS Average_Freight
FROM order_items;

-- Total freight
SELECT
    ROUND(SUM(freight_value), 2) AS Total_Freight
FROM order_items;

-- Highest value orders
SELECT
    order_id,
    ROUND(SUM(payment_value), 2) AS Order_Value
FROM payments
GROUP BY order_id
ORDER BY Order_Value DESC
LIMIT 10;

-- Main sales KPIs
SELECT
    COUNT(DISTINCT o.order_id) AS Total_Orders,
    COUNT(DISTINCT c.customer_unique_id) AS Customers,
    ROUND(SUM(p.payment_value), 2) AS Revenue,
    ROUND(AVG(p.payment_value), 2) AS Avg_Order_Value
FROM customers c
JOIN orders o
    ON c.customer_id = o.customer_id
JOIN payments p
    ON o.order_id = p.order_id;