USE tmart_staging;

# ------------------------------ PK checks ------------------------------
-- Expectation: No Result
SELECT COUNT(*) FROM tmart_int_customers WHERE customer_id IS NULL;
SELECT customer_id, COUNT(*) FROM tmart_int_customers GROUP BY customer_id HAVING COUNT(*) > 1;

SELECT COUNT(*) FROM tmart_int_order_items WHERE order_item_id IS NULL;
SELECT order_item_id, COUNT(*) FROM tmart_int_order_items GROUP BY order_item_id HAVING COUNT(*) > 1;
SELECT COUNT(*) FROM tmart_int_orders WHERE order_id IS NULL;
SELECT order_id, COUNT(*) FROM tmart_int_orders GROUP BY order_id HAVING COUNT(*) > 1;

SELECT COUNT(*) FROM tmart_int_products WHERE product_id IS NULL;
SELECT product_id, COUNT(*) FROM tmart_int_products GROUP BY product_id HAVING COUNT(*) > 1;
SELECT COUNT(*) FROM tmart_int_products_categories WHERE category_id IS NULL;
SELECT category_id, COUNT(*) FROM tmart_int_products_categories GROUP BY category_id HAVING COUNT(*) > 1;
SELECT COUNT(*) FROM tmart_int_products_subcategories WHERE subcategory_id IS NULL;
SELECT subcategory_id, COUNT(*) FROM tmart_int_products_subcategories GROUP BY subcategory_id HAVING COUNT(*) > 1;

# ------------------------------ FK checks ------------------------------
-- Expectation: No Results
SELECT DISTINCT o.order_id, o.customer_id, o.order_date FROM tmart_int_orders o WHERE NOT EXISTS(SELECT oi.order_id FROM tmart_int_order_items oi WHERE o.order_id = oi.order_id);
SELECT DISTINCT o.order_id, o.customer_id, o.order_date FROM tmart_int_orders o WHERE NOT EXISTS(SELECT c.customer_id FROM tmart_int_customers c WHERE o.customer_id = c.customer_id );
SELECT DISTINCT oi.order_id, oi.order_item_id FROM tmart_int_order_items oi WHERE NOT EXISTS(SELECT o.order_id FROM tmart_int_orders o WHERE o.order_id = oi.order_id);
SELECT DISTINCT oi.order_id, oi.order_item_id FROM tmart_int_order_items oi WHERE NOT EXISTS(SELECT p.product_id FROM tmart_int_products p WHERE p.product_id = oi.product_id);
SELECT DISTINCT p.product_id, p.name FROM tmart_int_products p WHERE NOT EXISTS(SELECT oi.product_id FROM tmart_int_order_items oi WHERE p.product_id = oi.product_id); -- ok, products not ordered
SELECT * FROM tmart_int_products_subcategories WHERE category_id NOT IN (SELECT category_id FROM tmart_int_products_categories);

# ------------------------------ Quality Check ------------------------------
-- Expectation: No Results
-- Duplicates or NULLs
SELECT COUNT(*) FROM tmart_int_products WHERE sku IS NULL;
SELECT sku, COUNT(*) FROM tmart_int_products GROUP BY sku HAVING COUNT(*) > 1;

-- Whitespace
SELECT customer_id, first_name, last_name, gender FROM tmart_int_customers WHERE first_name != TRIM(first_name) OR last_name != TRIM(last_name) OR gender != TRIM(gender);        
SELECT product_id, name, brand, sku FROM tmart_int_products WHERE name != TRIM(name) OR brand != TRIM(brand) OR sku != TRIM(sku);        
        
-- Date issues        
SELECT * FROM tmart_int_customers WHERE date_created IS NULL;
SELECT * FROM tmart_int_customers WHERE date_created > date_inactive;
select * from tmart_int_customers where dob > now();
select * from tmart_int_orders where order_date is null;
select * from tmart_int_orders where order_date > now();
select * from tmart_int_order_items where item_status = 'DELIVERED' and (ship_date is null or delivered_date is null or canceled_date is not null);
select * from tmart_int_order_items where item_status = 'SHIPPED' and (ship_date is null or delivered_date is not null or canceled_date is not null);
select * from tmart_int_order_items where item_status = 'CANCELED' and (ship_date is not null or delivered_date is not null or canceled_date is null);
select * from tmart_int_order_items where ship_date > delivered_date;
SELECT * FROM tmart_int_products WHERE date_created IS NULL;  
SELECT * FROM tmart_int_products WHERE date_created > date_inactive ;  

-- Negative or NULLs                              
SELECT * FROM tmart_int_products WHERE price < 0 OR price IS NULL;    
SELECT * FROM tmart_int_products WHERE  stock_quantity < 0 OR stock_quantity IS NULL; 
select * from tmart_int_orders where total_amount < 0 or delivery_cost < 0;
select * from tmart_int_order_items where line_total  <= 0 or unit_price <= 0 or quantity <= 0;
select * from tmart_int_order_items where line_total  is null or unit_price is null or quantity is null;

 -- Consistency 
select distinct gender from tmart_int_customers where gender not in ('Male', 'Female', 'Unknown');
select distinct county from tmart_int_customers;
SELECT * FROM tmart_int_customers WHERE email NOT LIKE '%@%.%' OR email IS NULL;
SELECT email, COUNT(*) FROM tmart_int_customers GROUP BY email HAVING COUNT(*) > 1;
select * from tmart_int_order_items where line_total != quantity * unit_price;
SELECT DISTINCT item_status FROM tmart_int_order_items where item_status not in ('DELIVERED','CANCELED','SHIPPED');
-- Does order total_amount match the sum of its line items?
SELECT o.order_id, o.total_amount, SUM(oi.line_total)  AS calculated_total
FROM tmart_int_orders o
JOIN tmart_int_order_items oi ON o.order_id = oi.order_id and oi.item_status != 'CANCELED'
GROUP BY o.order_id, o.total_amount, o.delivery_cost
HAVING o.total_amount != SUM(oi.line_total);


