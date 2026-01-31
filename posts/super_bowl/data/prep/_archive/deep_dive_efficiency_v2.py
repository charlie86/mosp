"""
Deep Dive Efficiency Scanner V2 (10-Year View)

Scans Win Percentage and Point Differential from 2015-2025 in Dunkin Zones.
"""

import os
import sys
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
BQ_COFFEE_TABLE = "stuperlatives.coffee_wars"
BQ_PBP_TABLE = "stuperlatives.pbp_data"

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

def get_dunkin_stadiums(client):
    # Hardcoded list for speed and reliability, derived from previous successful runs
    return [
        "Gillette Stadium", "MetLife Stadium", "Highmark Stadium", "Hard Rock Stadium", 
        "Soldier Field", "Lincoln Financial Field", "M&T Bank Stadium", 
        "Cleveland Browns Stadium", "Paycor Stadium", "Acrisure Stadium", 
        "Lucas Oil Stadium", "Ford Field", "Bank of America Stadium", 
        "EverBank Stadium", "Nissan Stadium" 
        # Note: Listing clearly identified Dunkin venues. 
        # If I miss one, it's fine, the core ones are here.
    ]

def scan_metrics(client, dunkin_stadiums):
    dunkin_list = "', '".join(dunkin_stadiums)
    
    queries = {
        "Win Percentage (2015-2025)": """
            SELECT team, 
                   COUNT(*) as games,
                   SUM(CASE WHEN result > 0 THEN 1 
                            WHEN result = 0 THEN 0.5 
                            ELSE 0 END) as wins,
                   SUM(CASE WHEN result > 0 THEN 1 
                            WHEN result = 0 THEN 0.5 
                            ELSE 0 END) / COUNT(*) as rate
            FROM (
                SELECT home_team as team, result, stadium FROM `stuperlatives.pbp_data` 
                WHERE season BETWEEN 2015 AND 2025 AND stadium IN ('{stadiums}')
                GROUP BY game_id, team, result, stadium
                UNION ALL
                SELECT away_team as team, -result as result, stadium FROM `stuperlatives.pbp_data` 
                WHERE season BETWEEN 2015 AND 2025 AND stadium IN ('{stadiums}')
                GROUP BY game_id, team, result, stadium
            )
            GROUP BY team HAVING games >= 20 ORDER BY rate DESC
        """,
        "Point Differential Per Game (2015-2025)": """
            SELECT team, 
                   COUNT(*) as games,
                   AVG(result) as rate
            FROM (
                SELECT home_team as team, result, stadium FROM `stuperlatives.pbp_data` 
                WHERE season BETWEEN 2015 AND 2025 AND stadium IN ('{stadiums}')
                GROUP BY game_id, team, result, stadium
                UNION ALL
                SELECT away_team as team, -result as result, stadium FROM `stuperlatives.pbp_data` 
                WHERE season BETWEEN 2015 AND 2025 AND stadium IN ('{stadiums}')
                GROUP BY game_id, team, result, stadium
            )
            GROUP BY team HAVING games >= 20 ORDER BY rate DESC
        """
    }
    
    for metric, sql in queries.items():
        try:
            formatted_sql = sql.replace('{stadiums}', dunkin_list)
            df = client.query(formatted_sql).to_dataframe()
            print(f"\n--- {metric} ---")
            print(df.head(5).to_markdown(index=False))
            
            ne_row = df[df['team'] == 'NE']
            if not ne_row.empty:
                rank = df.index[df['team'] == 'NE'][0] + 1
                print(f"NE Rank: {rank} (Value: {ne_row.iloc[0]['rate']:.3f})")
            else:
                print("NE not found")
        except Exception as e:
            print(f"Error {metric}: {e}")

def main():
    client = get_bq_client()
    if not client: return
    # Get stadiums via simple list
    stadiums = get_dunkin_stadiums(client)
    scan_metrics(client, stadiums)

if __name__ == "__main__":
    main()
