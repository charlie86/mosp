
import os
from google.cloud import bigquery
from google.oauth2 import service_account

# --- Configuration ---
BQ_PBP_TABLE = "stuperlatives.pbp_data"
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

def calculate_league_averages(client):
    query = f"""
    SELECT
        AVG(epa) as avg_epa,
        AVG(success) as avg_success
    FROM `{BQ_PBP_TABLE}`
    WHERE season >= 2015
      AND play_type = 'run'
    """
    row = client.query(query).to_dataframe().iloc[0]
    print(f"League Average Rushing EPA: {row['avg_epa']:.3f}")
    print(f"League Average Rushing Success Rate: {row['avg_success']*100:.1f}%")

if __name__ == "__main__":
    client = get_bq_client()
    if client:
        calculate_league_averages(client)
