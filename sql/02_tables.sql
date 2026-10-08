-- Database select kar rahe hain

-- Old Tables → Create Tables → Relationships → Indexes



USE ecommerce_supply_chain;


-- Pehle existing tables ko remove kar rahe hain
-- Child tables pehle delete karni padti hain kyunki foreign keys lagi hui hain

DROP TABLE IF EXISTS reviews;
DROP TABLE IF EXISTS payments;
DROP TABLE IF EXISTS order_items;
DROP TABLE IF EXISTS orders;
DROP TABLE IF EXISTS products;
DROP TABLE IF EXISTS sellers;
DROP TABLE IF EXISTS customers;
DROP TABLE IF EXISTS category_translation;
DROP TABLE IF EXISTS geolocation;


-- Customers ki information store karne ke liye table

CREATE TABLE customers (

    customer_id CHAR(32) PRIMARY KEY,

    customer_unique_id CHAR(32) NOT NULL,

    customer_zip_code_prefix INT NOT NULL,

    customer_city VARCHAR(100) NOT NULL,

    customer_state CHAR(2) NOT NULL

);


-- Product categories ko English name se map karne ke liye

CREATE TABLE category_translation (

    product_category_name VARCHAR(100) PRIMARY KEY,

    product_category_name_english VARCHAR(100) NOT NULL

);


-- Products ki basic information store karne ke liye

CREATE TABLE products (

    product_id CHAR(32) PRIMARY KEY,

    product_category_name VARCHAR(100),

    product_name_lenght INT,

    product_description_lenght INT,

    product_photos_qty INT,

    product_weight_g DECIMAL(10,2),

    product_length_cm DECIMAL(10,2),

    product_height_cm DECIMAL(10,2),

    product_width_cm DECIMAL(10,2),

    -- Product category ko category table se connect kar rahe hain
    CONSTRAINT fk_product_category
        FOREIGN KEY (product_category_name)
        REFERENCES category_translation(product_category_name)

);


-- Sellers ki information ke liye

CREATE TABLE sellers (

    seller_id CHAR(32) PRIMARY KEY,

    seller_zip_code_prefix INT,

    seller_city VARCHAR(100),

    seller_state CHAR(2)

);


-- Orders ki information store karne ke liye

CREATE TABLE orders (

    order_id CHAR(32) PRIMARY KEY,

    customer_id CHAR(32) NOT NULL,

    order_status VARCHAR(20),

    order_purchase_timestamp DATETIME,

    order_approved_at DATETIME,

    order_delivered_carrier_date DATETIME,

    order_delivered_customer_date DATETIME,

    order_estimated_delivery_date DATETIME,

    -- Har order ko ek customer se connect kar rahe hain
    CONSTRAINT fk_orders_customer
        FOREIGN KEY (customer_id)
        REFERENCES customers(customer_id)

);


-- Order ke andar kaunse products hain uski information

CREATE TABLE order_items (

    order_id CHAR(32),

    order_item_id INT,

    product_id CHAR(32),

    seller_id CHAR(32),

    shipping_limit_date DATETIME,

    price DECIMAL(10,2),

    freight_value DECIMAL(10,2),

    PRIMARY KEY (order_id, order_item_id),

    -- Order item ko order se connect kar rahe hain
    CONSTRAINT fk_order_items_orders
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id),

    -- Order item ko product se connect kar rahe hain
    CONSTRAINT fk_order_items_products
        FOREIGN KEY (product_id)
        REFERENCES products(product_id),

    -- Order item ko seller se connect kar rahe hain
    CONSTRAINT fk_order_items_sellers
        FOREIGN KEY (seller_id)
        REFERENCES sellers(seller_id)

);


-- Orders ke payment details store karne ke liye

CREATE TABLE payments (

    order_id CHAR(32),

    payment_sequential INT,

    payment_type VARCHAR(30),

    payment_installments INT,

    payment_value DECIMAL(10,2),

    PRIMARY KEY (order_id, payment_sequential),

    -- Payment ko order se connect kar rahe hain
    CONSTRAINT fk_payments_orders
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)

);


-- Customer reviews store karne ke liye

CREATE TABLE reviews (

    review_id CHAR(32) PRIMARY KEY,

    order_id CHAR(32),

    review_score INT,

    review_comment_title TEXT,

    review_comment_message TEXT,

    review_creation_date DATETIME,

    review_answer_timestamp DATETIME,

    -- Review ko order se connect kar rahe hain
    CONSTRAINT fk_reviews_orders
        FOREIGN KEY (order_id)
        REFERENCES orders(order_id)

);


-- Location aur coordinates ki information ke liye

CREATE TABLE geolocation (

    geolocation_zip_code_prefix INT,

    geolocation_lat DECIMAL(10,8),

    geolocation_lng DECIMAL(11,8),

    geolocation_city VARCHAR(100),

    geolocation_state CHAR(2)

);


-- Queries ko fast banane ke liye indexes create kar rahe hain

CREATE INDEX idx_orders_customer
ON orders(customer_id);

CREATE INDEX idx_order_items_product
ON order_items(product_id);

CREATE INDEX idx_order_items_seller
ON order_items(seller_id);

CREATE INDEX idx_payments_order
ON payments(order_id);

CREATE INDEX idx_reviews_order
ON reviews(order_id);

CREATE INDEX idx_products_category
ON products(product_category_name);

CREATE INDEX idx_customer_state
ON customers(customer_state);

CREATE INDEX idx_seller_state
ON sellers(seller_state);


-- Database tables aur indexes yaha complete hote hain