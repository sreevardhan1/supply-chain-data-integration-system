import pandas as pd
import numpy as np
import os

PRODUCT_PATH = "data/processed/product_dim.csv"
OUTPUT_PATH = "data/processed/dim_vendor.csv"

def create_vendor_dimension():

    df_product = pd.read_csv(PRODUCT_PATH)

    np.random.seed(42)

    vendors = ["Vendor A", "Vendor B", "Vendor C", "Vendor D"]

    df_product["vendor_name"] = np.random.choice(vendors, len(df_product))

    vendor_dim = df_product[["product_key", "vendor_name"]].copy()

    vendor_dim["vendor_key"] = vendor_dim["vendor_name"].astype("category").cat.codes + 1

    return vendor_dim[["vendor_key", "vendor_name", "product_key"]]


if __name__ == "__main__":
    os.makedirs("data/processed", exist_ok=True)
    df_vendor = create_vendor_dimension()
    df_vendor.to_csv(OUTPUT_PATH, index=False)
    print("Vendor dimension created successfully.")