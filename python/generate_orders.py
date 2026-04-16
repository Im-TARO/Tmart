import mysql.connector
import random
from datetime import datetime, timedelta

NUM_ORDERS = 10000

# -----------------------------
# DB CONNECTION
# -----------------------------
conn = mysql.connector.connect(
    host="localhost",
    user="user_name",
    password="password",
    database="tmart"
)

cursor = conn.cursor(dictionary=True)

# -----------------------------
# LOAD DATA
# -----------------------------
cursor.execute("SELECT customer_id, date_created, date_inactive FROM customers")
customers = cursor.fetchall()

cursor.execute("SELECT product_id, price FROM products WHERE is_active = 1")
products = cursor.fetchall()

# -----------------------------
# HELPERS
# -----------------------------
#def random_date(start_days_ago=2260):
#    base = datetime.now() - timedelta(days=random.randint(0, start_days_ago))
#    return base

def random_order_date(customer):

    start = customer["date_created"]

    if customer["date_inactive"]:
        end = customer["date_inactive"]
    else:
        end = datetime.now()

    # ensure valid range
    if start >= end:
        end = start + timedelta(days=1)

    # bias toward more recent dates
    delta_days = (end - start).days
    weighted_day = int(random.triangular(0, delta_days, delta_days))

    return start + timedelta(days=weighted_day)


def item_status_logic():
    # realistic distribution
    roll = random.random()

    if roll < 0.7:
        return "Delivered"
    elif roll < 0.9:
        return "Shipped"
    else:
        return "Cancelled"


# -----------------------------
# INSERT SQL
# -----------------------------
insert_order = """
INSERT INTO orders
(order_id, customer_id, order_date, total_amount, delivery_cost, date_created)
VALUES (%s, %s, %s, %s, %s, %s)
"""

insert_item = """
INSERT INTO order_items
(order_item_id, order_id, product_id, quantity, unit_price, line_total,
 item_status, ship_date, delivered_date, cancelled_date, date_created)
VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
"""

# -----------------------------
# GENERATION
# -----------------------------
order_id = 1
order_item_id = 1

for _ in range(NUM_ORDERS):

    customer = random.choice(customers)
    
    order_date = random_order_date(customer)
    total_amount = 0

    items = []

    num_items = random.randint(1, 8)

    chosen_products = random.sample(products, min(num_items, len(products)))

    for prod in chosen_products:

        product_id = prod["product_id"]
        price = float(prod["price"])

        quantity = random.randint(1, 5)

        unit_price = round(price * random.uniform(0.9, 1.1), 2)
        line_total = round(unit_price * quantity, 2)

        status = item_status_logic()

        ship_date = None
        delivered_date = None
        cancelled_date = None

        if status == "Delivered":
            ship_date = order_date + timedelta(days=random.randint(1, 3))
            delivered_date = ship_date + timedelta(days=random.randint(1, 5))

        elif status == "Shipped":
            ship_date = order_date + timedelta(days=random.randint(1, 3))

        elif status == "Cancelled":
            cancelled_date = order_date + timedelta(days=random.randint(0, 2))

        total_amount += line_total

        if total_amount >= 75:
            delivery_cost = 0
        elif total_amount >= 50:
            delivery_cost = 5
        elif total_amount >= 25:
            delivery_cost = 10            
        else:
            delivery_cost = 25

        items.append((
            order_item_id,
            order_id,
            product_id,
            quantity,
            unit_price,
            line_total,
            status,
            ship_date,
            delivered_date,
            cancelled_date,
            order_date
        ))

        order_item_id += 1

    # Insert order
    cursor.execute(insert_order, (
        order_id,
        customer["customer_id"],
        order_date,
        round(total_amount, 2),
        delivery_cost,
        order_date
    ))

    # Insert items
    for item in items:
        cursor.execute(insert_item, item)

    order_id += 1

conn.commit()

print(f"{NUM_ORDERS} orders generated successfully!")

cursor.close()
conn.close()