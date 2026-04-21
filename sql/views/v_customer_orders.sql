USE tmart;

CREATE OR REPLACE VIEW v_customer_orders AS
SELECT
  o.customer_id,
  c.dob customer_dob,
  c.city,
  c.state,
  c.zipcode,
  c.county,
  c.is_active customer_active,
  c.date_created customer_create_date,
  c.date_inactive customer_inactive_date,
  c.loyalty_member,
  o.order_id,
  o.order_date,
  o.total_amount,
  o.delivery_cost,
  oi.product_id,
  p.name product_name, 
  p.sku product_sku,
  p.is_active product_active,
  p.date_created product_create_date,
  p.date_inactive product_inactive_date,
  pc.name category,
  ps.name subcategory,
  oi.quantity item_qty,
  oi.unit_price item_unit_price,
  oi.line_total item_line_total,
  oi.item_status,
  oi.ship_date item_ship_date,
  oi.canceled_date item_cancel_date
FROM
  orders o
  JOIN order_items oi ON o.order_id = oi.order_id
  JOIN customers c ON o.customer_id = c.customer_id
  JOIN products p ON oi.product_id = p.product_id
  JOIN products_subcategories ps ON p.subcategory_id = ps.subcategory_id
  JOIN products_categories pc ON ps.category_id = pc.category_id;