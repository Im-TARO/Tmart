[![tmart logo](../images/ChatGPT_Tmart_logo_sm.png)](../README.md)

# 🔎 Data Analytics

| Key Insight | | |
| --- | --- | --- |
| 1 | [Change over time](#change-over-time-trends) | The data show increasing revenue and customer count over time.  2026 is incomplete, so the final trend for 2026 isn't know yet. |

## Change over time (trends)

Sales performance over time

<details>
<summary>Expand to view details.</summary><br>

```sql
-- by year
SELECT 
    d.year order_year,
    SUM(f.line_total) total_sales,
    COUNT(DISTINCT customer_key) AS total_customers,
    SUM(quantity) total_quantity
FROM
    dim_date d
        LEFT JOIN fact_orders f ON f.order_date_key = d.date_key
        AND f.item_status != 'CANCELED'
GROUP BY order_year
ORDER BY order_year;
```

### :arrows_counterclockwise: Result Grid

| order_year | total_sales | total_customers | total_quantity |
| --- | ---: | ---: | ---: |
| 2019 | 936.72 | 6 | 90 |
| 2020 | 20471.37 | 45 | 2120 |
| 2021 | 53640.34 | 98 | 5428 |
| 2022 | 90893.28 | 151 | 9381 |
| 2023 | 148550.78 | 191 | 14868 |
| 2024 | 234569.80 | 217 | 23480 |
| 2025 | 405137.34 | 246 | 40897 |
| 2026 | 265221.10 | 239 | 26580 |

```sql
-- by month
SELECT 
    d.month_sort,
    d.month_name order_month,
    SUM(f.line_total) total_sales,
    COUNT(DISTINCT customer_key) AS total_customers,
    SUM(quantity) total_quantity
FROM
    dim_date d
        LEFT JOIN
    fact_orders f ON f.order_date_key = d.date_key
        AND f.item_status != 'CANCELED'
GROUP BY month_sort , order_month
ORDER BY month_sort;
```

### :arrows_counterclockwise: Result Grid

| month_sort | order_month | total_sales | total_customers | total_quantity |
| ---: | --- | --- | ---: | ---: |
| 1 | January | 109162.22 | 261 | 10975 |
| 2 | February | 107835.56 | 268 | 10880 |
| 3 | March | 136713.79 | 274 | 13766 |
| 4 | April | 150075.86 | 281 | 14857 |
| 5 | May | 67863.56 | 230 | 7012 |
| 6 | June | 76388.35 | 237 | 7646 |
| 7 | July | 77023.17 | 245 | 7798 |
| 8 | August | 88441.79 | 242 | 8848 |
| 9 | September | 95546.27 | 246 | 9570 |
| 10 | October | 100565.47 | 260 | 10413 |
| 11 | November | 108057.29 | 258 | 10709 |
| 12 | December | 101747.40 | 261 | 10370 |

```sql
-- by weekday
SELECT 
    d.day_sort,
    d.day_name order_weekday,
    SUM(f.line_total) total_sales,
    COUNT(DISTINCT customer_key) AS total_customers,
    SUM(quantity) total_quantity
FROM
    dim_date d
        LEFT JOIN fact_orders f ON f.order_date_key = d.date_key
                  AND f.item_status != 'CANCELED'
GROUP BY day_sort , order_weekday
ORDER BY day_sort;
```

| day_sort | order_weekday | total_sales | total_customers | total_quantity |
| ---: | --- | ---: | ---: | ---: |
| 1 | Sunday | 176084.33 | 293 | 17612 |
| 2 | Monday | 173293.89 | 300 | 17681 |
| 3 | Tuesday | 168515.57 | 296 | 16846 |
| 4 | Wednesday | 181843.77 | 300 | 18186 |
| 5 | Thursday | 166736.91 | 296 | 16679 |
| 6 | Friday | 178409.98 | 296 | 18217 |
| 7 | Saturday | 174536.28 | 295 | 17623 |

</details>

## Cumulative Analysis

<details>
<summary>Expand to view details.</summary><br>

</details>

## Performance Analysis

<details>
<summary>Expand to view details.</summary><br>

</details>

## Part-to-whole (porportional)

<details>
<summary>Expand to view details.</summary><br>

</details>

## Data Segmentation

<details>
<summary>Expand to view details.</summary><br>

</details>

## Reporting

<details>
<summary>Expand to view details.</summary><br>

</details>
