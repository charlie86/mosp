
from google.cloud import bigquery
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')

client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)

# List stuperlatives tables
print("Tables in 'stuperlatives':")
try:
    tables = client.list_tables(f"{client.project}.stuperlatives")
    for t in tables:
        print(f"- {t.table_id}")
except Exception as e:
    print(f"Error listing stuperlatives: {e}")

# Inspect Blocking Summary
print("\nSchema for pff_blocking_summary_2025:")
try:
    t = client.get_table('pff_analysis.pff_blocking_summary_2025')
    cols = [s.name for s in t.schema]
    print(", ".join(cols))
except Exception as e:
    print(f"Error: {e}")
