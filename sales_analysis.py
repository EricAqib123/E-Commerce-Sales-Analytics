import pandas as pd

# ============================================================
# E-COMMERCE SALES ANALYTICS
# Data Loading + Cleaning + Revenue + Profit Analysis
# ============================================================


# ============================================================
# 1. LOAD DATASETS
# ============================================================

customers = pd.read_csv("dataset/customers.csv")
products = pd.read_csv("dataset/products.csv")
orders = pd.read_csv("dataset/orders.csv")
order_items = pd.read_csv("dataset/order_items.csv")

print("=" * 60)
print("DATASETS LOADED SUCCESSFULLY")
print("=" * 60)

print(f"Customers:   {customers.shape[0]:,} rows")
print(f"Products:    {products.shape[0]:,} rows")
print(f"Orders:      {orders.shape[0]:,} rows")
print(f"Order Items: {order_items.shape[0]:,} rows")


# ============================================================
# 2. DISPLAY FIRST FEW ROWS
# ============================================================

print("\n" + "=" * 60)
print("CUSTOMERS - FIRST 5 ROWS")
print("=" * 60)
print(customers.head())

print("\n" + "=" * 60)
print("PRODUCTS - FIRST 5 ROWS")
print("=" * 60)
print(products.head())

print("\n" + "=" * 60)
print("ORDERS - FIRST 5 ROWS")
print("=" * 60)
print(orders.head())

print("\n" + "=" * 60)
print("ORDER ITEMS - FIRST 5 ROWS")
print("=" * 60)
print(order_items.head())


# ============================================================
# 3. DATA INFORMATION
# ============================================================

print("\n" + "=" * 60)
print("CUSTOMERS INFORMATION")
print("=" * 60)
customers.info()

print("\n" + "=" * 60)
print("PRODUCTS INFORMATION")
print("=" * 60)
products.info()

print("\n" + "=" * 60)
print("ORDERS INFORMATION")
print("=" * 60)
orders.info()

print("\n" + "=" * 60)
print("ORDER ITEMS INFORMATION")
print("=" * 60)
order_items.info()


# ============================================================
# 4. CHECK MISSING VALUES
# ============================================================

print("\n" + "=" * 60)
print("MISSING VALUES")
print("=" * 60)

print("\nCustomers:")
print(customers.isnull().sum())

print("\nProducts:")
print(products.isnull().sum())

print("\nOrders:")
print(orders.isnull().sum())

print("\nOrder Items:")
print(order_items.isnull().sum())


# ============================================================
# 5. CHECK DUPLICATES
# ============================================================

print("\n" + "=" * 60)
print("DUPLICATE RECORDS")
print("=" * 60)

print(f"Customers duplicates:   {customers.duplicated().sum():,}")
print(f"Products duplicates:    {products.duplicated().sum():,}")
print(f"Orders duplicates:      {orders.duplicated().sum():,}")
print(f"Order Items duplicates: {order_items.duplicated().sum():,}")


# ============================================================
# 6. CLEAN ORDERS DATA
# ============================================================

orders["order_date"] = pd.to_datetime(
    orders["order_date"],
    errors="coerce"
)

orders = orders.drop_duplicates()


# ============================================================
# 7. CLEAN ORDER ITEMS
# ============================================================

order_items = order_items.drop_duplicates()

order_items["quantity"] = pd.to_numeric(
    order_items["quantity"],
    errors="coerce"
)

order_items["unit_price"] = pd.to_numeric(
    order_items["unit_price"],
    errors="coerce"
)

order_items = order_items.dropna(
    subset=["quantity", "unit_price"]
)


# ============================================================
# 8. CLEAN PRODUCTS
# ============================================================

products["cost"] = pd.to_numeric(
    products["cost"],
    errors="coerce"
)

products["selling_price"] = pd.to_numeric(
    products["selling_price"],
    errors="coerce"
)


# ============================================================
# 9. CALCULATE REVENUE
# ============================================================

order_items["revenue"] = (
    order_items["quantity"] *
    order_items["unit_price"]
)


# ============================================================
# 10. MERGE ORDER ITEMS WITH PRODUCTS
# ============================================================

sales = order_items.merge(
    products,
    on="product_id",
    how="left"
)


# ============================================================
# 11. CALCULATE COST
# ============================================================

sales["total_cost"] = (
    sales["quantity"] *
    sales["cost"]
)


# ============================================================
# 12. CALCULATE PROFIT
# ============================================================

sales["profit"] = (
    sales["revenue"] -
    sales["total_cost"]
)


