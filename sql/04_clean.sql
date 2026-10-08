-- 04_clean.sql
-- Short chain: Count → Duplicates → NULLs → Invalid Data → Relationships → Final Checks


USE ecommerce_supply_chain;


-- 1. ROW COUNT CHECK
-- Har table mein kitna data hai wo check kar rahe hain

SELECT 'customers' AS table_name, COUNT(*) AS total_rows FROM customers
UNION ALL
SELECT 'orders', COUNT(*) FROM orders
UNION ALL
SELECT 'products', COUNT(*) FROM products
UNION ALL
SELECT 'sellers', COUNT(*) FROM sellers
UNION ALL
SELECT 'order_items', COUNT(*) FROM order_items
UNION ALL
SELECT 'payments', COUNT(*) FROM payments
UNION ALL
SELECT 'reviews', COUNT(*) FROM reviews
UNION ALL
SELECT 'geolocation', COUNT(*) FROM geolocation
UNION ALL
SELECT 'category_translation', COUNT(*) FROM category_translation;


-- 2. DUPLICATE CHECKS
-- Check kar rahe hain ki important IDs duplicate toh nahi hain

-- Customers
SELECT customer_id, COUNT(*) AS duplicates
FROM customers
GROUP BY customer_id
HAVING COUNT(*) > 1;

-- Orders
SELECT order_id, COUNT(*) AS duplicates
FROM orders
GROUP BY order_id
HAVING COUNT(*) > 1;

-- Products
SELECT product_id, COUNT(*) AS duplicates
FROM products
GROUP BY product_id
HAVING COUNT(*) > 1;

-- Sellers
SELECT seller_id, COUNT(*) AS duplicates
FROM sellers
GROUP BY seller_id
HAVING COUNT(*) > 1;

-- Reviews
SELECT review_id, COUNT(*) AS duplicates
FROM reviews
GROUP BY review_id
HAVING COUNT(*) > 1;


-- 3. NULL VALUE CHECKS
-- Important columns mein missing values check kar rahe hain

SELECT
SUM(customer_id IS NULL) AS customer_id_null,
SUM(customer_unique_id IS NULL) AS customer_unique_id_null,
SUM(customer_city IS NULL) AS customer_city_null,
SUM(customer_state IS NULL) AS customer_state_null
FROM customers;

SELECT
SUM(product_category_name IS NULL) AS category_null,
SUM(product_name_length IS NULL) AS product_name_length_null,
SUM(product_description_length IS NULL) AS description_length_null,
SUM(product_weight_g IS NULL) AS weight_null
FROM products;

SELECT
SUM(order_purchase_timestamp IS NULL) AS purchase_null,
SUM(order_status IS NULL) AS status_null
FROM orders;

SELECT
SUM(payment_type IS NULL) AS payment_type_null,
SUM(payment_value IS NULL) AS payment_value_null
FROM payments;

SELECT
SUM(review_score IS NULL) AS review_score_null
FROM reviews;


-- 4. INVALID VALUES
-- Aise values check kar rahe hain jo logically possible nahi hain

-- Price zero ya negative toh nahi hai
SELECT *
FROM order_items
WHERE price <= 0;

-- Freight negative toh nahi hai
SELECT *
FROM order_items
WHERE freight_value < 0;

-- Product weight valid hai ya nahi
SELECT *
FROM products
WHERE product_weight_g <= 0;

-- Product dimensions valid hain ya nahi
SELECT *
FROM products
WHERE product_length_cm <= 0
OR product_width_cm <= 0
OR product_height_cm <= 0;

-- Payment value valid hai ya nahi
SELECT *
FROM payments
WHERE payment_value <= 0;


-- 5. REVIEW VALIDATION
-- Review score 1 se 5 ke beech hona chahiye

SELECT *
FROM reviews
WHERE review_score NOT BETWEEN 1 AND 5;


-- 6. DATE VALIDATION
-- Order dates ka sequence logically correct hai ya nahi check kar rahe hain

-- Delivery purchase se pehle toh nahi hui
SELECT *
FROM orders
WHERE order_delivered_customer_date < order_purchase_timestamp;

-- Approval purchase se pehle toh nahi hua
SELECT *
FROM orders
WHERE order_approved_at < order_purchase_timestamp;

-- Estimated delivery purchase se pehle toh nahi hai
SELECT *
FROM orders
WHERE order_estimated_delivery_date < order_purchase_timestamp;


-- 7. ORPHAN RECORD CHECKS
-- Check kar rahe hain ki child records ka parent record missing toh nahi hai

-- Aise orders jo kisi customer se connected nahi hain
SELECT o.order_id
FROM orders o
LEFT JOIN customers c
ON o.customer_id = c.customer_id
WHERE c.customer_id IS NULL;

-- Aise order items jo kisi product se connected nahi hain
SELECT oi.product_id
FROM order_items oi
LEFT JOIN products p
ON oi.product_id = p.product_id
WHERE p.product_id IS NULL;

-- Aise order items jo kisi seller se connected nahi hain
SELECT oi.seller_id
FROM order_items oi
LEFT JOIN sellers s
ON oi.seller_id = s.seller_id
WHERE s.seller_id IS NULL;

-- Aise payments jinka order exist nahi karta
SELECT p.order_id
FROM payments p
LEFT JOIN orders o
ON p.order_id = o.order_id
WHERE o.order_id IS NULL;

-- Aise reviews jinka order exist nahi karta
SELECT r.order_id
FROM reviews r
LEFT JOIN orders o
ON r.order_id = o.order_id
WHERE o.order_id IS NULL;


-- 8. ZIP CODE VALIDATION
-- Check kar rahe hain ki zip code valid value mein hai

SELECT *
FROM customers
WHERE customer_zip_code_prefix <= 0;

SELECT *
FROM sellers
WHERE seller_zip_code_prefix <= 0;

SELECT *
FROM geolocation
WHERE geolocation_zip_code_prefix <= 0;


-- 9. CATEGORY VALIDATION
-- Check kar rahe hain ki product ki category translation table mein available hai

SELECT DISTINCT product_category_name
FROM products
WHERE product_category_name IS NOT NULL
AND product_category_name NOT IN
(
SELECT product_category_name
FROM category_translation
);


-- 10. ORDER STATUS DISTRIBUTION
-- Orders ke different status ka count dekh rahe hain

SELECT
order_status,
COUNT(*) AS total_orders
FROM orders
GROUP BY order_status
ORDER BY total_orders DESC;


-- 11. PAYMENT TYPE DISTRIBUTION
-- Kaunsa payment method kitni baar use hua wo check kar rahe hain

SELECT
payment_type,
COUNT(*) AS total_payments
FROM payments
GROUP BY payment_type
ORDER BY total_payments DESC;


-- 12. REVIEW SCORE DISTRIBUTION
-- Har review score ka total count dekh rahe hain

SELECT
review_score,
COUNT(*) AS total_reviews
FROM reviews
GROUP BY review_score
ORDER BY review_score;


-- Data cleaning aur quality checks yaha complete hote hain