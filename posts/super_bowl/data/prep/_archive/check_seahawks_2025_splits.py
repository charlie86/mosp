"""
Check Seahawks 2025 Splits

Calculates Win Percentage and Metrics splits for Seahawks between Starbucks Land (Net < 0) and Dunkin Land (Net > 0) for the 2025 Season ONLY (Reg + Post).
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

def get_stadium_lists():
    # Hardcoded for reliability (same as v2 split script)
    dunkin = [
        "Gillette Stadium", "MetLife Stadium", "Highmark Stadium", "Hard Rock Stadium", 
        "Soldier Field", "Lincoln Financial Field", "M&T Bank Stadium", 
        "Cleveland Browns Stadium", "Paycor Stadium", "Acrisure Stadium", 
        "Lucas Oil Stadium", "Ford Field", "Bank of America Stadium", 
        "EverBank Stadium", "Nissan Stadium"
    ]
    
    # Full Starbucks List (Net < 0)
    starbucks = [
        "Lumen Field", "Levi's Stadium", "SoFi Stadium", "Allegiant Stadium",
        "State Farm Stadium", "Empower Field at Mile High",
        "U.S. Bank Stadium", "Caesars Superdome", "Mercedes-Benz Stadium",
        "Raymond James Stadium", "Commanders Field", "NRG Stadium",
        "Lambeau Field", "GEHA Field at Arrowhead Stadium", "AT&T Stadium"
    ]
    
    return dunkin, starbucks

def analyze_seahawks_2025(client, dunkin_list, starbucks_list):
    d_str = "', '".join([s.replace("'", "\\'") for s in dunkin_list])
    s_str = "', '".join([s.replace("'", "\\'") for s in starbucks_list])

    print("\nAnalyzing Seahawks Splits (2025 Reg + Post)...")

    # Clean Metrics Loop
    metric_configs = [
        ("Defensive EPA (Lower is Better)", "defteam = 'SEA'", "AVG(epa)"),
        ("Defensive Turnover Rate (Higher is Better)", "defteam = 'SEA'", "SUM(CAST(interception AS INT64) + CAST(fumble_lost AS INT64)) / COUNT(*)"),
        ("Defensive Sack Rate (Higher is Better)", "defteam = 'SEA' AND play_type='pass'", "SUM(CAST(sack AS INT64)) / COUNT(*)"),
        ("Rush EPA (Offense)", "posteam = 'SEA' AND play_type='run'", "AVG(epa)"),
        ("Pass EPA (Offense)", "posteam = 'SEA' AND play_type='pass'", "AVG(epa)"),
        ("Overall Offense EPA", "posteam = 'SEA'", "AVG(epa)")
    ]

    for name, filter_cond, agg_func in metric_configs:
        sql = f"""
            SELECT 
                (SELECT {agg_func} FROM `stuperlatives.pbp_data` 
                 WHERE season = 2025 AND season_type IN ('REG', 'POST') 
                 AND {filter_cond} AND stadium IN ('{d_str}')) as d_val,
                (SELECT {agg_func} FROM `stuperlatives.pbp_data` 
                 WHERE season = 2025 AND season_type IN ('REG', 'POST') 
                 AND {filter_cond} AND stadium IN ('{s_str}')) as s_val
        """
        try:
            df = client.query(sql).to_dataframe()
            if not df.empty:
                d = df.iloc[0]['d_val']
                s = df.iloc[0]['s_val']
                
                if d is not None and s is not None:
                    delta = s - d # Starbucks - Dunkin.
                    # If Higher is Better (Offense), Positive Delta = Starbucks Advantage.
                    # If Lower is Better (Defense), Negative Delta = Starbucks Advantage.
                    
                    advantage = "Starbucks" if (delta > 0 and "Def" not in name) or (delta < 0 and "Def" in name) else "Dunkin"
                    
                    print(f"--- {name} ---")
                    print(f"Dunkin: {d:.4f} | Starbucks: {s:.4f}")
                    print(f"Advantage: {advantage} (Delta: {delta:.4f})")
                else:
                    print(f"{name}: Missing Data")
        except Exception as e:
            print(f"Error {name}: {e}")

    # Win Percentage Clean
    win_sql = f"""
        WITH game_results AS (
            SELECT 
                game_id, 
                stadium,
                CASE WHEN home_team = 'SEA' THEN result 
                     WHEN away_team = 'SEA' THEN -result 
                     ELSE NULL END as margin
            FROM `stuperlatives.pbp_data`
            WHERE season = 2025 AND season_type IN ('REG', 'POST')
            AND (home_team = 'SEA' OR away_team = 'SEA')
            GROUP BY game_id, stadium, home_team, away_team, result
        )
        SELECT 
            (SELECT AVG(CASE WHEN margin > 0 THEN 1 WHEN margin = 0 THEN 0.5 ELSE 0 END) FROM game_results WHERE stadium IN ('{d_str}')) as d_val,
            (SELECT AVG(CASE WHEN margin > 0 THEN 1 WHEN margin = 0 THEN 0.5 ELSE 0 END) FROM game_results WHERE stadium IN ('{s_str}')) as s_val
    """
    try:
        df = client.query(win_sql).to_dataframe()
        d = df.iloc[0]['d_val']
        s = df.iloc[0]['s_val']
        if d is not None and s is not None:
             print(f"--- Win Percentage ---")
             print(f"Dunkin: {d:.4f} | Starbucks: {s:.4f} | Delta: {s-d:.4f}")
    except Exception as e:
        print(f"Error Win %: {e}")

def main():
    client = get_bq_client()
    d, s = get_stadium_lists()
    analyze_seahawks_2025(client, d, s)

if __name__ == "__main__":
    main()
