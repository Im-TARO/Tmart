"""
generate_orders.py
------------------
Synthetic order data generator for the T-Mart grocery store analytics project.
 
This script connects to a MySQL database and generates realistic, randomized
order and order-item records within a specified date range. It is designed to
populate the `orders` and `order_items` tables with synthetic transactional data.
 
Usage (PowerShell):
    $env:DB_USER = "your_username"
    $env:DB_PASSWORD = "your_password"
    python generate_orders.py 2024-01-01 2024-01-31 5000
 
Arguments:
    start_date  : Start of the order generation window (YYYY-MM-DD)
    end_date    : End of the order generation window (YYYY-MM-DD)
    num_orders  : Number of orders to generate (default: 1000)
 
Environment Variables:
    DB_HOST     : MySQL host (default: localhost)
    DB_USER     : MySQL username (required)
    DB_PASSWORD : MySQL password (required)
    DB_NAME     : Target database name (default: tmart)
 
Dependencies:
    mysql-connector-python
"""

import argparse
import os
import random
from datetime import datetime, timedelta, time

import mysql.connector

# ---------------------------------------------------------------------------
# Argument Parsing
# ---------------------------------------------------------------------------

def parse_args():
    """
    Parse and return command-line arguments.
 
    Returns:
        argparse.Namespace with attributes:
            - start_date (str)  : Start date string in YYYY-MM-DD format
            - end_date   (str)  : End date string in YYYY-MM-DD format
            - num_orders (int)  : Number of orders to generate (default: 1000)
    """    
    parser = argparse.ArgumentParser(description="Generate sample orders and order items.")
    parser.add_argument("start_date", help="Start date in YYYY-MM-DD format")
    parser.add_argument("end_date", help="End date in YYYY-MM-DD format")
    parser.add_argument("num_orders", 
                        nargs="?", 
                        type=int, 
                        default=1000, 
                        help="Number of orders to generate")
    return parser.parse_args()

# ---------------------------------------------------------------------------
# Date / Time Utilities
# ---------------------------------------------------------------------------

def parse_datetime_start(value: str) -> datetime:
    """
    Parse a date string into a datetime object at midnight (00:00:00).
 
    Args:
        value (str): Date string in YYYY-MM-DD format.
 
    Returns:
        datetime: Parsed datetime at the start of the given day.
 
    Raises:
        argparse.ArgumentTypeError: If the date string format is invalid.
    """    
    try:
        return datetime.strptime(value, "%Y-%m-%d")
    except ValueError as exc:
        raise argparse.ArgumentTypeError(f"Invalid date '{value}'. Use YYYY-MM-DD.") from exc


def random_datetime_between(start: datetime, end: datetime) -> datetime:
    """
    Generate a random datetime between two datetime bounds (inclusive).
 
    Args:
        start (datetime): Lower bound of the range.
        end   (datetime): Upper bound of the range.
 
    Returns:
        datetime: A random datetime within the range, or None if start > end.
    """    
    if start > end:
        return None
    delta_seconds = int((end - start).total_seconds())
    offset = random.randint(0, max(delta_seconds, 0))
    return start + timedelta(seconds=offset)


def random_order_datetime(customer_start, customer_end, global_start, global_end):
    """
    Generate a random order datetime that falls within both the customer's
    active window and the global date range specified by the user.
 
    This ensures orders are never placed before a customer was created
    or after they became inactive.
 
    Args:
        customer_start (datetime): Date the customer account was created.
        customer_end   (datetime): Date the customer became inactive (or now if still active).
        global_start   (datetime): Script-level start date argument.
        global_end     (datetime): Script-level end date argument.
 
    Returns:
        datetime: A valid order datetime, or None if no valid window exists.
    """    
    # Narrow the window to the customer lifetime and global range
    start = max(customer_start, global_start)
    end = min(customer_end, global_end)
    if start > end:
        return None
    return random_datetime_between(start, end)