# ============================================================
# 13. CALCULATE PROFIT MARGIN
# ============================================================

sales["profit_margin"] = (
    sales["profit"] /
    sales["revenue"]
) * 100


# ============================================================
# 14. MERGE ORDERS
# ============================================================

sales = sales.merge(
    orders[
        [
            "order_id",
            "customer_id",
            "order_date",
            "status"
        ]
    ],
    on="order_id",
    how="left"
)


# ============================================================
# 15. MERGE CUSTOMERS
# ============================================================

sales = sales.merge(
    customers[
        [
            "customer_id",
            "customer_name",
            "city",
            "country"
        ]
    ],
    on="customer_id",
    how="left"
)


# ============================================================
# 16. DISPLAY CLEAN SALES DATA
# ============================================================

print("\n" + "=" * 60)
print("FINAL SALES DATA")
print("=" * 60)

print(
    sales[
        [
            "order_id",
            "customer_id",
            "customer_name",
            "product_id",
            "quantity",
            "unit_price",
            "revenue",
            "total_cost",
            "profit",
            "profit_margin",
            "order_date",
            "status"
        ]
    ].head(20)
)


# ============================================================
# 17. BUSINESS SUMMARY
# ============================================================

total_revenue = sales["revenue"].sum()
total_cost = sales["total_cost"].sum()
total_profit = sales["profit"].sum()
total_quantity = sales["quantity"].sum()
total_orders = sales["order_id"].nunique()
total_customers = sales["customer_id"].nunique()


print("\n" + "=" * 60)
print("BUSINESS SUMMARY")
print("=" * 60)

print(f"Total Revenue:       ${total_revenue:,.2f}")
print(f"Total Cost:          ${total_cost:,.2f}")
print(f"Total Profit:        ${total_profit:,.2f}")
print(f"Total Items Sold:    {total_quantity:,.0f}")
print(f"Total Orders:        {total_orders:,}")
print(f"Total Customers:     {total_customers:,}")


# ============================================================
# 18. OVERALL PROFIT MARGIN
# ============================================================

if total_revenue != 0:
    overall_margin = (
        total_profit / total_revenue
    ) * 100
else:
    overall_margin = 0

print(f"Overall Profit Margin: {overall_margin:.2f}%")


# ============================================================
# 19. TOP 10 PRODUCTS BY REVENUE
# ============================================================

top_products_revenue = (
    sales.groupby(
        ["product_id", "product_name"],
        as_index=False
    )
    .agg(
        total_revenue=("revenue", "sum"),
        total_quantity=("quantity", "sum"),
        total_profit=("profit", "sum")
    )
    .sort_values(
        "total_revenue",
        ascending=False
    )
    .head(10)
)


print("\n" + "=" * 60)
print("TOP 10 PRODUCTS BY REVENUE")
print("=" * 60)

print(top_products_revenue)


# ============================================================
# 20. TOP 10 PRODUCTS BY PROFIT
# ============================================================

top_products_profit = (
    sales.groupby(
        ["product_id", "product_name"],
        as_index=False
    )
    .agg(
        total_revenue=("revenue", "sum"),
        total_profit=("profit", "sum"),
        total_quantity=("quantity", "sum")
    )
    .sort_values(
        "total_profit",
        ascending=False
    )
    .head(10)
)


print("\n" + "=" * 60)
print("TOP 10 PRODUCTS BY PROFIT")
print("=" * 60)

print(top_products_profit)


# ============================================================
# 21. SALES BY CATEGORY
# ============================================================

category_sales = (
    sales.groupby(
        "category",
        as_index=False
    )
    .agg(
        revenue=("revenue", "sum"),
        cost=("total_cost", "sum"),
        profit=("profit", "sum"),
        quantity=("quantity", "sum")
    )
    .sort_values(
        "revenue",
        ascending=False
    )
)


print("\n" + "=" * 60)
print("SALES BY CATEGORY")
print("=" * 60)

print(category_sales)


# ============================================================
# 22. SALES BY CUSTOMER
# ============================================================

customer_sales = (
    sales.groupby(
        ["customer_id", "customer_name"],
        as_index=False
    )
    .agg(
        total_revenue=("revenue", "sum"),
        total_profit=("profit", "sum"),
        total_orders=("order_id", "nunique"),
        total_quantity=("quantity", "sum")
    )
    .sort_values(
        "total_revenue",
        ascending=False
    )
)


print("\n" + "=" * 60)
print("TOP 10 CUSTOMERS BY REVENUE")
print("=" * 60)

