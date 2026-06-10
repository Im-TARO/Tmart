/*
DDL Script: Create Star Schema

Usage: tables to be queried for analytics and reporting
*/

use tmart_analytics;

ALTER TABLE fact_orders drop FOREIGN KEY FK1;        
ALTER TABLE fact_orders drop FOREIGN KEY FK2;

-- Create Dimension: dim_customers
DROP TABLE IF EXISTS dim_customers;
CREATE TABLE IF NOT EXISTS dim_customers AS
SELECT row_number() over (order by customer_id) customer_key, -- surrogate key
    c.customer_id,
    c.first_name,
    c.last_name,
    c.gender,
    c.phone_number,
    c.email email_address,
    c.address street_address,
    c.city,
    c.state,
    c.zipcode,
    c.county,
    c.dob birthdate,
    c.is_active,
    c.loyalty_member,
    c.date_created,
    c.date_inactive
FROM tmart_staging.tmart_int_customers c;
ALTER TABLE dim_customers ADD PRIMARY KEY (`customer_key`);


-- Create Dimension: dim_products
DROP TABLE IF EXISTS dim_products;
CREATE TABLE IF NOT EXISTS dim_products AS
SELECT row_number() over (order by date_created, sku) product_key, -- surrogate key
    p.product_id,
	 p.sku product_sku,
    p.name product_name,
    p.product_type,
    p.brand brand_name,
    p.subcategory_id,
    c.name category,
    s.name subcategory,    
    p.unit_size,
    p.price,
    p.stock_quantity,
    p.is_active,
    p.date_created,
    p.date_inactive
FROM tmart_staging.tmart_int_products p
        LEFT JOIN tmart_staging.tmart_int_products_subcategories s ON p.subcategory_id = s.subcategory_id
        LEFT JOIN tmart_staging.tmart_int_products_categories c ON s.category_id = c.category_id;
ALTER TABLE dim_products ADD PRIMARY KEY (`product_key`);        

-- Create Dimension: dim_date
DROP TABLE IF EXISTS dim_date;
CREATE TABLE dim_date (
  date_key int NOT NULL,
  date date DEFAULT NULL,
  year int DEFAULT NULL,
  quarter int DEFAULT NULL,
  month_name varchar(9) DEFAULT NULL,
  day_name varchar(9) DEFAULT NULL,
  is_weekend tinyint DEFAULT NULL,
  is_holiday tinyint DEFAULT NULL,
  PRIMARY KEY (date_key)
);

-- Create Fact Table: fact_orders
DROP TABLE IF EXISTS fact_orders;
CREATE TABLE IF NOT EXISTS fact_orders AS
SELECT i.order_id,
    i.order_item_id,
    p.product_key,
    c.customer_key,
    date_format(o.order_date,'%Y%m%d' ) order_date_key,
	 date_format(i.ship_date,'%Y%m%d' ) ship_date_key,
    date_format(i.delivered_date,'%Y%m%d' ) delivered_date_key,
    date_format(i.canceled_date,'%Y%m%d' ) canceled_date_key,
    o.order_date order_datetime, 
    i.ship_date ship_datetime,
    i.delivered_date delivered_datetime,
    i.canceled_date canceled_datetime,
    o.delivery_cost delivery_fee,
    i.quantity,
    i.unit_price,
    i.line_total,
    i.item_status
FROM tmart_staging.tmart_int_order_items i
        JOIN tmart_staging.tmart_int_orders o ON i.order_id = o.order_id
        LEFT JOIN tmart_analytics.dim_products p ON i.product_id = p.product_id
        LEFT JOIN tmart_analytics.dim_customers c ON o.customer_id = c.customer_id;
ALTER TABLE fact_orders ADD CONSTRAINT `FK1` FOREIGN KEY (`product_key`) REFERENCES dim_products (`product_key`) ON DELETE NO ACTION ON UPDATE NO ACTION;        
ALTER TABLE fact_orders ADD CONSTRAINT `FK2` FOREIGN KEY (`customer_key`) REFERENCES dim_customers (`customer_key`) ON DELETE NO ACTION ON UPDATE NO ACTION;
