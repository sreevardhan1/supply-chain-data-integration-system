import requests
import pandas as pd
import os

API_URL = "https://fakestoreapi.com/products"

RAW_SAVE_PATH = "data/raw/fakestore_products_raw.csv"

def fetch_products():
    response = requests.get(API_URL)

    if response.status_code != 200:
        raise Exception(f"API failed with status {response.status_code}")

    data = response.json()
    df = pd.DataFrame(data)

    return df


def save_raw_data(df):
    os.makedirs("data/raw", exist_ok=True)
    df.to_csv(RAW_SAVE_PATH, index=False)
    print(f"Raw API data saved to {RAW_SAVE_PATH}")


if __name__ == "__main__":
    df_products = fetch_products()
    save_raw_data(df_products)
    print(df_products.head())