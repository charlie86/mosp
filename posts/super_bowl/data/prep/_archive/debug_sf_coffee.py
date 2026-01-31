
import os
import pandas as pd
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
        return bigquery.Client()
    except: return None

client = get_bq_client()
if client:
    q = "SELECT team_name, stadium_name, dunkin, starbucks FROM `stuperlatives.coffee_wars` WHERE team_name = 'San Francisco 49ers'"
    df = client.query(q).to_dataframe()
    print(df)
    
    for idx, row in df.iterrows():
        print(f"\nRow {idx} Stadium: '{row['stadium_name']}'")
        d_locs = row['dunkin']['locations'] if row['dunkin'] and 'locations' in row['dunkin'] else []
        s_locs = row['starbucks']['locations'] if row['starbucks'] and 'locations' in row['starbucks'] else []
        print(f"Dunkin Locations: {len(d_locs)}")
        print(f"Starbucks Locations: {len(s_locs)}")
