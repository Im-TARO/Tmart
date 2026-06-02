/* 
|  =========================================================
|  Export Tmart tables to CSV
|  ---------------------------------------------------------
|  - Adds a header row using UNION
|	- Replace <PATH> with your desired export directory
|	========================================================= 
*/

SELECT
  'customer_id',
  'first_name',
  'last_name',
  'gender',
  'phone_number',
  'email',
  'address',
  'city',
  'state',
  'zipcode',
  'county',
  'dob',
  'is_active',
  'loyalty_member',
  'date_created',
  'date_inactive',
  'date_updated'
UNION
SELECT
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
FROM
  tmart.customers INTO OUTFILE '<PATH>/tmart_customers.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n';

SELECT
  'order_item_id',
  'order_id',
  'product_id',
  'quantity',
  'unit_price',
  'line_total',
  'item_status',
  'ship_date',
  'delivered_date',
  'canceled_date',
  'date_created',
  'date_updated'
UNION
SELECT
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
FROM
  tmart.order_items INTO OUTFILE '<PATH>/tmart_order_items.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n';

SELECT
  'order_id',
  'customer_id',
  'order_date',
  'total_amount',
  'delivery_cost',
  'date_created',
  'date_updated'
UNION
SELECT
  order_id,
  customer_id,
  order_date,
  total_amount,
  delivery_cost,
  date_created,
  date_updated
FROM
  tmart.orders INTO OUTFILE '<PATH>/tmart_orders.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n';

SELECT
  'product_id',
  'subcategory_id',
  'name',
  'brand',
  'sku',
  'unit_size',
  'price',
  'stock_quantity',
  'is_active',
  'date_created',
  'date_inactive',
  'date_updated'
UNION
SELECT
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
FROM
  tmart.products INTO OUTFILE '<PATH>/tmart_products.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n';

SELECT
  'category_id',
  'name',
  'description'
UNION
SELECT
  category_id,
  name,
  description
FROM
  tmart.products_categories INTO OUTFILE '<PATH>/tmart_products_categories.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n';

SELECT
  'subcategory_id',
  'category_id',
  'name',
  'description'
UNION
SELECT
  subcategory_id,
  category_id,
  name,
  description
FROM
  tmart.products_subcategories INTO OUTFILE '<PATH>/tmart_products_subcategories.csv' FIELDS TERMINATED BY ',' OPTIONALLY ENCLOSED BY '"' ESCAPED BY '\\' LINES TERMINATED BY '\n';