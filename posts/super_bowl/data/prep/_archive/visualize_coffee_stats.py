import os
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from google.cloud import bigquery
from google.oauth2 import service_account

# --- Configuration ---
BQ_PROJECT = "mosp-449117"
BQ_COFFEE_TABLE = "stuperlatives.coffee_wars"
BQ_PBP_TABLE = "stuperlatives.pbp_data"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
OUTPUT_DIR = os.path.dirname(__file__)

# --- Helper Functions (Reused) ---
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
    print("Fetching joined data...")
    # Doing the join in SQL for efficiency this time
    query = f"""
    WITH coffee_stats AS (
        SELECT 
            team_name, 
            MAX(CASE WHEN chain = 'Starbucks' THEN count_10mi ELSE 0 END) as starbucks_count,
            MAX(CASE WHEN chain = 'Dunkin\\'' THEN count_10mi ELSE 0 END) as dunkin_count
        FROM `{BQ_COFFEE_TABLE}`
        GROUP BY 1
    )
    SELECT
        g.game_id,
        g.season,
        g.week,
        g.posteam,
        AVG(g.epa) as rush_epa,
        c.starbucks_count,
        c.dunkin_count
    FROM `{BQ_PBP_TABLE}` g
    LEFT JOIN coffee_stats c ON 
        -- Approximate matching logic used in python script, identifying key teams directly here
        (g.home_team = 'NE' AND c.team_name = 'New England Patriots') OR
        (g.home_team = 'SEA' AND c.team_name = 'Seattle Seahawks') OR
        (g.home_team = 'MIA' AND c.team_name = 'Miami Dolphins') OR
        (g.home_team = 'NYJ' AND c.team_name = 'New York Jets') OR
        (g.home_team = 'BUF' AND c.team_name = 'Buffalo Bills') OR
        -- Add generic join if possible or just fetch all and map in python?
        -- Let's stick to the Python logic for team mapping to be safe/consistent with previous analysis
        1=0
    WHERE 
        g.season >= 2015
        AND g.posteam = 'NE'
        AND g.play_type = 'run'
    GROUP BY 1, 2, 3, 4, 6, 7
    """
    # Actually, let's reuse the python mapping logic to be consistent and safe
    # SQL Joining on team names is messy without a bridge table.
    return None

def fetch_and_process_python(client):
    # 1. Coffee Data - Fetch nested locations for Gravity Calculation
    q_coffee = f"""
    SELECT 
        team_name, 
        dunkin,
        starbucks
    FROM `{BQ_COFFEE_TABLE}`
    """
    print("Fetching coffee location data...")
    coffee_df = client.query(q_coffee).to_dataframe()
    
    # Calculate Gravity
    GRAVITY_CONSTANT = 1.0
    EPSILON_MILES = 0.1
    POWER = 2
    
    gravity_data = []
    
    for _, row in coffee_df.iterrows():
        # Dunkin Pull
        d_pull = 0.0
        # dunkin column is a dictionary/struct
        locations = row['dunkin'].get('locations', []) if row['dunkin'] else []
        # If locations is None (null in BQ), handle it
        if locations is None:
            locations = []
            
        for loc in locations:
            dist = loc.get('distance_miles', 1000)
            g = GRAVITY_CONSTANT / ((dist + EPSILON_MILES) ** POWER)
            d_pull += g
            
        gravity_data.append({
            'team_name': row['team_name'],
            'dunkin_gravity': d_pull
        })
        
    gravity_df = pd.DataFrame(gravity_data)

    # 2. Game Data (NE Rushing only)
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
    print("Fetching PBP data...")
    pbp_df = client.query(q_game).to_dataframe()
    
    # 3. Join
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
    
    # Agg EPA per game first
    game_epa = pbp_df.groupby(['game_id', 'mapped_home_team'])['epa'].mean().reset_index()
    game_epa.rename(columns={'epa': 'rushing_epa'}, inplace=True)
    
    # Merge
    merged = pd.merge(game_epa, gravity_df, left_on='mapped_home_team', right_on='team_name', how='inner')
    return merged

def plot_ne_dunkin(df):
    plt.figure(figsize=(10, 6))
    
    # Set theme
    sns.set_theme(style="whitegrid")
    
    # Plot
    sns.regplot(
        data=df, 
        x='dunkin_gravity', 
        y='rushing_epa',
        scatter_kws={'alpha':0.6, 'color': '#002244'}, # Patriots Blue
        line_kws={'color': '#C60C30'} # Patriots Red
    )
    
    # Highlight the Munchkin Threshold
    plt.axvline(x=2.0, color='#ff6200', linestyle='--', linewidth=2, label="Munchkin Threshold (2.0)")
    
    plt.title("The Physics of Coffee: NE Rushing vs Dunkin' Gravity", fontsize=16, fontweight='bold', color='#002244')
    plt.xlabel("Dunkin' Gravity Impact (Inverse Square Law)", fontsize=12)
    plt.ylabel("Rushing EPA / Play", fontsize=12)
    
    plt.legend(loc='upper left')
    
    output_path = os.path.join(OUTPUT_DIR, "ne_runs_on_dunkin.png")
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Chart saved to {output_path}")

if __name__ == "__main__":
    client = get_bq_client()
    if client:
        df = fetch_and_process_python(client)
        print(f"Data points: {len(df)}")
        plot_ne_dunkin(df)

