import os
from google.cloud import bigquery
from google.oauth2 import service_account

# --- Configuration ---
BQ_PROJECT = "mosp-449117"
BQ_COFFEE_TABLE = "stuperlatives.coffee_wars"
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

def list_dunkin_stadiums(client):
    query = f"""
    SELECT 
        team_name,
        stadium_name,
        count_10mi as dunkin_count
    FROM `{BQ_COFFEE_TABLE}`
    WHERE chain = 'Dunkin\\'' 
      AND count_10mi >= 15
    ORDER BY count_10mi DESC
    """
    results = client.query(query).to_dataframe()
    
    print("\n### The Dunkin' Belt (Stadiums with >= 15 Locations)")
    print("| Rank | Team | Stadium | Dunkin Count |")
    print("| :--- | :--- | :--- | :--- |")
    
    for idx, row in results.iterrows():
        print(f"| {idx+1} | {row['team_name']} | {row['stadium_name']} | {int(row['dunkin_count'])} |")

if __name__ == "__main__":
    client = get_bq_client()
    if client:
        list_dunkin_stadiums(client)
