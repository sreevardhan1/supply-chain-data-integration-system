# Connecting Python and Google BigQuery

from google.cloud import bigquery
from dotenv import load_dotenv
import os

# Load environment variables
load_dotenv()

# Optional: explicitly set credentials path
os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")

# Create BigQuery client
client = bigquery.Client(project=os.getenv("GCP_PROJECT_ID"))

print("✅ Connected to BigQuery")
print("Project:", client.project)

# Test: list datasets
datasets = list(client.list_datasets())
print("\nDatasets in project:")
for dataset in datasets:
    print("-", dataset.dataset_id)