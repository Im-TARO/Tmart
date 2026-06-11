USE tmart_staging;

-- ------------------------------------------
-- Count the number of rows in the raw tables
-- ------------------------------------------
SELECT count(*) FROM tmart_raw_customers;
SELECT count(*) FROM tmart_raw_order_items;
SELECT count(*) FROM tmart_raw_orders;
SELECT count(*) FROM tmart_raw_products;
SELECT count(*) FROM tmart_raw_products_categories;
SELECT count(*) FROM tmart_raw_products_subcategories;
