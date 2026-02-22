from google.cloud import bigquery
from dotenv import load_dotenv
import os

load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_ID = os.getenv("BQ_DATASET")

client = bigquery.Client(project=PROJECT_ID)

print("Dataset used:", DATASET_ID)

def load_dimension(csv_path, table_name):
    table_id = f"{PROJECT_ID}.{DATASET_ID}.{table_name}"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    )

    with open(csv_path, "rb") as f:
        job = client.load_table_from_file(f, table_id, job_config=job_config)

    job.result()
    print(f"{table_name} loaded successfully.")


def load_fact(csv_path):
    table_id = f"{PROJECT_ID}.{DATASET_ID}.fact_orders"

    job_config = bigquery.LoadJobConfig(
        source_format=bigquery.SourceFormat.CSV,
        skip_leading_rows=1,
        autodetect=True,
        write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
        time_partitioning=bigquery.TimePartitioning(
            type_=bigquery.TimePartitioningType.DAY,
            field="order_date",
        ),
        clustering_fields=["product_key", "customer_key"],
    )

    with open(csv_path, "rb") as f:
        job = client.load_table_from_file(f, table_id, job_config=job_config)

    job.result()
    print("fact_orders loaded successfully.")


if __name__ == "__main__":

    base_path = "D:/REVATURE/Project-1_SCIS/data/processed/"

    load_dimension(base_path + "date_dim.csv", "dim_date")
    load_dimension(base_path + "customer_dim.csv", "dim_customer")
    load_dimension(base_path + "location_dim.csv", "dim_location")
    load_dimension(base_path + "product_dim.csv", "dim_product")

    load_fact(base_path + "fact_orders.csv")

    print("All tables loaded successfully.")