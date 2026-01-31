
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
    # Query to get the most recent stadium for each home team in the 2024 (or 2025) season
    # Using pbp_data
    q = """
    SELECT home_team, stadium, MAX(game_date) as last_game
    FROM `stuperlatives.pbp_data`
    WHERE season >= 2024
    GROUP BY home_team, stadium
    ORDER BY home_team, last_game DESC
    """
    df = client.query(q).to_dataframe()
    
    # Get the top 1 for each team
    current_stadiums = df.sort_values('last_game', ascending=False).groupby('home_team').head(1)
    
    # Print as a nice dictionary for me to copy
    print("CURRENT_2024_STADIUMS = {")
    for _, row in current_stadiums.iterrows():
        print(f"    '{row['home_team']}': '{row['stadium']}',")
    print("}")
