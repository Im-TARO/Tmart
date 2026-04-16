USE tmart;

/* Create products raw table */
DROP TABLE IF EXISTS products_raw;

CREATE TABLE products_raw(
  product_id TEXT,
  category TEXT,
  subcategory TEXT,
  name TEXT,
  brand TEXT,
  sku TEXT,
  unit_size TEXT,
  price TEXT,
  stock_quantity TEXT,
  is_active TEXT
);

-- 10,000 rows loaded in the raw table  
SELECT
  COUNT(*),
  COUNT(DISTINCT sku), -- 10,000 unique SKUs
  COUNT(DISTINCT name, unit_size) -- 10,000 unique name/unit_size combo
FROM
  products_raw;

-- all the subcatogories in the raw table exist in the Tmart DB
SELECT
  subcategory
FROM
  products_raw
WHERE
  NOT EXISTS (
    SELECT
      name
    FROM
      products_subcategories
  );

/* Load the products raw data */
LOAD DATA INFILE '<path>/tmart_products.csv' INTO TABLE products_raw FIELDS TERMINATED BY ',' IGNORE 1 ROWS(
  product_id,
  category,
  subcategory,
  name,
  brand,
  sku,
  unit_size,
  price,
  stock_quantity,
  is_active
);

/* load raw data into the target table */
INSERT INTO
  products(subcategory_id, name, brand, sku, unit_size, price, stock_quantity, is_active)
SELECT
  CAST(s.subcategory_id AS UNSIGNED) subcategory_id,
  CAST(r.name AS CHAR) name,
  CAST(r.brand AS CHAR) brand,
  CAST(r.sku AS CHAR) sku,
  CAST(r.unit_size AS CHAR) unit_size,
  CAST(r.price AS DECIMAL(10, 2)) price,
  CAST(r.stock_quantity AS UNSIGNED) stock_quantity,
  CAST(r.is_active AS UNSIGNED) is_active
FROM
  products_raw r
  JOIN products_subcategories s ON r.subcategory = s.name;

-- 10,000 rows in the target table
SELECT
  COUNT(*)
FROM
  products;

/* export data */
SELECT
  'product_id',
  'category',
  'subcategory',
  'name',
  'brand',
  'sku',
  'unit_size',
  'price',
  'stock_quantity',
  'is_active',
  'date_created',
  'date_updated'
UNION
SELECT
  p.product_id,
  c.name,
  s.name,
  p.name,
  p.brand,
  p.sku,
  p.unit_size,
  p.price,
  p.stock_quantity,
  p.is_active,
  p.date_created,
  p.date_updated INTO OUTFILE '<path>/tmart_products_export.csv' FIELDS TERMINATED BY ','
FROM
  products p
  JOIN products_subcategories s ON p.subcategory_id = s.subcategory_id
  JOIN products_categories c ON s.category_id = c.category_id;