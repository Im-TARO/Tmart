# :telescope: Exploratory Data Analysis using SQL 

![Data](https://img.shields.io/badge/Data-Synthetic-gray?style=plastic&logoColor=white&logoSize=auto&labelColor=orange)

## :high_brightness: Insights

| Findings| |
| --- | --- |
| Customer mix | - The oldest customer is 86 and the youngest is 20, 66 years of age difference<br>- Customer base is fairly balanced by gender, male customers slightly higher |
| Dates | - Order history covers roughly 6 years (2026 is incomplete) |
| Geographic coverage | - Data covers 5 counties and 15 cities<br>- Wake County is the largest geographic market |
| Products | - There are 40 subcategories across 6 major category groups<br>- Food and Beverage contains the largest mix of subcategories<br>- Pet Care Products have the highest average price<br>- Food and Bererage has the lowest average price |

:link: [Data Visualizations](https://public.tableau.com/views/Tmart_EDA/AgeDistribution?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

## Table of Contents

- [Data Overview](#data-overview)
- [Dimensions & Measures](#dimensions--measures-by-table)
- [Missing Values](#missing-values)
- [Dimensions Exploration](#dimensions-exploration)
- [Date Exploration](#date-exploration)
- [Key metrics report](#key-metrics-report)
- [Magnitude Analysis](#magnitude-analysis)
- [Ranking Analysis](#ranking-analysis)

## Data Overview

### Schema - tmart_analytics

<div align="center">

| Table_in_tmart_analytics | Column Count | Table Rows |
| --- | ---: | ---: |
| dim_customers | 18 | 300 |
| dim_date | 10 | 2708 |
| dim_products | 15 | 10000 |
| fact_orders | 17 | 45473 |

</div>

<details>
<summary>Expand to view details.</summary><br>

### dim_customers

<details>
<summary>Expand to view details.</summary><br>

```sql
-- view table schema
SHOW columns
FROM dim_customers;
```

<div align="center">

| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| customer_key | bigint unsigned | NO | PRI | 0 | |
| customer_id | int | YES | | NULL | |
| first_name | varchar(50) | YES | | NULL | |
| last_name | varchar(50) | YES | | NULL | |
| gender | varchar(8) | YES | | NULL | |
| phone_number | varchar(12) | YES | | NULL | |
| email_address | varchar(255) | YES | | NULL | |
| street_address | varchar(200) | YES | | NULL | |
| city | varchar(100) | YES | | NULL | |
| state | char(2) | YES | | NULL | |
| zipcode | varchar(10) | YES | | NULL | |
| county | varchar(50) | YES | | NULL | |
| birthdate | date | YES | | NULL | |
| age | int | YES | | NULL | |
| is_active | tinyint | YES | | NULL | |
| loyalty_member | tinyint | YES | | NULL | |
| date_created | date | YES | | NULL | |
| date_inactive | date | YES | | NULL | |

</div>

```sql
-- preview first few rows
SELECT *
FROM dim_customers
LIMIT 5;
```

| customer_key | customer_id | first_name | last_name | gender | phone_number | email_address | street_address | city | state | zipcode | county | birthdate | age | is_active | loyalty_member | date_created | date_inactive |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | Joseph | Anderson | Male | 240-555-4124 | anderson590@notinbox.net | "80494 Hummingbird Dr" | Dunn | NC | 28334 | Harnett | 1952-04-22 | 74 | 1 | 1 | 2023-01-21 | NULL |
| 2 | 2 | Luna | Green | Female | 476-555-2407 | greenluna247@notinbox.net | "32235 Elm St" | "Holly Springs" | NC | 27540 | Wake | 1942-07-26 | 83 | 1 | 0 | 2019-03-15 | NULL |
| 3 | 3 | Richard | Hernandez | Male | 385-555-5744 | richardhernandez724@fakeinbox.net | "77657 Cardinal Ave" | Raleigh | NC | 27615 | Wake | 1940-06-22 | 85 | 1 | 0 | 2022-05-21 | NULL |
| 4 | 4 | Richard | Allen | Male | 315-555-9517 | richard595@fakeinbox.net | "13624 Dogwood St" | Raleigh | NC | 27612 | Wake | 1951-03-04 | 75 | 1 | 1 | 2020-10-08 | NULL |
| 5 | 5 | Susan | Johnson | Female | 365-555-6207 | johnsonsusan699@nachomail.net | "22809 Central Ave" | Garner | NC | 27529 | Wake | 1968-10-26 | 57 | 1 | 0 | 2024-12-20 | NULL |

</details>

### dim_date

<details>
<summary>Expand to view details.</summary><br>

```sql
-- view table schema
SHOW columns
FROM dim_date;
```

<div align="center">

| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| date_key | int | NO | PRI | NULL | |
| date | date | YES | | NULL | |
| year | int | YES | | NULL | |
| quarter | int | YES | | NULL | |
| month_name | varchar(9) | YES | | NULL | |
| month_sort | int | YES | | NULL | |
| day_name | varchar(9) | YES | | NULL | |
| day_sort | int | YES | | NULL | |
| is_weekend | tinyint | YES | | NULL | |
| is_holiday | tinyint | YES | | NULL | |

</div>

```sql
-- preview first few rows
SELECT *
FROM dim_date
LIMIT 5;
```

| date_key | date | year | quarter | month_name | month_sort | day_name | day_sort | is_weekend | is_holiday |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 20190101 | 2019-01-01 | 2019 | 1 | January | 1 | Tuesday | 3 | 0 | 1 |
| 20190102 | 2019-01-02 | 2019 | 1 | January | 1 | Wednesday | 4 | 0 | 0 |
| 20190103 | 2019-01-03 | 2019 | 1 | January | 1 | Thursday | 5 | 0 | 0 |
| 20190104 | 2019-01-04 | 2019 | 1 | January | 1 | Friday | 6 | 0 | 0 |
| 20190105 | 2019-01-05 | 2019 | 1 | January | 1 | Saturday | 7 | 1 | 0 |

</details>

### dim_products

<details>
<summary>Expand to view details.</summary><br>

```sql
-- view table schema
SHOW columns
FROM dim_products;
```

<div align="center">

| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| product_key | bigint unsigned | NO | PRI | NULL | |
| product_id | int | YES | | NULL | |
| product_sku | varchar(50) | YES | | NULL | |
| product_name | varchar(300) | YES | | NULL | |
| product_type | varchar(300) | YES | | NULL | |
| brand_name | varchar(100) | YES | | NULL | |
| subcategory_id | int | YES | | NULL | |
| category | varchar(100) | YES | | NULL | |
| subcategory | varchar(100) | YES | | NULL | |
| unit_size | varchar(50) | YES | | NULL | |
| price | decimal(10,2) | YES | | NULL | |
| stock_quantity | int | YES | | NULL | |
| is_active | tinyint | YES | | NULL | |
| date_created | date | YES | | NULL | |
| date_inactive | date | YES | | NULL | |

</div>

```sql
-- preview first few rows
SELECT *
FROM dim_products
LIMIT 5;
```

| product_key | product_id | product_sku | product_name | product_type | brand_name | subcategory_id | category | subcategory | unit_size | price | stock_quantity | is_active | date_created | date_inactive |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 4071 | SQ31REAUJF79 | GoldenVale Cheese Puffs | Cheese Puffs | GoldenVale | 3 | Food and Beverages | Snacks | 10 oz | 2.81 | 141 | 1 | 2018-12-02 | |
| 2 | 1827 | W3X1RXNJXOM2 | Velvessa Body Wash | Body Wash | Velvessa | 14 | Personal Care and Beauty | Bath and Body | 18 oz | 13.45 | 166 | 1 | 2018-12-02 | |
| 3 | 7979 | WEKMTINCNDXI | EverSip Club Soda | Club Soda | EverSip | 8 | Food and Beverages | Soda | 16 oz | 6.06 | 261 | 1 | 2018-12-02 | |
| 4 | 2586 | 3XO4CM2WN67O | Satori Bloom Green Tea | Green Tea | Satori Bloom | 11 | Food and Beverages | Tea | 20 ct | 2.66 | 279 | 1 | 2018-12-03 | |
| 5 | 5009 | 2X92FCNKBC3R | BrightBerry Minced Garlic | Minced Garlic | BrightBerry | 7 | Food and Beverages | Pantry | 8 oz | 5.63 | 270 | 1 | 2018-12-04 | |

</details>

### fact_orders

<details>
<summary>Expand to view details.</summary><br>

```sql
-- view table schema
SHOW columns
FROM fact_orders;
```

<div align="center">

| Field | Type | Null | Key | Default | Extra |
| --- | --- | --- | --- | --- | --- |
| order_id | int | YES | | NULL | |
| order_item_id | int | YES | | NULL | |
| product_key | bigint unsigned | YES | MUL | 0 | |
| customer_key | int | YES | MUL | 0 | |
| order_date_key | int | YES | | NULL | |
| ship_date_key | int | YES | | NULL | |
| delivered_date_key | int | YES | | NULL | |
| canceled_date_key | int | YES | | NULL | |
| order_datetime | datetime | YES | | NULL | |
| order_delivery_fee | decimal(10,2) | YES | | NULL | |
| ship_datetime | datetime | YES | | NULL | |
| delivered_datetime | datetime | YES | | NULL | |
| canceled_datetime | datetime | YES | | NULL | |
| quantity | int | YES | NULL | | |
| unit_price | decimal(10,2) | YES | | NULL | |
| line_total | decimal(10,2) | YES | | NULL | |
| item_status | varchar(50) | YES | | NULL | |

</div>

```sql
-- preview first few rows
SELECT *
FROM fact_orders
LIMIT 5;
```

| order_id | order_item_id | product_key | customer_key | order_date_key | ship_date_key | delivered_date_key | canceled_date_key | order_datetime | order_delivery_fee | ship_datetime | delivered_datetime | canceled_datetime | quantity | unit_price | line_total | item_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 1 | 1 | 2722 | 238 | 20260115 | 20260116 | 20260118 | | 2026-01-15 18:11:19 | 0.00 | 2026-01-16 17:28:00 | 2026-01-18 09:20:30 | | 5 | 11.13 | 55.65 | DELIVERED |
| 1 | 3 | 1242 | 238 | 20260115 | | | 20260115 | 2026-01-15 18:11:19 | 0.00 | | | 2026-01-15 00:00:00 | 2 | 4.39 | 8.78 | CANCELED |
| 1 | 5 | 4734 | 238 | 20260115 | 20260117 | 20260118 | | 2026-01-15 18:11:19 | 0.00 | 2026-01-17 16:39:00 | 2026-01-18 09:20:30 | | 3 | 33.46 | 100.38 | DELIVERED |
| 2 | 7 | 3312 | 119 | 20250128 | 20250131 | 20250201 | | 2025-01-28 12:05:44 | 0.00 | 2025-01-31 17:36:00 | 2025-02-01 11:25:46 | | 5 | 1.79 | 8.95 | DELIVERED |
| 3 | 13 | 3341 | 156 | 20260218 | 20260220 | 20260221 | | 2026-02-18 18:50:45 | 0.00 | 2026-02-20 15:41:00 | 2026-02-21 09:19:00 | | 2 | 12.82 | 25.64 | DELIVERED |

</details>

</details>

## Dimensions & Measures (by table)

<table>
  <tr>
    <th></th>
    <th>dim_customers</th>
    <th>dim_date</th>
    <th>dim_products</th>
    <th>fact_orders</th>
  </tr>
  <tr>
    <td valign=top><h3>Dimensions</h3></td>
    <td valign=top>customer_key<br>customer_id<br>first_name<br>last_name<br>gender<br>phone_number<br>email_address<br>street_address<br>city<br>state<br>zipcode<br>county<br>birthdate<br>is_active<br>loyalty_member<br>date_created<br>date_inactive</td>
    <td valign=top>date_key<br>date<br>year<br>quarter<br>month_name<br>day_name<br>is_weekend<br>is_holiday</td>
    <td valign=top>product_key<br>product_id<br>product_sku<br>product_name<br>product_type<br>brand_name<br>subcategory_id<br>category<br>subcategory<br>unit_size<br>is_active<br>date_created<br>date_inactive</td>
    <td valign=top>order_id<br>order_item_id<br>product_key<br>customer_key<br>order_date_key<br>ship_date_key<br>delivered_date_key<br>canceled_date_key<br>order_datetime<br>ship_datetime<br>delivered_datetime<br>canceled_datetime<br>item_status</td>
  </tr>
  <tr>
    <td valign=top><h3>Measures</h3></td>
    <td valign=top>age</td>
    <td valign=top></td>
    <td valign=top>price<br>stock_quantity</td>
    <td valign=top>order_delivery_fee<br>quantity<br>unit_price<br>line_total</td>
  </tr>  
</table>

## Missing Values

Identify missing values and strategy to handle them

| Table | | Strategy |
| --- | --- | --- |
| dim_customers | :small_blue_diamond: date_inactive shows 235 NULL entries, consistent with the number of active customers | NR |
| dim_products | :small_blue_diamond: date_inactive shows 10,000 NULL entries, consistent with the number of active products | NR |
| fact_orders | :small_blue_diamond: ship_date_key and ship_datetime contain 4,560 NULL values, representing line items that have not yet shipped or were canceled<br>:small_blue_diamond: delivered_date_key and delivered_datetime contain 4,621 NULL values, representing line items that have not yet been delivered or were canceled<br>:small_blue_diamond: canceled_date_key and canceled_datetime contain 40,913 NULL values, representing line items not canceled | NR |

<details>
<summary>Expand to view details.</summary><br>

```sql
-- check for missing values (dim_customers)
SELECT SUM(CASE WHEN customer_key IS NULL THEN 1 ELSE 0 END) missing_customer_key,
       SUM(CASE WHEN customer_id IS NULL THEN 1 ELSE 0 END) missing_customer_id,
       SUM(CASE WHEN first_name IS NULL THEN 1 ELSE 0 END) missing_first_name,
       SUM(CASE WHEN last_name IS NULL THEN 1 ELSE 0 END) missing_last_name,
       SUM(CASE WHEN gender IS NULL THEN 1 ELSE 0 END) missing_gender,
       SUM(CASE WHEN phone_number IS NULL THEN 1 ELSE 0 END) missing_phone_number,
       SUM(CASE WHEN email_address IS NULL THEN 1 ELSE 0 END) missing_email_address,
       SUM(CASE WHEN street_address IS NULL THEN 1 ELSE 0 END) missing_street_address,
       SUM(CASE WHEN city IS NULL THEN 1 ELSE 0 END) missing_city,
       SUM(CASE WHEN state IS NULL THEN 1 ELSE 0 END) missing_state,
       SUM(CASE WHEN zipcode IS NULL THEN 1 ELSE 0 END) missing_zipcode,
       SUM(CASE WHEN county IS NULL THEN 1 ELSE 0 END) missing_county,
       SUM(CASE WHEN birthdate IS NULL THEN 1 ELSE 0 END) missing_birthdate,
       SUM(CASE WHEN age IS NULL THEN 1 ELSE 0 END) missing_age,
       SUM(CASE WHEN is_active IS NULL THEN 1 ELSE 0 END) missing_is_active,
       SUM(CASE WHEN loyalty_member IS NULL THEN 1 ELSE 0 END) missing_loyalty_member,
       SUM(CASE WHEN date_created IS NULL THEN 1 ELSE 0 END) missing_date_created,
       SUM(CASE WHEN date_inactive IS NULL THEN 1 ELSE 0 END) missing_date_inactive
FROM dim_customers;
```

| missing_customer_key | missing_customer_id | missing_first_name | missing_last_name | missing_gender | missing_phone_number | missing_email_address | missing_street_address | missing_city | missing_state | missing_zipcode | missing_county | missing_birthdate | missing_age | missing_is_active | missing_loyalty_member | missing_date_created | missing_date_inactive |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 235 |

```sql
-- check for missing values (dim_products)
SELECT SUM(CASE WHEN product_key IS NULL THEN 1 ELSE 0 END) missing_product_key,
       SUM(CASE WHEN product_id IS NULL THEN 1 ELSE 0 END) missing_product_id,
       SUM(CASE WHEN product_sku IS NULL THEN 1 ELSE 0 END) missing_product_sku,
       SUM(CASE WHEN product_name IS NULL THEN 1 ELSE 0 END) missing_product_name,
       SUM(CASE WHEN product_type IS NULL THEN 1 ELSE 0 END) missing_product_type,
       SUM(CASE WHEN brand_name IS NULL THEN 1 ELSE 0 END) missing_brand_name,
       SUM(CASE WHEN subcategory_id IS NULL THEN 1 ELSE 0 END) missing_subcategory_id,
       SUM(CASE WHEN category IS NULL THEN 1 ELSE 0 END) missing_category,
       SUM(CASE WHEN subcategory IS NULL THEN 1 ELSE 0 END) missing_subcategory,
       SUM(CASE WHEN unit_size IS NULL THEN 1 ELSE 0 END) missing_unit_size,
       SUM(CASE WHEN price IS NULL THEN 1 ELSE 0 END) missing_price,
       SUM(CASE WHEN stock_quantity IS NULL THEN 1 ELSE 0 END) missing_stock_quantity,
       SUM(CASE WHEN is_active IS NULL THEN 1 ELSE 0 END) missing_is_active,
       SUM(CASE WHEN date_created IS NULL THEN 1 ELSE 0 END) missing_date_created,
       SUM(CASE WHEN date_inactive IS NULL THEN 1 ELSE 0 END) missing_date_inactive
FROM dim_products;
```

| missing_product_key | missing_product_id | missing_product_sku | missing_product_name | missing_product_type | missing_brand_name | missing_subcategory_id | missing_category | missing_subcategory | missing_unit_size | missing_price | missing_stock_quantity | missing_is_active | missing_date_created | missing_date_inactive |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 0 | 10000 |

```sql
-- check for missing values (fact_orders)
SELECT SUM(CASE WHEN order_id IS NULL THEN 1 ELSE 0 END) missing_order_id,
       SUM(CASE WHEN order_item_id IS NULL THEN 1 ELSE 0 END) missing_order_item_id,
       SUM(CASE WHEN product_key IS NULL THEN 1 ELSE 0 END) missing_product_key,
       SUM(CASE WHEN customer_key IS NULL THEN 1 ELSE 0 END) missing_customer_key,
       SUM(CASE WHEN order_date_key IS NULL THEN 1 ELSE 0 END) missing_order_date_key,
       SUM(CASE WHEN ship_date_key IS NULL THEN 1 ELSE 0 END) missing_ship_date_key,
       SUM(CASE WHEN delivered_date_key IS NULL THEN 1 ELSE 0 END) missing_delivered_date_key,
       SUM(CASE WHEN canceled_date_key IS NULL THEN 1 ELSE 0 END) missing_canceled_date_key,
       SUM(CASE WHEN order_datetime IS NULL THEN 1 ELSE 0 END) missing_order_datetime,
       SUM(CASE WHEN order_delivery_fee IS NULL THEN 1 ELSE 0 END) missing_order_delivery_fee,
       SUM(CASE WHEN ship_datetime IS NULL THEN 1 ELSE 0 END) missing_ship_datetime,
       SUM(CASE WHEN delivered_datetime IS NULL THEN 1 ELSE 0 END) missing_delivered_datetime,
       SUM(CASE WHEN canceled_datetime IS NULL THEN 1 ELSE 0 END) missing_canceled_datetime,
       SUM(CASE WHEN quantity IS NULL THEN 1 ELSE 0 END) missing_quantity,
       SUM(CASE WHEN unit_price IS NULL THEN 1 ELSE 0 END) missing_unit_price,
       SUM(CASE WHEN line_total IS NULL THEN 1 ELSE 0 END) missing_line_total,
       SUM(CASE WHEN item_status IS NULL THEN 1 ELSE 0 END) missing_item_status
FROM fact_orders;
```

| missing_order_id | missing_order_item_id | missing_product_key | missing_customer_key | missing_order_date_key | missing_ship_date_key | missing_delivered_date_key | missing_canceled_date_key | missing_order_datetime | missing_order_delivery_fee | missing_ship_datetime | missing_delivered_datetime | missing_canceled_datetime | missing_quantity | missing_unit_price | missing_line_total | missing_item_status |
| --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- | --- |
| 0 | 0 | 0 | 0 | 0 | 4560 | 4621 | 40913 | 0 | 0 | 4560 | 4621 | 40913 | 0 | 0 | 0 | 0 |

</details>

## Dimensions Exploration

SQL based Dimension Exploration - examining data by different categories

<details>
<summary>Expand to view details.</summary><br>

```sql
-- all counties/cities where active customers live
SELECT DISTINCT county, city
FROM dim_customers
WHERE is_active = 1
ORDER BY 1 , 2;
```

### :arrows_counterclockwise: Result Grid

| county | city |
| --- | --- |
| Durham | Durham |
| Harnett | Angier |
| Harnett | Broadway |
| Harnett | Dunn |
| Harnett | Erwin |
| Harnett | Lillington |
| Johnston | Clayton |
| Lee | Sanford |
| Wake | Apex |
| Wake | Cary |
| Wake | Fuquay-Varina |
| Wake | Garner |
| Wake | Holly Springs |
| Wake | Morrisville |
| Wake | Raleigh |


```sql
-- product categories/subcategories
SELECT DISTINCT category, subcategory
FROM dim_products
WHERE is_active = 1
ORDER BY 1 , 2;
```

### :arrows_counterclockwise: Result Grid

| category | subcategory |
| --- | --- |
| Baby and Childcare | Bathing and Skin Care |
| Baby and Childcare | Beverages |
| Baby and Childcare | Bottles and Cups |
| Baby and Childcare | Diapers and Wipes |
| Baby and Childcare | Food and Formula |
| Baby and Childcare | Health & Wellnes |
| Baby and Childcare | Toys |
| Food and Beverages | Baked Goods |
| Food and Beverages | Breakfast and Cereal |
| Food and Beverages | Coffee |
| Food and Beverages | Dairy |
| Food and Beverages | Juice |
| Food and Beverages | Meat |
| Food and Beverages | Pantry |
| Food and Beverages | Produce |
| Food and Beverages | Snacks |
| Food and Beverages | Soda |
| Food and Beverages | Tea |
| Food and Beverages | Water |
| Health and Wellness Products | Allergy and Sinus |
| Health and Wellness Products | Cold and Flu |
| Health and Wellness Products | First Aid |
| Health and Wellness Products | Pain Relief |
| Health and Wellness Products | Vitamins and Supplements |
| Household Goods and Cleaning Products | Air Fresheners |
| Household Goods and Cleaning Products | Cleaning Supplies |
| Household Goods and Cleaning Products | Disposable Tableware |
| Household Goods and Cleaning Products | Food Storages and Wraps |
| Household Goods and Cleaning Products | Laundry |
| Household Goods and Cleaning Products | Paper Products |
| Household Goods and Cleaning Products | Trash Bags |
| Personal Care and Beauty | Bath and Body |
| Personal Care and Beauty | Deodorant |
| Personal Care and Beauty | Hair Care |
| Personal Care and Beauty | Oral Care |
| Personal Care and Beauty | Skin Care |
| Pet Care Products | Birds |
| Pet Care Products | Cats |
| Pet Care Products | Dogs |
| Pet Care Products | Fish |

</details>

## Date Exploration

SQL-based Date Exploration - understanding the time span represented

<details>
<summary>Expand to view details.</summary><br>

```sql
 -- youngest and oldest customer
SELECT 
    MIN(birthdate) oldest_birthdate,
    MAX(age) oldest_age,
    MAX(birthdate) youngest_birthdate,
    MIN(age) youngest_age
FROM dim_customers;
```

### :arrows_counterclockwise: Result Grid

| oldest_birthdate | oldest_age | youngest_birthdate | youngest_age |
| --- | --- | --- | --- |
| 1940-01-07 | 86 | 2005-11-11 | 20 |

```sql
-- how many years of sales are available
SELECT 
    MIN(order_datetime) first_order_date,
    MAX(order_datetime) last_order_date,
    TIMESTAMPDIFF(YEAR, MIN(order_datetime), MAX(order_datetime)) order_range_years
FROM fact_orders;
```

### :arrows_counterclockwise: Result Grid

| first_order_date | last_order_date | order_range_years |
| --- | --- | --- |
| 2019-06-24 05:53:15 | 2026-04-30 22:05:01 | 6 |

</details>

## Key metrics report

 SQL queries that extract, aggregate, and display performance or business indicators from Star Schema

<details>
<summary>Expand to view details.</summary><br>

```sql
-- Generate a Report that shows key metrics of the business
SELECT 'Total Sales' measure_name, sum(line_total) measure_value
FROM fact_orders
WHERE item_status != 'CANCELED'
UNION ALL
SELECT 'Total Quantity' measure_name, sum(quantity) measure_value
FROM fact_orders
WHERE item_status != 'CANCELED'
UNION ALL
SELECT 'Average Price' measure_name, avg(unit_price) measure_value
FROM fact_orders
WHERE item_status != 'CANCELED'
UNION ALL
SELECT 'Total Num Orders' measure_name, count(DISTINCT order_id) measure_value
FROM fact_orders
WHERE item_status != 'CANCELED'
UNION ALL
SELECT 'Total Num Products' measure_name, count(product_key) measure_value
FROM dim_products
UNION ALL
SELECT 'Total Num Customers' measure_name, count(customer_key) measure_value
FROM dim_customers
UNION ALL
SELECT 'Num Customers to place an order' measure_name, count(DISTINCT customer_key) measure_value
FROM fact_orders
WHERE item_status != 'CANCELED';
```

### :arrows_counterclockwise: Result Grid

| measure_name | measure_value |
| --- | ---: |
| Total Sales | 1219420.730000 |
| Total Quantity | 122844.000000 |
| Average Price | 9.898647 |
| Total Num Orders | 10065.000000 |
| Total Num Products | 10000.000000 |
| Total Num Customers | 300.000000 |
| Num Customers to place an order | 300.000000 |

</details>

## Magnitude Analysis

SQL-based magnitude analysis - group and summarize data by dimensions to see distribution

<details>
<summary>Expand to view details.</summary><br>

```sql
-- Number of customers by county
SELECT county, COUNT(customer_key) total_customers, SUM(is_active) active_customers
FROM dim_customers
GROUP BY county 
ORDER BY total_customers DESC;
```

### :arrows_counterclockwise: Result Grid

| county | total_customers | active_customers |
| --- | --- | --- |
| Wake |181 | 139 |
| Harnett | 60 | 48 |
| Durham | 29 | 22 |
| Lee | 17 | 14 |
| Johnston | 13 | 12 |

```sql
-- Number of customers by gender
SELECT gender, COUNT(customer_key) total_customers, SUM(is_active) active_customers
FROM dim_customers
GROUP BY gender
ORDER BY total_customers DESC;
```

### :arrows_counterclockwise: Result Grid

| gender | total_customers | active_customers |
| --- | --- | --- |
| Male | 160 | 128 |
| Female | 140 | 107 |

```sql
-- Avg price in each category
SELECT category, AVG(price) avg_price
FROM dim_products
GROUP BY category
ORDER BY avg_price DESC;
```

### :arrows_counterclockwise: Result Grid

| category | avg_price |
| --- | --- |
| Pet Care Products | 21.099898 |
| Baby and Childcare | 18.544915 |
| Household Goods and Cleaning Products | 11.439111 |
| Health and Wellness Products | 10.884674 |
| Personal Care and Beauty | 9.909330 |
| Food and Beverages | 5.771493 |

```sql
-- Distribution of sold items across counties
SELECT c.county, SUM(f.quantity) total_items
FROM fact_orders f
        LEFT JOIN dim_customers c ON c.customer_key = f.customer_key
WHERE f.item_status != 'CANCELED'
GROUP BY county
ORDER BY total_items DESC;
```

### :arrows_counterclockwise: Result Grid

| county | total_items |
| --- | --- |
| Wake | 75016 |
| Harnett | 24545 |
| Durham | 11413 |
| Lee | 6637 |
| Johnston | 5233 |

```sql
-- Number of products by category
SELECT category, COUNT(product_key) total_products
FROM dim_products
GROUP BY category
ORDER BY total_products DESC;
```

### :arrows_counterclockwise: Result Grid

| category | total_products |
| --- | --- |
| Food and Beverages | 4808 |
| Household Goods and Cleaning Products | 1529 |
| Personal Care and Beauty | 1030 |
| Baby and Childcare | 995 |
| Health and Wellness Products | 950 |
| Pet Care Products | 688 |

</details>

## Ranking Analysis

SQL-based ranking analysis - ordering entities based on a metric

<details>
<summary>Expand to view details.</summary><br>

```sql
-- Top 5 products - generate highest revenue
SELECT p.product_name, SUM(f.line_total) total_revenue
FROM fact_orders f
        LEFT JOIN dim_products p ON p.product_key = f.product_key
WHERE f.item_status != 'CANCELED'
GROUP BY p.product_name
ORDER BY total_revenue DESC
LIMIT 5;
```

### :arrows_counterclockwise: Result Grid

| product_name | total_revenue |
| --- | ---: |
| NaturaPress Paws Cat Beds | 1552.43 |
| VitaVerde Pets Litter Box Filler | 1549.72 |
| PurePaw Naturals Dog Beds | 1450.90 |
| PurePaw Naturals Litter Box Filler | 1431.33 |
| ComfortCure Pets Dry Cat Food | 1335.85 |

```sql
-- 5 worst products - generate lowest revenue
SELECT p.product_name, SUM(f.line_total) total_revenue
FROM fact_orders f
        LEFT JOIN dim_products p ON p.product_key = f.product_key
WHERE f.item_status != 'CANCELED'
GROUP BY p.product_name
ORDER BY total_revenue
LIMIT 5;
```

### :arrows_counterclockwise: Result Grid

| product_name | total_revenue |
| --- | ---: |
| Crescent Grove Chicken Wings | 1.80 |
| Tmart Cabbage | 1.98 |
| Tmart Lettuce | 2.49 |
| Aurora Fields T-Bone Steak | 3.48 |
| Aurora Fields White Bread | 4.22 |

```sql
-- Top 10 customers with highest revenue
SELECT customer_rank,
       customer_key,
       last_name,
       age,
       city,
       total_revenue
FROM
  (SELECT c.customer_key,
          c.last_name,
          c.age,
          c.city,
          c.county,
          SUM(f.line_total) total_revenue,
          row_number() OVER (ORDER BY SUM(f.line_total) DESC) customer_rank
   FROM fact_orders f
   LEFT JOIN dim_customers c ON c.customer_key = f.customer_key
   WHERE f.item_status != 'CANCELED'
   GROUP BY customer_key,
            last_name,
            age,
            city,
            county) a
WHERE customer_rank <= 10;
```

### :arrows_counterclockwise: Result Grid

| customer_rank | customer_key | last_name | age | city | total_revenue |
| --- | --- | --- | --- | --- | ---: |
| 1 | 37 | Wilson | 80 | Morrisville | 6782.46 |
| 2 | 139 | Lee | 41 | Clayton | 6536.89 |
| 3 | 39 | Edwards | 35 | Cary | 6403.95 |
| 4 | 239 | Martinez | 50 | Raleigh | 6344.11 |
| 5 | 198 | Brown | 22 | Angier | 6285.58 |
| 6 | 214 | Moore | 63 | Fuquay-Varina | 6129.56 |
| 7 | 281 | Lopez | 68 | Broadway | 6035.77 |
| 8 | 171 | Brown | 54 | Fuquay-Varina | 5797.65 |
| 9 | 286 | Allen | 44 | Raleigh | 5617.75 |
| 10 | 4 | Allen | 75 | Raleigh | 5532.57 |

```sql
-- 3 customers with the fewest order placed
SELECT 
    c.customer_key,
    c.last_name,
    c.age,
    c.city,
    COUNT(DISTINCT order_id) total_orders
FROM
    fact_orders f
        LEFT JOIN dim_customers c ON c.customer_key = f.customer_key
WHERE
    f.item_status != 'CANCELED'
GROUP BY customer_key , first_name , last_name , city
ORDER BY total_orders
LIMIT 3;
```

| customer_key | last_name | age | city | total_orders |
| --- | --- | --- | --- | --- |
| 290 | Kelly | 28 | Raleigh | 18 |
| 125 | Kelly | 21 | Durham | 19 |
| 105 | Clark |86 | Morrisville | 21 |

</details>
