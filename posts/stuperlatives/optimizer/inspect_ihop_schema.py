
from google.cloud import bigquery
import os

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')

client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)

print("Schema for stuperlatives.ihop_data:")
try:
    t = client.get_table('stuperlatives.ihop_data')
    cols = [s.name for s in t.schema]
    print(", ".join(cols))
except Exception as e:
    print(f"Error: {e}")
