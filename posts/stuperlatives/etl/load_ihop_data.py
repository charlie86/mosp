
import os
import sys
import pandas as pd
import json

# Add path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from posts.stuperlatives.etl.bq_utils import get_bq_client, ensure_dataset, upload_dataframe

# Config
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))

def load_ihop_data():
    print("Initializing IHOP Data Load...")
    
    # 1. Setup BQ
    client = get_bq_client()
    if not client:
        print("Aborting: No BQ Client available.")
        return
        
    dataset_ref = ensure_dataset(client)
    
    # 2. Parse JSON
    print("\n--- Processing IHOP Gravitational Data ---")
    ihop_path = os.path.abspath(os.path.join(PROJECT_ROOT, 'posts/pff_analysis/data/stadium_gravitational_data.json'))
    
    if os.path.exists(ihop_path):
        try:
            with open(ihop_path, 'r') as f:
                data = json.load(f)
            
            ihop_rows = []
            for entry in data:
                team = entry.get('Team')
                ihops = entry.get('IHOPs', [])
                
                # Debug Buffalo
                if 'Buffalo' in str(team):
                    print(f"DEBUG: Found Buffalo entry. IHOP count: {len(ihops)}")
                    if ihops:
                        print(f"First IHOP distance: {ihops[0].get('DistanceMiles')}")

                if ihops:
                    # Find closest IHOP
                    # Ensure strict float conversion and handle potential key errors
                    distances = []
                    for i in ihops:
                        d = i.get('DistanceMiles')
                        if d is not None:
                            distances.append(float(d))
                    
                    if distances:
                        min_dist = min(distances)
                        ihop_rows.append({'Team': team, 'DistanceMiles': min_dist})
                    else:
                        print(f"Warning: {team} has IHOP list but no valid distances.")
                        ihop_rows.append({'Team': team, 'DistanceMiles': 999.0})
                else:
                    # No IHOPs found
                    print(f"Warning: No IHOPs found for {team}")
                    ihop_rows.append({'Team': team, 'DistanceMiles': 999.0})
            
            ihop_df = pd.DataFrame(ihop_rows)
            
            # 3. Map Teams
            TEAM_MAP = {
                'Arizona Cardinals': 'ARI', 'Atlanta Falcons': 'ATL', 'Baltimore Ravens': 'BAL', 'Buffalo Bills': 'BUF',
                'Carolina Panthers': 'CAR', 'Chicago Bears': 'CHI', 'Cincinnati Bengals': 'CIN', 'Cleveland Browns': 'CLE',
                'Dallas Cowboys': 'DAL', 'Denver Broncos': 'DEN', 'Detroit Lions': 'DET', 'Green Bay Packers': 'GB',
                'Houston Texans': 'HOU', 'Indianapolis Colts': 'IND', 'Jacksonville Jaguars': 'JAX', 'Kansas City Chiefs': 'KC',
                'Las Vegas Raiders': 'LV', 'Los Angeles Chargers': 'LAC', 'Los Angeles Rams': 'LAR', 'Miami Dolphins': 'MIA',
                'Minnesota Vikings': 'MIN', 'New England Patriots': 'NE', 'New Orleans Saints': 'NO', 'New York Giants': 'NYG',
                'New York Jets': 'NYJ', 'Philadelphia Eagles': 'PHI', 'Pittsburgh Steelers': 'PIT', 'San Francisco 49ers': 'SF',
                'Seattle Seahawks': 'SEA', 'Tampa Bay Buccaneers': 'TB', 'Tennessee Titans': 'TEN', 'Washington Commanders': 'WAS',
                'Washington Football Team': 'WAS', 'Washington Redskins': 'WAS' 
            }
            
            ihop_df['Team'] = ihop_df['Team'].map(TEAM_MAP).fillna(ihop_df['Team'])
            ihop_df = ihop_df.dropna(subset=['Team'])
            
            # 4. Dedup Logic (Pandas-side)
            # Ensure unique Team entries before upload
            count_before = len(ihop_df)
            ihop_df = ihop_df.drop_duplicates(subset=['Team'], keep='first')
            count_after = len(ihop_df)
            
            if count_before != count_after:
                print(f"Removed {count_before - count_after} duplicate entries.")
            
            print(f"Uploading {len(ihop_df)} unique IHOP proximity records...")
            
            # 5. Upload (WRITE_TRUNCATE is handled by upload_dataframe)
            upload_dataframe(client, ihop_df, 'ihop_data', dataset_ref)
            
        except Exception as e:
            print(f"Error processing IHOP json: {e}")
    else:
        print(f"IHOP data not found at {ihop_path}")
       
    print("\nIHOP Data Load Complete.")

if __name__ == "__main__":
    load_ihop_data()
