"""
Find Patriots Split

Calculates the performance split for New England between Dunkin Land (Net > 0) and Starbucks Land (Net < 0).
Looking for metrics where NE is Great in Dunkin and Bad in Starbucks.
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

def get_stadium_lists(client):
    # Retrieve all stadiums and classify them
    # For speed, hardcoding based on known reliable map data or re-fetching
    # Re-fetching ensures we use the exact current map
    import numpy as np
    
    STADIUM_COORDS = {
        "State Farm Stadium": (33.5276, -112.2626), "Mercedes-Benz Stadium": (33.7554, -84.4010),
        "M&T Bank Stadium": (39.2780, -76.6227), "Highmark Stadium": (42.7738, -78.7870),
        "Bank of America Stadium": (35.2258, -80.8528), "Soldier Field": (41.8623, -87.6167),
        "Paycor Stadium": (39.0955, -84.5161), "Cleveland Browns Stadium": (41.5061, -81.6995),
        "AT&T Stadium": (32.7478, -97.0928), "Empower Field at Mile High": (39.7439, -105.0201),
        "Ford Field": (42.3400, -83.0456), "Lambeau Field": (44.5013, -88.0622),
        "NRG Stadium": (29.6847, -95.4107), "Lucas Oil Stadium": (39.7601, -86.1639),
        "EverBank Stadium": (30.3239, -81.6373), "GEHA Field at Arrowhead Stadium": (39.0489, -94.4839),
        "SoFi Stadium": (33.9535, -118.3390), "Allegiant Stadium": (36.0909, -115.1833),
        "Hard Rock Stadium": (25.9580, -80.2389), "U.S. Bank Stadium": (44.9739, -93.2581),
        "Gillette Stadium": (42.0909, -71.2643), "Caesars Superdome": (29.9511, -90.0812),
        "MetLife Stadium": (40.8135, -74.0745), "Lincoln Financial Field": (39.9008, -75.1675),
        "Acrisure Stadium": (40.4468, -80.0158), "Levi's Stadium": (37.4032, -121.9698),
        "Lumen Field": (47.5952, -122.3316), "Raymond James Stadium": (27.9759, -82.5033),
        "Nissan Stadium": (36.1664, -86.7713), "Commanders Field": (38.9076, -76.8645),
    }

    def simple_hav(lo1, la1, lo2, la2):
        from math import radians, sin, cos, asin, sqrt
        lo1, la1, lo2, la2 = map(radians, [lo1, la1, lo2, la2])
        dlon = lo2 - lo1
        dlat = la2 - la1
        a = sin(dlat/2)**2 + cos(la1) * cos(la2) * sin(dlon/2)**2
        return 2 * asin(sqrt(a)) * 3956

    def calculate_stadium_gravity_single(stadium_lat, stadium_lng, d_locs, s_locs):
        INTERFERENCE_RADIUS = 0.5
        INTERFERENCE_STRENGTH = 1.0
        if len(d_locs) == 0 and len(s_locs) == 0: return 0.0
        
        d_masses = np.ones(len(d_locs))
        s_masses = np.ones(len(s_locs))
        if len(d_locs) > 0 and len(s_locs) > 0:
            for i, d in enumerate(d_locs):
                for j, s in enumerate(s_locs):
                    dist = simple_hav(d['lng'], d['lat'], s['lng'], s['lat'])
                    if dist < INTERFERENCE_RADIUS:
                        reduction = INTERFERENCE_STRENGTH * (1.0 - dist/INTERFERENCE_RADIUS)
                        d_masses[i] -= reduction
                        s_masses[j] -= reduction
        
        dunkin = 0.0
        starbucks = 0.0
        for i, loc in enumerate(d_locs):
            if d_masses[i] > 0:
                dist = simple_hav(loc['lng'], loc['lat'], stadium_lng, stadium_lat)
                dunkin += d_masses[i] * np.exp(-0.5 * dist)
        for i, loc in enumerate(s_locs):
            if s_masses[i] > 0:
                dist = simple_hav(loc['lng'], loc['lat'], stadium_lng, stadium_lat)
                starbucks += s_masses[i] * np.exp(-0.5 * dist)
        return dunkin - starbucks

    query = f"SELECT stadium_name, dunkin, starbucks FROM `{BQ_COFFEE_TABLE}`"
    df = client.query(query).to_dataframe()
    dunkin_stadiums = []
    starbucks_stadiums = []
    
    for _, row in df.iterrows():
        stadium_name = row['stadium_name']
        if stadium_name not in STADIUM_COORDS: continue
        stadium_lat, stadium_lng = STADIUM_COORDS[stadium_name]
        d_locs = row['dunkin'].get('locations', []) if row['dunkin'] else []
        s_locs = row['starbucks'].get('locations', []) if row['starbucks'] else []
        if d_locs is None: d_locs = []
        if s_locs is None: s_locs = []
        
        net_grav = calculate_stadium_gravity_single(stadium_lat, stadium_lng, d_locs, s_locs)
        if net_grav > 0:
            dunkin_stadiums.append(stadium_name)
        else:
            starbucks_stadiums.append(stadium_name)
            
    return dunkin_stadiums, starbucks_stadiums

    queries = {
        "Rush Success Rate": """
            AVG(CAST(success AS FLOAT64))
        """,
        "Win Percentage": """
            AVG(CASE WHEN result > 0 THEN 1 WHEN result = 0 THEN 0.5 ELSE 0 END) -- This is messy in PBP rows
        """
    }
    
    # Better to calculate Win % correctly by grouping by game_id first
    # So I will use a separate query loop for Win %
    
    # First, standard row metrics
    row_queries = {
        "Rush Success Rate": """
            AVG(CASE WHEN play_type = 'run' THEN CAST(success AS FLOAT64) ELSE NULL END)
        """
    }
    
    print("\nAnalyzing Patriots Splits (2015-2025) - Additional Metrics...")
    
    for metric_name, agg_func in row_queries.items():
        sql = f"""
            SELECT 
                '{metric_name}' as metric,
                (SELECT {agg_func} FROM `stuperlatives.pbp_data` WHERE season BETWEEN 2015 AND 2025 AND posteam = 'NE' AND stadium IN ('{dunkin_list}')) as dunkin_val,
                (SELECT {agg_func} FROM `stuperlatives.pbp_data` WHERE season BETWEEN 2015 AND 2025 AND posteam = 'NE' AND stadium IN ('{starbucks_list}')) as starbucks_val
        """
        try:
            df = client.query(sql).to_dataframe()
            if not df.empty and df.iloc[0]['dunkin_val'] is not None:
                d_val = df.iloc[0]['dunkin_val']
                s_val = df.iloc[0]['starbucks_val']
                delta = d_val - s_val
                print(f"--- {metric_name} ---")
                print(f"Dunkin: {d_val:.4f} | Starbucks: {s_val:.4f} | Delta: {delta:.4f}")
        except Exception as e:
            print(f"Error {metric_name}: {e}")

    # Win Percentage Split (Complex)
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
             FROM game_results WHERE stadium IN ('{dunkin_list}')) as dunkin_val,
            (SELECT AVG(CASE WHEN ne_margin > 0 THEN 1 WHEN ne_margin = 0 THEN 0.5 ELSE 0 END) 
             FROM game_results WHERE stadium IN ('{starbucks_list}')) as starbucks_val
    """
    try:
        df = client.query(win_sql).to_dataframe()
        d_val = df.iloc[0]['dunkin_val']
        s_val = df.iloc[0]['starbucks_val']
        delta = d_val - s_val
        print(f"--- Win Percentage ---")
        print(f"Dunkin: {d_val:.4f} | Starbucks: {s_val:.4f} | Delta: {delta:.4f}")
    except Exception as e:
        print(f"Error Win Percentage: {e}")


def main():
    client = get_bq_client()
    if not client: return
    d_list, s_list = get_stadium_lists(client)
    analyze_splits(client, d_list, s_list)

if __name__ == "__main__":
    main()
