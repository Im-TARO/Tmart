# load int data
use tmart_staging;

-- -----------------------------------------------------
-- Table tmart_staging.tmart_int_customers
-- -----------------------------------------------------
truncate TABLE tmart_int_customers;

INSERT INTO tmart_int_customers
(customer_id,
first_name,
last_name,
gender,
phone_number,
email,
address,
city,
state,
zipcode,
county,
dob,
is_active,
loyalty_member,
date_created,
date_inactive,
date_updated)
SELECT 
    customer_id,
    TRIM(first_name) first_name,
    TRIM(last_name) last_name,
    CASE
        WHEN TRIM(UPPER(gender)) = 'F' THEN 'Female'
        WHEN TRIM(UPPER(gender)) = 'M' THEN 'Male'
        WHEN TRIM(UPPER(gender)) = 'O' THEN 'Other'
        ELSE 'Unknown'
    END gender,
    phone_number,
    TRIM(email) email,
    TRIM(address) address,
    TRIM(city) city,
    TRIM(UPPER(state)) state,
    zipcode,
    TRIM(county) county,
    CASE
        WHEN dob > NOW() THEN NULL
        ELSE dob
    END dob,
    is_active,
    loyalty_member,
    CAST(date_created AS DATE) date_created,
    CAST(date_inactive AS DATE) date_inactive,
    date_updated
FROM
    tmart_raw_customers;


-- -----------------------------------------------------
-- Table tmart_staging.tmart_int_order_items
-- -----------------------------------------------------
truncate TABLE tmart_int_order_items;

INSERT INTO tmart_int_order_items
(order_item_id,
order_id,
product_id,
quantity,
unit_price,
line_total,
item_status,
ship_date,
delivered_date,
canceled_date,
date_created,
date_updated)
SELECT 
    order_item_id,
    order_id,
    product_id,
    quantity,
    unit_price,
    line_total,
    UPPER(TRIM(item_status)) item_status,
    ship_date,
    delivered_date,
    canceled_date,
    date_created,
    date_updated
FROM
    tmart_raw_order_items;

-- -----------------------------------------------------
-- Table tmart_staging.tmart_int_orders
-- -----------------------------------------------------
truncate TABLE tmart_int_orders;

INSERT INTO tmart_int_orders
(order_id,
customer_id,
order_date,
total_amount,
delivery_cost,
date_created,
date_updated)
SELECT order_id,
    customer_id,
    order_date,
    total_amount,
    delivery_cost,
    cast(date_created as date) date_created,
    date_updated
FROM tmart_raw_orders;


-- -----------------------------------------------------
-- Table tmart_staging.tmart_int_products
-- -----------------------------------------------------
truncate TABLE tmart_int_products;

INSERT INTO tmart_int_products
(product_id,
subcategory_id,
name,
product_type, 
brand,
sku,
unit_size,
price,
stock_quantity,
is_active,
date_created,
date_inactive,
date_updated)
SELECT product_id,
    subcategory_id,
    trim(name) name,
    trim(substring(name, length(trim(brand))+1)) product_type, -- derived column
    trim(brand) brand,
    trim(upper(sku)) sku,
    trim(unit_size) unit_size,
    price,
    stock_quantity,
    is_active,
    cast(date_created as date) date_created,
    cast(date_inactive as date) date_inactive,
    date_updated
FROM tmart_raw_products;

-- -----------------------------------------------------
-- Table tmart_staging.tmart_int_products_categories
-- -----------------------------------------------------
truncate TABLE tmart_int_products_categories;

INSERT INTO tmart_int_products_categories
(category_id,
name,
description)
SELECT 
    category_id,
    trim(name) name,
    trim(description) description
FROM
    tmart_raw_products_categories;

-- -----------------------------------------------------
-- Table tmart_staging.tmart_int_products_subcategories
-- -----------------------------------------------------
truncate TABLE tmart_int_products_subcategories;

INSERT INTO tmart_int_products_subcategories
(subcategory_id,
category_id,
name,
description)
SELECT 
    subcategory_id,
    category_id,
    trim(name) name,
    trim(description) description
FROM
    tmart_raw_products_subcategories;
