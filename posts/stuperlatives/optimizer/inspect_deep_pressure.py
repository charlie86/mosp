
from google.cloud import bigquery
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')

client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)
dataset_id = 'pff_analysis'

tables_to_inspect = [
    'pff_passing_depth_deep_2025',
    'pff_passing_pressure_general_2025',
    'pff_defense_coverage_2025',
    'pff_defense_pass_rush_2025'
]

for table_name in tables_to_inspect:
    table_id = f"{client.project}.{dataset_id}.{table_name}"
    print(f"\nInspecting {table_id} schema:")
    try:
        table = client.get_table(table_id)
        cols = [f"{s.name}" for s in table.schema]
        print(", ".join(cols))
    except Exception as e:
        print(f"Error inspecting {table_name}: {e}")
