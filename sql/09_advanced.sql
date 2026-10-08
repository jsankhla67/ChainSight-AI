-- 09_advanced_sql.sql
-- Rank → CTE → Running Total → Moving Avg → LAG/LEAD → Growth → Contribution

USE ecommerce_supply_chain;

-- Customer ranking
SELECT
    customer_unique_id,
    Total_Spent,
    ROW_NUMBER() OVER (ORDER BY Total_Spent DESC) AS Customer_Rank
FROM
(
    SELECT
        c.customer_unique_id,
        SUM(p.payment_value) AS Total_Spent
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN payments p
        ON o.order_id = p.order_id
    GROUP BY c.customer_unique_id
) x;

-- Top customers ranking
SELECT
    customer_unique_id,
    Total_Spent,
    RANK() OVER (ORDER BY Total_Spent DESC) AS Ranking
FROM
(
    SELECT
        c.customer_unique_id,
        SUM(payment_value) AS Total_Spent
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN payments p
        ON o.order_id = p.order_id
    GROUP BY customer_unique_id
) t;

-- Seller ranking
SELECT
    seller_id,
    Revenue,
    DENSE_RANK() OVER (ORDER BY Revenue DESC) AS Seller_Rank
FROM
(
    SELECT
        seller_id,
        SUM(price) Revenue
    FROM order_items
    GROUP BY seller_id
) s;

-- Top 10 sellers
WITH SellerRevenue AS
(
    SELECT
        seller_id,
        SUM(price) Revenue
    FROM order_items
    GROUP BY seller_id
)

SELECT *
FROM SellerRevenue
ORDER BY Revenue DESC
LIMIT 10;

-- Monthly revenue
WITH MonthlySales AS
(
    SELECT
        YEAR(o.order_purchase_timestamp) Year,
        MONTH(o.order_purchase_timestamp) Month,
        SUM(payment_value) Revenue
    FROM orders o
    JOIN payments p
        ON o.order_id = p.order_id
    GROUP BY Year, Month
)

SELECT *
FROM MonthlySales
ORDER BY Year, Month;

-- Running total
WITH MonthlyRevenue AS
(
    SELECT
        DATE_FORMAT(order_purchase_timestamp, '%Y-%m') Month,
        SUM(payment_value) Revenue
    FROM orders o
    JOIN payments p
        ON o.order_id = p.order_id
    GROUP BY Month
)

SELECT
    Month,
    Revenue,
    SUM(Revenue) OVER (ORDER BY Month) Running_Total
FROM MonthlyRevenue;

-- Moving average
WITH MonthlyRevenue AS
(
    SELECT
        DATE_FORMAT(order_purchase_timestamp, '%Y-%m') Month,
        SUM(payment_value) Revenue
    FROM orders o
    JOIN payments p
        ON o.order_id = p.order_id
    GROUP BY Month
)

SELECT
    Month,
    Revenue,
    AVG(Revenue) OVER (
        ORDER BY Month
        ROWS BETWEEN 2 PRECEDING AND CURRENT ROW
    ) Moving_Average
FROM MonthlyRevenue;

-- Previous month
WITH MonthlyRevenue AS
(
    SELECT
        DATE_FORMAT(order_purchase_timestamp, '%Y-%m') Month,
        SUM(payment_value) Revenue
    FROM orders o
    JOIN payments p
        ON o.order_id = p.order_id
    GROUP BY Month
)

SELECT
    Month,
    Revenue,
    LAG(Revenue) OVER (ORDER BY Month) Previous_Month
FROM MonthlyRevenue;

-- Next month
WITH MonthlyRevenue AS
(
    SELECT
        DATE_FORMAT(order_purchase_timestamp, '%Y-%m') Month,
        SUM(payment_value) Revenue
    FROM orders o
    JOIN payments p
        ON o.order_id = p.order_id
    GROUP BY Month
)

SELECT
    Month,
    Revenue,
    LEAD(Revenue) OVER (ORDER BY Month) Next_Month
FROM MonthlyRevenue;

-- Monthly growth
WITH MonthlyRevenue AS
(
    SELECT
        DATE_FORMAT(order_purchase_timestamp, '%Y-%m') Month,
        SUM(payment_value) Revenue
    FROM orders o
    JOIN payments p
        ON o.order_id = p.order_id
    GROUP BY Month
)

SELECT
    Month,
    Revenue,
    ROUND(
        100 * (
            Revenue -
            LAG(Revenue) OVER (ORDER BY Month)
        )
        /
        LAG(Revenue) OVER (ORDER BY Month),
        2
    ) Growth_Percentage
FROM MonthlyRevenue;

-- Customer quartiles
SELECT
    customer_unique_id,
    Total_Spent,
    NTILE(4) OVER (ORDER BY Total_Spent DESC) Customer_Quartile
FROM
(
    SELECT
        customer_unique_id,
        SUM(payment_value) Total_Spent
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN payments p
        ON o.order_id = p.order_id
    GROUP BY customer_unique_id
) x;

-- Highest value order per customer
SELECT *
FROM
(
    SELECT
        customer_unique_id,
        o.order_id,
        payment_value,
        ROW_NUMBER() OVER (
            PARTITION BY customer_unique_id
            ORDER BY payment_value DESC
        ) rn
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN payments p
        ON o.order_id = p.order_id
) x
WHERE rn = 1;

-- Top product per seller
SELECT *
FROM
(
    SELECT
        seller_id,
        product_id,
        SUM(price) Revenue,
        ROW_NUMBER() OVER (
            PARTITION BY seller_id
            ORDER BY SUM(price) DESC
        ) rn
    FROM order_items
    GROUP BY seller_id, product_id
) x
WHERE rn = 1;

-- Category ranking
SELECT
    product_category_name_english,
    Revenue,
    RANK() OVER (ORDER BY Revenue DESC) Category_Rank
FROM
(
    SELECT
        ct.product_category_name_english,
        SUM(price) Revenue
    FROM order_items oi
    JOIN products p
        ON oi.product_id = p.product_id
    LEFT JOIN category_translation ct
        ON p.product_category_name = ct.product_category_name
    GROUP BY product_category_name_english
) x;

-- Customer contribution
WITH CustomerSales AS
(
    SELECT
        customer_unique_id,
        SUM(payment_value) Revenue
    FROM customers c
    JOIN orders o
        ON c.customer_id = o.customer_id
    JOIN payments p
        ON o.order_id = p.order_id
    GROUP BY customer_unique_id
)

SELECT
    customer_unique_id,
    Revenue,
    ROUND(
        Revenue /
        SUM(Revenue) OVER () * 100,
        2
    ) Contribution_Percentage
FROM CustomerSales;