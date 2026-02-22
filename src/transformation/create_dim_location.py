# Preparing Location Dimension Table

import pandas as pd
import os

INPUT_PATH = "data/processed/superstore_cleaned.csv"
OUTPUT_PATH = "data/processed/location_dim.csv"

def create_dim_location():
    df = pd.read_csv(INPUT_PATH)

    location_dim = df[['Country', 'State', 'City', 'Region']].drop_duplicates()

    location_dim = location_dim.sort_values(['Country', 'State', 'City']).reset_index(drop=True)

    location_dim.insert(0,'location_key',range(1,len(location_dim)+1))

    location_dim.rename(columns={
        'Country': 'country',
        'State':'state',
        'City' : 'city',
        'Region' : 'region'
    },inplace=True)

    return location_dim


if __name__ == "__main__":
    os.makedirs("data/processed",exist_ok=True)
    location_dim = create_dim_location()
    location_dim.to_csv(OUTPUT_PATH, index=False)
    print("location_dim created successfully")
    print(location_dim.head())
