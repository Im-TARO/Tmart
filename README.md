![logo](images/ChatGPT_Tmart_logo_sm.png)

# Welcome to the Tmart Project

![Data](https://img.shields.io/badge/Data-Synthetic-white?style=plastic&logoColor=white&logoSize=auto&labelColor=orange)
![MySQL](https://img.shields.io/badge/MySQL-Database-white?style=plastic&logo=mysql&logoColor=white&logoSize=auto&labelColor=blue)
![Python](https://img.shields.io/badge/Python-Language-white?style=plastic&logo=python&logoColor=white&logoSize=auto&labelColor=yellow)
![Tableau](https://img.shields.io/badge/Tableau-Visualization-white?style=plastic&logoColor=white&logoSize=auto&labelColor=blue)
![Excel](https://img.shields.io/badge/Excel-Tool-white?style=plastic&logoColor=white&logoSize=auto&labelColor=green)
![Dataoi](https://img.shields.io/badge/draw.io-Tool-white?style=plastic&logoColor=white&logoSize=auto&labelColor=orange)

# :pushpin: Overview

Tmart is a simulated retail (grocery) data project that simulates the backend database of a small grocery and household goods store.

The project includes relational database design, synthetic data generation, and transactional order simulation using MySQL and Python.  Rather than relying on a prebuilt dataset, custom Python generators were developed to create realistic data including products, customers order, shipments, cancellations, and customer purchasing behavior.

The database schema, product hierarchy, and business rules were intentionally designed to support real scenarios, such as:

- customer behavior
- sales trends
- order fulfillment and cancellation analysis

ChatGPT was used to accelerate the data generation.

<!-- ![Status](https://img.shields.io/badge/Project-Complete-brightgreen)
![Power BI](https://img.shields.io/badge/Visualization-Power%20BI-F2C811?logo=powerbi&logoColor=black) -->

### :link: Links

[![Tableau](https://go-skill-icons.vercel.app/api/icons?i=tableau&theme=dark)](https://public.tableau.com/views/Tmart/Sheet1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
[![LinkedIn](https://skillicons.dev/icons?i=linkedin&theme=dark&perline=15)](https://www.linkedin.com/in/robinsontd/)
[![GitHub](https://skillicons.dev/icons?i=github&theme=dark&perline=15)](https://github.com/Im-TARO)

<br>

# :dart: Objectives

- Design a scalable retail database schema
- Generate realistic, high-volume data
- Simulate real-world business scenarios
- Enable analytics-ready datasets

<br>

# 🚀 Future Enhancements

- seasonal demand
- historical pricing
- promotions / discounts
- inventory tracking
- dashboards
- automation

<br>

# :file_folder: Tmart's transactional database

Create the DB structure for Tmart

<details>
<summary>Expand to view details</summary>

## Table of Contents

- [Schema Diagram](#schema-diagram)
- [Data Dictionary](#data-dictionary)
- [Data Generation](#data-generation)
- [Data Changes](#data-changes)
- [Generate CSV Files](#generate-csv-files)

## Schema Diagram

[__Click to view the DDL__](sql/Tmart_db/create_db_tmart.sql)

![ER Diagram](images/Tmart_ER_Diagram.png)

## Data Dictionary

| Table Name (click to view) | Description |
| --- | --- |
| [customers](#customers) | Stores one record for each customer |
| [orders](#orders) | Stores one record per order placed |
| [order_items](#order_items) | Stores one record per product line within an order |
| [products](#products) | Stores one record per product |
| [products_subcategories](#products_subcategories) | Lookup table mapping products to their subcategories |
| [products_categories](#products_categories) | Top-level product classification |

## customers

Stores one record for each customer, a customer may be active or inactive.

<details>
<summary>Expand to view details</summary>

Primary Key: `customer_id`

| Column | Data Type | Nullable | Description | Example |
| -- | -- | -- | -- | -- |
| `customer_id` | INT | No | Unique identifier for each customer. AUTO_INCREMENT | `1001` |
| `first_name` | VARCHAR(50) | No | Customer's first name | `John` |
| `last_name` | VARCHAR(50) | No | Customer's last name | `Doe` |
| `gender` | CHAR(1) | Yes | Customer's self-reported gender. | `M`, `F` |
| `phone_number` | VARCHAR(12) | Yes | Customer's self-reported gender. | `555-123-1234` |
| `email` | VARCHAR(255) | Yes | Customer's email address | `name@domain.com` |
| `address` | VARCHAR(200) | Yes | Customer's street address | `Austin` |
| `city` | VARCHAR(100) | Yes | City of the customer's primary address. | `Austin` |
| `state` | VARCHAR(100) | Yes | US state of the customer's primary address. Standardized to uppercase abbreviation. | `TX` |
| `zipcode` | VARCHAR(10) | Yes | Zipcode of the customer's primary address. | `00000` |
| `county` | VARCHAR(50) | Yes | County of the customer's primary address. | `Travis` |
| `dob` | DATE | Yes | Customer's date of birth | `1985-06-14` |
| `is_active` | TINYINT | Yes | Flag indicating whether the customer is currently available. `1` = active, `0` = inactive.| `1` |
| `loyalty_member` | TINYINT | Yes | Flag indicating whether the customer is a loyalty member. `1` = yes, `0` = no. | `0` |
| `date_created` | DATETIME | No | Timestamp when the customer account was created | `2023-03-15 09:22:00` |
| `date_inactive` | DATETIME | Yes | Timestamp when the customer account was deactivated. `NULL` indicates the customer is currently active. | `2024-11-01 00:00:00` |
| `date_updated` | DATETIME | No | Timestamp when the customer account was last updated. | `2024-11-01 00:00:00` |

</details>

## orders

Stores one record per order placed. Each order belongs to one customer and may contain one or more line items in `order_items`.

<details>
<summary>Expand to view details</summary>

Primary Key: `order_id`  
Foreign Key: `customer_id` &xrarr; `customers.customer_id`

| Column | Data Type | Nullable | Description | Example |
| --- | --- | --- | --- | --- |
| `order_id` | INT | No | Unique identifier for each order. AUTO_INCREMENT | `5001` |
| `customer_id` | INT | No | References the customer who placed the order. Foreign key to `customers`. | `1001` |
| `order_date` | DATETIME | No | Timestamp when the order was placed. | `2024-02-10 14:35:22` |
| `total_amount` | DECIMAL(10,2) | No | Sum of `line_total` for all non-canceled items in the order. Does not include delivery cost.  | `87.45` |
| `delivery_cost` | DECIMAL(10,2) | No | Delivery fee charged to the customer | `5.00` |
| `date_created` | DATETIME | No | Timestamp when the order record was inserted. Matches `order_date` in the synthetic dataset. | `2024-02-10 14:35:22` |
| `date_updated` | DATETIME | No | Timestamp when the order was last updated. | `2024-11-01 00:00:00` |

### Delivery Cost Tiers

| Order Total | Loyalty Member | Non-loyalty Member |
| --- | ---: | ---: |
| **>= 75** | $0 | $0 |
| **>= 50** | $0 | $5 |
| **>= 25** | $5 | $10 |
| **> 0** | $10 | $25 |

</details>

## order_items

Stores one record per product line within an order. An order may have multiple line items. Each item has its own fulfillment status and set of date timestamps.

<details>
<summary>Expand to view details</summary>

Primary Key: `order_item_id`  
Foreign Keys:  
- `order_id` &xrarr; `orders.order_id`  
- `product_id` &xrarr; `products.product_id`

| Column | Data Type | Nullable | Description | Example |
| -------- | ----------- | ---------- | ------------- | --------- |
| `order_item_id` | INT | No | Unique identifier for each order line item. AUTO_INCREMENT | `10001` |
| `order_id` | INT | No | References the parent order. Foreign key to `orders`. | `5001` |
| `product_id` | INT | No | References the product ordered. Foreign key to `products`. | `201` |
| `quantity` | INT | No | Number of units ordered for this line item. | `3` |
| `unit_price` | DECIMAL(10,2) | No | Actual price paid per unit at time of purchase. May differ from `products.price` due to a simulated ±10% price variance representing promotions or price drift. | `4.49` |
| `line_total` | DECIMAL(10,2) | No | Total value for this line item. Calculated as `unit_price × quantity`. | `13.47` |
| `item_status` | VARCHAR(20) | No | Fulfillment status of the line item. | `Delivered` |
| `ship_date` | DATETIME | Yes | Timestamp when the item was shipped. Populated for `Delivered` and `Shipped` items only. `NULL` for `Canceled` items. | `2024-02-12 10:15:00` |
| `delivered_date` | DATETIME | Yes | Timestamp when the item was delivered. Populated for `Delivered` items only. Items shipped on the same day share the same `delivered_date`. | `2024-02-15 00:00:00` |
| `canceled_date` | DATETIME | Yes | Timestamp when the item was canceled. Populated for `Canceled` items only.  | `2024-02-11 00:00:00` |
| `date_created` | DATETIME | No | Timestamp when the record was inserted. Matches `order_date` of the parent order in the synthetic dataset. | `2024-02-10 14:35:22` |
| `date_updated` | DATETIME | No | Timestamp when the order item was last updated. | `2024-11-01 00:00:00` |

### Date Population Rules by Status:

| Value | Description | ship_date | delivered_date | canceled_date | Included in total_amount |
| ----- | ----------- | --------- | -------------- | ------------- | ------------------------- |
| `Delivered` | Item fulfilled end-to-end | Populated | Populated | NULL | Yes |
| `Shipped` | Item in transit, not yet delivered | Populated | NULL | NULL | Yes |
| `Canceled` | Item canceled before fulfillment | NULL | NULL | Populated | No |

</details>

## products

Stores one record per product in the catalog. Products belong to a subcategory which rolls up to a category.

<details>
<summary>Expand to view details</summary>

Primary Key: `product_id`  
Foreign Key: `subcategory_id` → `product_subcategories.subcategory_id`

| Column | Data Type | Nullable | Description | Example |
| ------ | --------- | -------- | ----------- | ------- |
| `product_id` | INT | No | Unique identifier for each product. AUTO_INCREMENT | `201` |
| `subcategory_id` | INT | No | References the product subcategory. Foreign key to `product_subcategories`. | `12` |
| `name` | VARCHAR(300) | No | Full product name as displayed to customers. | `Organic Whole Milk 1 Gallon` |
| `brand` | VARCHAR(100) | Yes | Brand or manufacturer name. | `Horizon Organic` |
| `sku` | VARCHAR(50) | Yes | Stock Keeping Unit — unique product identifier used in inventory management. | `MILK-HOR-001` |
| `unit_size` | VARCHAR(50) | Yes | Package size or weight description. | `1 gallon`, `12 oz`, `500g` |
| `price` | DECIMAL(10,2) | No | Current list price of the product. | `5.99` |
| `stock_quantity` |INT | No | Current stock level | `100` |
| `is_active` | TINYINT(1) | No | Flag indicating whether the product is currently available. `1` = active, `0` = inactive. | `1` |
| `date_created` | DATETIME | No | Timestamp when the product was added to the catalog. | `2023-01-01 00:00:00` |
| `date_inactive` | DATETIME | Yes | Timestamp when the product was discontinued or delisted. `NULL` indicates the product is currently active. | `2024-06-30 00:00:00` |
| `date_updated` | DATETIME | No | Timestamp when the product was last updated. | `2024-11-01 00:00:00` |

### Notes -

- `is_active = 1` - products are the only ones eligible for new order generation
- `unit_price` in `order_items` - reflects the price at time of sale, not the current `products.price`

</details>

## products_subcategories

Lookup table mapping products to their subcategories. Each subcategory belongs to one parent category.

<details>
<summary>Expand to view details</summary>

Primary Key: `subcategory_id`  
Foreign Key: `category_id` &xrarr; `products_categories.category_id`

| Column | Data Type | Nullable | Description | Example |
| --- | --- | --- | --- | --- |
| `subcategory_id` | INT | No | Unique identifier for each product subcategory. | `12` |
| `category_id` | INT | No | References the parent category. Foreign key to `products_categories`. | `3` |
| `name` | VARCHAR(100) | No | Subcategory display name. | `Dairy` |
| `description` | VARCHAR(255) | Yes | Category description. | `Cheese, milk, yogurt, butter, eggs` |

</details>

## products_categories

Top-level product classification. Each category contains one or more subcategories.

<details>
<summary>Expand to view details</summary>

Primary Key: `category_id`

| Column | Data Type | Nullable | Description | Example |
| --- | --- | --- | --- | --- |
| `category_id` | INT | No | Unique identifier for each product category. | `3` |
| `name` | VARCHAR(100) | No | Category display name. | `Food and Beverages` |
| `description` | VARCHAR(255) | Yes | Category description. | `Groceries, snacks, drinks` |

</details>

## Data Generation

### List of Product Categories and Subcategories were provided

Insert into `tmart.product_categories` and `tmart.product_subcategories`

[__Click to view the DML__](sql/Tmart_db/insert_products_categories.sql)

### Asked ChatGPT to create Python scripts to create synthetic data

I reviewed and tailored the scripts to better meet my needs.

<details>
<summary>Expand to view details</summary>

#### Pythons scripts used to create synthetic data

<div align="center">

| [generate_products.py](python/Tmart_db/generate_products.py) | |
| -- | -- |
| Usage | > python .\generate_products.py |
| Output | csv file |
| Insert | [DML command](sql/Tmart_db/insert_products.sql) |
| Tables(s) | `tmart.products` |

| [generate_customers.py](python/Tmart_db/generate_customers.py) | |
| -- | -- |
| Usage | Usage (PowerShell): with optional overrides: <br> > python generate_customers.py \` <br> --num-customers 100 \` <br> --dob-start-year 1960 \` <br>--created-start 2026-03-01 \` <br> --created-end   2026-03-31 |
| Output | csv file |
| Insert | [DML command](sql/Tmart_db/insert_customers.sql) |
| Tables(s) | `tmart.customers` |

| [generate_orders.py](python/Tmart_db/generate_orders.py) | |
| -- | -- |
| Usage | Usage (PowerShell): <br> $env:DB_USER = "your_username" <br> $env:DB_PASSWORD = "your_password" <br> python generate_orders.py 2024-01-01 2024-01-31 5000 <br><br> Arguments: <br> start_date  : Start of the order generation window (YYYY-MM-DD) <br> end_date    : End of the order generation window (YYYY-MM-DD) <br> num_orders  : Number of orders to generate (default: 1000) <br><br> Environment Variables: <br> DB_HOST     : MySQL host (default: localhost) <br>     DB_USER     : MySQL username (required) <br> DB_PASSWORD : MySQL password (required) <br> DB_NAME     : Target database name (default: tmart) |
| Output | none |
| Insert | Python script inserts orders into the MySQL DB |
| Tables(s) | `tmart.orders` `tmart.order_items` |

</div>
</details>

## Data Changes

`tmart.orders.total_amount` - When an order contains **canceled** item line(s), the total amount was incorrect  
`tmart.orders.delivery_cost` - Delivery charges may need to be revised for orders that include **canceled** item lines

<details>
<summary>Expand to view details.</summary>

### Business rule for Delivery Cost

| Order Amount | Delivery Cost | Loyalty Members |
| -- | :--: | :--: |
| Orders >= $75 | Free | Free |
| Orders >= $50 | $5 | Free |
| Orders >= $25 | 10 | $5 |
| Orders < $25 | $25 | $10 |

```sql
-- Select orders with canceled items

WITH canceled_items AS
  (SELECT DISTINCT oi.order_id,
                   o.total_amount,
                   o.delivery_cost,
                   o.customer_id,
                   c.loyalty_member
   FROM order_items oi
   JOIN orders o ON oi.order_id = o.order_id
   JOIN customers c ON o.customer_id = c.customer_id
   WHERE oi.item_status = 'Canceled'),
     new_totals AS
  (SELECT i.order_id,
          group_concat(DISTINCT i.item_status) statuses,
          SUM(CASE
                  WHEN item_status != 'Canceled' THEN line_total
                  ELSE 0
              END) AS new_total
   FROM order_items i
   JOIN canceled_items ci ON i.order_id = ci.order_id
   GROUP BY 1)
SELECT n.order_id,
       n.statuses,
       c.total_amount old_total,
       n.new_total,
       c.loyalty_member,
       c.delivery_cost old_delivery_cost,
       CASE
           WHEN n.new_total = 0 THEN 0
           WHEN c.loyalty_member THEN CASE
                                          WHEN n.new_total >= 50 THEN 0
                                          WHEN n.new_total >= 25 THEN 5
                                          ELSE 10
                                      END
           ELSE CASE
                    WHEN n.new_total >= 75 THEN 0
                    WHEN n.new_total >= 50 THEN 5
                    WHEN n.new_total >= 25 THEN 10
                    ELSE 25
                END
       END new_delivery_cost
FROM new_totals n
JOIN canceled_items c ON n.order_id = c.order_id
LIMIT 15;
```

| order_id | statuses | old_total | new_total | loyalty_member | old_delivery_cost | new_delivery_cost |
| -- | -- | --: | --: | -- | --: | --: |
| 1 | Canceled,Delivered,Shipped | 214.80 | 206.02 | 1 | 0.00 | 0 |
| 6 | Canceled,Delivered,Shipped | 132.53 | 99.89 | 1 | 0.00 | 0 |
| 9 | Canceled | 7.40 | 0.00 | 1 | 25.00 | 0 |
| 10 | Canceled | 38.95 | 0.00 | 1 | 10.00 | 0 |
| 11 | Canceled,Delivered | 171.84 | 145.09 | 1 | 0.00 | 0 |
| 14 | Canceled,Delivered | 245.90 | 228.11 | 1 | 0.00 | 0 |
| 15 | Canceled,Delivered | 74.89 | 26.85 | 1 | 5.00 | 5 |
| 17 | Canceled,Delivered,Shipped | 105.37 | 82.15 | 1 | 0.00 | 0 |
| 18 | Canceled,Delivered,Shipped | 86.71 | 72.85 | 0 | 0.00 | 5 |
| 21 | Canceled,Delivered | 109.87 | 71.56 | 1 | 0.00 | 0 |
| 24 | Canceled,Delivered,Shipped | 64.40 | 41.04 | 0 | 5.00 | 10 |
| 25 | Canceled,Delivered | 42.70 | 33.46 | 0 | 10.00 | 10 |
| 28 | Canceled,Delivered,Shipped | 222.62 | 216.31 | 1 | 0.00 | 0 |
| 29 | Canceled,Delivered | 38.29 | 31.93 | 1 | 10.00 | 5 |
| 31 | Canceled,Delivered,Shipped | 295.28 | 253.68 | 0 | 0.00 | 0 |

### Stored Procedure Created

Created a resuable procedure to fix order totals and delivery fees.  
[__Click to view the DDL__](sql/Tmart_db/create_sp_fix_order_totals.sql)

```sql
CALL tmart.fix_order_totals();
```

### Validation Query

```sql
-- check order.total_amount and order.delivery_cost columns
SELECT o.order_id,
       o.total_amount,
       SUM(CASE
               WHEN oi.item_status != 'Canceled' THEN oi.line_total
               ELSE 0
           END) AS expected_total,
       o.delivery_cost,
       CASE
           WHEN o.total_amount = 0 THEN 0
           WHEN c.loyalty_member THEN CASE
                                          WHEN o.total_amount >= 50 THEN 0
                                          WHEN o.total_amount >= 25 THEN 5
                                          ELSE 10
                                      END
           ELSE CASE
                    WHEN o.total_amount >= 75 THEN 0
                    WHEN o.total_amount >= 50 THEN 5
                    WHEN o.total_amount >= 25 THEN 10
                    ELSE 25
                END
       END expected_delivery_cost
FROM orders o
JOIN customers c ON o.customer_id = c.customer_id
JOIN order_items oi ON o.order_id = oi.order_id
GROUP BY o.order_id
HAVING o.total_amount != expected_total
OR o.delivery_cost != expected_delivery_cost;
```

**0 row(s) returned**

</details>  

</br>

`tmart.customer.gender` - add gender to the customer profile

<details>
<summary>Expand to view details.</summary>

```sql
ALTER TABLE tmart.customers ADD COLUMN gender CHAR(1) NULL AFTER last_name;

UPDATE customers
SET gender = 'M'
WHERE first_name IN ('Andrew', 'Charles', 'Christopher', 'Daniel',
                     'David', 'James', 'Jason', 'John', 'Joseph',
                     'Liam', 'Matthew', 'Michael', 'Randy',
                     'Richard', 'Robert', 'Thomas', 'William');


UPDATE customers
SET gender = 'F'
WHERE first_name NOT IN ('Andrew', 'Charles', 'Christopher', 'Daniel',
                         'David', 'James', 'Jason', 'John', 'Joseph',
                         'Liam', 'Matthew', 'Michael', 'Randy',
                         'Richard', 'Robert', 'Thomas', 'William');

SELECT first_name, last_name, gender
FROM tmart.customers
LIMIT 5;
```

| first_name | last_name | gender |
| --- | --- | --- |
| Joseph | Anderson | M |
| Luna | Green | F |
| Richard | Hernandez | M |
| Richard | Allen | M |
| Susan | Johnson | F |

</details>

## Generate CSV Files

[__Click to view the SQL script__](sql/Tmart_db/create_csv_files.sql)

</details>

<br><br>

# :triangular_ruler: Data Engineering

Make the database ready for analytics, enabling BI reporting and dashboards.

<details>
<summary>Expand to view details.</summary>

## Table of Contents

- [Overview](#overview)
- [Source Data](#source-data)
- [Staging Raw Layer](#1-staging-raw-layer)
- [Staging Intermediate Layer](#2-staging-intermediate-layer)
- [Dimensional Model](#3-dimensional-model)

## Overview

Note: All source data is synthetic, generated via a Python script.  

<div align="center">

| Component | Detail |
| -- | -- |
| Tech Stack | MySQL, Python |
| Source Data | cvs files (exported from Tmart DB) |
| Staging Schema | tmart_staging (raw & intermediate) |
| Analytics Schema | tmart_analytics (analytics-ready) |
| Data Type | Synthetic - generated via Python |

</div>

### General Rules

- Naming Conventions: Use snakecase
- Avoid Reserved Words: Do not use SQL reserved words

<br>

![HighLevelArch](images/HighLevelArchitechture.jpg)

## Source Data

### Files & Row Counts

<div align="center">

| File | Description | Approx. Rows |
| -- | -- | --: |
| tmart_customers.csv | Customer data | 300 |
| tmart_orders.csv | Order header records | 10,200 |
| tmart_order_items.csv | Line-level order detail | 45,473 |
| tmart_products.csv | Product catelog | 10,000 |
| tmart_products_subcategories.csv | Subcategory reference | 40 |
| tmart_products_categories.csv | Category reference | 6 |

</div>

![SourceData](images/Source_Data.jpg)

### Date Range

<div align="center">

| Attribute | Value |
| -- | -- |
| Earliest Order | 2019-06-24 |
| Latest Order | 2026-04-30 |
| Customer Records Span | 2019-01-22 to 2026-04-06 |

</div>

## 1. Staging Raw Layer

The raw staging tables (tmart_raw_*) act as a landing zone for source data, no changes to the data.

<details>
<summary>Expand to view details.</summary>

<br>

**Data Flow**  
![DataFlow1](images/Raw_DataFlow.jpg)

## Rules

- All tables names must start with the source DB name followed by \_raw\_
- <DB name>\_raw\_\<entity\>
  - Example: tmart_raw_customers - customer table from the tmart DB

## Tables of Contents

- [Analysis](#1a-analysis)
- [Create Raw Tables](#1b-create-raw-tables)
- [Data Load](#1c-data-load)
- [Validataion](#1d-validation)

### 1a. Analysis

![SourceData](images/Raw_Layer.jpg)

| csv file | # of rows | Column Headers |
| --- | ---: | --- |
| tmart_customers.csv | 300 | customer_id, first_name, last_name, gender, <br> phone_number, email, address, city, state, zipcode, <br> county, dob, is_active, loyalty_member, date_created, <br> date_inactive, date_updated |
| tmart_order_items.csv | 45,473 | order_item_id, order_id, product_id, <br> quantity, unit_price, line_total, item_status, <br> ship_date, delivered_date, canceled_date, <br> date_created, date_updated |
| tmart_orders.csv | 10,200 | order_id, customer_id, order_date, total_amount, <br> delivery_cost, date_created, date_updated |
| tmart_products. csv | 10,000 | product_id, subcategory_id, name, brand, sku, unit_size, <br> price, stock_quantity, is_active, date_created, <br> date_inactive, date_updated |
| tmart_products_categories.csv | 6 | category_id, name, description |
| tmart_products_subcategories.cvs | 40 | subcategory_id, category_id, name, description |

### 1b. Create Raw Tables

[__Click to view the DDL__](sql/staging_raw/create_raw_tables.sql)

### 1c. Data Load

#### Refreshing the raw tables

[__Click to view the DML__](sql/staging_raw/load_raw_tables.sql)

### 1d. Validation

<ins>__Check Number of Rows__</ins>

| File | # rows file | Table | # rows in DB | column names match |
| --- | ---: | --- | ---: | :---: |
| tmart_customers.csv | 300 | tmart_raw_customers | 300 | Y |
| tmart_order_items.csv | 45,473 | tmart_raw_order_items | 45,473 | Y |
| tmart_orders.csv | 10,200 | tmart_raw_orders | 10,200 | Y |
| tmart_products.csv | 10,000 | tmart_raw_products | 10,000 | Y |
| tmart_products_categories.csv | 6 | tmart_raw_products_categories | 6 | Y |
| tmart_products_subcategories.csv | 40 | tmart_raw_products_subcategories | 40 | Y |

</details>

<br>

## 2. Staging Intermediate Layer

The intermediate staging tables (tmart_int_*) store cleaned and standardized data.

<details>
<summary>Expand to view details.</summary>

<br>

**Data Flow**  
![DataFlow1](images/Int_DataFlow.jpg)

## Tables of Contents

- [Analyze](#2a-analyze)
- [Create Tables](#2b-create-tables)
- [Data Cleaning & Load](#2c-data-cleansing--load)
- [Validataion](#2d-validation)

### 2a. Analyze

#### Table Relationships (Raw Layer)

![RawData](images/Raw_Data.jpg)

### 2b. Create Tables

[__Click to view the DDL__](sql/staging_int/create_int_tables.sql)

### 2c. Data Cleansing & Load

[__Click to view the DML__](sql/staging_int/load_int_tables.sql)

#### Transformations

<div align="center">

| Table | Transformation | Reason |
| -- | -- | -- |
| All | TRIM() on all VARCHAR fields | remove unwanted spaces |
| tmart_int_customers | UPPER(state) <br> gender changed to 'Male','Female','Other','Unknown' <br> date_created and date_inactive cast as date (no time on the datetime column in the raw data) <br> if dob is in the future, set to NULL | Consistent values |
| tmart_int_order_items | UPPER(item_status) | Consistent status values |
| tmart_int_orders | date_created cast as date | no time on the datatime column in the raw data |
| tmart_int_products | UPPER(sku) <br> product_type (derived column: product name minus the brand) <br> date_created and date_inactive cast as date (no time on the datetime column in the raw data)| Consistent values |

</div>


### 2d. Validation
[__Click to view the Validation__](sql/staging_int/int_validation.sql)

</details>

## 3. Dimensional Model

A star schema is built on top of the staging layer to optimize query performance and simplify dashboard development.

<details>
<summary>Expand to view details.</summary>

![coming soon](images/torn_coming_soon.jpg)
[Designed by Freepik](www.freepik.com)

<!--
**Fact Tables**

<ins>fact_orders</ins> - Order header grain (one row per order)

<div align="center">

| Column | Type | Source | Notes |
| -- | -- | -- | -- |
| order_id | INT | orders.order_id | Primary key |
| customer_id | INT | orders.customer_id | FK → dim_customer |
| date_key | INT | Derived from order_date | FK → dim_date |
| total_amount | DECIMAL | orders.total_amount | Product revenue only |
| delivery_cost | DECIMAL | orders.delivery_cost | Customer-facing delivery fee |
| gross_revenue | DECIMAL | total_amount + delivery_cost | Derived field |

</div>

<ins>fact_order_items</ins> - Order item grain (one row per item)

<div align="center">

| Column | Type | Source | Notes |
| -- | -- | -- | -- |
| order_item_id | INT | order_items | Primary key |
| order_id | INT | order_items | FK → fact_orders |
| product_id | INT | order_items | FK → dim_product |
| ship_date_key | INT | Derived from ship_date | FK → dim_date |
| delivered_date_key | INT | Derived from delivered_date | FK → dim_date |
| quantity | INT | order_items.quantity | |
| unit_price | DECIMAL | order_items.unit_price | Actual sell price |
| line_total | DECIMAL | order_items.line_total | |
| item_status | VARCHAR | order_items.item_status | Standardized |
| is_canceled | TINYINT | Derived | 1 if canceled |
| days_to_ship | INT | ship_date - order_date | Derived |
| days_to_deliver | INT | delivered_date - ship_date | Derived |

</div>

**Dimension Tables**

<ins>dim_customer</ins>

<div align="center">

| Column | Type | Source | Notes |
| -- | -- | -- | -- |
| customer_id | INT | customers.customer_id | Primary key |
| gender | VARCHAR | stg_customers.gender | Standardized to uppercase |
| city | VARCHAR | stg_customers.city | |
| state | VARCHAR | stg_customers.state | Standardized to uppercase |
| age | INT | Derived from dob | Calculated at query time |
| age_group | VARCHAR | Derived from age | Under 25, 25-34, etc. |
| is_active | TINYINT | Derived | 1 if date_inactive IS NULL |

</div>

<ins>dim_product</ins>

<div align="center">

| Column | Type | Source | Notes |
| -- | -- | -- | -- |
| product_id | INT | products.product_id | Primary key |
| name | VARCHAR | products.name | |
| brand | VARCHAR | products.brand | |
| list_price | DECIMAL | products.price | Catalog price |
| subcategory_name | VARCHAR | product_subcategories.name | Denormalized |
| category_name | VARCHAR | product_categories.name | Denormalized |
| is_active | TINYINT | Derived from date_inactive | |

</div>

<ins>dim_date</ins>

<div align="center">

| Column | Type | Notes |
| -- | -- | -- |
| date_key | INT | YYYYMMDD format (e.g. 20240115) |
| date | DATE | Actual date |
| year | INT | |
| quarter | INT | 1-4 |
| month_name | VARCHAR | January, February, etc. |
| day_name | VARCHAR | Monday, Tuesday, etc. |
| is_weekend | TINYINT | 1 if Saturday or Sunday |
| is_holiday | TINYINT | 1 if US public holiday |

</div>
-->
</details>

</details>

<br><br>

# :bar_chart: Business Intelligence

<details>
<summary>Expand to view details.</summary>

![coming soon](images/torn_coming_soon.jpg)
[Designed by Freepik](www.freepik.com)

</details>

<br><br>

# :mag: Data Analytics

<details>
<summary>Expand to view details.</summary>

![coming soon](images/torn_coming_soon.jpg)
[Designed by Freepik](www.freepik.com)

</details>

<!--

## :flashlight: Examine the Data (work in progress)

### Customers

<details>
<summary>Expand to view details.</summary>

```sql
-- num of customers and avg age in each county/city
SELECT county,
       city,
       sum(if(is_active, 1, 0)) active_customers,
       round(avg(CASE
                     WHEN is_active THEN YEAR(CURDATE()) - YEAR(dob) - (RIGHT(CURDATE(), 5) < RIGHT(dob, 5))
                 END)) avg_age_active,
       sum(if(is_active, 0, 1)) inactive_customers,
       round(avg(CASE
                     WHEN NOT is_active THEN YEAR(CURDATE()) - YEAR(dob) - (RIGHT(CURDATE(), 5) < RIGHT(dob, 5))
                 END)) avg_age_not_active
FROM customers
GROUP BY 1,
         2
ORDER BY active_customers DESC,
         avg_age_active DESC;
```

| county | city | active_customers | avg_age_active | inactive_customers | avg_age_not_active |
| -- | -- | :--: | :--: | :--: | :--: |
| Wake | Raleigh | 67 | 52 | 24 | 56 |
| Durham | Durham | 22 | 48 | 7 | 56 |
| Wake | Cary | 18 | 59 | 3 | 54 |
| Wake | Garner | 15 | 44 | 5 | 40 |
| Wake | Morrisville | 14 | 65 | 3 | 42 |
| Lee | Sanford | 14 | 45 | 3 | 32 |
| Harnett | Broadway | 13 | 62 | 1 | 63 |
| Johnston | Clayton | 12 | 45 | 1 | 47 |
| Harnett | Erwin | 11 | 55 | 5 | 50 |
| Harnett | Angier | 9 | 50 | 1 | 46 |
| Wake | Apex | 9 | 42 | 1 | 84 |
| Wake | Fuquay-Varina | 8 | 66 | 3 | 34 |
| Wake | Holly Springs | 8 | 58 | 3 | 44 |
| Harnett | Lillington | 8 | 56 | 1 | 80 |
| Harnett | Dunn | 7 | 52 | 4 | 60 |

![Age Gender](images/AgeGenderDistribution.jpg)

![Age Distribution](images/AgeDistributionbyCounty.jpg)
</details>

### Products

<details>
<summary>Expand to view details.</summary>

```sql
SELECT c.name category,
       s.name subcategory,
       sum(is_active) num_active_products,
       count(DISTINCT sku) num_skus,
       count(DISTINCT brand) num_brands
FROM products_categories c
JOIN products_subcategories s ON c.category_id = s.category_id
JOIN products p ON s.subcategory_id = p.subcategory_id
WHERE p.is_active = 1
GROUP BY 1,
         2
ORDER BY 1,
         2
```

| category | subcategory | num_active_products | num_skus | num_brands |
| -- | -- | --: | --: | --: |
| Baby and Childcare | Bathing and Skin Care | 160 | 160 | 10 |
| Baby and Childcare | Beverages | 132 | 132 | 11 |
| Baby and Childcare | Bottles and Cups | 140 | 140 | 10 |
| Baby and Childcare | Diapers and Wipes | 160 | 160 | 10 |
| Baby and Childcare | Food and Formula | 143 | 143 | 11 |
| Baby and Childcare | Health & Wellnes | 80 | 80 | 10 |
| Baby and Childcare | Toys | 180 | 180 | 10 |
| Food and Beverages | Baked Goods | 419| 419 | 11 |
| Food and Beverages | Breakfast and Cereal | 291 | 291 | 11 |
| Food and Beverages | Coffee | 252 | 252 | 11 |
| Food and Beverages | Dairy | 543 | 543 | 11 |
| Food and Beverages | Juice | 342 | 342 | 11 |
| Food and Beverages | Meat | 533 | 533 | 11 |
| Food and Beverages | Pantry | 599 | 599 | 11 |
| Food and Beverages | Produce | 542 | 542 | 11 |
| Food and Beverages | Snacks | 526 | 526 | 11 |
| Food and Beverages | Soda | 442 | 442 | 11 |
| Food and Beverages | Tea | 154 | 154 | 11 |
| Food and Beverages | Water | 165 | 165 | 11 |
| Health and Wellness Products | Allergy and Sinus | 190 | 190 | 10 |
| Health and Wellness Products | Cold and Flu | 180 | 180 | 10 |
| Health and Wellness Products | First Aid | 170 | 170 | 10 |
| Health and Wellness Products | Pain Relief | 200 | 200 | 10 |
| Health and Wellness Products | Vitamins and Supplements | 210 | 210 | 10 |
| Household Goods and Cleaning Products | Air Fresheners | 286 | 286 | 11 |
| Household Goods and Cleaning Products | Cleaning Supplies | 286 | 286 | 11 |
| Household Goods and Cleaning Products | Disposable Tableware | 174 | 174 | 11 |
| Household Goods and Cleaning Products | Food Storages and Wraps | 220 | 220 | 11 |
| Household Goods and Cleaning Products | Laundry | 198 | 198 | 11 |
| Household Goods and Cleaning Products | Paper Products | 189 | 189 | 11 |
| Household Goods and Cleaning Products | Trash Bags | 176 | 176 | 11 |
| Personal Care and Beauty | Bath and Body | 220 | 220 | 11 |
| Personal Care and Beauty | Deodorant | 160 | 160 | 10 |
| Personal Care and Beauty | Hair Care | 210 | 210 | 10 |
| Personal Care and Beauty | Oral Care | 230 | 230 | 10 |
| Personal Care and Beauty | Skin Care | 210 | 210 | 10 |
| Pet Care Products | Birds | 100 | 100 | 10 |
| Pet Care Products | Cats | 213 | 213 | 10 |
| Pet Care Products | Dogs | 215 | 215 | 10 |
| Pet Care Products | Fish | 160 | 160 | 10 |

![ProductCategories](images/ProductCategories.jpg)

</details>

### Orders

<details>
<summary>Expand to view details.</summary>

```sql
WITH cte_years AS
   (SELECT year(o.order_date) yr,
           c.county,
           sum(total_amount + delivery_cost) tot_order_amount
    FROM orders o
    JOIN customers c ON o.customer_id = c.customer_id
    WHERE year(order_date) < year(sysdate())
    GROUP BY 1,
             2),
cte_compare AS
   (SELECT yr,
           county,
           tot_order_amount current_year_amount,
           lag(tot_order_amount) over(PARTITION BY county ORDER BY yr) previous_year_amount,
           tot_order_amount 
                - lag(tot_order_amount) over(PARTITION BY county ORDER BY yr) YoY_order_amount_change
    FROM cte_years)
SELECT yr,
       county,
       current_year_amount total_order_amount,
       YoY_order_amount_change,
       ((current_year_amount - previous_year_amount)/previous_year_amount) * 100 YoY_growth
FROM cte_compare ;
```

| yr | county | total_order_amount | YoY_order_amount_change | YoY_growth |
| -- | -- | --: | --: | --: |
| 2020 | Durham | 1300.29 | NULL | NULL |
| 2021 | Durham | 6397.54 | 5097.25 | 392.008700 |
| 2022 | Durham | 7861.58 | 1464.04 | 22.884400 |
| 2023 | Durham | 17864.47 | 10002.89 | 127.237700 |
| 2024 | Durham | 20481.28 | 2616.81 | 14.648100 |
| 2025 | Durham | 35429.51 | 14948.23 | 72.984800 |
| 2020 | Harnett | 1583.54 | NULL | NULL |
| 2021 | Harnett | 4875.37 | 3291.83 | 207.877900 |
| 2022 | Harnett | 10563.94 | 5688.57 | 116.679800 |
| 2023 | Harnett | 29232.37 | 18668.43 | 176.718400 |
| 2024 | Harnett | 49998.43 | 20766.06 | 71.037900 |
| 2025 | Harnett | 91161.96 | 41163.53 | 82.329600 |
| 2020 | Johnston | 363.85 | NULL | NULL |
| 2021 | Johnston | 146.00 | -217.85 | -59.873600 |
| 2022 | Johnston | 2034.84 | 1888.84 | 1293.726000 |
| 2023 | Johnston | 3656.17 | 1621.33 | 79.678500 |
| 2024 | Johnston | 9990.39 | 6334.22 | 173.247400 |
| 2025 | Johnston | 20158.51 | 10168.12 | 101.779000 |
| 2020 | Lee | 73.94 | NULL | NULL |
| 2021 | Lee | 2491.88 | 2417.94 | 3270.137900 |
| 2022 | Lee | 3466.95 | 975.07 | 39.129900 |
| 2023 | Lee | 10167.32 | 6700.37 | 193.264100 |
| 2024 | Lee | 13994.18 | 3826.86 | 37.638800 |
| 2025 | Lee | 20973.68 | 6979.50 | 49.874300 |
| 2019 | Wake | 966.72 | NULL | NULL |
| 2020 | Wake | 17434.75 | 16468.03 | 1703.495300 |
| 2021 | Wake | 40744.55 | 23309.80 | 133.697400 |
| 2022 | Wake | 69515.97 | 28771.42 | 70.614200 |
| 2023 | Wake | 90985.45 | 21469.48 | 30.884200 |
| 2024 | Wake | 145530.52 | 54545.07 | 59.949200 |
| 2025 | Wake | 246473.68 | 100943.16 | 69.362200 |

![coming soon](images/torn_coming_soon.jpg)
[Designed by Freepik](www.freepik.com)
</details>

## :window: Views

### [v_customer_orders](sql/views/v_customer_orders.sql)

| Column | Datatype | |
| --| -- | -- |
| customer_id | INT | |
| city | VARCHAR | |
| state | CHAR | |
| zipcode | VARCHAR | |
| county | VARCHAR | |
| customer_active | TINYINT | |
| customer_create_date | DATETIME | |
| customer_inactive_date | DATETIME | |
| loyalty_member | TINYINT | |
| order_date| DATETIME | |
| total_amount | DECIMAL | |
| delivery_cost | DECIMAL | |
| product_id | INT | |
| product_name | VARCHAR | |
| category | VARCHAR | |
| subcategory | VARCHAR | |
| item_qty | INT,binary | |
| item_unit_price | DECIMAL | |
| item_line_total | DECIMAL | |
| item_status | VARCHAR | |
| item_ship_date | DATETIME | | 
-->
