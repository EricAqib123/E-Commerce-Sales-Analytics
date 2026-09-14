import pandas as pd

# ============================================================
# 1. LOAD DATA
# ============================================================

customers = pd.read_csv("dataset/customers.csv")
products = pd.read_csv("dataset/products.csv")
orders = pd.read_csv("dataset/orders.csv")
order_items = pd.read_csv("dataset/order_items.csv")


# ============================================================
# 2. CLEAN ORDERS DATA
# ============================================================

print("===== ORDERS INFORMATION =====")
orders.info()

print("\n===== MISSING VALUES =====")
print(orders.isnull().sum())

print("\n===== DUPLICATE ROWS =====")
print(orders.duplicated().sum())

orders["order_date"] = pd.to_datetime(
    orders["order_date"]
)

orders = orders.drop_duplicates()


# ============================================================
# 3. CALCULATE REVENUE
# ============================================================

order_items["revenue"] = (
    order_items["quantity"] *
    order_items["unit_price"]
)


# ============================================================
# 4. MERGE PRODUCTS WITH ORDER ITEMS
# ============================================================

sales = order_items.merge(
    products,
    on="product_id"
)


# ============================================================
# 5. CALCULATE PROFIT
# ============================================================

sales["profit"] = (
    sales["revenue"] -
    sales["quantity"] * sales["cost"]
)


# ============================================================
# 6. DISPLAY RESULTS
# ============================================================

print("\n===== CUSTOMERS =====")
print(customers.head())

print("\n===== PRODUCTS =====")
print(products.head())

print("\n===== ORDERS =====")
print(orders.head())

print("\n===== ORDER ITEMS =====")
print(order_items.head())

print("\n===== SALES DATA =====")
print(
    sales[
        [
            "order_id",
            "product_id",
            "quantity",
            "unit_price",
            "revenue",
            "cost",
            "profit"
        ]
    ].head(20)
)


# ============================================================
# 7. TOTAL SALES & PROFIT
# ============================================================

total_revenue = sales["revenue"].sum()
total_profit = sales["profit"].sum()

print("\n===== BUSINESS SUMMARY =====")
print(f"Total Revenue: ${total_revenue:,.2f}")
print(f"Total Profit: ${total_profit:,.2f}")