print(customer_sales.head(10))


# ============================================================
# 23. MONTHLY SALES
# ============================================================

sales["month"] = sales["order_date"].dt.to_period("M")

monthly_sales = (
    sales.groupby(
        "month",
        as_index=False
    )
    .agg(
        revenue=("revenue", "sum"),
        cost=("total_cost", "sum"),
        profit=("profit", "sum"),
        orders=("order_id", "nunique")
    )
)


print("\n" + "=" * 60)
print("MONTHLY SALES")
print("=" * 60)

print(monthly_sales)


# ============================================================
# 24. ORDER STATUS ANALYSIS
# ============================================================

status_analysis = (
    sales.groupby(
        "status",
        as_index=False
    )
    .agg(
        orders=("order_id", "nunique"),
        revenue=("revenue", "sum"),
        profit=("profit", "sum")
    )
    .sort_values(
        "revenue",
        ascending=False
    )
)


print("\n" + "=" * 60)
print("ORDER STATUS ANALYSIS")
print("=" * 60)

print(status_analysis)


# ============================================================
# 25. SAVE CLEAN SALES DATA
# ============================================================

sales.to_csv(
    "dataset/clean_sales.csv",
    index=False
)

print("\n" + "=" * 60)
print("CLEAN DATA SAVED")
print("=" * 60)

print("File: dataset/clean_sales.csv")


# ============================================================
# 26. SAVE ANALYSIS RESULTS
# ============================================================

top_products_revenue.to_csv(
    "dataset/top_products_revenue.csv",
    index=False
)

top_products_profit.to_csv(
    "dataset/top_products_profit.csv",
    index=False
)

category_sales.to_csv(
    "dataset/category_sales.csv",
    index=False
)

customer_sales.to_csv(
    "dataset/customer_sales.csv",
    index=False
)

monthly_sales.to_csv(
    "dataset/monthly_sales.csv",
    index=False
)

status_analysis.to_csv(
    "dataset/status_analysis.csv",
    index=False
)


# ============================================================
# 27. FINAL MESSAGE
# ============================================================

print("\n" + "=" * 60)
print("ANALYSIS COMPLETED SUCCESSFULLY!")
print("=" * 60)
# ============================================================
# 19. TOP 10 PRODUCTS BY REVENUE
# ============================================================

top_products_revenue = (
    sales.groupby(
        ["product_id", "product_name", "category"],
        as_index=False
    )
    .agg(
        units_sold=("quantity", "sum"),
        total_orders=("order_id", "nunique"),
        total_revenue=("revenue", "sum"),
        total_cost=("total_cost", "sum"),
        total_profit=("profit", "sum")
    )
)

# Calculate profit margin
top_products_revenue["profit_margin"] = (
    top_products_revenue["total_profit"] /
    top_products_revenue["total_revenue"]
) * 100

# Sort by revenue
top_products_revenue = (
    top_products_revenue
    .sort_values(
        "total_revenue",
        ascending=False
    )
    .head(10)
)

# Display results
print("\n" + "=" * 80)
print("TOP 10 PRODUCTS BY REVENUE")
print("=" * 80)

print(
    top_products_revenue.to_string(index=False)
)


# ============================================================
# 20. TOP 10 PRODUCTS BY PROFIT
# ============================================================

top_products_profit = (
    sales.groupby(
        ["product_id", "product_name", "category"],
        as_index=False
    )
    .agg(
        units_sold=("quantity", "sum"),
        total_orders=("order_id", "nunique"),
        total_revenue=("revenue", "sum"),
        total_cost=("total_cost", "sum"),
        total_profit=("profit", "sum")
    )
)

# Calculate profit margin
top_products_profit["profit_margin"] = (
    top_products_profit["total_profit"] /
    top_products_profit["total_revenue"]
) * 100

# Sort by profit
top_products_profit = (
    top_products_profit
    .sort_values(
        "total_profit",
        ascending=False
    )
    .head(10)
)

# Display results
print("\n" + "=" * 80)
print("TOP 10 PRODUCTS BY PROFIT")
print("=" * 80)

print(
    top_products_profit.to_string(index=False)
)


# ============================================================
# 21. TOP 10 PRODUCTS BY UNITS SOLD
# ============================================================

top_products_quantity = (
    sales.groupby(
        ["product_id", "product_name", "category"],
        as_index=False
    )
    .agg(
        units_sold=("quantity", "sum"),
        total_revenue=("revenue", "sum"),
        total_profit=("profit", "sum")
    )
    .sort_values(
        "units_sold",
        ascending=False
    )
    .head(10)
)

