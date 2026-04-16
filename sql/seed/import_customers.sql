USE tmart;

/* Load the products raw data */
LOAD DATA INFILE '<path>/customers.csv' INTO
TABLE customers FIELDS TERMINATED BY ',' IGNORE 1 ROWS(
  customer_id,
  first_name,
  last_name,
  phone_number,
  email,
  address,
  city,
  state,
  zipcode,
  county,
  dob,
  is_active,
  loyalty_memeber
);

SELECT *
  FROM customers
 LIMIT 20;