![logo](images/ChatGPT_Tmart_logo_sm.png)

# Welcome to the Tmart Project

## :pushpin: Overview

Tmart is a simulated retail (grocery) data project that simulates the backend database of a small grocery and household goods store.

The project includes relational database design, synthetic data generation, and transactional order simulation using MySQL and Python.  Rather than relying on a prebuilt dataset, custom Python generators were developed to create realistic data including products, customers order, shipments, cancellations, and customer purchasing behavior.

The database schema, product hierarchy, and business rules were intentionally designed to support real scenarios, such as:

- customer behavior
- sales trends
- order fulfillment and cancellation analysis

ChatGPT was used to accelerate the data generation.

![MySQL](https://img.shields.io/badge/Database-MySQL-blue)
![Python](https://img.shields.io/badge/Language-Python-yellow)
![Tableau](https://img.shields.io/badge/Visualization-Tableau-E97627?logo=tableau&logoColor=white)
![Excel](https://img.shields.io/badge/Tool-Excel-217346?logo=microsoft-excel&logoColor=white)
![ChatGPT](https://img.shields.io/badge/AI-ChatGPT-10A37F?logo=openai&logoColor=white)
![Data](https://img.shields.io/badge/Data-Synthetic-orange)
<!-- ![Status](https://img.shields.io/badge/Project-Complete-brightgreen)
![Power BI](https://img.shields.io/badge/Visualization-Power%20BI-F2C811?logo=powerbi&logoColor=black) -->

### :link: Links

[![Tableau](https://go-skill-icons.vercel.app/api/icons?i=tableau&theme=dark)](https://public.tableau.com/views/Tmart/Sheet1?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)
[![LinkedIn](https://skillicons.dev/icons?i=linkedin&theme=dark&perline=15)](https://www.linkedin.com/in/robinsontd/)
[![GitHub](https://skillicons.dev/icons?i=github&theme=dark&perline=15)](https://github.com/Im-TARO)

## :dart: Objectives

- Design a scalable retail database schema
- Generate realistic, high-volume data
- Simulate real-world business scenarios
- Enable analytics-ready datasets

## 🚀 Future Enhancements

- seasonal demand
- historical pricing
- promotions / discounts
- inventory tracking
- dashboards

## :file_folder: Create a raw transactional database

<details>
<summary>Expand to view details.</summary>

### Schema

---

<details>
<summary>Expand to view DDL</summary>

```sql
SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema tmart
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `tmart` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

USE `tmart`;

-- -----------------------------------------------------
-- Table `tmart`.`customers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tmart`.`customers` (
  `customer_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `gender` CHAR(1) NULL DEFAULT NULL,
  `phone_number` VARCHAR(12) NULL DEFAULT NULL,
  `email` VARCHAR(255) NULL DEFAULT NULL,
  `address` VARCHAR(200) NULL DEFAULT NULL,
  `city` VARCHAR(100) NULL DEFAULT NULL,
  `state` CHAR(2) NULL DEFAULT NULL,
  `zipcode` VARCHAR(10) NULL DEFAULT NULL,
  `county` VARCHAR(50) NULL DEFAULT NULL,
  `dob` DATE NULL DEFAULT NULL,
  `is_active` TINYINT NULL DEFAULT NULL,
  `loyalty_member` TINYINT NULL DEFAULT NULL,
  `date_created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_inactive` DATETIME NULL DEFAULT NULL,
  `date_updated` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(`customer_id`)
) ENGINE = InnoDB AUTO_INCREMENT = 301 DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Table `tmart`.`products_categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tmart`.`products_categories` (
  `category_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `description` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY(`category_id`)
) ENGINE = InnoDB AUTO_INCREMENT = 7 DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Table `tmart`.`products_subcategories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tmart`.`products_subcategories` (
  `subcategory_id` INT NOT NULL AUTO_INCREMENT,
  `category_id` INT NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `description` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY(`subcategory_id`),
  INDEX `fk_prod_subcategory_category` (`category_id` ASC) VISIBLE,
  CONSTRAINT `fk_prod_subcategory_category` FOREIGN KEY(`category_id`) REFERENCES `tmart`.`products_categories` (`category_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 41 DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Table `tmart`.`products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tmart`.`products` (
  `product_id` INT NOT NULL AUTO_INCREMENT,
  `subcategory_id` INT NOT NULL,
  `name` VARCHAR(300) NOT NULL,
  `brand` VARCHAR(100) NULL DEFAULT NULL,
  `sku` VARCHAR(50) NULL DEFAULT NULL,
  `unit_size` VARCHAR(50) NULL DEFAULT NULL,
  `price` DECIMAL(10, 2) NOT NULL,
  `stock_quantity` INT NOT NULL DEFAULT '0',
  `is_active` TINYINT(1) NOT NULL DEFAULT '1',
  `date_created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_inactive` DATETIME NULL DEFAULT NULL,
  `date_updated` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(`product_id`),
  INDEX `fk_product_subcategory` (`subcategory_id` ASC) VISIBLE,
  CONSTRAINT `fk_product_subcategory` FOREIGN KEY(`subcategory_id`) REFERENCES `tmart`.`products_subcategories` (`subcategory_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 10001 DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Table `tmart`.`orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tmart`.`orders` (
  `order_id` INT NOT NULL AUTO_INCREMENT,
  `customer_id` INT NULL DEFAULT NULL,
  `order_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `total_amount` DECIMAL(10, 2) NULL DEFAULT NULL,
  `delivery_cost` DECIMAL(10, 2) NULL DEFAULT NULL,
  `date_created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_updated` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(`order_id`),
  INDEX `fk_customer` (`customer_id` ASC) VISIBLE,
  CONSTRAINT `fk_customer` FOREIGN KEY(`customer_id`) REFERENCES `tmart`.`customers` (`customer_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 10001 DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Table `tmart`.`order_items`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tmart`.`order_items` (
  `order_item_id` INT NOT NULL AUTO_INCREMENT,
  `order_id` INT NULL DEFAULT NULL,
  `product_id` INT NULL DEFAULT NULL,
  `quantity` INT NULL DEFAULT NULL,
  `unit_price` DECIMAL(10, 2) NULL DEFAULT NULL,
  `line_total` DECIMAL(10, 2) NULL DEFAULT NULL,
  `item_status` VARCHAR(50) NULL DEFAULT NULL,
  `ship_date` DATETIME NULL DEFAULT NULL,
  `delivered_date` DATETIME NULL DEFAULT NULL,
  `canceled_date` DATETIME NULL DEFAULT NULL,
  `date_created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_updated` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(`order_item_id`),
  INDEX `fk_order` (`order_id` ASC) VISIBLE,
  INDEX `pk_products` (`product_id` ASC) VISIBLE,
  CONSTRAINT `fk_order` FOREIGN KEY(`order_id`) REFERENCES `tmart`.`orders` (`order_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `pk_products` FOREIGN KEY(`product_id`) REFERENCES `tmart`.`products` (`product_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 44969 DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;
```

</details>

### Table of Contents

- [customers](#customers)
- [orders](#orders)
- [order_items](#order_items)
- [products](#products)
- [products_subcategories](#products_subcategories)
- [products_categories](#products_categories)
- [Schema Diagram](#schema-diagram)

---

### customers

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

### orders

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

**Delivery Cost Tiers**

| Order Total | Loyalty Member | Non-loyalty Member |
| --- | ---: | ---: |
| **>= 75** | $0 | $0 |
| **>= 50** | $0 | $5 |
| **>= 25** | $5 | $10 |
| **> 0** | $10 | $25 |

</details>

### order_items

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

**Date Population Rules by Status:**

| Value | Description | ship_date | delivered_date | canceled_date | Included in total_amount |
| ----- | ----------- | --------- | -------------- | ------------- | ------------------------- |
| `Delivered` | Item fulfilled end-to-end | Populated | Populated | NULL | Yes |
| `Shipped` | Item in transit, not yet delivered | Populated | NULL | NULL | Yes |
| `Canceled` | Item canceled before fulfillment | NULL | NULL | Populated | No |

</details>

### products

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


**Notes:**
- `is_active = 1` products are the only ones eligible for new order generation
- `unit_price` in `order_items` reflects the price at time of sale, not the current `products.price`


</details>

### products_subcategories

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

### products_categories

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

#### Schema Diagram

![ER Diagram](images/Tmart_ER_Diagram.png)

### Data Generation

---
**Product Categories were provided**

Insert the Product Categories/Subcategories into then MySQL DB

<div align="center">

| SQL | Table(s) |
| -- | -- |
| [Insert statement](sql/seed/insert_tmart_products_categories.sql) | tmart.product_categories <br> tmart.product_subcategories |

</div>

### Asked ChatGPT to create python scripts to create synthetic data

---
I reviewed and tailored the scripts to meet my needs.

<div align="center">

| Python script | Output | Insert | Table(s) |
| -- | -- | -- | -- |
| [generate_products.py](python/generate_tmart_products.py) | [Products csv file](data/raw/tmart_products.csv) | [Insert Products](sql/seed/import_tmart_products.sql) | tmart.products |
| [generate_customers.py](python/generate_customers.py) | [Customer csv file](data/raw/tmart_products.csv) | [Insert Customers](sql/seed/import_customers.sql) | tmart.customers |
| [generate_orders.py](python/generate_orders.py) | n/a | script inserts data into tables | tmart.orders <br> tmart.order_items |

</div>

</details>

## :building_construction: Data Engineering

Make the database analytics-ready for BI reporting and dashboards

<details>
<summary>Expand to view details.</summary>

### Table of Contents

- [Overview](#overview)
- [Source Data](#source-data)
- [Data Audit & Profiling](#data-audit--profiling)
- [Staging Layer](#staging-layer)
- [Dimensional Model](#dimensional-model)

### Overview

---
All source data is synthetic, generated bia a Python script.  

<div align="center">

| Component | Detail |
| -- | -- |
| Tech Stack | MySQL, Python |
| Source Schema | tmart (raw/transactional) |
| Analytics Schema | tmart_analytics (staging + dimensional) |
| Data Type | Synthetic - generated via Python |

</div>

### Source Data

---

**Tables & Row Counts**

<div align="center">

| Table | Description | Approx. Rows |
| -- | -- | --: |
| customers | Customer data | 300 |
| orders | Order header records | 10,200 |
| order_items | Line-level order detail | 45,473 |
| products | Product catelog | 10,000 |
| products_subcategories | Subcategory reference | 40 |
| products_categories | Category reference | 6 |

</div>

**Date Range**

<div align="center">

| Attribute | Value | 
| -- | -- |
| Earliest Order | 2019-06-24 |
| Latest Order | 2026-04-30 |
| Customer Records Span | 2019-01-22 to 2026-04-06 |

</div>

**Schema Diagram:**
![ER Diagram](images/Tmart_ER_Diagram.png)

### Data Audit & Profiling

---
Done prior to transformation, providing a clear view of raw data and informing all downstream decisions.

<details>
<summary>Expand to view details.</summary>

**NULL Analysis**

<div align="center">

| Table | Column | NULL Count | NULL % | Action |
| -- | -- | --: | --: | -- |
| customers | date_inactive | 235 | 78% | Expected - active customers |
| order_items | ship_date | 4560 | 10% | Expected- canceled items |
| order_items | delivered_date | 4621 | 10% | Expected - shipped/canceled items |
| order_items | canceled_date | 40913 | 90% | Expected - non-canceled items |
| order_items | item_status | 0 | 0% | Expected - all items have a status |
| products | date_inactive | 0 | 0% | Expected - no inactive products |

</div>

**Duplicate Check**

<div align="center">

| Table | Key Columns(s) | Duplicates Found | Resolution |
| -- | -- | :--: | :--: |
| customers | customer_id | N | n/a |
| order_items | order_item_id | N | n/a |
| orders | order_id | N | n/a |
| products | product_id | N | n/a |
| products_categories | category_id | N | n/a |
| products_subcategories | subcategory_id | N | n/a |

</div>

**Referential Integrity Check**

<div align="center">

| Relationship | Orphans Found | Resolution |
| -- | :--: | :--: |
| order_items.order_id &xrarr; orders.order_id | N | n/a |
| order_items.product_id &xrarr; products.product_id | N | n/a |
| orders.customer_id  &xrarr; customers.customer_id | N | n/a |
| products.subcategory_id &xrarr; products_subcategories.subcategory_id | N | n/a |
| products_subcategories.category_id &xrarr; products_categories.category_id | N | n/a |

</div>

**Date Logic Validation**

<div align="center">

| Check | Violations Found | Resolution |
| -- | :--: | :--: |
| order_items.ship_date >= orders.order_date | N | n/a |
| order_items.delivered_date >= order_items.ship_date | N | n/a |
| order_items.canceled_date >= orders.order_date | Y | add time component to canceled_date |
| customers.date_inactive >= customers.date_created | N | n/a |

</div>

**Categorical Value Audit**

<div align="center">

| Column | Expected Values | Unexpected Values Found |
| -- | -- | -- |
| order_items.item_status | Delivered, Shipped, Canceled | none |
| customers.gender | M, F | none |

</div>

</details>

### Staging Layer

---
Staging tables (stg_*) clean and standerdize raw data without applying business logic.  Records with issues are flagged rather than dropped.

**Transformations**

<div align="center">

| Table | Transformation | Reason |
| -- | -- | -- |
| All | TRIM() on all VARCHAR fields | Prevent join failures from whitespace |
| customers | UPPER(gender), UPPER(state) | Standardize categorical values |
| order_items | UPPER(item_status) | Consistent status values |

</div>

### Dimensional Model

---
A star schema is built on top of the staging layer to optimize query performance and simplify dashboard development.

<details>
<summary>Expand to view details.</summary>

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

</details>

</details>

## :bar_chart: Business Intelligence

<details>
<summary>Expand to view details.</summary>

![coming soon](images/torn_coming_soon.jpg)
[Designed by Freepik](www.freepik.com)

</details>

## :mag: Data Analytics

<details>
<summary>Expand to view details.</summary>

![coming soon](images/torn_coming_soon.jpg)
[Designed by Freepik](www.freepik.com)

</details>

<!--
## :wrench: Data Cleaning (work in progress)

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

### Stored Procedure

create resuable procedure to fix order totals and delivery fees

```sql
DELIMITER $$

CREATE PROCEDURE fix_order_totals()
comment 'Procedure to fix the order total_amount and delivery_cost when items are canceled: CALL fix_order_totals();'
BEGIN

    UPDATE orders o
    JOIN (
    with canceled as (select distinct i.order_id, c.loyalty_member from order_items i join orders o on i.order_id = o.order_id join customers c on o.customer_id = c.customer_id where i.item_status = 'Canceled')
        SELECT
            o.order_id, c.loyalty_member,
            SUM(CASE
                WHEN o.item_status != 'Canceled' THEN line_total
                ELSE 0
            END) AS new_total
        FROM order_items o  join canceled c on o.order_id = c.order_id
        GROUP BY 1,2
    ) t ON o.order_id = t.order_id
    SET
        o.total_amount = ROUND(t.new_total, 2),
        o.delivery_cost =
       CASE
           WHEN t.new_total = 0 THEN 0
           WHEN t.loyalty_member THEN CASE
                                          WHEN t.new_total >= 50 THEN 0
                                          WHEN t.new_total >= 25 THEN 5
                                          ELSE 10
                                      END
           ELSE CASE
                    WHEN t.new_total >= 75 THEN 0
                    WHEN t.new_total >= 50 THEN 5
                    WHEN t.new_total >= 25 THEN 10
                    ELSE 25
                END
       END;

END $$

DELIMITER ;
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

SELECT DISTINCT first_name,
                gender
FROM customers;


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
```

</details>  

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
