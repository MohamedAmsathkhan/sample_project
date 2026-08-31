-- =========================================================
-- SQL Analytics Queries for E-Commerce Dataset
-- Database: ecommerce.db (Table: sales)
-- Can be executed in VS Code using SQLTools or SQLite Viewer
-- =========================================================

-- 1. Total Revenue and Transaction Summary
SELECT 
    COUNT(*) AS total_orders,
    SUM(quantity) AS total_items_sold,
    ROUND(SUM(total_amount), 2) AS grand_total_revenue,
    ROUND(AVG(total_amount), 2) AS avg_order_value
FROM sales
WHERE order_status = 'Completed';


-- 2. Revenue and Orders by Category
SELECT 
    category,
    COUNT(order_id) AS total_orders,
    SUM(quantity) AS units_sold,
    ROUND(SUM(total_amount), 2) AS total_revenue
FROM sales
WHERE order_status = 'Completed'
GROUP BY category
ORDER BY total_revenue DESC;


-- 3. Top 5 Revenue Generating Products
SELECT 
    product_name,
    category,
    unit_price,
    SUM(quantity) AS total_quantity,
    ROUND(SUM(total_amount), 2) AS total_revenue
FROM sales
WHERE order_status = 'Completed'
GROUP BY product_name
ORDER BY total_revenue DESC
LIMIT 5;


-- 4. Customer Spend Analysis (Top Customers)
SELECT 
    customer_name,
    city,
    COUNT(order_id) AS total_purchases,
    ROUND(SUM(total_amount), 2) AS total_spent
FROM sales
WHERE order_status = 'Completed'
GROUP BY customer_name
ORDER BY total_spent DESC;


-- 5. Order Status & Return Rate Breakdown
SELECT 
    order_status,
    COUNT(*) AS total_orders,
    ROUND(COUNT(*) * 100.0 / (SELECT COUNT(*) FROM sales), 2) AS percentage
FROM sales
GROUP BY order_status;
