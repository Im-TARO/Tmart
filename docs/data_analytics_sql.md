[![logo](../images/ChatGPT_Tmart_logo_sm.png)](README.md)

# 🔎 Marketing Queries

![Data](https://img.shields.io/badge/Data-Synthetic-gray?style=plastic&logoColor=white&logoSize=auto&labelColor=orange)
![MySQL](https://img.shields.io/badge/MySQL-Database-gray?style=plastic&logo=mysql&logoColor=white&logoSize=auto&labelColor=blue)

## Focus: Customer Acquisition & Growth

<details>
<summary>Expand to view details.</summary><br>

```sql
-- customer acquisition and churn by county
SELECT county,
       COUNT(*) AS new_customer_count,
       sum(CASE
               WHEN date_inactive IS NOT NULL THEN 1
               ELSE 0
           END) churned_customer_count
FROM dim_customers
GROUP BY county
ORDER BY new_customer_count DESC;
```

#### :arrows_counterclockwise: Result Grid  - 5 row(s) returned

![county_new_churned](../images/sql_results/county_new_churn.jpg)

```sql
-- Total new customers by county(all time)
SET @sql = NULL;

SELECT
    GROUP_CONCAT(
        DISTINCT concat(
            'sum(case when year(date_created) = ',
            YEAR(date_created),
            ' then 1 else 0 end) ',
            concat('acquired_', YEAR(date_created))
        )
    ) INTO @sql
FROM
    dim_customers;

SET @sql = concat('select county, ', @sql, ' from dim_customers group by county order by county');
  
prepare stmt FROM @sql;
execute stmt;
deallocate prepare stmt;
```

#### :arrows_counterclockwise: Result Grid  - 5 row(s) returned

![county](../images/sql_results/county_all_time.jpg)

```sql
-- Total new customers by city (all time)
SET @sql = NULL;

SELECT
    GROUP_CONCAT(
        DISTINCT concat(
            'sum(case when year(date_created) = ',
            YEAR(date_created),
            ' then 1 else 0 end) ',
            concat('acquired_', YEAR(date_created))
        )
    ) INTO @sql
FROM
    dim_customers;

SET @sql = concat('select county, city, ', @sql, ' from dim_customers group by county, city order by county, city');
  
prepare stmt FROM @sql;
execute stmt;
deallocate prepare stmt;
```

#### :arrows_counterclockwise: Result Grid - 15 row(s) returned

![city](../images/sql_results/city_all_time.jpg)

```sql
-- New customers by county per month
--     show which counties are trending up or down over time
WITH date_county AS
  (SELECT DISTINCT date_format(date, '%Y-%m') year_mon,
                   c.county
   FROM dim_date d
   JOIN
     (SELECT DISTINCT county
      FROM dim_customers
      ORDER BY county) c) ,
     monthly_county_counts AS
  (SELECT d.year_mon,
          d.county,
          count(c.customer_id) new_customer_count
   FROM date_county d
   LEFT JOIN dim_customers c ON d.year_mon = date_format(c.date_created, '%Y-%m')
   AND d.county = c.county
   GROUP BY d.county,
            d.year_mon
   ORDER BY county,
            year_mon)
SELECT year_mon,
       county,
       new_customer_count,
       new_customer_count - lag(new_customer_count) OVER (PARTITION BY county
                                                          ORDER BY year_mon) AS growth_from_prev_month
FROM monthly_county_counts;
```

#### :arrows_counterclockwise: Result Grid - 445 row(s) returned

![county_mom](../images/sql_results/county_mom.jpg)

```sql
-- County growth comparison — first half vs second half of dataset      
WITH half AS
  (SELECT county,
          SUM(CASE WHEN date_created < '2022-09-01' THEN 1 ELSE 0 END) AS first_half,
          SUM(CASE WHEN date_created >= '2022-09-01' THEN 1 ELSE 0 END) AS second_half
   FROM dim_customers
   GROUP BY county)
SELECT county,
       first_half,
       second_half,
       (second_half - first_half) AS growth,
       ROUND((second_half - first_half) / NULLIF(first_half, 0) * 100 , 2) AS growth_pct
FROM half
ORDER BY growth_pct DESC;
```

#### :arrows_counterclockwise: Result Grid - 5 rows(s) returned

![county_half](../images/sql_results/half_compare.jpg)

```sql
-- Fastest growing cities — comparing two periods
WITH half AS
  (SELECT city,
          SUM(CASE WHEN date_created < '2022-09-01' THEN 1 ELSE 0 END) AS first_half,
          SUM(CASE WHEN date_created >= '2022-09-01' THEN 1 ELSE 0 END) AS second_half
   FROM dim_customers
   GROUP BY city)
SELECT city,
       first_half,
       second_half,
       (second_half - first_half) AS growth,
       ROUND((second_half - first_half) / NULLIF(first_half, 0) * 100 , 2) AS growth_pct
FROM half
ORDER BY growth_pct DESC;
```

#### :arrows_counterclockwise: Result Grid - 15 row(s) returned

![city_half](../images/sql_results/city_half_compare.jpg)

</details>