#!/usr/bin/env python3
"""
Validation script for Coffee Wars analysis
Calculates exact gravity scores for all NFL stadiums and validates the report claims
"""

import os
import ast
import pandas as pd
import numpy as np
from google.cloud import bigquery
from google.oauth2 import service_account
from math import radians, cos, sin, asin, sqrt

# Configuration matching the map generation
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
BQ_COFFEE_TABLE = "stuperlatives.coffee_wars"
INTERFERENCE_RADIUS = 0.5  # miles
INTERFERENCE_STRENGTH = 1.0

# Stadium coordinates (matches generate_gravity_field_all.py)
STADIUM_COORDS = {
    "State Farm Stadium": (33.5276, -112.2626),
    "Mercedes-Benz Stadium": (33.7554, -84.4010),
    "M&T Bank Stadium": (39.2780, -76.6227),
    "Highmark Stadium": (42.7738, -78.7870),
    "Bank of America Stadium": (35.2258, -80.8528),
    "Soldier Field": (41.8623, -87.6167),
    "Paycor Stadium": (39.0955, -84.5161),
    "Cleveland Browns Stadium": (41.5061, -81.6995),
    "AT&T Stadium": (32.7478, -97.0928),
    "Empower Field at Mile High": (39.7439, -105.0201),
    "Ford Field": (42.3400, -83.0456),
    "Lambeau Field": (44.5013, -88.0622),
    "NRG Stadium": (29.6847, -95.4107),
    "Lucas Oil Stadium": (39.7601, -86.1639),
    "EverBank Stadium": (30.3239, -81.6373),
    "GEHA Field at Arrowhead Stadium": (39.0489, -94.4839),
    "SoFi Stadium": (33.9535, -118.3390),
    "Allegiant Stadium": (36.0909, -115.1833),
    "Hard Rock Stadium": (25.9580, -80.2389),
    "U.S. Bank Stadium": (44.9739, -93.2581),
    "Gillette Stadium": (42.0909, -71.2643),
    "Caesars Superdome": (29.9511, -90.0812),
    "MetLife Stadium": (40.8135, -74.0745),
    "Lincoln Financial Field": (39.9008, -75.1675),
    "Acrisure Stadium": (40.4468, -80.0158),
    "Levi's Stadium": (37.4032, -121.9698),
    "Lumen Field": (47.5952, -122.3316),
    "Raymond James Stadium": (27.9759, -82.5033),
    "Nissan Stadium": (36.1664, -86.7713),
    "Commanders Field": (38.9076, -76.8645),
}

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
    """Haversine distance in miles"""
    lo1, la1, lo2, la2 = map(radians, [lo1, la1, lo2, la2])
    dlon = lo2 - lo1
    dlat = la2 - la1
    a = sin(dlat/2)**2 + cos(la1) * cos(la2) * sin(dlon/2)**2
    return 2 * asin(sqrt(a)) * 3956

def calculate_stadium_gravity(stadium_name, stadium_lat, stadium_lng, d_locs, s_locs):
    """
    Calculate net gravity at a stadium using the interference model
    Returns: (dunkin_gravity, starbucks_gravity, net_gravity)
    """
    if len(d_locs) == 0 and len(s_locs) == 0:
        return 0.0, 0.0, 0.0
    
    # Initialize masses
    d_masses = np.ones(len(d_locs))
    s_masses = np.ones(len(s_locs))
    
    # Apply interference reduction
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
    
    # Calculate gravity at stadium location
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
    
    net_gravity = dunkin_gravity - starbucks_gravity
    return dunkin_gravity, starbucks_gravity, net_gravity

