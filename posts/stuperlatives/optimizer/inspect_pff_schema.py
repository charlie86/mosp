
from google.cloud import bigquery
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')

client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)
dataset_id = 'pff_analysis'

# List tables to see years
tables = client.list_tables(dataset_id)
table_names = [t.table_id for t in tables if 'rushing_summary' in t.table_id]
print("Found Rushing Summary Tables:", table_names)

if table_names:
    # Pick the latest one
    table_id = f"{client.project}.{dataset_id}.{table_names[-1]}"
    print(f"\nInspecting {table_id} schema:")
    table = client.get_table(table_id)
    for schema in table.schema:
        print(f"- {schema.name} ({schema.field_type})")
        
    # Get a sample row to see data granularity (Game level or Season level?)
    print(f"\nSample Data from {table_id}:")
    rows = client.query(f"SELECT * FROM `{table_id}` LIMIT 1").to_dataframe()
    print(rows.T)
