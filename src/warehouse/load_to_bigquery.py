from google.cloud import bigquery
from dotenv import load_dotenv
import os

load_dotenv()

PROJECT_ID = os.getenv("GCP_PROJECT_ID")
DATASET_ID = os.getenv("BQ_DATASET")

client = bigquery.Client(project=PROJECT_ID)

print("PROJECT_ID:", PROJECT_ID)
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

    schema = [
        bigquery.SchemaField("order_key", "INT64"),
        bigquery.SchemaField("order_id", "STRING"),
        bigquery.SchemaField("order_date", "DATE"),
        bigquery.SchemaField("date_key", "INT64"),
        bigquery.SchemaField("customer_key", "INT64"),
        bigquery.SchemaField("location_key", "INT64"),
        bigquery.SchemaField("product_key", "INT64"),
        bigquery.SchemaField("sales", "FLOAT64"),
        bigquery.SchemaField("quantity", "INT64"),
        bigquery.SchemaField("discount", "FLOAT64"),
        bigquery.SchemaField("profit", "FLOAT64"),
        bigquery.SchemaField("lead_time_days", "INT64"),
    ]

    job_config = bigquery.LoadJobConfig(
    schema=schema,
    source_format=bigquery.SourceFormat.CSV,
    skip_leading_rows=1,
    write_disposition=bigquery.WriteDisposition.WRITE_TRUNCATE,
    create_disposition=bigquery.CreateDisposition.CREATE_IF_NEEDED,
    # time_partitioning=bigquery.TimePartitioning(
    #     type_=bigquery.TimePartitioningType.DAY,
    #     field="order_date"
    # ),
    clustering_fields=["product_key", "customer_key"],
)

    with open(csv_path, "rb") as f:
        job = client.load_table_from_file(f, table_id, job_config=job_config)

    job.result()

    print("Job State:", job.state)
    print("Rows Loaded:", job.output_rows)
    print("Errors:", job.errors)

    # print("Rows loaded:", job.output_rows)
    print("fact_orders loaded successfully.")


def load_generic(csv_path, table_name):
    """
    Generic loader for non-partitioned tables.
    Used for inventory and vendor marts.
    """
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


if __name__ == "__main__":

    base_path = "D:/REVATURE/Project-1_SCIS/data/processed/"

    # Dimensions
    load_dimension(base_path + "date_dim.csv", "dim_date")
    load_dimension(base_path + "customer_dim.csv", "dim_customer")
    load_dimension(base_path + "location_dim.csv", "dim_location")
    load_dimension(base_path + "product_dim.csv", "dim_product")
    
    # Inventory and Vendor
    load_generic(base_path + "fact_inventory.csv", "fact_inventory")
    load_generic(base_path + "dim_vendor.csv", "dim_vendor")
    load_generic(base_path + "fact_vendor_performance.csv", "fact_vendor_performance")

    # Main Fact
    load_fact(base_path + "fact_orders.csv")

    print("All tables loaded successfully.")