
from google.cloud import bigquery
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')

client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)
dataset_id = 'pff_analysis'
tables_to_inspect = [
    'pff_passing_concept_screen_2025',
    'pff_passing_depth_short_2025',
    'pff_passing_depth_intermediate_2025',
    'pff_passing_depth_behind_los_2025',
    'pff_passing_pressure_blitz_2025',
    'pff_passing_time_pocket_pa_2025'
]

for t_name in tables_to_inspect:
    try:
        table_id = f"{client.project}.{dataset_id}.{t_name}"
        t = client.get_table(table_id)
        cols = [s.name for s in t.schema]
        print(f"\nSchema for {t_name}:")
        print(", ".join(cols))
    except Exception as e:
        print(f"Error reading {t_name}: {e}")