print("\n" + "=" * 80)
print("TOP 10 PRODUCTS BY UNITS SOLD")
print("=" * 80)

print(
    top_products_quantity.to_string(index=False)
)
# ============================================================
# 22. CUSTOMER LIFETIME VALUE (CLV)
# ============================================================

# Calculate customer-level metrics
customer_ltv = (
    sales.groupby(
        ["customer_id", "customer_name"],
        as_index=False
    )
    .agg(
        total_orders=("order_id", "nunique"),
        total_quantity=("quantity", "sum"),
        total_revenue=("revenue", "sum"),
        total_cost=("total_cost", "sum"),
        total_profit=("profit", "sum"),
        first_purchase=("order_date", "min"),
        last_purchase=("order_date", "max")
    )
)


# ============================================================
# 23. CALCULATE AVERAGE ORDER VALUE
# ============================================================

customer_ltv["average_order_value"] = (
    customer_ltv["total_revenue"] /
    customer_ltv["total_orders"]
)


# ============================================================
# 24. CALCULATE CUSTOMER LIFESPAN
# ============================================================

customer_ltv["customer_lifespan_days"] = (
    customer_ltv["last_purchase"] -
    customer_ltv["first_purchase"]
).dt.days


# ============================================================
# 25. CALCULATE PROFIT MARGIN
# ============================================================

customer_ltv["profit_margin"] = (
    customer_ltv["total_profit"] /
    customer_ltv["total_revenue"]
) * 100


# ============================================================
# 26. HISTORICAL CUSTOMER LIFETIME VALUE
# ============================================================

customer_ltv["customer_lifetime_value"] = (
    customer_ltv["total_revenue"]
)


# ============================================================
# 27. SORT CUSTOMERS BY CLV
# ============================================================

customer_ltv = (
    customer_ltv
    .sort_values(
        "customer_lifetime_value",
        ascending=False
    )
)


# ============================================================
# 28. DISPLAY TOP 10 CUSTOMERS BY CLV
# ============================================================

print("\n" + "=" * 80)
print("TOP 10 CUSTOMERS BY CUSTOMER LIFETIME VALUE")
print("=" * 80)

print(
    customer_ltv[
        [
            "customer_id",
            "customer_name",
            "total_orders",
            "total_quantity",
            "total_revenue",
            "total_profit",
            "average_order_value",
            "customer_lifespan_days",
            "profit_margin",
            "customer_lifetime_value"
        ]
    ]
    .head(10)
    .to_string(index=False)
)


# ============================================================
# 29. ROUND FINANCIAL VALUES
# ============================================================

customer_ltv[
    [
        "total_revenue",
        "total_cost",
        "total_profit",
        "average_order_value",
        "profit_margin",
        "customer_lifetime_value"
    ]
] = customer_ltv[
    [
        "total_revenue",
        "total_cost",
        "total_profit",
        "average_order_value",
        "profit_margin",
        "customer_lifetime_value"
    ]
].round(2)


# ============================================================
# 30. CUSTOMER VALUE SEGMENTATION
# ============================================================

customer_ltv["customer_segment"] = pd.cut(
    customer_ltv["customer_lifetime_value"],
    bins=[
        -float("inf"),
        1000,
        5000,
        10000,
        float("inf")
    ],
    labels=[
        "Low Value",
        "Medium Value",
        "High Value",
        "VIP"
    ]
)


# ============================================================
# 31. CUSTOMER SEGMENT SUMMARY
# ============================================================

customer_segments = (
    customer_ltv
    .groupby(
        "customer_segment",
        observed=False
    )
    .agg(
        customers=("customer_id", "count"),
        revenue=("total_revenue", "sum"),
        profit=("total_profit", "sum"),
        average_clv=("customer_lifetime_value", "mean")
    )
    .reset_index()
)


print("\n" + "=" * 80)
print("CUSTOMER VALUE SEGMENTS")
print("=" * 80)

print(
    customer_segments.to_string(index=False)
)


# ============================================================
# 32. SAVE CUSTOMER LTV ANALYSIS
# ============================================================

customer_ltv.to_csv(
    "dataset/customer_lifetime_value.csv",
    index=False
)

customer_segments.to_csv(
    "dataset/customer_segments.csv",
    index=False
)


print("\n" + "=" * 80)
print("CUSTOMER LIFETIME VALUE ANALYSIS COMPLETED")
print("=" * 80)

print("Saved:")
print("dataset/customer_lifetime_value.csv")
print("dataset/customer_segments.csv")
