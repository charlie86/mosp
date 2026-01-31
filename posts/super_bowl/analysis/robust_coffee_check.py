
import os
import sys
import pandas as pd
import numpy as np
from google.cloud import bigquery
from google.oauth2 import service_account

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

# --- Configuration ---
TARGET_SEASON = 2025
BQ_COFFEE_TABLE = "stuperlatives.coffee_wars"
BQ_PBP_TABLE = "stuperlatives.pbp_data"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))

def get_bq_client():
    """Get BigQuery client with service account credentials"""
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
    from math import radians, sin, cos, asin, sqrt
    lo1, la1, lo2, la2 = map(radians, [lo1, la1, lo2, la2])
    dlon = lo2 - lo1
    dlat = la2 - la1
    a = sin(dlat/2)**2 + cos(la1) * cos(la2) * sin(dlon/2)**2
    return 2 * asin(sqrt(a)) * 3956

def calculate_stadium_gravity_single(stadium_lat, stadium_lng, d_locs, s_locs):
    """
    Calculate net gravity at a stadium using the interference model
    Returns: (dunkin_gravity, starbucks_gravity, net_gravity)
    """
    INTERFERENCE_RADIUS = 0.5  # miles
    INTERFERENCE_STRENGTH = 1.0
    
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

def calculate_coffee_gravity(client):
    """
    Calculate Starbucks gravity for each stadium using the same model 
    Returns a DataFrame mapping home_team to net_gravity
    """
    print("Calculating Coffee Gravity for all stadiums...")
    
    # Stadium coordinates (current NFL stadiums)
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
    
    # Load coffee data from BigQuery
    query = f"""
    SELECT 
        stadium_name,
        team_name,
        dunkin,
        starbucks
    FROM `{BQ_COFFEE_TABLE}`
    """
    
    df = client.query(query).to_dataframe()
    
    # Calculate gravity for all current stadiums
    results = []
    for _, row in df.iterrows():
        stadium_name = row['stadium_name']
        team = row['team_name']
        
        # Only process current stadiums
        if stadium_name not in STADIUM_COORDS:
            continue
            
        stadium_lat, stadium_lng = STADIUM_COORDS[stadium_name]
        
        # Locations are in struct format from BigQuery
        d_locs = row['dunkin'].get('locations', []) if row['dunkin'] else []
        s_locs = row['starbucks'].get('locations', []) if row['starbucks'] else []
        
        # Convert to lists if needed
        if d_locs is None or (hasattr(d_locs, '__len__') and len(d_locs) == 0):
            d_locs = []
        if s_locs is None or (hasattr(s_locs, '__len__') and len(s_locs) == 0):
            s_locs = []
        
        d_grav, s_grav, net_grav = calculate_stadium_gravity_single(
            stadium_lat, stadium_lng, d_locs, s_locs
        )
        
        results.append({
            'stadium_name': stadium_name,
            'team_name': team,
            'dunkin_gravity': d_grav,
            'starbucks_gravity': s_grav,
            'net_gravity': net_grav,
        })
    
    gravity_df = pd.DataFrame(results)
    return gravity_df

