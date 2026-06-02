USE tmart_staging;

-- -----------------------------------------------------
-- Table tmart_staging.tmart_int_customers
-- -----------------------------------------------------
DROP TABLE IF EXISTS tmart_int_customers;

CREATE TABLE IF NOT EXISTS tmart_int_customers(
  customer_id INT,
  first_name VARCHAR(50),
  last_name VARCHAR(50),
  gender VARCHAR(8),
  phone_number VARCHAR(12),
  email VARCHAR(255),
  address VARCHAR(200),
  city VARCHAR(100),
  state CHAR(2),
  zipcode VARCHAR(10),
  county VARCHAR(50),
  dob DATE,
  is_active TINYINT,
  loyalty_member TINYINT,
  date_created DATE,
  date_inactive DATE,
  date_updated DATETIME,
  dwh_create_date DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table tmart_staging.tmart_int_products_categories
-- -----------------------------------------------------
DROP TABLE IF EXISTS tmart_int_products_categories;

CREATE TABLE IF NOT EXISTS tmart_int_products_categories (
    category_id INT,
    name VARCHAR(100),
    description VARCHAR(255),
    dwh_create_date DATETIME DEFAULT CURRENT_TIMESTAMP
)  ENGINE=INNODB;

-- -----------------------------------------------------
-- Table tmart_staging.tmart_int_products_subcategories
-- -----------------------------------------------------
DROP TABLE IF EXISTS tmart_int_products_subcategories;

CREATE TABLE IF NOT EXISTS tmart_int_products_subcategories(
	subcategory_id INT, 
   category_id INT, 
   name VARCHAR(100), 
   description VARCHAR(255),
   dwh_create_date DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table tmart_staging.tmart_int_products
-- -----------------------------------------------------
DROP TABLE IF EXISTS tmart_int_products;

CREATE TABLE IF NOT EXISTS tmart_int_products(
  product_id INT,
  subcategory_id INT,
  name VARCHAR(300),
  product_type VARCHAR(300),
  brand VARCHAR(100),
  sku VARCHAR(50),
  unit_size VARCHAR(50),
  price DECIMAL(10, 2),
  stock_quantity INT,
  is_active TINYINT,
  date_created DATE,
  date_inactive DATE,
  date_updated DATETIME,
  dwh_create_date DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table tmart_staging.tmart_int_orders
-- -----------------------------------------------------
DROP TABLE IF EXISTS tmart_int_orders;

CREATE TABLE IF NOT EXISTS tmart_int_orders(
  order_id INT,
  customer_id INT,
  order_date DATETIME,
  total_amount DECIMAL(10, 2),
  delivery_cost DECIMAL(10, 2),
  date_created DATE,
  date_updated DATETIME,
  dwh_create_date DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB;

-- -----------------------------------------------------
-- Table tmart_staging.tmart_int_order_items
-- -----------------------------------------------------
DROP TABLE IF EXISTS tmart_int_order_items;

CREATE TABLE IF NOT EXISTS tmart_int_order_items(
  order_item_id INT,
  order_id INT,
  product_id INT,
  quantity INT,
  unit_price DECIMAL(10, 2),
  line_total DECIMAL(10, 2),
  item_status VARCHAR(50),
  ship_date DATETIME,
  delivered_date DATETIME,
  canceled_date DATETIME,
  date_created DATETIME,
  date_updated DATETIME,
  dwh_create_date DATETIME DEFAULT CURRENT_TIMESTAMP
) ENGINE = InnoDB;