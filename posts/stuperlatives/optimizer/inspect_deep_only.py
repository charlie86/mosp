
from google.cloud import bigquery
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')

client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)
dataset_id = 'pff_analysis'
table = 'pff_passing_depth_deep_2025'
table_id = f"{client.project}.{dataset_id}.{table}"

try:
    t = client.get_table(table_id)
    cols = [s.name for s in t.schema]
    print(f"Schema for {table}:")
    print(", ".join(cols))
except Exception as e:
    print(f"Error: {e}")
