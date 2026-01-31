"""
League Dunkin Comparison

Finds stats where the Patriots are #1 in the league specifically in "Dunkin Land" (Net Gravity > 0).
Scans PBP data from 2015-2025 and PFF data from 2024-2025.
"""

import os
import sys
import pandas as pd
import numpy as np
from google.cloud import bigquery
from google.oauth2 import service_account

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

BQ_PROJECT = "gen-lang-client-0400686052"
BQ_COFFEE_TABLE = "stuperlatives.coffee_wars"
BQ_PBP_TABLE = "stuperlatives.pbp_data"
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
    
    if len(d_locs) == 0 and len(s_locs) == 0: return 0.0, 0.0, 0.0
    
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
        d_masses = np.maximum(d_masses, 0.0)
        s_masses = np.maximum(s_masses, 0.0)
    
    dunkin_gravity = 0.0
    starbucks_gravity = 0.0
    
    for i, loc in enumerate(d_locs):
        if d_masses[i] > 0:
            dist = simple_hav(loc['lng'], loc['lat'], stadium_lng, stadium_lat)
            dunkin_gravity += d_masses[i] * np.exp(-0.5 * dist)
    
    for i, loc in enumerate(s_locs):
        if s_masses[i] > 0:
            dist = simple_hav(loc['lng'], loc['lat'], stadium_lng, stadium_lat)
            starbucks_gravity += s_masses[i] * np.exp(-0.5 * dist)
    
    return dunkin_gravity, starbucks_gravity, dunkin_gravity - starbucks_gravity

def get_dunkin_stadiums(client):
    """Identify stadiums with Net Gravity > 0"""
    print("Calculating stadium gravity...")
    
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
        
        _, _, net_grav = calculate_stadium_gravity_single(stadium_lat, stadium_lng, d_locs, s_locs)
        
        if net_grav > 0:
            dunkin_stadiums.append(stadium_name)
            
    print(f"Identified {len(dunkin_stadiums)} stadiums in Dunkin Land (Net > 0)")
    return dunkin_stadiums

def analyze_creative_metrics(client, dunkin_stadiums):
    """Analyze creative metrics for all teams in Dunkin stadiums"""
    print("Analyzing metrics for ALL TEAMS in Dunkin stadiums (2015-2025)...")
    
    dunkin_list = "', '".join(dunkin_stadiums)
    
    # 1. Screen Passes in Dunkin Land (The Donut Screen)
    # 2. QB Sneaks (Run on Dunkin)
    # 3. 4th Quarter Comebacks
    # 4. Success Rate vs Bird Teams
    # 5. Red Zone Rush TD %
    
    queries = {
        "Rush Yards Per Attempt (YPA)": """
            SELECT 
                posteam as team,
                COUNT(*) as attempts,
                SUM(yards_gained) / COUNT(*) as rate
            FROM `stuperlatives.pbp_data`
            WHERE season = 2025
            AND stadium IN ('{}')
            AND play_type = 'run'
            GROUP BY posteam
            HAVING attempts >= 100
            ORDER BY rate DESC
        """,
        "Rush Success Rate": """
            SELECT 
                posteam as team,
                COUNT(*) as attempts,
                AVG(CAST(success AS FLOAT64)) as rate
            FROM `stuperlatives.pbp_data`
            WHERE season = 2025
            AND stadium IN ('{}')
            AND play_type = 'run'
            GROUP BY posteam
            HAVING attempts >= 100
            ORDER BY rate DESC
        """,
        "Rush First Down Rate": """
            SELECT 
                posteam as team,
                COUNT(*) as attempts,
                SUM(CAST(first_down_rush AS INT64)) / COUNT(*) as rate
            FROM `stuperlatives.pbp_data`
            WHERE season = 2025
            AND stadium IN ('{}')
            AND play_type = 'run'
            GROUP BY posteam
            HAVING attempts >= 100
            ORDER BY rate DESC
        """
    }
    
    # Run PBP queries
    for metric_name, sql_template in queries.items():
        sql = sql_template.format(dunkin_list)
        try:
            df = client.query(sql).to_dataframe()
            print(f"\n--- {metric_name} (Top 5) ---")
            print(df.head(5).to_markdown(index=False))
            
            ne_row = df[df['team'] == 'NE']
            if not ne_row.empty:
                rank = df.index[df['team'] == 'NE'][0] + 1
                print(f"NE Rank: {rank} (Value: {ne_row.iloc[0]['rate']:.3f})")
            else:
                print("NE not found in dataset")
        except Exception as e:
            print(f"Error measuring {metric_name}: {e}")

def main():
    client = get_bq_client()
    if not client: return
    
    dunkin_stadiums = get_dunkin_stadiums(client)
    analyze_creative_metrics(client, dunkin_stadiums)

if __name__ == "__main__":
    main()
