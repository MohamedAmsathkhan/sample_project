# 📊 Data Analytics Portfolio Project: E-Commerce Sales & Customer Insights

## 📌 Project Overview

This end-to-end Data Analytics project is designed to showcase your skills in **SQL Database Querying**, **Python Data Wrangling**, **Visual Data Exploration**, and **Power BI Dashboard Design**.

You will analyze an E-Commerce store's transactional data to answer real-world business questions:

- What are the monthly revenue trends and growth rates?
- Who are the top 10 revenue-generating products and categories?
- How can we segment customers using **RFM (Recency, Frequency, Monetary)** analysis?
- What are the customer return rates and order status breakdowns?

---

## 🛠️ Tools & Tech Stack Used

| Tool / Technology               | Role in Project                                                                            | Extension / Software Used                      |
| :------------------------------ | :----------------------------------------------------------------------------------------- | :--------------------------------------------- |
| **SQL / SQLite**          | Storing & querying transactional database tables (`orders`, `customers`, `products`) | **SQLTools** & **SQLite Viewer**   |
| **Data Wrangling**        | Cleaning, transforming missing values, formatting dates                                    | **FastWrangler Plus** & **Pandas** |
| **Python**                | Automating analysis, calculating KPIs, exporting clean datasets                            | **Python** extension & `pandas`        |
| **Visualization**         | Building statistical charts and EDA plots                                                  | **Seaborn** & **Matplotlib**       |
| **File Formatting**       | Inspecting raw data and CSV structures                                                     | **Rainbow CSV**                          |
| **Interactive Dashboard** | Building an executive dashboard for stakeholders                                           | **Power BI Desktop**                     |

---

## 📁 Project Folder Structure

```text
data_analytics_project/
├── project_idea.md          # Project documentation (This file)
├── data/
│   ├── raw_sales.csv        # Raw transaction log
│   └── ecommerce.db         # SQLite Relational Database
├── sql/
│   ├── 01_schema.sql        # Table creation scripts
│   └── 02_analysis.sql      # Business SQL queries
├── python/
│   ├── data_cleaner.py      # Python script to clean & transform data
│   └── generate_charts.py   # Python script to generate analytical plots
└── powerbi/
    └── sales_dashboard.pbix # Power BI Interactive Dashboard file
```

---

## 🛢️ 1. Database Schema & Sample SQL Queries

### Relational Schema

* **`customers`**: `customer_id`, `name`, `city`, `state`, `signup_date`
* **`products`**: `product_id`, `product_name`, `category`, `price`
* **`orders`**: `order_id`, `customer_id`, `order_date`, `order_status`
* **`order_items`**: `item_id`, `order_id`, `product_id`, `quantity`, `unit_price`

### Core SQL Business Queries to Implement:

1. **Total Revenue by Product Category**:
   ```sql
   SELECT 
       p.category,
       SUM(oi.quantity * oi.unit_price) AS total_revenue,
       COUNT(DISTINCT o.order_id) AS total_orders
   FROM order_items oi
   JOIN products p ON oi.product_id = p.product_id
   JOIN orders o ON oi.order_id = o.order_id
   WHERE o.order_status = 'Completed'
   GROUP BY p.category
   ORDER BY total_revenue DESC;
   ```
2. **Monthly Sales Trend**:
   ```sql
   SELECT 
       strftime('%Y-%m', o.order_date) AS sales_month,
       ROUND(SUM(oi.quantity * oi.unit_price), 2) AS monthly_revenue
   FROM orders o
   JOIN order_items oi ON o.order_id = oi.order_id
   WHERE o.order_status = 'Completed'
   GROUP BY sales_month
   ORDER BY sales_month ASC;
   ```

---

## 🐍 2. Python Data Wrangling & Exploratory Analysis

Using `pandas` and `seaborn` to perform Exploratory Data Analysis (EDA):

* Clean null values in customer location data.
* Calculate Customer Lifetime Value (CLV).
* Perform **RFM Segmentation** (Segment customers into *VIP*, *Regular*, *At-Risk*, *Lost*).
* Generate plot images:
  * `revenue_by_category.png` (Bar Chart)
  * `monthly_trend.png` (Line Chart)
  * `customer_segments.png` (Pie Chart / Donut Chart)

---

## 📈 3. Power BI Executive Dashboard Requirements

Build a 3-Page Interactive Power BI Report:

1. **Page 1: Executive Summary**
   * **KPI Cards**: Total Revenue, Total Orders, Average Order Value (AOV), Total Customers.
   * **Line Chart**: Monthly Revenue vs. Target.
   * **Donut Chart**: Revenue by Category.
2. **Page 2: Product & Sales Performance**
   * **Bar Chart**: Top 10 Best-Selling Products.
   * **Matrix Table**: Category Sales, Profit Margin, and Return Rates.
   * **Slicers**: Filter by Date Range, Region, and Order Status.
3. **Page 3: Customer Insights**
   * **Treemap**: Customer Segmentation by RFM Score.
   * **Map Visual**: Customer Distribution by State/City.

---

## 🎯 Deliverables & Resume Impact

When completed, this project gives you:

1. A **GitHub Repository** with clean SQL scripts and Python code.
2. A downloadable **Power BI Report (`.pbix`)**.
3. A strong **Portfolio Case Study** for your resume highlighting: SQL Joins/Aggregations, Data Cleaning with Pandas, and Power BI Dashboarding.
