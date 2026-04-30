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
- promotions / discounts
- inventory tracking
- dashboards

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
-- Select orders canceled items lines

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


<!--
![coming soon](images/torn_coming_soon.jpg)
[Designed by Freepik](www.freepik.com)
-->
</details>

<!--
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
