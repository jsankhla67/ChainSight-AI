-- 05_eda.sql

-- Short chain: Count → Customers/Orders → Location → Products → Payments → Trends → Top Performers


USE ecommerce_supply_chain;


-- 1. TOTAL RECORDS IN EACH TABLE

-- Har table mein total kitne records hain wo dekh rahe hain

SELECT 'Customers' AS Table_Name, COUNT(*) AS Total_Records FROM customers
UNION ALL
SELECT 'Orders', COUNT(*) FROM orders
UNION ALL
SELECT 'Products', COUNT(*) FROM products
UNION ALL
SELECT 'Sellers', COUNT(*) FROM sellers
UNION ALL
SELECT 'Order Items', COUNT(*) FROM order_items
UNION ALL
SELECT 'Payments', COUNT(*) FROM payments
UNION ALL
SELECT 'Reviews', COUNT(*) FROM reviews
UNION ALL
SELECT 'Geolocation', COUNT(*) FROM geolocation
UNION ALL
SELECT 'Category Translation', COUNT(*) FROM category_translation;


-- 2. TOTAL UNIQUE CUSTOMERS
-- Total unique customers count kar rahe hain

SELECT COUNT(DISTINCT customer_unique_id) AS Unique_Customers
FROM customers;


-- 3. TOTAL ORDERS
-- Total orders count kar rahe hain

SELECT COUNT(*) AS Total_Orders
FROM orders;


-- 4. TOTAL PRODUCTS
-- Total products count kar rahe hain

SELECT COUNT(*) AS Total_Products
FROM products;


-- 5. TOTAL SELLERS
-- Total sellers count kar rahe hain

SELECT COUNT(*) AS Total_Sellers
FROM sellers;


-- 6. TOTAL PAYMENTS
-- Total payment records count kar rahe hain

SELECT COUNT(*) AS Total_Payments
FROM payments;


-- 7. TOTAL REVIEWS
-- Total reviews count kar rahe hain

SELECT COUNT(*) AS Total_Reviews
FROM reviews;


-- 8. ORDER STATUS DISTRIBUTION
-- Orders kis status mein kitne hain wo dekh rahe hain

SELECT
order_status,
COUNT(*) AS Total_Orders
FROM orders
GROUP BY order_status
ORDER BY Total_Orders DESC;


-- 9. PAYMENT METHOD DISTRIBUTION
-- Kaunsa payment method kitni baar use hua wo check kar rahe hain

SELECT
payment_type,
COUNT(*) AS Total
FROM payments
GROUP BY payment_type
ORDER BY Total DESC;


-- 10. REVIEW SCORE DISTRIBUTION
-- Har review score ka count dekh rahe hain

SELECT
review_score,
COUNT(*) AS Total
FROM reviews
GROUP BY review_score
ORDER BY review_score;


-- 11. TOP 10 STATES BY CUSTOMERS
-- Sabse zyada customers wale top 10 states dekh rahe hain

SELECT
customer_state,
COUNT(*) AS Total_Customers
FROM customers
GROUP BY customer_state
ORDER BY Total_Customers DESC
LIMIT 10;


-- 12. TOP 10 CUSTOMER CITIES
-- Sabse zyada customers wali top 10 cities dekh rahe hain

SELECT
customer_city,
COUNT(*) AS Customers
FROM customers
GROUP BY customer_city
ORDER BY Customers DESC
LIMIT 10;


-- 13. TOP 10 SELLER STATES
-- Sabse zyada sellers wale top 10 states dekh rahe hain

SELECT
seller_state,
COUNT(*) AS Sellers
FROM sellers
GROUP BY seller_state
ORDER BY Sellers DESC
LIMIT 10;


-- 14. TOP 10 SELLER CITIES
-- Sabse zyada sellers wali top 10 cities dekh rahe hain

SELECT
seller_city,
COUNT(*) AS Sellers
FROM sellers
GROUP BY seller_city
ORDER BY Sellers DESC
LIMIT 10;


-- 15. PRODUCT CATEGORY DISTRIBUTION
-- Kaunsi product categories mein sabse zyada products hain

SELECT
product_category_name,
COUNT(*) AS Products
FROM products
GROUP BY product_category_name
ORDER BY Products DESC
LIMIT 15;


-- 16. CATEGORY NAME WITH ENGLISH TRANSLATION
-- Product category ka original aur English name dono dekh rahe hain

SELECT
p.product_category_name,
c.product_category_name_english,
COUNT(*) AS Total
FROM products p
LEFT JOIN category_translation c
ON p.product_category_name = c.product_category_name
GROUP BY
p.product_category_name,
c.product_category_name_english
ORDER BY Total DESC
LIMIT 20;


-- 17. MONTHLY ORDERS
-- Har month mein kitne orders aaye wo dekh rahe hain

SELECT

YEAR(order_purchase_timestamp) AS Year,

MONTH(order_purchase_timestamp) AS Month,

COUNT(*) AS Orders

FROM orders

GROUP BY Year, Month

ORDER BY Year, Month;


-- 18. YEARLY ORDERS
-- Har year mein kitne orders aaye wo dekh rahe hain

SELECT

YEAR(order_purchase_timestamp) AS Year,

COUNT(*) AS Orders

FROM orders

GROUP BY Year

ORDER BY Year;


-- 19. AVERAGE PAYMENT VALUE
-- Average payment amount calculate kar rahe hain

SELECT

ROUND(AVG(payment_value),2) AS Average_Payment

FROM payments;


-- 20. MIN / MAX PAYMENT
-- Sabse low aur highest payment value check kar rahe hain

SELECT

MIN(payment_value) AS Minimum_Payment,

MAX(payment_value) AS Maximum_Payment

FROM payments;


-- 21. AVERAGE PRODUCT PRICE
-- Products ka average selling price calculate kar rahe hain

SELECT

ROUND(AVG(price),2) AS Average_Product_Price

FROM order_items;


-- 22. MOST EXPENSIVE PRODUCTS SOLD
-- Sabse high price wale top 20 products dekh rahe hain

SELECT

product_id,

MAX(price) AS Highest_Price

FROM order_items

GROUP BY product_id

ORDER BY Highest_Price DESC

LIMIT 20;


-- 23. CHEAPEST PRODUCTS
-- Sabse low price wale top 20 products dekh rahe hain

SELECT

product_id,

MIN(price) AS Lowest_Price

FROM order_items

GROUP BY product_id

ORDER BY Lowest_Price

LIMIT 20;


-- 24. TOP 20 SELLERS BY PRODUCTS SOLD
-- Sabse zyada products sell karne wale top 20 sellers

SELECT

seller_id,

COUNT(*) AS Products_Sold

FROM order_items

GROUP BY seller_id

ORDER BY Products_Sold DESC

LIMIT 20;


-- 25. TOP 20 CUSTOMERS BY NUMBER OF ORDERS
-- Sabse zyada orders karne wale top 20 customers

SELECT

c.customer_unique_id,

COUNT(o.order_id) AS Orders

FROM customers c

JOIN orders o

ON c.customer_id = o.customer_id

GROUP BY c.customer_unique_id

ORDER BY Orders DESC

LIMIT 20;


