# :telescope: Exploratory Data Analysis using SQL

## :high_brightness: Insights

### Descriptive Analysis

| About the Data| |
| --- | --- |
| Customer mix | - The oldest customer is 86 and the youngest is 20, 66 years of age difference<br>- Customer base is fairly balanced by gender, male customers slightly higher |
| Dates | - Order history covers roughly 6 years (2026 is incomplete) |
| Geographic coverage | - Data covers 5 counties and 15 cities<br>- Wake County is the largest geographic market |
| Products | - There are 40 subcategories across 6 major category groups<br>- Food and Beverage contains the largest mix of subcategories<br>- Pet Care Products have the highest average price<br>- Food and Bererage has the lowest average price |

:link: [Data Visualizations](https://public.tableau.com/views/Tmart_EDA/AgeDistribution?:language=en-US&:sid=&:redirect=auth&:display_count=n&:origin=viz_share_link)

## Table of Contents

- [Dimensions & Measures](#dimensions--measures-by-table)
- [Dimensions Exploration](#dimensions-exploration)
- [Date Exploration](#date-exploration)
- [Key metrics report](#key-metrics-report)
- [Magnitude Analysis](#magnitude-analysis)
- [Ranking Analysis](#ranking-analysis)

## Dimensions & Measures (by table)

<details>
<summary>Expand to view details.</summary><br>

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