def random_ship_datetime(order_dt: datetime) -> datetime:
    """
    Generate a realistic ship datetime based on the order datetime.
 
    Shipping is scheduled 1–3 days after the order date. 85% of shipments
    occur during business hours (8am–5pm); the remaining 15% can occur at
    any time, simulating overnight or automated fulfillment runs.
 
    Args:
        order_dt (datetime): The datetime the order was placed.
 
    Returns:
        datetime: The datetime the order was shipped.
    """    
    ship_day = order_dt.date() + timedelta(days=random.randint(1, 3))

    if random.random() < 0.85:
        hour = random.randint(8, 17)
        minute = random.randint(0, 59)
    else:
        hour = random.randint(0, 23)
        minute = random.randint(0, 59)

    second = random.randint(0, 59)
    return datetime.combine(ship_day, time(hour, minute, second))

# ---------------------------------------------------------------------------
# Business Logic
# ---------------------------------------------------------------------------

def item_status_logic():
    """
    Randomly assign a fulfillment status to an order item using weighted
    probability to simulate realistic order outcomes.
 
    Distribution:
        - 70% Delivered  (order fulfilled end-to-end)
        - 20% Shipped    (in transit, not yet delivered)
        - 10% Canceled   (order was canceled before fulfillment)
 
    Returns:
        str: One of 'Delivered', 'Shipped', or 'Canceled'.
    """    
    roll = random.random()
    if roll < 0.7:
        return "Delivered"
    if roll < 0.9:
        return "Shipped"
    return "Canceled"

# ---------------------------------------------------------------------------
# Database Connection
# ---------------------------------------------------------------------------

def get_db_connection():
    """
    Establish and return a MySQL database connection using environment variables.
 
    Environment Variables:
        DB_HOST     : MySQL server hostname (default: localhost)
        DB_USER     : MySQL username (required)
        DB_PASSWORD : MySQL password (required)
        DB_NAME     : Target database name (default: tmart)
 
    Returns:
        mysql.connector.connection.MySQLConnection: Active database connection.
 
    Raises:
        mysql.connector.Error: If the connection cannot be established.
    """            
    return mysql.connector.connect(
        host=os.getenv("DB_HOST", "localhost"),
        user=os.getenv("DB_USER"),
        password=os.getenv("DB_PASSWORD"),
        database=os.getenv("DB_NAME", "tmart"),
    )

# ---------------------------------------------------------------------------
# Main Entry Point
# ---------------------------------------------------------------------------

