import pandas as pd
import os

FACT_PATH = "data/processed/fact_orders.csv"
VENDOR_PATH = "data/processed/dim_vendor.csv"
OUTPUT_PATH = "data/processed/fact_vendor_performance.csv"

def create_vendor_performance():

    df_fact = pd.read_csv(FACT_PATH)
    df_vendor = pd.read_csv(VENDOR_PATH)

    df = df_fact.merge(df_vendor, on="product_key", how="left")

    vendor_perf = df.groupby(["vendor_key", "vendor_name"]).agg(
        total_orders=("order_id", "count"),
        avg_lead_time=("lead_time_days", "mean"),
        total_sales=("sales", "sum")
    ).reset_index()

    return vendor_perf


if __name__ == "__main__":
    os.makedirs("data/processed", exist_ok=True)
    df_vendor_perf = create_vendor_performance()
    df_vendor_perf.to_csv(OUTPUT_PATH, index=False)
    print("Vendor performance fact created successfully.")