def main():
    print("=" * 80)
    print("COFFEE WARS VALIDATION REPORT")
    print("=" * 80)
    print()
    
    # Get data from BigQuery
    client = get_bq_client()
    if not client:
        print("ERROR: Could not create BigQuery client")
        return
    
    query = f"""
    SELECT 
        stadium_name,
        team_name,
        dunkin,
        starbucks
    FROM `{BQ_COFFEE_TABLE}`
    """
    
    df = client.query(query).to_dataframe()
    print(f"Loaded {len(df)} total stadium records from BigQuery")
    print(f"Processing {len(STADIUM_COORDS)} current NFL stadiums\n")
    
    # Calculate gravity for all current stadiums
    results = []
    for _, row in df.iterrows():
        stadium_name = row['stadium_name']
        team = row['team_name']
        
        # Only process current stadiums
        if stadium_name not in STADIUM_COORDS:
            continue
            
        stadium_lat, stadium_lng = STADIUM_COORDS[stadium_name]
        
        # Locations are already in array format from BigQuery
        d_locs = row['dunkin'].get('locations', []) if row['dunkin'] else []
        s_locs = row['starbucks'].get('locations', []) if row['starbucks'] else []
        
        # Convert numpy arrays to lists if needed
        if d_locs is None or (hasattr(d_locs, '__len__') and len(d_locs) == 0):
            d_locs = []
        if s_locs is None or (hasattr(s_locs, '__len__') and len(s_locs) == 0):
            s_locs = []
        
        d_grav, s_grav, net_grav = calculate_stadium_gravity(
            stadium_name, stadium_lat, stadium_lng, d_locs, s_locs
        )
        
        results.append({
            'stadium_name': stadium_name,
            'team': team,
            'dunkin_gravity': d_grav,
            'starbucks_gravity': s_grav,
            'net_gravity': net_grav,
            'dunkin_count': len([m for m in d_locs if m]),
            'starbucks_count': len([m for m in s_locs if m])
        })
    
    results_df = pd.DataFrame(results)
    
    # Sort by net gravity
    results_df = results_df.sort_values('net_gravity', ascending=False)
    
    print("\n" + "=" * 80)
    print("TOP 10 DUNKIN' GRAVITY STADIUMS (Positive Net Gravity)")
    print("=" * 80)
    top_dunkin = results_df.head(10)
    for idx, row in top_dunkin.iterrows():
        print(f"{row['stadium_name']:40} ({row['team'][:15]:15}) Net: +{row['net_gravity']:6.2f}  "
              f"D:{row['dunkin_gravity']:5.2f} S:{row['starbucks_gravity']:5.2f}")
    
    print("\n" + "=" * 80)
    print("TOP 10 STARBUCKS GRAVITY STADIUMS (Negative Net Gravity)")
    print("=" * 80)
    top_starbucks = results_df.tail(10).iloc[::-1]
    for idx, row in top_starbucks.iterrows():
        print(f"{row['stadium_name']:40} ({row['team'][:15]:15}) Net: {row['net_gravity']:7.2f}  "
              f"D:{row['dunkin_gravity']:5.2f} S:{row['starbucks_gravity']:5.2f}")
    
    # Validate specific stadiums mentioned in the report
    print("\n" + "=" * 80)
    print("VALIDATION: STADIUMS MENTIONED IN REPORT")
    print("=" * 80)
    
    check_stadiums = [
        "Gillette Stadium",
        "Lumen Field",
        "Levi's Stadium",
        "M&T Bank Stadium",
        "SoFi Stadium",
    ]
    
    for stadium in check_stadiums:
        matches = results_df[results_df['stadium_name'] == stadium]
        if len(matches) > 0:
            row = matches.iloc[0]
            print(f"\n{stadium}:")
            print(f"  Dunkin' Gravity:    {row['dunkin_gravity']:6.2f}")
            print(f"  Starbucks Gravity:  {row['starbucks_gravity']:6.2f}")
            print(f"  Net Gravity:        {row['net_gravity']:+7.2f}")
            print(f"  Store Counts: D={row['dunkin_count']} S={row['starbucks_count']}")
    
    # Export full results
    output_file = "coffee_gravity_validation.csv"
    results_df.to_csv(output_file, index=False)
    print(f"\n\nFull results exported to: {output_file}")
    
    print("\n" + "=" * 80)
    print("KEY FINDINGS")
    print("=" * 80)
    print(f"Most Dunkin'-Dominated:  {results_df.iloc[0]['stadium_name']} (Net: +{results_df.iloc[0]['net_gravity']:.2f})")
    print(f"Most Starbucks-Dominated: {results_df.iloc[-1]['stadium_name']} (Net: {results_df.iloc[-1]['net_gravity']:.2f})")
    print(f"Median Net Gravity:       {results_df['net_gravity'].median():+.2f}")
    print(f"Mean Net Gravity:         {results_df['net_gravity'].mean():+.2f}")
    
if __name__ == "__main__":
    main()
