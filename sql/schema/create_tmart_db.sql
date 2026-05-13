SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0;
SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0;
SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION';

-- -----------------------------------------------------
-- Schema tmart
-- -----------------------------------------------------
CREATE SCHEMA IF NOT EXISTS `tmart` DEFAULT CHARACTER SET utf8mb4 COLLATE utf8mb4_0900_ai_ci;

USE `tmart`;

-- -----------------------------------------------------
-- Table `tmart`.`customers`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tmart`.`customers` (
  `customer_id` INT NOT NULL AUTO_INCREMENT,
  `first_name` VARCHAR(50) NOT NULL,
  `last_name` VARCHAR(50) NOT NULL,
  `gender` CHAR(1) NULL DEFAULT NULL,
  `phone_number` VARCHAR(12) NULL DEFAULT NULL,
  `email` VARCHAR(255) NULL DEFAULT NULL,
  `address` VARCHAR(200) NULL DEFAULT NULL,
  `city` VARCHAR(100) NULL DEFAULT NULL,
  `state` CHAR(2) NULL DEFAULT NULL,
  `zipcode` VARCHAR(10) NULL DEFAULT NULL,
  `county` VARCHAR(50) NULL DEFAULT NULL,
  `dob` DATE NULL DEFAULT NULL,
  `is_active` TINYINT NULL DEFAULT NULL,
  `loyalty_member` TINYINT NULL DEFAULT NULL,
  `date_created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_inactive` DATETIME NULL DEFAULT NULL,
  `date_updated` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(`customer_id`)
) ENGINE = InnoDB AUTO_INCREMENT = 301 DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Table `tmart`.`products_categories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tmart`.`products_categories` (
  `category_id` INT NOT NULL AUTO_INCREMENT,
  `name` VARCHAR(100) NOT NULL,
  `description` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY(`category_id`)
) ENGINE = InnoDB AUTO_INCREMENT = 7 DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Table `tmart`.`products_subcategories`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tmart`.`products_subcategories` (
  `subcategory_id` INT NOT NULL AUTO_INCREMENT,
  `category_id` INT NOT NULL,
  `name` VARCHAR(100) NOT NULL,
  `description` VARCHAR(255) NULL DEFAULT NULL,
  PRIMARY KEY(`subcategory_id`),
  INDEX `fk_prod_subcategory_category` (`category_id` ASC) VISIBLE,
  CONSTRAINT `fk_prod_subcategory_category` FOREIGN KEY(`category_id`) REFERENCES `tmart`.`products_categories` (`category_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 41 DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Table `tmart`.`products`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tmart`.`products` (
  `product_id` INT NOT NULL AUTO_INCREMENT,
  `subcategory_id` INT NOT NULL,
  `name` VARCHAR(300) NOT NULL,
  `brand` VARCHAR(100) NULL DEFAULT NULL,
  `sku` VARCHAR(50) NULL DEFAULT NULL,
  `unit_size` VARCHAR(50) NULL DEFAULT NULL,
  `price` DECIMAL(10, 2) NOT NULL,
  `stock_quantity` INT NOT NULL DEFAULT '0',
  `is_active` TINYINT(1) NOT NULL DEFAULT '1',
  `date_created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_inactive` DATETIME NULL DEFAULT NULL,
  `date_updated` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(`product_id`),
  INDEX `fk_product_subcategory` (`subcategory_id` ASC) VISIBLE,
  CONSTRAINT `fk_product_subcategory` FOREIGN KEY(`subcategory_id`) REFERENCES `tmart`.`products_subcategories` (`subcategory_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 10001 DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Table `tmart`.`orders`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tmart`.`orders` (
  `order_id` INT NOT NULL AUTO_INCREMENT,
  `customer_id` INT NULL DEFAULT NULL,
  `order_date` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `total_amount` DECIMAL(10, 2) NULL DEFAULT NULL,
  `delivery_cost` DECIMAL(10, 2) NULL DEFAULT NULL,
  `date_created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_updated` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(`order_id`),
  INDEX `fk_customer` (`customer_id` ASC) VISIBLE,
  CONSTRAINT `fk_customer` FOREIGN KEY(`customer_id`) REFERENCES `tmart`.`customers` (`customer_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 10001 DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

-- -----------------------------------------------------
-- Table `tmart`.`order_items`
-- -----------------------------------------------------
CREATE TABLE IF NOT EXISTS `tmart`.`order_items` (
  `order_item_id` INT NOT NULL AUTO_INCREMENT,
  `order_id` INT NULL DEFAULT NULL,
  `product_id` INT NULL DEFAULT NULL,
  `quantity` INT NULL DEFAULT NULL,
  `unit_price` DECIMAL(10, 2) NULL DEFAULT NULL,
  `line_total` DECIMAL(10, 2) NULL DEFAULT NULL,
  `item_status` VARCHAR(50) NULL DEFAULT NULL,
  `ship_date` DATETIME NULL DEFAULT NULL,
  `delivered_date` DATETIME NULL DEFAULT NULL,
  `canceled_date` DATETIME NULL DEFAULT NULL,
  `date_created` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP,
  `date_updated` DATETIME NOT NULL DEFAULT CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP,
  PRIMARY KEY(`order_item_id`),
  INDEX `fk_order` (`order_id` ASC) VISIBLE,
  INDEX `pk_products` (`product_id` ASC) VISIBLE,
  CONSTRAINT `fk_order` FOREIGN KEY(`order_id`) REFERENCES `tmart`.`orders` (`order_id`) ON DELETE RESTRICT ON UPDATE CASCADE,
  CONSTRAINT `pk_products` FOREIGN KEY(`product_id`) REFERENCES `tmart`.`products` (`product_id`) ON DELETE RESTRICT ON UPDATE CASCADE
) ENGINE = InnoDB AUTO_INCREMENT = 44969 DEFAULT CHARACTER SET = utf8mb4 COLLATE = utf8mb4_0900_ai_ci;

SET SQL_MODE=@OLD_SQL_MODE;
SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS;
SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS;