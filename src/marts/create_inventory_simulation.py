"""
Inventory Simulation Module
---------------------------
Simulates inventory levels and calculates turnover metrics.
"""

import pandas as pd
import numpy as np
import os

FACT_PATH = "data/processed/fact_orders.csv"
PRODUCT_PATH = "data/processed/product_dim.csv"
OUTPUT_PATH = "data/processed/fact_inventory.csv"


def create_inventory_simulation():

    df_fact = pd.read_csv(FACT_PATH)
    df_product = pd.read_csv(PRODUCT_PATH)

    # Aggregate yearly sales per product
    product_sales = df_fact.groupby("product_key").agg(
        total_quantity=("quantity", "sum")
    ).reset_index()

    # Merge with product dimension
    df_inventory = df_product[["product_key", "product_name"]].merge(
        product_sales,
        on="product_key",
        how="left"
    )

    df_inventory["total_quantity"] = df_inventory["total_quantity"].fillna(0)

    # Simulate initial stock
    np.random.seed(42)
    df_inventory["initial_stock"] = np.random.randint(500, 2000, size=len(df_inventory))

    # Simulate reorder point
    df_inventory["reorder_point"] = df_inventory["initial_stock"] * 0.25

    # Current stock
    df_inventory["current_stock"] = (
        df_inventory["initial_stock"] - df_inventory["total_quantity"]
    ).clip(lower=0)

    # Inventory turnover ratio
    df_inventory["inventory_turnover"] = (
        df_inventory["total_quantity"] / df_inventory["initial_stock"]
    )

    # Days Inventory Outstanding (DIO)
    df_inventory["days_inventory_outstanding"] = (
        365 / df_inventory["inventory_turnover"].replace(0, np.nan)
    )

    return df_inventory


if __name__ == "__main__":
    os.makedirs("data/processed", exist_ok=True)
    df_inventory = create_inventory_simulation()
    df_inventory.to_csv(OUTPUT_PATH, index=False)
    print("Inventory simulation created successfully.")