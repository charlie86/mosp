
import os
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
BQ_COFFEE_TABLE = "stuperlatives.coffee_wars"

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
        return bigquery.Client()
    except: return None

client = get_bq_client()
if client:
    q = f"SELECT team_name, stadium_name FROM `{BQ_COFFEE_TABLE}` ORDER BY team_name"
    df = client.query(q).to_dataframe()
    # Print groupings
    for team, group in df.groupby('team_name'):
        print(f"{team}: {group['stadium_name'].tolist()}")
