import os
import difflib
import pandas as pd
import numpy as np
from google.cloud import bigquery
from google.oauth2 import service_account

# --- Configuration ---
BQ_PROJECT = "gen-lang-client-0400686052" # Inferred from context or we can let client helper find it
BQ_COFFEE_TABLE = "stuperlatives.coffee_wars"
BQ_PBP_TABLE = "stuperlatives.pbp_data"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))

# --- Helper Functions ---

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

def fetch_coffee_data(client):
    print("Fetching coffee data...")
    # Pivot logic in SQL or Pandas. SQL is cleaner.
    query = f"""
    SELECT 
        team_name, 
        dunkin.count_10mi as dunkin_count,
        starbucks.count_10mi as starbucks_count,
        dunkin.closest_miles as dunkin_dist,
        starbucks.closest_miles as starbucks_dist
    FROM `{BQ_COFFEE_TABLE}`
    """
    df = client.query(query).to_dataframe()
    # Metrics:
    # 1. Net Starbucks (Starbucks - Dunkin) -> Higher means more Starbucks dominance
    # 2. Dunkin Share (Dunkin / Total) -> Higher means more Dunkin dominance
    df['net_starbucks'] = df['starbucks_count'] - df['dunkin_count']
    df['total_coffee'] = df['starbucks_count'] + df['dunkin_count']
    df['dunkin_share'] = df.apply(lambda x: x['dunkin_count'] / x['total_coffee'] if x['total_coffee'] > 0 else 0, axis=1)
    df['starbucks_share'] = df.apply(lambda x: x['starbucks_count'] / x['total_coffee'] if x['total_coffee'] > 0 else 0, axis=1)
    return df

def fetch_game_data(client):
    print("Fetching game data (2015-Present)...") # 10 years roughly
    # We focus on NE and SEA games
    # We need to know who the HOME team is to link to coffee territory
    query = f"""
    SELECT
        game_id,
        season,
        week,
        home_team,
        away_team,
        posteam,
        defteam,
        play_type,
        epa,
        success,
        down,
        penalty,
        penalty_type,
        incomplete_pass,
        sack,
        interception,
        fumble,
        pass_touchdown,
        rush_touchdown,
        home_score,
        away_score,
        CASE WHEN home_score > away_score THEN home_team 
             WHEN away_score > home_score THEN away_team 
             ELSE 'TIE' END as winner
    FROM `{BQ_PBP_TABLE}`
    WHERE season >= 2015
      AND (home_team IN ('NE', 'SEA') OR away_team IN ('NE', 'SEA'))
    """
    return client.query(query).to_dataframe()

def standardize_teams(coffee_df, pbp_df):
    """
    Map full team names from Coffee df to Abbr in PBP df.
    """
    # Manual Mapping based on standard NFL abbreviations
    # Manual Mapping based on standard NFL abbreviations
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
    def get_best_match(abbr): return pbp_to_coffee_map.get(abbr, '')
    pbp_df['mapped_home_team'] = pbp_df['home_team'].apply(get_best_match)
    return pbp_df

def calculate_game_metrics(game_plays, team):
    """
    Generate a WIDE variety of metrics to fish for correlations.
    """
    # Filter for when 'team' is on Offense (posteam) or Defense (defteam)
    # For simplicity, let's focus on OFFENSIVE performance and WINNING.
    off_plays = game_plays[game_plays['posteam'] == team]
    if off_plays.empty: return None

    # 1. Outcome
    row = game_plays.iloc[0]
    is_win = 1 if row['winner'] == team else 0
    score = row['home_score'] if row['home_team'] == team else row['away_score']
    
    # 2. General Offense
    epa_overall = off_plays['epa'].mean()
    success_rate = off_plays['success'].mean()
    
    # 3. Passing specific
    pass_plays = off_plays[off_plays['play_type'] == 'pass']
    epa_pass = pass_plays['epa'].mean() if len(pass_plays) > 0 else 0
    completion_rate = pass_plays['success'].mean() if len(pass_plays) > 0 else 0 # Rough proxy
    sacks_allowed = pass_plays['sack'].sum()
    
    # 4. Rushing specific
    rush_plays = off_plays[off_plays['play_type'] == 'run']
    epa_rush = rush_plays['epa'].mean() if len(rush_plays) > 0 else 0
    rush_success = rush_plays['success'].mean() if len(rush_plays) > 0 else 0

    return {
        'Win': is_win,
        'Points': score,
        'EPA_Total': epa_overall,
        'Success_Total': success_rate,
        'EPA_Pass': epa_pass,
        'EPA_Rush': epa_rush,
        'Sacks_Allowed': sacks_allowed,
        'Pass_Touchdowns': off_plays['pass_touchdown'].sum(),
        'Rush_Touchdowns': off_plays['rush_touchdown'].sum()
    }

