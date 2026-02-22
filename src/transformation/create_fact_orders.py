# Preparing Fact Table: fact_orders

import pandas as pd
import os

# Input files
SUPERSTORE_PATH = "data/processed/superstore_cleaned.csv"
DIM_DATE_PATH = "data/processed/date_dim.csv"
DIM_CUSTOMER_PATH = "data/processed/customer_dim.csv"
DIM_LOCATION_PATH = "data/processed/location_dim.csv"
DIM_PRODUCT_PATH = "data/processed/product_dim.csv"

OUTPUT_PATH = "data/processed/fact_orders.csv"


def create_fact_orders():
    df = pd.read_csv(SUPERSTORE_PATH)
    print("Original Rows: ",len(df))

    dim_date = pd.read_csv(DIM_DATE_PATH)
    dim_customer = pd.read_csv(DIM_CUSTOMER_PATH)
    dim_location = pd.read_csv(DIM_LOCATION_PATH)
    dim_product = pd.read_csv(DIM_PRODUCT_PATH)

    # Convert dates
    df['Order Date'] = pd.to_datetime(df['Order Date'])
    dim_date['full_date'] = pd.to_datetime(dim_date['full_date'])

    # Merge date_key
    df = df.merge(dim_date[['date_key', 'full_date']],
                  left_on='Order Date',
                  right_on='full_date',
                  how='left')
    print("After date merge:", len(df))

    # Merge customer_key
    df = df.merge(dim_customer[['customer_key', 'customer_id']],
                  left_on='Customer ID',
                  right_on='customer_id',
                  how='left')
    print("After customer merge:", len(df))

    # Merge location_key
    df = df.merge(dim_location[['location_key', 'country', 'state', 'city', 'region']],
                  left_on=['Country', 'State', 'City', 'Region'],
                  right_on=['country', 'state', 'city', 'region'],
                  how='left')
    print("After customer merge:", len(df))

    # temp
    print("Before product merge:", len(df))
    print("dim_product rows:", len(dim_product))
    print("dim_product unique product_id:", dim_product['product_id'].nunique())


    df['Product ID'] = df['Product ID'].astype(str).str.strip()
    dim_product['product_id'] = dim_product['product_id'].astype(str).str.strip()
    # Merge product_key
    df = df.merge(dim_product[['product_key', 'product_id']],
                  left_on='Product ID',
                  right_on='product_id',
                  how='left')
    print("After product merge:", len(df))

    # Select fact columns
    fact_orders = df[[
        'Order ID',
        'Order Date',
        'date_key',
        'customer_key',
        'location_key',
        'product_key',
        'Sales',
        'Quantity',
        'Discount',
        'Profit',
        'Lead_Time'
    ]].copy()

    # Rename
    fact_orders.rename(columns={
        'Order ID': 'order_id',
        'Order Date': 'order_date',
        'Sales': 'sales',
        'Quantity': 'quantity',
        'Discount': 'discount',
        'Profit': 'profit',
        'Lead_Time' :'lead_time_days'
    }, inplace=True)

    # Create surrogate order_key
    fact_orders = fact_orders.reset_index(drop=True)
    fact_orders.insert(0, 'order_key', range(1, len(fact_orders) + 1))

    return fact_orders


if __name__ == "__main__":
    os.makedirs("data/processed", exist_ok=True)
    fact_orders = create_fact_orders()
    fact_orders.to_csv(OUTPUT_PATH, index=False)
    print("fact_orders created successfully")
    print(fact_orders.head())