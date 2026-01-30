
import os
from google.cloud import bigquery
from google.oauth2 import service_account

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))

def get_bq_client():
    try:
        possible_keys = [
            'shhhh/service_account.json',
            '../../../shhhh/service_account.json',
            os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')
        ]
        key_path = next((p for p in possible_keys if os.path.exists(p)), None)
        
        if key_path:
            credentials = service_account.Credentials.from_service_account_file(key_path)
            return bigquery.Client(credentials=credentials, project=credentials.project_id)
        else:
            return bigquery.Client()
    except Exception as e:
        print(f"Error creating BQ client: {e}")
        return None

client = get_bq_client()
if client:
    # Check if stadium is in PBP
    try:
        query = "SELECT * FROM `stuperlatives.pbp_data` LIMIT 1"
        df = client.query(query).to_dataframe()
        print("PBP Columns:", df.columns.tolist())
    except Exception as e:
        print(e)