def load_pbp_data(client, gravity_df):
    """Load PBP data and join with gravity"""
    print("Loading PBP Data...")
    
    query = f"""
    SELECT 
        season, week, game_id, 
        home_team, away_team, posteam, defteam,
        play_type, yards_gained, epa,
        pass_attempt, complete_pass, pass_touchdown, interception, sack,
        rush_attempt, rush_touchdown, fumble_lost,
        home_score, away_score,
        passer_player_name
    FROM `{BQ_PBP_TABLE}`
    WHERE season = {TARGET_SEASON}
    AND season_type IN ('REG', 'POST')
    AND play_type IN ('run', 'pass', 'no_play')
    """
    
    # Note: 'no_play' is often where sacks/penalties live in some cuts, 
    # but nflverse usually flags sacks in 'pass' or 'run' or with sack=1.
    # We include no_play to be safe if filtering for sacks explicitly from flags.
    # Actually, nflverse 'sack' column is 1 on sack plays which are usually play_type='pass' or 'sack' (older).
    # In 2024+ data, play_type is usually 'pass' for sacks.
    
    pbp_df = client.query(query).to_dataframe()
    
    # Map team names in gravity_df to abbr
    team_mapping = {
        'Arizona Cardinals': 'ARI', 'Atlanta Falcons': 'ATL', 'Baltimore Ravens': 'BAL',
        'Buffalo Bills': 'BUF', 'Carolina Panthers': 'CAR', 'Chicago Bears': 'CHI',
        'Cincinnati Bengals': 'CIN', 'Cleveland Browns': 'CLE', 'Dallas Cowboys': 'DAL',
        'Denver Broncos': 'DEN', 'Detroit Lions': 'DET', 'Green Bay Packers': 'GB',
        'Houston Texans': 'HOU', 'Indianapolis Colts': 'IND', 'Jacksonville Jaguars': 'JAX',
        'Kansas City Chiefs': 'KC', 'Los Angeles Chargers': 'LAC', 'San Diego Chargers': 'SD',
        'Los Angeles Rams': 'LA', 'St. Louis Rams': 'STL', 'Las Vegas Raiders': 'LV',
        'Oakland Raiders': 'OAK', 'Miami Dolphins': 'MIA', 'Minnesota Vikings': 'MIN',
        'New England Patriots': 'NE', 'New Orleans Saints': 'NO', 'New York Giants': 'NYG',
        'New York Jets': 'NYJ', 'Philadelphia Eagles': 'PHI', 'Pittsburgh Steelers': 'PIT',
        'San Francisco 49ers': 'SF', 'Seattle Seahawks': 'SEA', 'Tampa Bay Buccaneers': 'TB',
        'Tennessee Titans': 'TEN', 'Washington Commanders': 'WAS'
    }
    
    gravity_df['home_team_abbr'] = gravity_df['team_name'].map(team_mapping)
    
    # Join PBP with Gravity (on home_team)
    # Using left join to keep games even if stadium mapping fails (though it shouldn't for modern)
    merged = pd.merge(pbp_df, gravity_df, left_on='home_team', right_on='home_team_abbr', how='left')
    
    return merged

