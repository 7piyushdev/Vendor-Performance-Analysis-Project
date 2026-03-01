                                                    Vendor Performance Analysis Project

# 📌 Project Overview

This project focuses on analyzing vendor performance by integrating and summarizing data from multiple transactional tables. The objective is to evaluate purchasing behavior, sales performance, freight costs, and pricing efficiency across vendors and brands.

The analysis consolidates data spread across different sources into a single summary view to support business insights and decision-making.

# 📂 Dataset Description

1. Purchases Table

The purchases table contains actual purchase transaction data, including:

Date of purchase

Products (brands) purchased by vendors

Quantity purchased

Amount paid (in dollars)

2. Purchase Prices Table

The purchase_prices table provides product-wise pricing information, including:

Actual product price

Purchase price

Each record in this table is uniquely identified by a vendor–brand combination.
The purchase price used in the purchases table is derived from this dataset.

3. Vendor Invoice Table

The vendor_invoice table aggregates data from the purchases table and includes:

Total quantity purchased
Total dollar amount
Freight cost
This table maintains uniqueness based on vendor and purchase order (PO) number.

4. Sales Table

The sales table captures actual sales transaction data, including:

Brands sold by vendors
Quantity sold
Selling price
Revenue earned

# 🎯 Analysis Objective

Since the data required for analysis is distributed across multiple tables, the primary goal of this project is to create a consolidated summary table that includes:

Purchase transactions made by vendors
Sales transaction details
Freight costs for each vendor
Actual product prices sourced from vendors

This summary enables a holistic evaluation of vendor performance across procurement, logistics, and sales dimensions.

# 🛠 Tools & Technologies

Python
Pandas
Jupyter Notebook
SQL (for data extraction and joins)

# 📌 Notes

Raw datasets are not included in this repository due to size constraints.
The project structure follows best practices for data analytics workflows.
All analysis is reproducible using the provided notebooks and scripts.


# 🚀 Performance Optimization
This query is optimized for handling large-scale datasets where efficiency is critical.

Heavy Joins & Aggregations: The query handles complex joins and aggregations on large datasets like sales and purchases.
Pre-aggregated Results: Storing the results of these computations avoids the need for repeated, expensive calculations.
Comprehensive Analysis: It enables deep-dive analysis into sales, purchases, and pricing strategies across different vendors and brands.
Dashboarding & Reporting: Future-proofing the data by storing it allows for significantly faster loading times in dashboards and reporting tools.
Efficiency: Instead of executing expensive queries for every user request, dashboards can fetch pre-processed data quickly from the vendor_sales_summary table.

# Removed Inconsistensies

dtype change, replace empty with 0 value, extra spaces removed from the names.