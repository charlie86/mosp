
from google.cloud import bigquery
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')

client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)
dataset_id = 'pff_analysis'

# List tables to see years
tables = client.list_tables(dataset_id)
# Filter for defense tables in 2025
def_tables = [t.table_id for t in tables if 'defense' in t.table_id and '2025' in t.table_id]
print("Found Defense Tables (2025):", def_tables)

for table_name in def_tables:
    table_id = f"{client.project}.{dataset_id}.{table_name}"
    print(f"\nInspecting {table_id} schema:")
    try:
        table = client.get_table(table_id)
        cols = [f"{s.name} ({s.field_type})" for s in table.schema]
        print(", ".join(cols))
    except Exception as e:
        print(f"Error inspecting {table_name}: {e}")
