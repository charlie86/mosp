"""
Deep Dive Efficiency Scanner

Scans niche rate-based stats to find where the Patriots are #1 in Dunkin Zones (Net > 0) for the 2025 Season.
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
    # Hardcoded Dunkin Stadiums based on previous runs (Net > 0)
    # This matches the result "Identified 16 stadiums in Dunkin Land"
    # To be safe, re-querying or just using the precise list is better.
    # For speed, I'll use the logic.
    query = """
    SELECT stadium_name, 
           (IFNULL(dunkin_gravity, 0) - IFNULL(starbucks_gravity, 0)) as net_gravity 
    FROM (
        SELECT stadium_name,
            -- Re-implement simple gravity approximation for selection or rely on known list
            -- Actually, simpler to just fetch the table and filter
            team_name
        FROM `stuperlatives.coffee_wars`
    )
    """
    # I will stick to the Python calculation wrapper reused from before to ensure consistency
    # importing the logic would be cleaner, but I'll just paste the stadium list I found earlier
    # 16 Stadiums: 
    # Gillette, MetLife, Highmark, Hard Rock, Soldier Field, Lincoln Financial, M&T Bank, 
    # Cleveland Browns, Paycor, Acrisure, Lucas Oil, Ford Field, Bank of America, TIAA Bank (EverBank), 
    # Nissan? No, checking the previous output...
    
    # Actually, the previous script output "Identified 16 stadiums".
    # I will paste the calculation logic again to be 100% accurate.
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
            
    return dunkin_stadiums

def scan_metrics(client, dunkin_stadiums):
    dunkin_list = "', '".join(dunkin_stadiums)
    
    # 2025 SEASON ONLY
    queries = {
        "Rush Yard Share (Runs on Dunkin)": """
            SELECT posteam as team, 
                   SUM(yards_gained) as total_yards,
                   SUM(CASE WHEN play_type = 'run' THEN yards_gained ELSE 0 END) as rush_yards,
                   SUM(CASE WHEN play_type = 'run' THEN yards_gained ELSE 0 END) / SUM(yards_gained) as rate
            FROM `stuperlatives.pbp_data`
            WHERE season = 2025 AND stadium IN ('{stadiums}')
            AND play_type IN ('run', 'pass')
            GROUP BY posteam HAVING total_yards >= 1000 ORDER BY rate DESC
        """,
        "Rush TD Share (Points on Dunkin)": """
             SELECT posteam as team, 
                   SUM(CAST(touchdown AS INT64)) as total_tds,
                   SUM(CASE WHEN play_type = 'run' AND touchdown = 1 THEN 1 ELSE 0 END) as rush_tds,
                   SUM(CASE WHEN play_type = 'run' AND touchdown = 1 THEN 1 ELSE 0 END) / NULLIF(SUM(CAST(touchdown AS INT64)),0) as rate
            FROM `stuperlatives.pbp_data`
            WHERE season = 2025 AND stadium IN ('{stadiums}')
            AND play_type IN ('run', 'pass')
            GROUP BY posteam HAVING total_tds >= 5 ORDER BY rate DESC
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
    stadiums = get_dunkin_stadiums(client)
    scan_metrics(client, stadiums)

if __name__ == "__main__":
    main()
