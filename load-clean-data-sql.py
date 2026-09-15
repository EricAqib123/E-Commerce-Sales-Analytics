import mysql.connector
import pandas as pd
import os

# ============================================================
# 1. CONNECT TO MYSQL
# ============================================================

mydb = mysql.connector.connect(
    host="localhost",
    port=3306,
    user="root",
    password="123456",
    database="ecommerce_sales"
)

mycursor = mydb.cursor()

print("Database connected successfully!")


# ============================================================
# 2. CREATE TABLES
# ============================================================

create_customers = """
CREATE TABLE IF NOT EXISTS customers (
    customer_id INT PRIMARY KEY,
    customer_name VARCHAR(255),
    city VARCHAR(100),
    country VARCHAR(100),
    signup_date DATE
)
"""

create_products = """
CREATE TABLE IF NOT EXISTS products (
    product_id INT PRIMARY KEY,
    product_name VARCHAR(255),
    category VARCHAR(100),
    cost DECIMAL(10,2),
    selling_price DECIMAL(10,2)
)
"""

create_orders = """
CREATE TABLE IF NOT EXISTS orders (
    order_id INT PRIMARY KEY,
    customer_id INT,
    order_date DATE,
    status VARCHAR(50),
    FOREIGN KEY (customer_id) REFERENCES customers(customer_id)
)
"""

create_order_items = """
CREATE TABLE IF NOT EXISTS order_items (
    order_id INT,
    product_id INT,
    quantity INT,
    unit_price DECIMAL(10,2),
    PRIMARY KEY (order_id, product_id),
    FOREIGN KEY (order_id) REFERENCES orders(order_id),
    FOREIGN KEY (product_id) REFERENCES products(product_id)
)
"""

mycursor.execute(create_customers)
mycursor.execute(create_products)
mycursor.execute(create_orders)
mycursor.execute(create_order_items)

mydb.commit()

print("Tables created successfully!")


# ============================================================
# 3. CSV FILE LOCATIONS
# ============================================================

base_path = r"D:\E-Commerce Sales Analytics"

customers_file = os.path.join(base_path, "dataset/customers.csv")
products_file = os.path.join(base_path, "dataset/products.csv")
orders_file = os.path.join(base_path, "dataset/orders.csv")
order_items_file = os.path.join(base_path, "dataset/order_items.csv")


# ============================================================
# 4. FUNCTION TO CLEAN COLUMN NAMES
# ============================================================

def clean_columns(df):
    df.columns = (
        df.columns
        .str.strip()
        .str.lower()
        .str.replace(" ", "_")
    )

    return df


# ============================================================
# 5. LOAD CUSTOMERS
# ============================================================

print("\nLoading customers...")

customers = pd.read_csv(customers_file)

customers = clean_columns(customers)

customers = customers.drop_duplicates()

customers["customer_id"] = pd.to_numeric(
    customers["customer_id"],
    errors="coerce"
)

customers = customers.dropna(subset=["customer_id"])

customers["customer_id"] = customers["customer_id"].astype(int)

customers["signup_date"] = pd.to_datetime(
    customers["signup_date"],
    errors="coerce"
).dt.date

customers = customers.where(pd.notnull(customers), None)

customer_sql = """
INSERT IGNORE INTO customers
(customer_id, customer_name, city, country, signup_date)
VALUES (%s, %s, %s, %s, %s)
"""

for _, row in customers.iterrows():
    mycursor.execute(
        customer_sql,
        (
            row["customer_id"],
            row["customer_name"],
            row["city"],
            row["country"],
            row["signup_date"]
        )
    )

mydb.commit()

print(f"Customers loaded: {len(customers)}")


# ============================================================
# 6. LOAD PRODUCTS
# ============================================================

print("\nLoading products...")

products = pd.read_csv(products_file)

products = clean_columns(products)

products = products.drop_duplicates()

products["product_id"] = pd.to_numeric(
    products["product_id"],
    errors="coerce"
)

products = products.dropna(subset=["product_id"])

