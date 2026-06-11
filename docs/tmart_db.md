# :file_folder: Tmart's transactional database

## Table of Contents

- [Schema Diagram](#schema-diagram)
- [Data Dictionary](#data-dictionary)
- [Data Generation](#data-generation)
- [Data Changes](#data-changes)
- [Generate CSV Files](#generate-csv-files)

## Schema Diagram

[__Click to view the DDL__](../sql/Tmart_db/create_db_tmart.sql)

![ER Diagram](../images/Tmart_ER_Diagram.png)

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

[__Click to view the DML__](../sql/Tmart_db/insert_products_categories.sql)

### Asked ChatGPT to create Python scripts to create synthetic data

Reviewed and tailored the scripts to better meet my needs.

<details>
<summary>Expand to view details</summary>

#### Pythons scripts used to create synthetic data

<div align="center">

| [generate_products.py](../python/Tmart_db/generate_products.py) | |
| -- | -- |
| Usage | > python .\generate_products.py |
| Output | csv file |
| Insert | [DML command](../sql/Tmart_db/insert_products.sql) |
| Tables(s) | `tmart.products` |

| [generate_customers.py](../python/Tmart_db/generate_customers.py) | |
| -- | -- |
| Usage | Usage (PowerShell): with optional overrides: <br> > python generate_customers.py \` <br> --num-customers 100 \` <br> --dob-start-year 1960 \` <br>--created-start 2026-03-01 \` <br> --created-end   2026-03-31 |
| Output | csv file |
| Insert | [DML command](../sql/Tmart_db/insert_customers.sql) |
| Tables(s) | `tmart.customers` |

| [generate_orders.py](../python/Tmart_db/generate_orders.py) | |
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
[__Click to view the DDL__](../sql/Tmart_db/create_sp_fix_order_totals.sql)

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

[__Click to view the SQL script__](../sql/Tmart_db/create_csv_files.sql)


