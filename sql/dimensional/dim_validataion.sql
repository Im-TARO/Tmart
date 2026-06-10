/* Check quality */
use tmart_analytics;

-- check for uniqueness of keys
-- expections: no results

SELECT customer_key, COUNT(*) dup_count
FROM dim_customers
GROUP BY customer_key
HAVING COUNT(*) > 1;

SELECT product_key, COUNT(*) dup_count
FROM dim_products
GROUP BY product_key
HAVING COUNT(*) > 1;

-- check connectivity between fact and dimensions
-- expections: no results
SELECT *
FROM fact_orders f
        LEFT JOIN dim_customers c ON f.customer_key = c.customer_key
        LEFT JOIN dim_products p ON f.product_key = p.product_key
WHERE c.customer_key IS NULL
        OR p.product_key IS NULL;