products["product_id"] = products["product_id"].astype(int)

products["cost"] = pd.to_numeric(
    products["cost"],
    errors="coerce"
)

products["selling_price"] = pd.to_numeric(
    products["selling_price"],
    errors="coerce"
)

products = products.where(pd.notnull(products), None)

product_sql = """
INSERT IGNORE INTO products
(product_id, product_name, category, cost, selling_price)
VALUES (%s, %s, %s, %s, %s)
"""

for _, row in products.iterrows():
    mycursor.execute(
        product_sql,
        (
            row["product_id"],
            row["product_name"],
            row["category"],
            row["cost"],
            row["selling_price"]
        )
    )

mydb.commit()

print(f"Products loaded: {len(products)}")


# ============================================================
# 7. LOAD ORDERS
# ============================================================

print("\nLoading orders...")

orders = pd.read_csv(orders_file)

orders = clean_columns(orders)

orders = orders.drop_duplicates()

orders["order_id"] = pd.to_numeric(
    orders["order_id"],
    errors="coerce"
)

orders["customer_id"] = pd.to_numeric(
    orders["customer_id"],
    errors="coerce"
)

orders = orders.dropna(
    subset=["order_id", "customer_id"]
)

orders["order_id"] = orders["order_id"].astype(int)
orders["customer_id"] = orders["customer_id"].astype(int)

orders["order_date"] = pd.to_datetime(
    orders["order_date"],
    errors="coerce"
).dt.date

orders = orders.where(pd.notnull(orders), None)

order_sql = """
INSERT IGNORE INTO orders
(order_id, customer_id, order_date, status)
VALUES (%s, %s, %s, %s)
"""

for _, row in orders.iterrows():
    mycursor.execute(
        order_sql,
        (
            row["order_id"],
            row["customer_id"],
            row["order_date"],
            row["status"]
        )
    )

mydb.commit()

print(f"Orders loaded: {len(orders)}")


# ============================================================
# 8. LOAD ORDER ITEMS
# ============================================================

print("\nLoading order items...")

order_items = pd.read_csv(order_items_file)

order_items = clean_columns(order_items)

order_items = order_items.drop_duplicates()

order_items["order_id"] = pd.to_numeric(
    order_items["order_id"],
    errors="coerce"
)

order_items["product_id"] = pd.to_numeric(
    order_items["product_id"],
    errors="coerce"
)

order_items["quantity"] = pd.to_numeric(
    order_items["quantity"],
    errors="coerce"
)

order_items["unit_price"] = pd.to_numeric(
    order_items["unit_price"],
    errors="coerce"
)

order_items = order_items.dropna(
    subset=["order_id", "product_id", "quantity", "unit_price"]
)

order_items["order_id"] = order_items["order_id"].astype(int)
order_items["product_id"] = order_items["product_id"].astype(int)
order_items["quantity"] = order_items["quantity"].astype(int)

order_items = order_items.where(
    pd.notnull(order_items),
    None
)

order_item_sql = """
INSERT IGNORE INTO order_items
(order_id, product_id, quantity, unit_price)
VALUES (%s, %s, %s, %s)
"""

for _, row in order_items.iterrows():
    mycursor.execute(
        order_item_sql,
        (
            row["order_id"],
            row["product_id"],
            row["quantity"],
            row["unit_price"]
        )
    )

mydb.commit()

print(f"Order items loaded: {len(order_items)}")


# ============================================================
# 9. VERIFY DATA
# ============================================================

print("\n==============================")
print("DATABASE VERIFICATION")
print("==============================")

tables = [
    "customers",
    "products",
    "orders",
    "order_items"
]

for table in tables:
    mycursor.execute(
        f"SELECT COUNT(*) FROM {table}"
    )

    count = mycursor.fetchone()[0]

    print(f"{table}: {count} records")


# ============================================================
# 10. CLOSE CONNECTION
# ============================================================

mycursor.close()
mydb.close()

print("\nDatabase connection closed.")
print("Data loading completed successfully!")
