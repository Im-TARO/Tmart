USE tmart;

DROP TABLE if EXISTS order_items;
DROP TABLE if EXISTS orders;

CREATE TABLE orders(
  order_id INT AUTO_INCREMENT PRIMARY KEY,
  customer_id INT,
  order_date datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  total_amount decimal(10, 2),
  delivery_cost decimal(10, 2),
  date_created datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  date_updated datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_customer FOREIGN KEY(customer_id) REFERENCES customers(customer_id) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE = INNODB DEFAULT CHARSET = UTF8MB4;

CREATE TABLE order_items(
  order_item_id INT AUTO_INCREMENT PRIMARY KEY,
  order_id INT,
  product_id INT,
  quantity INT,
  unit_price decimal(10, 2),
  line_total decimal(10, 2),
  item_status varchar(50),
  ship_date datetime,
  delivered_date datetime,
  cancelled_date datetime,
  date_created datetime NOT NULL DEFAULT CURRENT_TIMESTAMP,
  date_updated datetime NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  CONSTRAINT fk_order FOREIGN KEY(order_id) REFERENCES orders(order_id) ON UPDATE CASCADE ON DELETE RESTRICT,
  CONSTRAINT pk_products FOREIGN KEY(product_id) REFERENCES products(product_id) ON UPDATE CASCADE ON DELETE RESTRICT
) ENGINE = INNODB DEFAULT CHARSET = UTF8MB4;