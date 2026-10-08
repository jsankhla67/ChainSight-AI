-- 08_supply_chain_analytics.sql
-- Delivery → Freight → Sellers → Products → Shipping → KPI

USE ecommerce_supply_chain;

-- Average delivery time
SELECT
    ROUND(
        AVG(
            DATEDIFF(
                order_delivered_customer_date,
                order_purchase_timestamp
            )
        ),
        2
    ) AS Avg_Delivery_Days
FROM orders
WHERE order_delivered_customer_date IS NOT NULL;

-- Fastest deliveries
SELECT
    order_id,
    DATEDIFF(
        order_delivered_customer_date,
        order_purchase_timestamp
    ) AS Delivery_Days
FROM orders
WHERE order_delivered_customer_date IS NOT NULL
ORDER BY Delivery_Days
LIMIT 20;

-- Slowest deliveries
SELECT
    order_id,
    DATEDIFF(
        order_delivered_customer_date,
        order_purchase_timestamp
    ) AS Delivery_Days
FROM orders
WHERE order_delivered_customer_date IS NOT NULL
ORDER BY Delivery_Days DESC
LIMIT 20;

-- On time vs late
SELECT
    CASE
        WHEN order_delivered_customer_date <= order_estimated_delivery_date
        THEN 'On Time'
        ELSE 'Late'
    END AS Delivery_Status,
    COUNT(*) AS Orders
FROM orders
WHERE order_delivered_customer_date IS NOT NULL
GROUP BY Delivery_Status;

-- Late delivery %
SELECT
    ROUND(
        100 * SUM(
            CASE
                WHEN order_delivered_customer_date >
                     order_estimated_delivery_date
                THEN 1
                ELSE 0
            END
        ) / COUNT(*),
        2
    ) AS Late_Delivery_Percentage
FROM orders
WHERE order_delivered_customer_date IS NOT NULL;

-- Average freight
SELECT
    ROUND(AVG(freight_value), 2) AS Avg_Freight_Cost
FROM order_items;

-- Total freight
SELECT
    ROUND(SUM(freight_value), 2) AS Total_Freight
FROM order_items;

-- Highest freight orders
SELECT
    order_id,
    freight_value
FROM order_items
ORDER BY freight_value DESC
LIMIT 20;

-- Lowest freight orders
SELECT
    order_id,
    freight_value
FROM order_items
ORDER BY freight_value
LIMIT 20;

-- Top sellers by orders
SELECT
    seller_id,
    COUNT(*) AS Orders
FROM order_items
GROUP BY seller_id
ORDER BY Orders DESC
LIMIT 10;

-- Top sellers by revenue
SELECT
    seller_id,
    ROUND(SUM(price), 2) AS Revenue
FROM order_items
GROUP BY seller_id
ORDER BY Revenue DESC
LIMIT 10;

-- Average items per order
SELECT
    ROUND(AVG(item_count), 2) AS Avg_Items_Per_Order
FROM
(
    SELECT
        order_id,
        COUNT(*) AS item_count
    FROM order_items
    GROUP BY order_id
) x;

-- Heaviest products
SELECT
    product_id,
    product_weight_g
FROM products
ORDER BY product_weight_g DESC
LIMIT 20;

-- Largest products
SELECT
    product_id,
    (
        product_length_cm *
        product_height_cm *
        product_width_cm
    ) AS Volume
FROM products
ORDER BY Volume DESC
LIMIT 20;

-- States with most sellers
SELECT
    seller_state,
    COUNT(*) AS Sellers
FROM sellers
GROUP BY seller_state
ORDER BY Sellers DESC;

-- States with most customers
SELECT
    customer_state,
    COUNT(*) AS Customers
FROM customers
GROUP BY customer_state
ORDER BY Customers DESC;

-- Shipping time
SELECT
    ROUND(
        AVG(
            DATEDIFF(
                shipping_limit_date,
                order_purchase_timestamp
            )
        ),
        2
    ) AS Avg_Days_To_Shipping
FROM order_items oi
JOIN orders o
    ON oi.order_id = o.order_id;

-- Categories with high shipping cost
SELECT
    ct.product_category_name_english,
    ROUND(AVG(oi.freight_value), 2) AS Avg_Freight
FROM order_items oi
JOIN products p
    ON oi.product_id = p.product_id
LEFT JOIN category_translation ct
    ON p.product_category_name = ct.product_category_name
GROUP BY ct.product_category_name_english
ORDER BY Avg_Freight DESC
LIMIT 15;

-- Delivery KPIs
SELECT
    COUNT(*) AS Delivered_Orders,
    ROUND(
        AVG(
            DATEDIFF(
                order_delivered_customer_date,
                order_purchase_timestamp
            )
        ),
        2
    ) AS Avg_Delivery_Days,
    ROUND(
        AVG(
            DATEDIFF(
                order_estimated_delivery_date,
                order_purchase_timestamp
            )
        ),
        2
    ) AS Avg_Estimated_Days
FROM orders
WHERE order_delivered_customer_date IS NOT NULL;

-- Supply chain summary
SELECT
    COUNT(DISTINCT seller_id) AS Total_Sellers,
    COUNT(DISTINCT product_id) AS Total_Products,
    ROUND(AVG(price), 2) AS Avg_Product_Price,
    ROUND(AVG(freight_value), 2) AS Avg_Freight,
    ROUND(MAX(freight_value), 2) AS Max_Freight
FROM order_items;