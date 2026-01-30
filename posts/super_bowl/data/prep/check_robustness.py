
import os
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from google.cloud import bigquery
from google.oauth2 import service_account

# --- Configuration ---
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
    print("Fetching coffee data...")
    q_coffee = f"""
    SELECT 
        team_name, 
        dunkin
    FROM `{BQ_COFFEE_TABLE}`
    """
    coffee_df = client.query(q_coffee).to_dataframe()
    
    print("Fetching NE Rushing data...")
    q_game = f"""
    SELECT
        game_id,
        home_team,
        posteam,
        epa
    FROM `{BQ_PBP_TABLE}`
    WHERE season >= 2015
      AND posteam = 'NE'
      AND play_type = 'run'
    """
    pbp_df = client.query(q_game).to_dataframe()
    
    # Mapping
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
    
    # Calculate Various Gravity Models
    results = []
    
    for _, row in coffee_df.iterrows():
        locations = row['dunkin'].get('locations', []) if row['dunkin'] else []
        if locations is None: locations = []
        
        # 1. Inverse Square (Physics)
        g_inv_sq = 0.0
        # 2. Exponential Decay (Retail/Demographics) - decay constant lambda ~ 0.5?
        g_exp = 0.0
        # 3. Gaussian/KDE (Statistics) - bandwidth sigma ~ 2 miles
        g_gauss = 0.0
        # 4. Simple Count (10 mi)
        count = len(locations)
        
        for loc in locations:
            d = loc.get('distance_miles', 100)
            
            # Inverse Square
            g_inv_sq += 1.0 / ((d + 0.1) ** 2)
            
            # Exponential (Decay by 50% every 2 miles? e^-0.35d)
            # Let's say lambda = 0.5
            g_exp += np.exp(-0.5 * d)
            
            # Gaussian (Sigma = 2.0 miles)
            g_gauss += np.exp(-(d**2) / (2 * (2.0**2)))
            
        results.append({
            'team_name': row['team_name'],
            'G_InvSq': g_inv_sq,
            'G_Exp': g_exp,
            'G_Gauss': g_gauss,
            'Count': count
        })
        
    gravity_df = pd.DataFrame(results)
    
    # Merge
    merged = pd.merge(pbp_df, gravity_df, left_on='mapped_home_team', right_on='team_name', how='inner')
    return merged

def check_robustness(df):
    # Aggregate to Game Level first to avoid play-count weighting bias
    game_agg = df.groupby(['game_id', 'G_InvSq', 'G_Exp', 'G_Gauss', 'Count'])['epa'].mean().reset_index()
    
    print("\n--- Robustness Check: Correlation with Rushing EPA (Game Level) ---")
    corr = game_agg[['epa', 'G_InvSq', 'G_Exp', 'G_Gauss', 'Count']].corr()['epa']
    print(corr)
    
    # Check "Munchkin Threshold" Performance across models
    # We'll split each metric at its median and check the Delta EPA
    print("\n--- Split Test (Top 50% vs Bottom 50%) ---")
    metrics = ['G_InvSq', 'G_Exp', 'G_Gauss', 'Count']
    for m in metrics:
        median = game_agg[m].median()
        high = game_agg[game_agg[m] >= median]['epa'].mean()
        low = game_agg[game_agg[m] < median]['epa'].mean()
        print(f"{m}: High={high:.3f}, Low={low:.3f}, Delta={high-low:.3f}")

if __name__ == "__main__":
    client = get_bq_client()
    if client:
        df = fetch_data(client)
        check_robustness(df)