def calculate_metrics(df, team, is_offense=True, filter_desc=""):
    """
    Calculate the requested metrics for a subset of data.
    """
    metrics = {}
    
    # Filter for the specific team
    if is_offense:
        team_df = df[df['posteam'] == team].copy()
    else:
        team_df = df[df['defteam'] == team].copy()
        
    if len(team_df) == 0:
        return {k: 0 for k in ['Games', 'Comp %', 'YPA', 'TD/INT', 'Rating', 'Sack Rate', 'PPG', 'YPG', 'YPP', 'Rush EPA', 'Turnovers']}
    
    games = team_df['game_id'].nunique()
    metrics['Games'] = games
    
    if is_offense:
        # --- QB/Passing Metrics ---
        # Completion %
        attempts = team_df['pass_attempt'].sum()
        completions = team_df['complete_pass'].sum()
        metrics['Comp %'] = (completions / attempts * 100) if attempts > 0 else 0.0
        
        # YPA
        pass_yards = team_df[team_df['play_type'] == 'pass']['yards_gained'].sum() # Simple filter
        # Better: use 'pass_attempt' == 1 rows for YPA denominator? Or all pass plays? 
        # Usually YPA is Total Passing Yards / Attempts.
        # pass_yards should separate sack yards? 
        # In nflverse, yards_gained on a sack is negative.
        # Passing yards usually excludes sacks.
        # Let's use clean passing yards: play_type='pass' and sack=0
        pass_plays = team_df[(team_df['play_type'] == 'pass') & (team_df['sack'] == 0)]
        clean_pass_yards = pass_plays['yards_gained'].sum()
        metrics['YPA'] = (clean_pass_yards / attempts) if attempts > 0 else 0.0
        
        # TD/INT Ratio
        tds = team_df['pass_touchdown'].sum()
        ints = team_df['interception'].sum()
        metrics['TD/INT'] = (tds / ints) if ints > 0 else float(tds) # Or Inf
        
        # Rating (Formula: https://en.wikipedia.org/wiki/Passer_rating)
        if attempts > 0:
            a = (completions / attempts - 0.3) * 5
            b = (clean_pass_yards / attempts - 3) * 0.25
            c = (tds / attempts) * 20
            d = 2.375 - (ints / attempts * 25)
            rating = (max(0, min(2.375, a)) + max(0, min(2.375, b)) + max(0, min(2.375, c)) + max(0, min(2.375, d))) / 6 * 100
            metrics['Rating'] = rating
        else:
            metrics['Rating'] = 0.0
            
        # Sack Rate
        # Sacks / Dropbacks (Attempts + Sacks)
        sacks = team_df['sack'].sum()
        dropbacks = attempts + sacks
        metrics['Sack Rate'] = (sacks / dropbacks * 100) if dropbacks > 0 else 0.0
        
        # --- Offense Totals ---
        # PPG
        # Need to find final score per game.
        # We can take the max score for the team in each game_id
        game_scores = []
        for gid in team_df['game_id'].unique():
            g = team_df[team_df['game_id'] == gid].iloc[0]
            if g['home_team'] == team:
                game_scores.append(g['home_score'])
            else:
                game_scores.append(g['away_score'])
        metrics['PPG'] = np.mean(game_scores) if game_scores else 0.0
        
        # YPG
        total_yards = team_df['yards_gained'].sum()
        metrics['YPG'] = (total_yards / games) if games > 0 else 0.0
        
        # YPP
        # Plays = count of rows where play_type in run or pass?
        # Roughly count of plays
        plays = len(team_df[team_df['play_type'].isin(['run', 'pass'])])
        metrics['YPP'] = (total_yards / plays) if plays > 0 else 0.0
        
        # Rush EPA
        rush_plays = team_df[team_df['play_type'] == 'run']
        rush_epa = rush_plays['epa'].mean()
        metrics['Rush EPA'] = rush_epa if not np.isnan(rush_epa) else 0.0
        
    else:
        # --- Defense Metrics ---
        # PPG Allowed
        game_scores_allowed = []
        for gid in team_df['game_id'].unique():
            g = team_df[team_df['game_id'] == gid].iloc[0]
            if g['home_team'] == team:
                game_scores_allowed.append(g['away_score']) # Allowed = opponent score
            else:
                game_scores_allowed.append(g['home_score'])
        metrics['PPG Allowed'] = np.mean(game_scores_allowed) if game_scores_allowed else 0.0
        
        # Opposing WR Rating (Approx as Opposing QB Rating)
        # Using same logic as offense but for the opponent (posteam)
        opp_attempts = team_df['pass_attempt'].sum()
        opp_completions = team_df['complete_pass'].sum()
        
        # Opposing Pass Yards
        opp_pass_plays = team_df[(team_df['play_type'] == 'pass') & (team_df['sack'] == 0)]
        opp_pass_yards = opp_pass_plays['yards_gained'].sum()
        
        opp_tds = team_df['pass_touchdown'].sum()
        opp_ints = team_df['interception'].sum()
        
        if opp_attempts > 0:
            a = (opp_completions / opp_attempts - 0.3) * 5
            b = (opp_pass_yards / opp_attempts - 3) * 0.25
            c = (opp_tds / opp_attempts) * 20
            d = 2.375 - (opp_ints / opp_attempts * 25)
            rating = (max(0, min(2.375, a)) + max(0, min(2.375, b)) + max(0, min(2.375, c)) + max(0, min(2.375, d))) / 6 * 100
            metrics['Opp Passer Rating'] = rating
        else:
            metrics['Opp Passer Rating'] = 0.0
        
        # Sack Rate (generated by defense)
        my_sacks = team_df['sack'].sum()
        opp_dropbacks = opp_attempts + my_sacks
        metrics['Sack Rate (Def)'] = (my_sacks / opp_dropbacks * 100) if opp_dropbacks > 0 else 0.0
        
        # YPC for Opposing RB
        # Filter for runs by RBs? or just all runs?
        # Notes said "ypc for opposing RB".
        # We'll approximate with all runs.
        rush_plays = team_df[team_df['play_type'] == 'run']
        rush_yards_allowed = rush_plays['yards_gained'].sum()
        rush_attempts_against = team_df['rush_attempt'].sum()
        metrics['Opp YPC'] = (rush_yards_allowed / rush_attempts_against) if rush_attempts_against > 0 else 0.0

        # Turnovers (Defense)
        # int + fumble_lost
        ints = team_df['interception'].sum()
        fumbles = team_df['fumble_lost'].sum()
        total_turnovers = ints + fumbles
        metrics['Turnovers'] = total_turnovers
        metrics['Turnovers/Game'] = (total_turnovers / games) if games > 0 else 0.0

    return metrics

