![logo](images/ChatGPT_Tmart_logo_sm.png)

# Welcome to the Tmart Project

![MySQL](https://img.shields.io/badge/Database-MySQL-blue)
![Python](https://img.shields.io/badge/Language-Python-yellow)
![Tableau](https://img.shields.io/badge/Visualization-Tableau-E97627?logo=tableau&logoColor=white)
![Excel](https://img.shields.io/badge/Tool-Excel-217346?logo=microsoft-excel&logoColor=white)
![ChatGPT](https://img.shields.io/badge/AI-ChatGPT-10A37F?logo=openai&logoColor=white)
![Data](https://img.shields.io/badge/Data-Synthetic-orange)
<!-- ![Status](https://img.shields.io/badge/Project-Complete-brightgreen)
![Power BI](https://img.shields.io/badge/Visualization-Power%20BI-F2C811?logo=powerbi&logoColor=black) -->

## :pushpin: Overview

Tmart is a simulated retail (grocery) data project that simulates the backend database of a small grocery and household goods store

## :dart: Objectives

- Design a scalable retail database schema
- Generate realistic, high-volume data
- Simulate real-world business scenarios
- Enable analytics-ready datasets

## :books: Create Schema

1. [Create Schema](sql/schema/create_tmart_db.sql)
2. [Create Product tables](sql/schema/product_tables.sql)
3. [Create Customer table](sql/schema/customer_table.sql)
4. [Create Order tables](sql/schema/order_tables.sql)

## :cd: ER Diagram

![ER Diagram](images/Tmart_ER_Diagram.png)

## :gear: Data Generation

### Product Categories were provided

Insert the Product Categories/Subcategories into then MySQL DB

| SQL | Table | DB export (csv) |
| -- | -- | -- |
| [Insert statement](sql/seed/insert_tmart_products_categories.sql) | tmart.product_categories | [Product Categories export](data/DB_exports/tmart_products_categories_export.csv) |
| | tmart.product_subcategories | [Product Subcategory export](data/DB_exports/tmart_products_subcategories_export.csv) |

### Asked ChatGPT to create python scripts to create synthetic data

I reviewed and tailored the scripts to meet my needs.

| Python script | Output | Insert | Target table | DB export |
| -- | -- | -- | -- | --|
| [generate_products.py](python/generate_tmart_products.py) | [Products csv file](data/raw/tmart_products.csv) | [Insert Products](sql/seed/import_tmart_products.sql) | tmart.products | [Products DB export](data/DB_exports/tmart_products_export.csv) |
| [generate_customers.py](python/generate_customers.py) | [Customer csv file](data/raw/tmart_products.csv) | [Insert Customers](sql/seed/import_customers.sql) | tmart.customers | [Customer DB export](python/DB_exports/generate_customers.py) |
| [generate_orders.py](python/generate_orders.py) | n/a | script inserts data into tables | tmart.orders <br> tmart.order_items | [Orders DB export](data/DB_exports/tmart_orders_export.csv) <br> [Order Items DB export](data/DB_exports/tmart_order_items_export.csv) |

## 🚀 Future Enhancements

- seasonal demand
- promotions / discounts
- inventory tracking
- dashboards