def main():
    """
    Main execution function, order generation pipeline:
 
        1. Parse and validate command-line arguments
        2. Connect to the MySQL database
        3. Load active customers and products
        4. Determine the next available order_id and order_item_id
        5. Generate randomized orders within the specified date window:
            - Respect each customer's active date range
            - Randomly select 1–8 products per order
            - Apply ±10% price variance to simulate promotions / price drift
            - Assign fulfillment status (Delivered / Shipped / Canceled)
            - Group delivered items by ship day for consistent delivery dates
            - Apply tiered delivery cost based on order total
        6. Commit all records to the database in a single transaction
 
    Raises:
        SystemExit: On validation errors, database errors, or unexpected failures.
    """    
    args = parse_args()

    # Parse dates; set end_date to the last second of the specified day    
    start_date = parse_datetime_start(args.start_date)
    end_date = parse_datetime_start(args.end_date) + timedelta(days=1) - timedelta(seconds=1)

    # Validate date range
    if start_date > end_date:
        raise SystemExit("Error: start_date must be earlier than or equal to end_date.")

    # Validate order count
    if args.num_orders <= 0:
        raise SystemExit("Error: num_orders must be a positive integer.")

    insert_order = """
    INSERT INTO orders
    (order_id, customer_id, order_date, total_amount, delivery_cost, date_created)
    VALUES (%s, %s, %s, %s, %s, %s)
    """

    insert_item = """
    INSERT INTO order_items
    (order_item_id, order_id, product_id, quantity, unit_price, line_total,
     item_status, ship_date, delivered_date, canceled_date, date_created)
    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s, %s, %s)
    """

    conn = None
    cursor = None

    try:
        conn = get_db_connection()
        cursor = conn.cursor(dictionary=True)

         # --- Load reference data ---

        cursor.execute("SELECT customer_id, date_created, date_inactive, loyalty_member FROM customers")
        customers = cursor.fetchall()

        # Only generate orders for products currently listed as active
        cursor.execute("SELECT product_id, price FROM products WHERE is_active = 1")
        products = cursor.fetchall()

        if not customers:
            raise SystemExit("Error: no customers found.")
        if not products:
            raise SystemExit("Error: no active products found.")

        # --- Determine starting IDs to avoid primary key conflicts ---
        
        cursor.execute("SELECT COALESCE(MAX(order_id), 0) + 1 AS next_id FROM orders")
        order_id = cursor.fetchone()["next_id"]

        cursor.execute("SELECT COALESCE(MAX(order_item_id), 0) + 1 AS next_id FROM order_items")
        order_item_id = cursor.fetchone()["next_id"]

        generated_orders = 0

         # --- Order Generation Loop ---
        for _ in range(args.num_orders):

            # Pick a random customer and define their valid ordering window
            customer = random.choice(customers)
            customer_start = customer["date_created"]
            customer_end = customer["date_inactive"] or datetime.now()
            customer_loyalty_member = customer["loyalty_member"]

            # Generate an order datetime within the valid window
            order_dt = random_order_datetime(customer_start, customer_end, start_date, end_date)
            if not order_dt:
                # Skip if no valid window exists for this customer in the date range
                continue

            # Select 1–8 unique products for this order
            num_items = random.randint(1, 8)
            chosen_products = random.sample(products, min(num_items, len(products)))

            items = []
            total_amount = 0.0

            # Track delivery dates by ship day so items shipped together arrive together
            delivered_date_by_ship_day = {}

            for prod in chosen_products:
                product_id = prod["product_id"]
                base_price = float(prod["price"])
                quantity = random.randint(1, 5)

                # Apply a ±10% price variance to simulate real-world price fluctuation
                unit_price = round(base_price * random.uniform(0.9, 1.1), 2)
                line_total = round(unit_price * quantity, 2)

                # Assign item status and populate fulfillment dates accordingly
                status = item_status_logic()
                ship_date = None
                delivered_date = None
                canceled_date = None

                if status == "Delivered":
                    ship_date = random_ship_datetime(order_dt)
                    ship_day = ship_date.date()

                    # Reuse the delivery date for items shipped on the same day
                    if ship_day not in delivered_date_by_ship_day:
                        delivered_date_by_ship_day[ship_day] = ship_date + timedelta(days=random.randint(1, 5))

                    delivered_date = delivered_date_by_ship_day[ship_day]
                    total_amount += line_total
                elif status == "Shipped":
                    ship_date = random_ship_datetime(order_dt)
                    total_amount += line_total
                else:
                    # Canceled items: set a cancellation date within 2 days of the order
                    canceled_date = order_dt + timedelta(days=random.randint(0, 2))
                    # Canceled items are excluded from total_amount

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
                    canceled_date,
                    order_dt
                ))
                order_item_id += 1

            # --- Tiered Delivery Cost ---
            # Free delivery at $75+, scaled cost for smaller orders
            if total_amount == 0 or total_amount >= 75:
                delivery_cost = 0
            elif customer_loyalty_member:
                if total_amount >= 50:
                    delivery_cost = 0
                elif total_amount >= 25:
                    delivery_cost = 5
                else:
                    delivery_cost =10
            else:
                if total_amount >= 50:
                    delivery_cost = 5
                elif total_amount >= 25:
                    delivery_cost = 10
                else:
                    delivery_cost =25

            # --- Insert Order and Items ---
            cursor.execute(insert_order, (
                order_id,
                customer["customer_id"],
                order_dt,
                round(total_amount, 2),
                delivery_cost,
                order_dt
            ))

            for item in items:
                cursor.execute(insert_item, item)

            order_id += 1
            generated_orders += 1

        # Commit all inserts as a single transaction
        conn.commit()
        print(f"{generated_orders} orders generated successfully!")

    except mysql.connector.Error as exc:
        if conn:
            conn.rollback()
        raise SystemExit(f"Database error: {exc}") from exc

    except Exception as exc:
        if conn:
            conn.rollback()
        raise SystemExit(f"Unexpected error: {exc}") from exc

    finally:
        if cursor:
            cursor.close()
        if conn:
            conn.close()


if __name__ == "__main__":
    main()