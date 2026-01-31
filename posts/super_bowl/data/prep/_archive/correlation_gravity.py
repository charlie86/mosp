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
            'stadium_name': row['stadium_name'], # Note: we just need team mapping mostly
            'net_gravity': d_pull - s_pull, # Positive = Dunkin, Negative = Starbucks
            'dunkin_gravity': d_pull,
            'starbucks_gravity': s_pull
        })
    return pd.DataFrame(results)

def fetch_game_data(client):
    # Same as coffee_correlation.py but maybe simpler aggregation
    query = f"""
    SELECT
        game_id, home_team, posteam, dp.epa, dp.success, dp.pass_touchdown, dp.rush_touchdown, dp.sack, dp.home_score, dp.away_score
    FROM `{BQ_PBP_TABLE}` as dp
    WHERE season >= 2015 AND (home_team IN ('NE', 'SEA') OR away_team IN ('NE', 'SEA'))
    """
    return client.query(query).to_dataframe()

def standardize_teams(pbp_df):
    pbp_to_coffee_map = {
        'NE': 'New England Patriots', 'SEA': 'Seattle Seahawks'
        # ... others if needed but we focus on these 2
    }
    def get_best_match(abbr): # Simplified map just for focus teams to avoid import issues
        for k, v in pbp_to_coffee_map.items():
            if abbr == k: return v
        return ''
    pbp_df['mapped_home_team'] = pbp_df['home_team'].apply(get_best_match)
    return pbp_df

def analyze_gravity_correlation():
    client = get_bq_client()
    grav_df = calculate_gravity(client)
    # Average gravity per team (in case they moved stadiums, though usually consistent)
    grav_team = grav_df.groupby('team_name')[['net_gravity', 'dunkin_gravity', 'starbucks_gravity']].mean().reset_index()
    
    pbp_df = fetch_game_data(client)
    pbp_df = standardize_teams(pbp_df)
    
    # Merge
    merged = pd.merge(pbp_df, grav_team, left_on='mapped_home_team', right_on='team_name', how='inner')
    
    # Analyze NE and SEA separately
    for team_abbr in ['NE', 'SEA']:
        team_games = merged[(merged['posteam'] == team_abbr)] # Offense only
        
        # Agg per game
        game_stats = team_games.groupby('game_id').agg({
            'epa': 'mean',
            'pass_touchdown': 'sum',
            'rush_touchdown': 'sum',
            'sack': 'sum',
            'net_gravity': 'first',
            'dunkin_gravity': 'first',
            'starbucks_gravity': 'first'
        }).reset_index()
        
        # Correlations
        print(f"\n--- {team_abbr} Analysis ---")
        corr = game_stats[['net_gravity', 'dunkin_gravity', 'starbucks_gravity', 'epa', 'pass_touchdown', 'rush_touchdown', 'sack']].corr()
        print(corr[['net_gravity', 'dunkin_gravity', 'starbucks_gravity']].loc[['epa', 'pass_touchdown', 'rush_touchdown', 'sack']])
        
        # Determine Narrative Fit
        # NE: Want Positive Corr with Net/Dunkin Gravity for EPA/TDs. Negative for Sacks.
        # SEA: Want Negative Corr with Net Gravity (since Starbucks is negative) for EPA/TDs? 
        #      Or Positive with Starbucks Gravity (magnitude).
        
if __name__ == "__main__":
    analyze_gravity_correlation()
