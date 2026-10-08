-- 03_import.sql
--  CSV → Import → Row Count → Final Check

USE ecommerce_supply_chain;


-- 1. CUSTOMERS

-- Customer data
LOAD DATA LOCAL INFILE '/Users/jatinsankhla/Desktop/E-Commerce-Supply-Chain-Intelligence/data/raw/olist_customers_dataset.csv'
INTO TABLE customers
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
customer_id,
customer_unique_id,
customer_zip_code_prefix,
customer_city,
customer_state
);

-- Kitne rows aaye
SELECT 'Customers' AS Table_Name, COUNT(*) AS Total_Rows
FROM customers;

-- 2. CATEGORY TRANSLATION

-- Category translation data
LOAD DATA LOCAL INFILE '/Users/jatinsankhla/Desktop/E-Commerce-Supply-Chain-Intelligence/data/raw/product_category_name_translation.csv'
INTO TABLE category_translation
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
product_category_name,
product_category_name_english
);

-- Kitne rows aaye
SELECT 'Category Translation' AS Table_Name, COUNT(*) AS Total_Rows
FROM category_translation;


-- 3. PRODUCTS


-- Product data
LOAD DATA LOCAL INFILE '/Users/jatinsankhla/Desktop/E-Commerce-Supply-Chain-Intelligence/data/raw/olist_products_dataset.csv'
INTO TABLE products
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
product_id,
product_category_name,
@product_name_lenght,
@product_description_lenght,
product_photos_qty,
product_weight_g,
product_length_cm,
product_height_cm,
product_width_cm
)
SET
product_name_length = NULLIF(@product_name_lenght,''),
product_description_length = NULLIF(@product_description_lenght,'');

-- Kitne products aaye
SELECT 'Products' AS Table_Name, COUNT(*) AS Total_Rows
FROM products;


-- 4. SELLERS


-- Seller data
LOAD DATA LOCAL INFILE '/Users/jatinsankhla/Desktop/E-Commerce-Supply-Chain-Intelligence/data/raw/olist_sellers_dataset.csv'
INTO TABLE sellers
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
seller_id,
seller_zip_code_prefix,
seller_city,
seller_state
);

-- Kitne sellers aaye
SELECT 'Sellers' AS Table_Name, COUNT(*) AS Total_Rows
FROM sellers;


-- 5. ORDERS


-- Order data
LOAD DATA LOCAL INFILE '/Users/jatinsankhla/Desktop/E-Commerce-Supply-Chain-Intelligence/data/raw/olist_orders_dataset.csv'
INTO TABLE orders
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
order_id,
customer_id,
order_status,
@purchase,
@approved,
@carrier,
@delivered,
@estimated
)
SET
order_purchase_timestamp = NULLIF(@purchase,''),
order_approved_at = NULLIF(@approved,''),
order_delivered_carrier_date = NULLIF(@carrier,''),
order_delivered_customer_date = NULLIF(@delivered,''),
order_estimated_delivery_date = NULLIF(@estimated,'');

-- Kitne orders aaye
SELECT 'Orders' AS Table_Name, COUNT(*) AS Total_Rows
FROM orders;


-- 6. ORDER ITEMS


-- Order items data
LOAD DATA LOCAL INFILE '/Users/jatinsankhla/Desktop/E-Commerce-Supply-Chain-Intelligence/data/raw/olist_order_items_dataset.csv'
INTO TABLE order_items
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
order_id,
order_item_id,
product_id,
seller_id,
@shipping_limit,
price,
freight_value
)
SET
shipping_limit_date = NULLIF(@shipping_limit,'');

-- Kitne order items aaye
SELECT 'Order Items' AS Table_Name, COUNT(*) AS Total_Rows
FROM order_items;

-- =====================================================
-- 7. PAYMENTS
-- =====================================================

-- Payment data
LOAD DATA LOCAL INFILE '/Users/jatinsankhla/Desktop/E-Commerce-Supply-Chain-Intelligence/data/raw/olist_order_payments_dataset.csv'
INTO TABLE payments
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
order_id,
payment_sequential,
payment_type,
payment_installments,
payment_value
);

-- Kitne payments aaye
SELECT 'Payments' AS Table_Name, COUNT(*) AS Total_Rows
FROM payments;

-- =====================================================
-- 8. REVIEWS
-- =====================================================

-- Review data
LOAD DATA LOCAL INFILE '/Users/jatinsankhla/Desktop/E-Commerce-Supply-Chain-Intelligence/data/raw/olist_order_reviews_dataset.csv'
INTO TABLE reviews
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
review_id,
order_id,
review_score,
review_comment_title,
review_comment_message,
@creation,
@answer
)
SET
review_creation_date = NULLIF(@creation,''),
review_answer_timestamp = NULLIF(@answer,'');

-- Kitne reviews aaye
SELECT 'Reviews' AS Table_Name, COUNT(*) AS Total_Rows
FROM reviews;


-- 9. GEOLOCATION


-- Location data
LOAD DATA LOCAL INFILE '/Users/jatinsankhla/Desktop/E-Commerce-Supply-Chain-Intelligence/data/raw/olist_geolocation_dataset.csv'
INTO TABLE geolocation
FIELDS TERMINATED BY ','
ENCLOSED BY '"'
LINES TERMINATED BY '\n'
IGNORE 1 ROWS
(
geolocation_zip_code_prefix,
geolocation_lat,
geolocation_lng,
geolocation_city,
geolocation_state
);

-- Kitne location rows aaye
SELECT 'Geolocation' AS Table_Name, COUNT(*) AS Total_Rows
FROM geolocation;


-- FINAL VALIDATION


-- Tables check
SHOW TABLES;

-- Sabhi tables ka final count
SELECT COUNT(*) AS Customers FROM customers;
SELECT COUNT(*) AS Categories FROM category_translation;
SELECT COUNT(*) AS Products FROM products;
SELECT COUNT(*) AS Sellers FROM sellers;
SELECT COUNT(*) AS Orders FROM orders;
SELECT COUNT(*) AS Order_Items FROM order_items;
SELECT COUNT(*) AS Payments FROM payments;
SELECT COUNT(*) AS Reviews FROM reviews;
SELECT COUNT(*) AS Geolocation FROM geolocation;