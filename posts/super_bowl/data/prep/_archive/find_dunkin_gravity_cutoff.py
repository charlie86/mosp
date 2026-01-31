import os
import pandas as pd
import numpy as np
from google.cloud import bigquery
from google.oauth2 import service_account

# --- Configuration ---
BQ_PROJECT = "gen-lang-client-0400686052"
BQ_COFFEE_TABLE = "stuperlatives.coffee_wars"
BQ_PBP_TABLE = "stuperlatives.pbp_data"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
GRAVITY_CONSTANT = 1.0 
EPSILON_MILES = 0.1 
POWER = 2 

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
            return bigquery.Client(credentials=credentials, project=BQ_PROJECT)
        else:
            return bigquery.Client(project=BQ_PROJECT)
    except Exception: return None

def calculate_gravity(client):
    query = f"SELECT team_name, stadium_name, dunkin, starbucks FROM `{BQ_COFFEE_TABLE}`"
    df = client.query(query).to_dataframe()
    results = []
    for _, row in df.iterrows():
        d_pull = sum([GRAVITY_CONSTANT / ((loc['distance_miles'] + EPSILON_MILES) ** POWER) for loc in row['dunkin']['locations']])
        s_pull = sum([GRAVITY_CONSTANT / ((loc['distance_miles'] + EPSILON_MILES) ** POWER) for loc in row['starbucks']['locations']])
        results.append({
            'team_name': row['team_name'], 
            'stadium_name': row['stadium_name'], 
            'dunkin_gravity': d_pull,
            'starbucks_gravity': s_pull,
            'net_gravity': d_pull - s_pull
        })
    return pd.DataFrame(results)

def fetch_ne_rushing_data(client):
    # Fetch NE Rushing plays 2015-Present
    query = f"""
    SELECT
        game_id, 
        home_team, 
        posteam, 
        epa, 
        rush_touchdown,
        success
    FROM `{BQ_PBP_TABLE}`
    WHERE season >= 2015 
      AND posteam = 'NE'
      AND play_type = 'run'
    """
    return client.query(query).to_dataframe()

def standardize_teams(pbp_df):
    pbp_to_coffee_map = {
        'NE': 'New England Patriots', 
        'ARI': 'Arizona Cardinals', 'ATL': 'Atlanta Falcons', 'BAL': 'Baltimore Ravens', 'BUF': 'Buffalo Bills',
        'CAR': 'Carolina Panthers', 'CHI': 'Chicago Bears', 'CIN': 'Cincinnati Bengals', 'CLE': 'Cleveland Browns',
        'DAL': 'Dallas Cowboys', 'DEN': 'Denver Broncos', 'DET': 'Detroit Lions', 'GB': 'Green Bay Packers',
        'HOU': 'Houston Texans', 'IND': 'Indianapolis Colts', 'JAX': 'Jacksonville Jaguars', 'KC': 'Kansas City Chiefs',
        'LAC': 'Los Angeles Chargers', 'SD': 'San Diego Chargers', 
        'LA': 'Los Angeles Rams', 'STL': 'St. Louis Rams',
        'LV': 'Las Vegas Raiders', 'OAK': 'Oakland Raiders',
        'MIA': 'Miami Dolphins', 'MIN': 'Minnesota Vikings', 'NO': 'New Orleans Saints',
        'NYG': 'New York Giants', 'NYJ': 'New York Jets', 'PHI': 'Philadelphia Eagles', 'PIT': 'Pittsburgh Steelers',
        'SF': 'San Francisco 49ers', 'SEA': 'Seattle Seahawks', 'TB': 'Tampa Bay Buccaneers', 'TEN': 'Tennessee Titans',
        'WAS': 'Washington Commanders'
    }
    
    def get_best_match(abbr): 
        return pbp_to_coffee_map.get(abbr, '')
        
    pbp_df['mapped_home_team'] = pbp_df['home_team'].apply(get_best_match)
    return pbp_df

def find_cutoff():
    client = get_bq_client()
    grav_df = calculate_gravity(client)
    # Average gravity per team 
    grav_team = grav_df.groupby('team_name')[['dunkin_gravity']].mean().reset_index()
    
    pbp_df = fetch_ne_rushing_data(client)
    pbp_df = standardize_teams(pbp_df)
    
    # Merge
    merged = pd.merge(pbp_df, grav_team, left_on='mapped_home_team', right_on='team_name', how='inner')
    
    # Analyze Thresholds
    thresholds = [0.5, 1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 12, 15, 20, 25, 30]
    
    results = []
    
    global_epa = merged['epa'].mean()
    print(f"Global NE Rushing EPA: {global_epa:.4f}")
    
    for t in thresholds:
        with_grav = merged[merged['dunkin_gravity'] >= t]
        without_grav = merged[merged['dunkin_gravity'] < t]
        
        if len(with_grav) < 100 or len(without_grav) < 100: continue # Min sample size of plays
        
        epa_with = with_grav['epa'].mean()
        epa_without = without_grav['epa'].mean()
        delta = epa_with - epa_without
        
        td_rate_with = with_grav['rush_touchdown'].mean()
        td_rate_without = without_grav['rush_touchdown'].mean()
        td_delta = td_rate_with - td_rate_without
        
        results.append({
            'Threshold': t,
            'Num_Plays_With': len(with_grav),
            'EPA_With': epa_with,
            'EPA_Without': epa_without,
            'EPA_Delta': delta,
            'TD_Rate_With': td_rate_with,
            'TD_Rate_Without': td_rate_without,
            'TD_Delta': td_delta
        })
        
    res_df = pd.DataFrame(results)
    res_df = res_df.sort_values(by='EPA_Delta', ascending=False)
    
    print("\n--- Dunkin Gravity Cutoff Analysis (Sorted by EPA Benefit) ---")
    print(res_df.to_string(index=False))
    
    best = res_df.iloc[0]
    best_t = best['Threshold']
    print(f"\nBest Threshold: >= {best_t} Gravity")
    print(f"EPA Delta: {best['EPA_Delta']:.4f} (With: {best['EPA_With']:.4f}, Without: {best['EPA_Without']:.4f})")
    
    print(f"\n--- Stadiums with Dunkin Gravity >= {best_t} ---")
    # Get unique stadiums meeting criteria
    qualifiers = grav_df[grav_df['dunkin_gravity'] >= best_t].sort_values(by='dunkin_gravity', ascending=False)
    print(qualifiers[['team_name', 'stadium_name', 'dunkin_gravity']].to_string(index=False))
    
if __name__ == "__main__":
    find_cutoff()
