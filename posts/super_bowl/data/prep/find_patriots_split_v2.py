"""
Find Patriots Split V2

Calculates Win Percentage and Rush Metric splits for New England between Dunkin Land (Net > 0) and Starbucks Land (Net < 0).
"""

import os
import sys
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

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

def get_stadium_lists(client):
    # Hardcoded for reliability
    # Starbucks list (Net < 0)
    # Dunkin list (Net > 0)
    # Based on previous successful runs logic
    
    # Dunkin: Gillette, MetLife, Highmark, etc.
    dunkin = [
        "Gillette Stadium", "MetLife Stadium", "Highmark Stadium", "Hard Rock Stadium", 
        "Soldier Field", "Lincoln Financial Field", "M&T Bank Stadium", 
        "Cleveland Browns Stadium", "Paycor Stadium", "Acrisure Stadium", 
        "Lucas Oil Stadium", "Ford Field", "Bank of America Stadium", 
        "EverBank Stadium", "Nissan Stadium"
    ]
    
    # Starbucks: Lumen, Levi's, SoFi, Allegiant, State Farm, Empower, etc.
    starbucks = [
        "Lumen Field", "Levi's Stadium", "SoFi Stadium", "Allegiant Stadium",
        "State Farm Stadium", "Empower Field at Mile High",
        "U.S. Bank Stadium", "Caesars Superdome", "Mercedes-Benz Stadium",
        "Raymond James Stadium", "Commanders Field", "NRG Stadium",
        "Lambeau Field", "GEHA Field at Arrowhead Stadium", "AT&T Stadium"
    ]
    
    return dunkin, starbucks

def analyze_splits(client, dunkin_list, starbucks_list):
    d_str = "', '".join([s.replace("'", "\\'") for s in dunkin_list])
    s_str = "', '".join([s.replace("'", "\\'") for s in starbucks_list])

    print("\nAnalyzing Patriots Splits (2015-2025)...")

    # Win Percentage
    win_sql = f"""
        WITH game_results AS (
            SELECT 
                game_id, 
                stadium,
                CASE WHEN home_team = 'NE' THEN result ELSE -result END as ne_margin
            FROM `stuperlatives.pbp_data`
            WHERE season BETWEEN 2015 AND 2025
            AND (home_team = 'NE' OR away_team = 'NE')
            GROUP BY game_id, stadium, home_team, result
        )
        SELECT 
            'Win Percentage' as metric,
            (SELECT AVG(CASE WHEN ne_margin > 0 THEN 1 WHEN ne_margin = 0 THEN 0.5 ELSE 0 END) 
             FROM game_results WHERE stadium IN ('{d_str}')) as dunkin_val,
            (SELECT AVG(CASE WHEN ne_margin > 0 THEN 1 WHEN ne_margin = 0 THEN 0.5 ELSE 0 END) 
             FROM game_results WHERE stadium IN ('{s_str}')) as starbucks_val
    """
    try:
        df = client.query(win_sql).to_dataframe()
        d = df.iloc[0]['dunkin_val']
        s = df.iloc[0]['starbucks_val']
        print(f"--- Win Percentage ---")
        print(f"Dunkin: {d:.4f} | Starbucks: {s:.4f} | Delta: {d-s:.4f}")
    except Exception as e:
        print(f"Error Win %: {e}")

    # Metrics
    metrics = {
        "Rush Success Rate": "AVG(CASE WHEN play_type = 'run' THEN CAST(success AS FLOAT64) END)",
        "Rush EPA": "AVG(CASE WHEN play_type = 'run' THEN epa END)",
        "Pass EPA": "AVG(CASE WHEN play_type = 'pass' THEN epa END)",
        "Turnover Rate (Lower is Better)": "SUM(CAST(interception AS INT64) + CAST(fumble_lost AS INT64)) / COUNT(*)"
    }
    
    for m, agg in metrics.items():
        sql = f"""
            SELECT 
                (SELECT {agg} FROM `stuperlatives.pbp_data` 
                 WHERE season BETWEEN 2015 AND 2025 AND posteam = 'NE' AND stadium IN ('{d_str}')) as d_val,
                (SELECT {agg} FROM `stuperlatives.pbp_data` 
                 WHERE season BETWEEN 2015 AND 2025 AND posteam = 'NE' AND stadium IN ('{s_str}')) as s_val
        """
        try:
            df = client.query(sql).to_dataframe()
            d = df.iloc[0]['d_val']
            s = df.iloc[0]['s_val']
            delta = d - s
            if "Lower" in m: delta = -delta
            print(f"--- {m} ---")
            print(f"Dunkin: {d:.4f} | Starbucks: {s:.4f} | Delta: {delta:.4f}")
        except Exception as e:
            print(f"Error {m}: {e}")

def main():
    client = get_bq_client()
    d, s = get_stadium_lists(client)
    analyze_splits(client, d, s)

if __name__ == "__main__":
    main()
