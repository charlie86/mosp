
from google.cloud import bigquery
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')

client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)
dataset_id = 'pff_analysis'

# List tables to find blocking
tables = client.list_tables(dataset_id)
blocking_tables = [t.table_id for t in tables if ('blocking' in t.table_id or 'offense' in t.table_id) and '2025' in t.table_id]
print("Found Blocking/Offense Tables (2025):")
for t in blocking_tables:
    print(f"- {t}")

# Inspect IHOP table
ihop_table_id = f"{client.project}.stuperlatives.stadium_gravitational_pull"
try:
    t = client.get_table(ihop_table_id)
    cols = [s.name for s in t.schema]
    print(f"\nSchema for {ihop_table_id}:")
    print(", ".join(cols))
except Exception as e:
    print(f"Error reading IHOP table: {e}")
