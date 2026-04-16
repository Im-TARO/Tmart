-- create product tables
USE tmart;

DROP TABLE if EXISTS products;
DROP TABLE if EXISTS products_subcategories;
DROP TABLE if EXISTS products_categories;

-- Categories(top-level)
CREATE TABLE products_categories(
  category_id INT AUTO_INCREMENT PRIMARY KEY,
  name VARCHAR(100) NOT NULL,
  description VARCHAR(255) DEFAULT NULL
) ENGINE = INNODB DEFAULT CHARSET = UTF8MB4;

-- Sub-categories(child of categories)
CREATE TABLE products_subcategories(
  subcategory_id INT AUTO_INCREMENT PRIMARY KEY,
  category_id INT NOT NULL,
  name VARCHAR(100) NOT NULL,
  description VARCHAR(255),
  CONSTRAINT fk_prod_subcategory_category FOREIGN KEY(category_id) REFERENCES products_categories(category_id) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE = INNODB DEFAULT CHARSET = UTF8MB4;

-- Products
CREATE TABLE products(
  product_id INT AUTO_INCREMENT PRIMARY KEY,
  subcategory_id INT NOT NULL,
  name VARCHAR(150) NOT NULL,
  brand VARCHAR(100),
  sku VARCHAR(50),
  unit_size VARCHAR(50),
  price DECIMAL(10, 2) NOT NULL,
  stock_quantity INT NOT NULL DEFAULT 0,
  is_active TINYINT(1) NOT NULL DEFAULT 1,
  date_created DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  date_inactive DATETIME DEFAULT NULL,
  date_updated DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_product_subcategory FOREIGN KEY(subcategory_id) REFERENCES products_subcategories(subcategory_id) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE = INNODB DEFAULT CHARSET = UTF8MB4;