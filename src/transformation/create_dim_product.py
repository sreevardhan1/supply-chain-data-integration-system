# Preparing Product Dimension Table

import pandas as pd
import os

import pandas as pd
import os

SUPERSTORE_PATH = "data/processed/superstore_cleaned.csv"
API_PATH = "data/processed/fakestore_products_cleaned.csv"
OUTPUT_PATH = "data/processed/product_dim.csv"

def create_dim_product():
    df_super = pd.read_csv(SUPERSTORE_PATH)
    df_api = pd.read_csv(API_PATH)

    df_super['Product ID'] = df_super['Product ID'].astype(str).str.strip()

    # Step 1: Extract unique products from Superstore
    product_dim = df_super[['Product ID', 'Category', 'Sub-Category', 'Product Name']] \
    .copy()

    # Clean keys
    product_dim['Product ID'] = product_dim['Product ID'].str.strip()

    # Remove exact duplicates
    product_dim = product_dim.drop_duplicates()

    # Now ensure one row per Product ID
    product_dim = product_dim.groupby('Product ID').first().reset_index()
    
    # Validate uniqueness
    assert product_dim['Product ID'].is_unique, "Product ID still not unique!"

    # Rename Columns
    product_dim.rename(columns={
        'Product ID': 'product_id',
        'Category': 'category',
        'Sub-Category': 'sub_category',
        'Product Name': 'product_name'
    }, inplace=True)

    # Simple enrichment logic (random mapping)
    df_api_sample = df_api[['product_price','rating_rate','rating_count']]

    # Repeat API rows safely (without affecting product uniqueness)
    df_api_repeat = df_api_sample.sample(
        n=len(product_dim),
        replace=True,
        random_state=42
    ).reset_index(drop=True)

    product_dim = product_dim.reset_index(drop=True)

    # Concatenating Safely
    product_dim = pd.concat([product_dim, df_api_repeat], axis=1)

    # Adding Surrogate Key
    product_dim.insert(0, 'product_key', range(1, len(product_dim) + 1))

    return product_dim


if __name__ == "__main__":
    os.makedirs("data/processed", exist_ok=True)
    product_dim = create_dim_product()
    product_dim.to_csv(OUTPUT_PATH, index=False)
    print("product_dim created successfully")
    print(product_dim.head())