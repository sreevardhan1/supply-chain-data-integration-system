import pandas as pd
import os

RAW_PATH = "data/raw/fakestore_products_raw.csv"
PROCESSED_PATH = "data/processed/fakestore_products_cleaned.csv"


def transform_products():
    # Flattening of JSON string to python dictionary
    df = pd.read_csv(RAW_PATH)

    # Convert rating string to dictionary
    df['rating'] = df['rating'].apply(eval)

    # Extract nested values
    df['rating_rate'] = df['rating'].apply(lambda x: x.get('rate'))
    df['rating_count'] = df['rating'].apply(lambda x: x.get('count'))

    # Drop original nested column
    df.drop(columns=['rating'], inplace=True)

    # Rename columns to warehouse-friendly naming
    df.rename(columns={
        'id': 'api_product_id',
        'title': 'product_title',
        'price': 'product_price'
    }, inplace=True)

    return df


def save_cleaned_data(df):
    os.makedirs("data/processed", exist_ok=True)
    df.to_csv(PROCESSED_PATH, index=False)
    print(f"Processed API data saved to {PROCESSED_PATH}")


if __name__ == "__main__":
    df_clean = transform_products()
    save_cleaned_data(df_clean)
    print(df_clean.head())
    