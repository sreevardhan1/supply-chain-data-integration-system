# Preparing Date Dimension Table

import pandas as pd
import os

INPUT_PATH = "data/processed/superstore_cleaned.csv"
OUTPUT_PATH = "data/processed/date_dim.csv"

def create_dim_date():
    df = pd.read_csv(INPUT_PATH)

    df['Order Date'] = pd.to_datetime(df['Order Date'])

    # Get unique dates
    date_dim = df[['Order Date']].drop_duplicates().copy()

    # Adding attributes
    date_dim['year'] = date_dim['Order Date'].dt.year       # 'The .dt accessor is used when the column contains datetime values. It allows you to extract specific components (like year, month, day, weekday, etc.) from each timestamp.'
    date_dim['quarter'] = date_dim['Order Date'].dt.quarter
    date_dim['month'] = date_dim['Order Date'].dt.month
    date_dim['day'] = date_dim['Order Date'].dt.day

    # Creating Surrogate Keys
    date_dim = date_dim.sort_values('Order Date').reset_index(drop=True)
    date_dim.insert(0,'date_key',range(1,len(date_dim) + 1))

    date_dim.rename(columns={'Order Date': 'full_date'}, inplace=True)

    return date_dim


if __name__ == "__main__":
    os.makedirs("data/processed", exist_ok=True)
    date_dim = create_dim_date()
    date_dim.to_csv(OUTPUT_PATH,index=False)
    print('date_dim created successfully')
    print(date_dim.head())