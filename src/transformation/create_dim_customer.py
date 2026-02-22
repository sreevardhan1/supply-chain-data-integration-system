# Preparing Customer Dimension Table

import pandas as pd
import os

INPUT_PATH = "data/processed/superstore_cleaned.csv"
OUTPUT_PATH = "data/processed/customer_dim.csv"

def create_dim_customer():
    df = pd.read_csv(INPUT_PATH)

    customer_dim = df[['Customer ID', 'Customer Name', 'Segment']].drop_duplicates()

    customer_dim = customer_dim.sort_values('Customer ID').reset_index(drop=True)

    # Creating Surrogate keys
    customer_dim.insert(0,'customer_key',range(1,len(customer_dim)+1))

    customer_dim.rename(columns={
        'Customer ID': 'customer_id',
        'Customer Name': 'customer_name',
        'Segment': 'segment'
    }, inplace= True)

    return customer_dim


if __name__ == "__main__":
    os.makedirs("data/processed",exist_ok=True)
    customer_dim = create_dim_customer()
    customer_dim.to_csv(OUTPUT_PATH,index=False)
    print("customer_dim created successfully")
    print(customer_dim.head())