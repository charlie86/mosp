
from google.cloud import bigquery
import os
import pandas as pd

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), "../../../"))
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')

client = bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)

BIRD_TEAMS = ['ARI', 'ATL', 'BAL', 'PHI', 'SEA']
bird_str = "', '".join(BIRD_TEAMS)

query = f"""
    SELECT season, week, posteam, defteam, home_team, away_team
    FROM `stuperlatives.pbp_data`
    WHERE season = 2025
    AND (
        (posteam = 'NE' AND defteam IN ('{bird_str}'))
        OR
        (posteam IN ('{bird_str}') AND defteam = 'NE')
    )
    GROUP BY 1,2,3,4,5,6
    ORDER BY week
"""

df = client.query(query).to_dataframe()
print(f"NE Games vs Bird Teams ({BIRD_TEAMS}):")
print(df)
