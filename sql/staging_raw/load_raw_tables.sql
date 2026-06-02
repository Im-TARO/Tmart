/*
| ******************
|  load raw data
| ******************
 */
 
use tmart_staging;

/*
| --------------------------------------------------------
| Table tmart_staging.tmart_raw_customers
| -------------------------------------------------------
*/
truncate TABLE tmart_raw_customers;

load data INFILE '<PATH>/tmart_customers.csv' INTO
TABLE tmart_raw_customers FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n' IGNORE 1 ROWS(
  customer_id,
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
  date_updated
);

/*
| ----------------------------------------------------------
| Table tmart_staging.tmart_raw_order_items
| ----------------------------------------------------------
*/
truncate TABLE tmart_raw_order_items;

load data INFILE '<PATH>/tmart_order_items.csv' INTO
TABLE tmart_raw_order_items FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n' IGNORE 1 ROWS(
  order_item_id,
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
  date_updated
);

/*
| ---------------------------------------------------
| Table tmart_staging.tmart_raw_orders
| ---------------------------------------------------
*/
truncate TABLE tmart_raw_orders;

load data INFILE '<PATH>/tmart_orders.csv' INTO
TABLE tmart_raw_orders FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n' IGNORE 1 ROWS(
order_id, customer_id, order_date, total_amount, delivery_cost, date_created, date_updated
);

/*
| -----------------------------------------------------
| Table tmart_staging.tmart_raw_products
| -----------------------------------------------------
*/
truncate TABLE tmart_raw_products;

load data INFILE '<PATH>/tmart_products.csv' INTO
TABLE tmart_raw_products FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n' IGNORE 1 ROWS(
  product_id,
  subcategory_id,
  name,
  brand,
  sku,
  unit_size,
  price,
  stock_quantity,
  is_active,
  date_created,
  date_inactive,
  date_updated
);

/*
| ---------------------------------------------------------------------
| Table tmart_staging.tmart_raw_products_categories
| ---------------------------------------------------------------------
*/
truncate TABLE tmart_raw_products_categories;

load data INFILE '<PATH>/tmart_products_categories.csv' INTO
TABLE tmart_raw_products_categories FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n' IGNORE 1 ROWS(
category_id, name, description
);

/*
| --------------------------------------------------------------------------
| Table tmart_staging.tmart_raw_products_subcategories
| --------------------------------------------------------------------------
*/
truncate TABLE tmart_raw_products_subcategories;

load data INFILE '<PATH>/tmart_products_subcategories.csv' INTO
TABLE tmart_raw_products_subcategories FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n' IGNORE 1 ROWS(
subcategory_id, category_id, name, description
);