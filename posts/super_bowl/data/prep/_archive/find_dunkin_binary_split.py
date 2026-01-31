import os
import pandas as pd
import numpy as np
from google.cloud import bigquery
from google.oauth2 import service_account

# --- Configuration ---
BQ_PROJECT = "mosp-449117"
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

def fetch_data(client):
    # Fetch Data
    # 1. Coffee (Gravity)
    q_coffee = f"""
    SELECT 
        team_name, 
        dunkin,
        starbucks
    FROM `{BQ_COFFEE_TABLE}`
    """
    coffee_df = client.query(q_coffee).to_dataframe()
    
    # Calculate Gravity
    GRAVITY_CONSTANT = 1.0
    EPSILON_MILES = 0.1
    POWER = 2
    
    gravity_data = []
    
    for _, row in coffee_df.iterrows():
        # Dunkin Pull
        d_pull = 0.0
        locations = row['dunkin'].get('locations', []) if row['dunkin'] else []
        if locations is None: locations = []
            
        for loc in locations:
            dist = loc.get('distance_miles', 1000)
            # Exponential Decay: e^(-0.5 * d)
            g = np.exp(-0.5 * dist)
            d_pull += g
            
        gravity_data.append({
            'team_name': row['team_name'],
            'dunkin_gravity': d_pull
        })
        
    gravity_df = pd.DataFrame(gravity_data)

    # 2. Game Data (NE Rushing)
    q_game = f"""
    SELECT
        game_id,
        home_team,
        posteam,
        epa,
        success,
        rush_touchdown
    FROM `{BQ_PBP_TABLE}`
    WHERE season >= 2015
      AND posteam = 'NE'
      AND play_type = 'run'
    """
    pbp_df = client.query(q_game).to_dataframe()
    
    # 3. Map
    pbp_to_coffee_map = {
        'ARI': 'Arizona Cardinals', 'ATL': 'Atlanta Falcons', 'BAL': 'Baltimore Ravens', 'BUF': 'Buffalo Bills',
        'CAR': 'Carolina Panthers', 'CHI': 'Chicago Bears', 'CIN': 'Cincinnati Bengals', 'CLE': 'Cleveland Browns',
        'DAL': 'Dallas Cowboys', 'DEN': 'Denver Broncos', 'DET': 'Detroit Lions', 'GB': 'Green Bay Packers',
        'HOU': 'Houston Texans', 'IND': 'Indianapolis Colts', 'JAX': 'Jacksonville Jaguars', 'KC': 'Kansas City Chiefs',
        'LAC': 'Los Angeles Chargers', 'SD': 'San Diego Chargers', 
        'LA': 'Los Angeles Rams', 'STL': 'St. Louis Rams',
        'LV': 'Las Vegas Raiders', 'OAK': 'Oakland Raiders',
        'MIA': 'Miami Dolphins', 'MIN': 'Minnesota Vikings', 'NE': 'New England Patriots', 'NO': 'New Orleans Saints',
        'NYG': 'New York Giants', 'NYJ': 'New York Jets', 'PHI': 'Philadelphia Eagles', 'PIT': 'Pittsburgh Steelers',
        'SF': 'San Francisco 49ers', 'SEA': 'Seattle Seahawks', 'TB': 'Tampa Bay Buccaneers', 'TEN': 'Tennessee Titans',
        'WAS': 'Washington Commanders'
    }
    pbp_df['mapped_home_team'] = pbp_df['home_team'].map(pbp_to_coffee_map)
    
    # 4. Agg to Game Level
    # Note: We want weighted average of EPA? Or average of averages.
    # To reproduce table numbers exactly, we should ideally work at Play Level if possible, then split.
    # But sticking to game agg logic from before is safer for stability.
    # Let's use Play Level join to be precise for "EPA/Play"
    
    merged = pd.merge(pbp_df, gravity_df, left_on='mapped_home_team', right_on='team_name', how='inner')
    return merged

def find_best_split(df):
    results = []
    
    # Exponential Scores are generally lower than Gravity near-zero, but higher distributed.
    # Scores for top teams: MetLife (Singularity) will be lower than 42.
    # Scan range: 0.1 to 10
    scan_gravity = [0.1, 0.5, 1.0, 1.5, 2.0, 2.5, 3.0, 4.0, 5.0, 7.5, 10.0]
    
    print(f"\nScanning {len(scan_gravity)} thresholds for optimum Munchkin Threshold (Exponential)...")
    
    for g in scan_gravity:
        in_group = df[df['dunkin_gravity'] >= g] # High Gravity
        out_group = df[df['dunkin_gravity'] < g] # Low Gravity
        
        # Ensure decent sample size (at least 100 plays in each bucket)
        if len(in_group) < 100 or len(out_group) < 100: continue
        
        epa_diff = in_group['epa'].mean() - out_group['epa'].mean()
        
        results.append({
            'Threshold': g,
            'Label': f">= {g} Gravity",
            'EPA_Diff': epa_diff,
            'High_Gravity_EPA': in_group['epa'].mean(),
            'Low_Gravity_EPA': out_group['epa'].mean(),
            'High_Gravity_Success': in_group['success'].mean(),
            'Low_Gravity_Success': out_group['success'].mean(),
            'Sample_High': len(in_group),
            'Sample_Low': len(out_group)
        })
        
    # Sort by EPA Diff (finding the biggest advantage)
    results.sort(key=lambda x: x['EPA_Diff'], reverse=True)
    
    print("\n--- Top Gravity Splits ---")
    for r in results[:3]:
         print(f"Threshold: {r['Threshold']} | Delta: +{r['EPA_Diff']:.3f} | High: {r['High_Gravity_EPA']:.3f} | Low: {r['Low_Gravity_EPA']:.3f}")

    # Explicitly calculate for 2.0 (The chosen Munchkin Threshold)
    target = next((r for r in results if r['Threshold'] == 2.0), None)
    if target:
        print(f"\n--- The Munchkin Threshold (Gravity = 2.0) ---")
        print("| Environment | Dunkin' Gravity | Rushing EPA/Play | Rushing Success Rate |")
        print("| :--- | :--- | :--- | :--- |")
        print(f"| **High Gravity** | >= 2.0 | **{target['High_Gravity_EPA']:.3f}** | **{target['High_Gravity_Success']*100:.1f}%** |")
        print(f"| **Low Gravity** | < 2.0 | **{target['Low_Gravity_EPA']:.3f}** | **{target['Low_Gravity_Success']*100:.1f}%** |")
        print(f"| **The Delta** | | **+{target['EPA_Diff']:.3f}** | **+{(target['High_Gravity_Success'] - target['Low_Gravity_Success'])*100:.1f}%** |")


if __name__ == "__main__":
    client = get_bq_client()
    if client:
        df = fetch_data(client)
        find_best_split(df)