def main():
    client = get_bq_client()
    if not client: return

    # 1. Get Coffee Gravity
    gravity_df = calculate_coffee_gravity(client)
    
    # 2. Get PBP Data merged with Gravity
    df = load_pbp_data(client, gravity_df)
    
    # 3. Create subsets
    # We want "Away Games Only" logic for the analysis
    
    # ----------------------------------------------------
    # PATRIOTS (Dunkin Analysis)
    # ----------------------------------------------------
    print("\n--- PATRIOTS (Runs on Dunkin) ---")
    ne_away = df[(df['posteam'] == 'NE') & (df['home_team'] != 'NE')]
    
    # Define "Dunkin Zone" vs "Starbucks Zone" (or Non-Dunkin)
    # Using net_gravity > 0 as Dunkin Zone
    ne_dunkin = ne_away[ne_away['net_gravity'] > 0]
    ne_starbucks = ne_away[ne_away['net_gravity'] <= 0]
    
    # Maye only
    maye_dunkin = ne_dunkin[ne_dunkin['passer_player_name'] == 'D.Maye']
    maye_starbucks = ne_starbucks[ne_starbucks['passer_player_name'] == 'D.Maye']
    
    ne_metrics = {
        'Drake Maye (Away - Dunkin Zone)': calculate_metrics(maye_dunkin, 'NE', True),
        'Drake Maye (Away - Starbucks Zone)': calculate_metrics(maye_starbucks, 'NE', True),
        'Offense (Away - Dunkin Zone)': calculate_metrics(ne_dunkin, 'NE', True),
        'Offense (Away - Starbucks Zone)': calculate_metrics(ne_starbucks, 'NE', True),
    }

    # ----------------------------------------------------
    # SEAHAWKS (Starbucks Analysis)
    # ----------------------------------------------------
    print("\n--- SEAHAWKS (Chaos on Starbucks) ---")
    sea_away_def = df[(df['defteam'] == 'SEA') & (df['home_team'] != 'SEA')]
    
    # Define "Starbucks Zone" vs "Dunkin Zone"
    # Using net_gravity < 0 as Starbucks Zone
    # Maybe use the "Death Zone" (< -4.5) for sharper contrast?
    # Notes verify: "look at seahawks_starbucks_summary for details on the current state. what i want to do is look at the metrics i outlined in the notes file... i also want to try looking at this for away games only"
    
    sea_sb = sea_away_def[sea_away_def['net_gravity'] < 0]
    sea_non_sb = sea_away_def[sea_away_def['net_gravity'] >= 0]
    
    # Also check "Death Zone" specifically if data allows
    sea_death = sea_away_def[sea_away_def['net_gravity'] <= -4]
    
    # Offense check specifically for Sam Darnold?
    # Notes said: "Sam Darnold --- (blank)"
    # Let's check Sam Darnold stats if he played for SEA?
    # Darnold is on MIN Vikings usually. Did user mean Darnold vs SEA? Or Darnold on SEA?
    # Wait, SEA QB is Geno Smith usually.
    # Ah, in 2025 maybe Darnold is on SEA? Or maybe they mean "Sam Darnold" section separate?
    # "Sam Darnold" was a separate header in notes.
    # I will check if Darnold has stats in 2025 and for which team.
    # If he's on SEA, I'll run him. If he's on MIN, I'll run him.
    # I'll check his team from the data.
    
    sea_metrics = {
        'Defense (Away - Starbucks Zone)': calculate_metrics(sea_sb, 'SEA', False),
        'Defense (Away - Death Zone < -4)': calculate_metrics(sea_death, 'SEA', False),
        'Defense (Away - Dunkin Zone)': calculate_metrics(sea_non_sb, 'SEA', False),
    }
    
    # Sam Darnold Check
    sea_passers = sea_away_def['passer_player_name'].unique()
    print(f"SEA Passers found: {sea_passers}")
    
    darnold_df = df[df['passer_player_name'] == 'S.Darnold']
    if len(darnold_df) > 0:
        darnold_team = darnold_df.iloc[0]['posteam']
        print(f"Sam Darnold found on: {darnold_team}")
        
        # Analyze Darnold based on HIS team's away games
        sd_away = darnold_df[darnold_df['home_team'] != darnold_team]
        sd_sb = sd_away[sd_away['net_gravity'] < 0]
        sd_dunkin = sd_away[sd_away['net_gravity'] > 0]
        
        sea_metrics[f'Sam Darnold ({darnold_team}) Away - Starbucks'] = calculate_metrics(sd_sb, darnold_team, True)
        sea_metrics[f'Sam Darnold ({darnold_team}) Away - Dunkin'] = calculate_metrics(sd_dunkin, darnold_team, True)
        # sd_rate_sb = get_game_metric(sd_sb, darnold_team, 'passer_rating')
        # sd_rate_dunkin = get_game_metric(sd_dunkin, darnold_team, 'passer_rating')
        # print_significance(f"Sam Darnold ({darnold_team}) Rating", sd_rate_dunkin, sd_rate_sb, 'ttest', 'Rating')

    # --- WIN-LOSS RECORD CHECK ---
    print("\n\n--- WIN-LOSS RECORD CHECK ---")
    
    def get_record(df, team):
        wins = 0
        losses = 0
        ties = 0
        for gid in df['game_id'].unique():
            g = df[df['game_id'] == gid].iloc[0]
            if g['home_team'] == team:
                score = g['home_score']
                opp_score = g['away_score']
            else:
                score = g['away_score']
                opp_score = g['home_score']
            
            if score > opp_score: wins += 1
            elif score < opp_score: losses += 1
            else: ties += 1
        return f"{wins}-{losses}-{ties}"

    # Patriots
    ne_rec_dunkin = get_record(ne_dunkin, 'NE')
    ne_rec_sb = get_record(ne_starbucks, 'NE')
    print(f"Patriots (Away): Dunkin Zone (>0): {ne_rec_dunkin}, Starbucks Zone (<=0): {ne_rec_sb}")
    
    # Seahawks
    sea_rec_sb = get_record(sea_sb, 'SEA')
    sea_rec_dunkin = get_record(sea_non_sb, 'SEA') 
    print(f"Seahawks (Away): Starbucks Zone (<0): {sea_rec_sb}, Dunkin Zone (>=0): {sea_rec_dunkin}")

    # Output Report
    output_path = os.path.join(os.path.dirname(__file__), '../docs/robust_coffee_metrics.md')
    with open(output_path, 'w') as f:
        f.write("# Robust Coffee Metrics (Away Games Only)\n\n")
        
        f.write("## Patriots @ Dunkin vs Starbucks Zones (Away Only)\n")
        f.write("| Metric | Drake Maye (Dunkin) | Drake Maye (Starbucks) | Offense (Dunkin) | Offense (Starbucks) |\n")
        f.write("|---|---|---|---|---|\n")
        
        row_keys = ['Games', 'Comp %', 'YPA', 'TD/INT', 'Rating', 'Sack Rate', 'PPG', 'YPG', 'YPP', 'Rush EPA']
        
        for k in row_keys:
            v1 = ne_metrics['Drake Maye (Away - Dunkin Zone)'].get(k, 0)
            v2 = ne_metrics['Drake Maye (Away - Starbucks Zone)'].get(k, 0)
            v3 = ne_metrics['Offense (Away - Dunkin Zone)'].get(k, 0)
            v4 = ne_metrics['Offense (Away - Starbucks Zone)'].get(k, 0)
            
            # Format
            if k == 'Games': fstr = "{:.0f}"
            elif k in ['Comp %', 'Sack Rate']: fstr = "{:.1f}%"
            elif k in ['YPA', 'YPP']: fstr = "{:.2f}"
            elif k == 'Rating': fstr = "{:.1f}"
            elif k == 'TD/INT': fstr = "{:.2f}"
            elif k == 'Rush EPA': fstr = "{:.3f}"
            else: fstr = "{:.1f}"
             
            f.write(f"| {k} | {fstr.format(v1)} | {fstr.format(v2)} | {fstr.format(v3)} | {fstr.format(v4)} |\n")
        
        f.write("\n\n")
        
        f.write("## Seahawks Defense @ Starbucks vs Dunkin Zones (Away Only)\n")
        f.write("| Metric | Starbucks Zone (<0) | Death Zone (<-4) | Dunkin Zone (>0) |\n")
        f.write("|---|---|---|---|\n")
        
        def_keys = ['Games', 'PPG Allowed', 'Opp Passer Rating', 'Sack Rate (Def)', 'Opp YPC', 'Turnovers', 'Turnovers/Game']
        
        for k in def_keys:
            v1 = sea_metrics['Defense (Away - Starbucks Zone)'].get(k, 0)
            v2 = sea_metrics['Defense (Away - Death Zone < -4)'].get(k, 0)
            v3 = sea_metrics['Defense (Away - Dunkin Zone)'].get(k, 0)
            
            if k == 'Games': fstr = "{:.0f}"
            elif k in ['Sack Rate (Def)']: fstr = "{:.1f}%"
            elif k in ['Opp Passer Rating']: fstr = "{:.1f}"
            elif k in ['Opp YPC', 'Turnovers/Game']: fstr = "{:.2f}"
            elif k == 'Turnovers': fstr = "{:.0f}"
            else: fstr = "{:.1f}"
            
            f.write(f"| {k} | {fstr.format(v1)} | {fstr.format(v2)} | {fstr.format(v3)} |\n")
            
        f.write("\n\n")
        
        # Darnold Section
        if any('Sam Darnold' in k for k in sea_metrics):
             f.write("## Sam Darnold Checks (Away Only)\n")
             f.write("| Metric | Starbucks Zone | Dunkin Zone |\n")
             f.write("|---|---|---|\n")
             
             # Extract the keys dynamically
             keys = [k for k in sea_metrics.keys() if 'Sam Darnold' in k]
             sb_key = next((k for k in keys if 'Starbucks' in k), None)
             dd_key = next((k for k in keys if 'Dunkin' in k), None)
             
             for k in row_keys:
                 v1 = sea_metrics[sb_key].get(k, 0) if sb_key else 0
                 v2 = sea_metrics[dd_key].get(k, 0) if dd_key else 0
                 
                 if k == 'Games': fstr = "{:.0f}"
                 elif k in ['Comp %', 'Sack Rate']: fstr = "{:.1f}%"
                 elif k in ['YPA', 'YPP']: fstr = "{:.2f}"
                 elif k == 'Rating': fstr = "{:.1f}"
                 elif k == 'TD/INT': fstr = "{:.2f}"
                 else: fstr = "{:.1f}"
                 
                 f.write(f"| {k} | {fstr.format(v1)} | {fstr.format(v2)} |\n")
    # Output SQL Values for Gravity CTE
    print("\n--- SQL VALUES FOR GRAVITY CTE ---")
    print("VALUES")
    for _, row in gravity_df.iterrows():
        print(f"  ('{row['stadium_name']}', '{row['team_name']}', {row['net_gravity']:.4f}),")
    print("  ('END', 'END', 0.0);")

    # Output SQL Values for Gravity CTE
    print("\n--- SQL VALUES FOR GRAVITY CTE ---")
    print("VALUES")
    for _, row in gravity_df.iterrows():
        print(f"  ('{row['stadium_name']}', '{row['team_name']}', {row['net_gravity']:.4f}),")
    print("  ('END', 'END', 0.0);")

if __name__ == "__main__":
    main()