def analyze_correlation():
    client = get_bq_client()
    if not client: return

    coffee_df = fetch_coffee_data(client)
    pbp_df = fetch_game_data(client)
    pbp_df = standardize_teams(coffee_df, pbp_df)
    
    # Config: Coffee Vars to check
    # We want: 
    #   SEA -> Positive Corr with 'net_starbucks' or 'starbucks_share'
    #   NE  -> Positive Corr with 'dunkin_share' (or Negative with 'net_starbucks')
    coffee_vars = ['net_starbucks', 'starbucks_share', 'dunkin_share', 'starbucks_dist', 'dunkin_dist']
    
    # Agg Coffee by Team
    coffee_agg = coffee_df.groupby('team_name')[coffee_vars].mean().reset_index()
    
    # Link to Game by Home Team
    merged = pd.merge(pbp_df, coffee_agg, left_on='mapped_home_team', right_on='team_name', how='inner')
    
    FOCUS_TEAMS = ['NE', 'SEA']
    
    findings = []

    print("\n--- Narrative Mining ---")
    
    for team in FOCUS_TEAMS:
        # Get one row per game with metrics
        team_games_df = merged[(merged['posteam'] == team) | (merged['defteam'] == team)]
        
        game_rows = []
        for g_id, g_df in team_games_df.groupby('game_id'):
            env_row = g_df.iloc[0]
            coffee_metrics = {k: env_row[k] for k in coffee_vars}
            perf = calculate_game_metrics(g_df, team)
            if perf:
                game_rows.append({**coffee_metrics, **perf})
        
        gm_df = pd.DataFrame(game_rows)
        
        # Calculate Correlations
        perf_cols = ['Win', 'Points', 'EPA_Total', 'Success_Total', 'EPA_Pass', 'EPA_Rush', 'Sacks_Allowed', 'Pass_Touchdowns', 'Rush_Touchdowns']
        corr_matrix = gm_df[coffee_vars + perf_cols].corr(method='pearson')
        
        # Search for desired correlations
        # We define "Supporting Narrative" as:
        # For SEA: Positive corr with Starbucks metrics (Share, Net) OR Negative corr with Starbucks Dist (Closer is better)
        # For NE: Positive corr with Dunkin metrics (Share) OR Negative with Dunkin Dist OR Negative with Net Starbucks
        
        all_coffee_metrics = coffee_vars
        
        for p_col in perf_cols:
            for c_col in all_coffee_metrics:
                r = corr_matrix.loc[c_col, p_col]
                if pd.isna(r): continue
                
                # SEA Logic
                if team == 'SEA':
                    # Starbucks Good?
                    is_starbucks_metric = 'starbucks' in c_col and 'dunkin' not in c_col and 'net' not in c_col
                    is_net_starbucks = 'net_starbucks' in c_col
                    
                    if is_starbucks_metric or is_net_starbucks:
                        # If Count/Share/Net -> Want Positive Correlation (More Sbucks = Good)
                        # Unless metric is 'Sacks' -> Want Negative
                        if 'dist' not in c_col:
                            if p_col == 'Sacks_Allowed':
                                if r < -0.01: # Lower threshold to find *something*
                                    findings.append({'Team': 'SEA', 'Coffee_Var': c_col, 'Metric': p_col, 'Corr': r, 'Narrative': f"More Starbucks ({c_col}) = Fewer Sacks"})
                            else:
                                if r > 0.01:
                                    findings.append({'Team': 'SEA', 'Coffee_Var': c_col, 'Metric': p_col, 'Corr': r, 'Narrative': f"More Starbucks ({c_col}) = Higher {p_col}"})
                        else:
                            # If Distance -> Want Negative Correlation (Closer Sbucks = Good)
                            # Unless metric is 'Sacks' -> Want Positive (Closer Sbucks = Less Sacks... wait. Closer = Low Dist. Low Dist -> Low Sacks = Positive Corr. Wait.
                            # Low Dist (0) -> Low Sacks (0). High Dist (100) -> High Sacks (5). Moves together. Positive Corr.
                            # So: Closer Sbucks (Good) should mean Better Perf.
                            # Better Perf (Win, EPA) is High. Low Dist -> High EPA. Negative Corr.
                            # Better Perf (Sacks) is Low. Low Dist -> Low Sacks. Positive Corr.
                            if p_col == 'Sacks_Allowed':
                                if r > 0.01:
                                    findings.append({'Team': 'SEA', 'Coffee_Var': c_col, 'Metric': p_col, 'Corr': r, 'Narrative': f"Closer Starbucks ({c_col}) = Fewer Sacks"})
                            else:
                                if r < -0.01:
                                    findings.append({'Team': 'SEA', 'Coffee_Var': c_col, 'Metric': p_col, 'Corr': r, 'Narrative': f"Closer Starbucks ({c_col}) = Higher {p_col}"})

                # NE Logic
                if team == 'NE':
                    # Dunkin Good?
                    is_dunkin_metric = 'dunkin' in c_col and 'starbucks' not in c_col
                    
                    if is_dunkin_metric:
                        if 'dist' not in c_col:
                            # Share/Count. Want Positive.
                            if p_col == 'Sacks_Allowed':
                                if r < -0.01:
                                    findings.append({'Team': 'NE', 'Coffee_Var': c_col, 'Metric': p_col, 'Corr': r, 'Narrative': f"More Dunkin ({c_col}) = Fewer Sacks"})
                            else:
                                if r > 0.01:
                                    findings.append({'Team': 'NE', 'Coffee_Var': c_col, 'Metric': p_col, 'Corr': r, 'Narrative': f"More Dunkin ({c_col}) = Higher {p_col}"})

    # Output Findings
    print(f"Found {len(findings)} potential narrative stats.")
    
    findings.sort(key=lambda x: abs(x['Corr']), reverse=True)
    
    report_path = os.path.join(os.path.dirname(__file__), "coffee_narrative_findings.md")
    with open(report_path, "w") as f:
        f.write("# Coffee Narrative Findings\n\n")
        f.write("Stats strictly selected to back the hypothesis: NE loves Dunkin, SEA loves Starbucks.\n\n")
        f.write("| Team | Coffee Metric | Perf Metric | Correlation | Narrative |\n")
        f.write("| :--- | :--- | :--- | :--- | :--- |\n")
        for res in findings:
            f.write(f"| {res['Team']} | {res['Coffee_Var']} | {res['Metric']} | {res['Corr']:.3f} | {res['Narrative']} |\n")
            
    print(f"Report saved to {report_path}")

if __name__ == "__main__":
    analyze_correlation()
