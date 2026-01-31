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
            # Suppress explicit project warning by explicitly passing project
            return bigquery.Client(credentials=credentials, project=credentials.project_id)
        else:
            print("Key file not found in common locations. Using default credentials.")
            return bigquery.Client()
    except Exception as e:
        print(f"Error creating BQ client: {e}")
        return None

if __name__ == "__main__":
    client = get_bq_client()
    table_id = "stuperlatives.coffee_wars"
    print(f"Deleting table {table_id}...")
    client.delete_table(table_id, not_found_ok=True)
    print("Done.")
