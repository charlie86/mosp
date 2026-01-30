
from google.cloud import bigquery
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')

client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)
dataset_id = 'pff_analysis'

tables = client.list_tables(dataset_id)
# Filter for passing tables in 2025
pass_tables = [t.table_id for t in tables if 'passing' in t.table_id and '2025' in t.table_id]
print("Found Passing Tables (2025):")
for t in pass_tables:
    print(f"- {t}")
