"""
Patriots Dunkin Gravity Optimizer

Finds positive stats showing the Patriots perform better when Dunkin gravity is higher (Net Gravity > 0).
Uses the same approach as seahawks_starbucks_optimizer.py but flipped for NE and Dunkin.
"""

import os
import sys
import itertools
import pandas as pd
import numpy as np
import duckdb
import multiprocessing
from tqdm import tqdm
from google.cloud import bigquery
from google.oauth2 import service_account

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

# --- Configuration ---
TARGET_SEASONS = [2015, 2016, 2017, 2018, 2019, 2020, 2021, 2022, 2023, 2024, 2025]
BQ_PROJECT = "gen-lang-client-0400686052"
BQ_COFFEE_TABLE = "stuperlatives.coffee_wars"
BQ_PBP_TABLE = "stuperlatives.pbp_data"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))

# Defense Tables (using 2025 as template)
DEFENSE_SUMMARY = "pff_defense_summary_2025"
DEFENSE_COVERAGE = "pff_defense_coverage_2025"
DEFENSE_RUSH = "pff_defense_pass_rush_2025"

# Metrics are generic enough to reuse
DEFENSE_METRICS = {
    # Summary Grades
    'Median Defense Grade': ('MEDIAN(grades_defense)', 'DESC', 'COUNT(*)', 1),
    'Median Coverage Grade': ('MEDIAN(grades_coverage_defense)', 'DESC', 'COUNT(*)', 1),
    'Median Pass Rush Grade': ('MEDIAN(grades_pass_rush_defense)', 'DESC', 'COUNT(*)', 1),
    
    # Production
    'Interceptions': ('SUM(interceptions)', 'DESC', 'COUNT(*)', 1),
    'Total Pressures': ('SUM(total_pressures)', 'DESC', 'COUNT(*)', 1),
    'Sacks': ('SUM(sacks)', 'DESC', 'COUNT(*)', 1),
    'Stops': ('SUM(stops)', 'DESC', 'COUNT(*)', 1),
    'Pass Break Ups': ('SUM(pass_break_ups)', 'DESC', 'COUNT(*)', 1),
    
    # Efficiency
    'Median Forced Inc Rate': ('MEDIAN(forced_incompletion_rate)', 'DESC', 'COUNT(*)', 1),
    'Median Yds Per Cov Snap': ('MEDIAN(yards_per_coverage_snap)', 'ASC', 'COUNT(*)', 1),
    'Median PRP': ('MEDIAN(prp)', 'DESC', 'COUNT(*)', 1),
    'Median Win Rate': ('MEDIAN(pass_rush_win_rate)', 'DESC', 'COUNT(*)', 1),
    'Median Missed Tackle Rate': ('MEDIAN(missed_tackle_rate)', 'ASC', 'COUNT(*)', 1),
}

OFFENSE_METRICS = {
    # Rushing Performance
    'EPA Per Rush': ('AVG(epa)', 'DESC', 'COUNT(*)', 10),
    'Rush Success Rate': ('AVG(CAST(success AS FLOAT64))', 'DESC', 'COUNT(*)', 10),
    'Total Rush Yards': ('SUM(yards_gained)', 'DESC', 'COUNT(*)', 10),
    'Rush TDs': ('SUM(CAST(rush_touchdown AS INT64))', 'DESC', 'COUNT(*)', 5),
    
    # Passing Performance
    'EPA Per Pass': ('AVG(epa)', 'DESC', 'COUNT(*)', 10),
    'Pass Success Rate': ('AVG(CAST(success AS FLOAT64))', 'DESC', 'COUNT(*)', 10),
    'Pass TDs': ('SUM(CAST(pass_touchdown AS INT64))', 'DESC', 'COUNT(*)', 5),
    'Sack Rate': ('SUM(CAST(sack AS INT64)) / COUNT(*)', 'ASC', 'COUNT(*)', 10),
    
    # Overall
    'Total EPA': ('SUM(epa)', 'DESC', 'COUNT(*)', 10),
    'Total Yards': ('SUM(yards_gained)', 'DESC', 'COUNT(*)', 10),
}

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
    Calculate Starbucks gravity for each stadium using the same model from coffee_narrative_report.md
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
    
    # Map team names to abbreviations
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
    
    gravity_df['team_abbr'] = gravity_df['team_name'].map(team_mapping)
    
    # Define Gravity Zones based on the Dunkin view
    def classify_gravity(net_grav):
        if net_grav <= -1:
            return 'Starbucks Zone'
        elif net_grav <= 1:
            return 'Neutral Zone'
        elif net_grav <= 3:
            return 'Mild Dunkin Zone'
        elif net_grav <= 5:
            return 'Dunkin Stronghold'
        else:
            return 'Dunkin Safe Zone'
    
    gravity_df['gravity_zone'] = gravity_df['net_gravity'].apply(classify_gravity)
    
    return gravity_df[['team_abbr', 'dunkin_gravity', 'starbucks_gravity', 'net_gravity', 'gravity_zone']]

def load_defense_data(client, gravity_df):
    """Load NE defense data with coffee gravity context"""
    print("Loading NE Defense Data...")
    
    # Load defense summary
    def_query = f"""
    SELECT 
        team_name as player, 
        team_name, 
        week,
        grades_defense, 
        grades_coverage_defense, 
        grades_pass_rush_defense,
        interceptions, 
        pass_break_ups, 
        missed_tackle_rate, 
        sacks, 
        stops, 
        total_pressures
    FROM `pff_analysis.{DEFENSE_SUMMARY}`
    WHERE team_name = 'NE'
    """
    
    def_df = client.query(def_query).to_dataframe()
    
    # Load coverage stats
    try:
        cov_query = f"""
        SELECT 
            team_name, 
            week, 
            forced_incompletion_rate, 
            yards_per_coverage_snap
        FROM `pff_analysis.{DEFENSE_COVERAGE}`
        WHERE team_name = 'NE'
        """
        cov_df = client.query(cov_query).to_dataframe()
        cov_agg = cov_df.groupby(['team_name', 'week']).mean().reset_index()
        def_df = pd.merge(def_df, cov_agg, on=['team_name', 'week'], how='left')
    except Exception as e:
        print(f"Could not load coverage data: {e}")
    
    # Load pass rush stats
    try:
        rush_query = f"""
        SELECT 
            team_name, 
            week, 
            prp, 
            pass_rush_win_rate
        FROM `pff_analysis.{DEFENSE_RUSH}`
        WHERE team_name = 'NE'
        """
        rush_df = client.query(rush_query).to_dataframe()
        rush_agg = rush_df.groupby(['team_name', 'week']).mean().reset_index()
        def_df = pd.merge(def_df, rush_agg, on=['team_name', 'week'], how='left')
    except Exception as e:
        print(f"Could not load pass rush data: {e}")
    
    # Join with schedule to get opponent and home team
    schedule_query = f"""
    SELECT DISTINCT
        week,
        posteam,
        defteam,
        home_team,
        away_team
    FROM `{BQ_PBP_TABLE}`
    WHERE season = 2025
        AND (posteam = 'NE' OR defteam = 'NE')
    """
    
    schedule_df = client.query(schedule_query).to_dataframe()
    
    # For defense, NE is the defteam
    schedule_df = schedule_df[schedule_df['defteam'] == 'NE']
    schedule_df = schedule_df.rename(columns={'posteam': 'opponent'})
    
    def_df = pd.merge(def_df, schedule_df[['week', 'home_team', 'opponent']], 
                      on='week', how='inner')
    
    # Join with coffee gravity
    def_df = pd.merge(def_df, gravity_df, 
                      left_on='home_team', right_on='team_abbr', how='inner')
    
    def_df['type'] = 'defense'
    
    return def_df

def load_offense_data(client, gravity_df):
    """Load NE offensive play-by-play data with coffee gravity"""
    print("Loading NE Offense Data (Play-by-Play)...")
    
    # Get play-by-play data for NE offense
    pbp_query = f"""
    SELECT
        pbp.week,
        pbp.home_team,
        pbp.play_type,
        pbp.epa,
        pbp.success,
        pbp.yards_gained,
        pbp.rush_touchdown,
        pbp.pass_touchdown,
        pbp.sack,
        pbp.interception,
        pbp.defteam as opponent
    FROM `{BQ_PBP_TABLE}` pbp
    WHERE pbp.season = 2025
        AND pbp.posteam = 'NE'
        AND pbp.play_type IN ('run', 'pass')
        AND pbp.epa IS NOT NULL
    """
    
    pbp_df = client.query(pbp_query).to_dataframe()
    
    # Join with coffee gravity based on home team
    pbp_df = pd.merge(pbp_df, gravity_df,
                      left_on='home_team', right_on='team_abbr', how='inner')
    
    return pbp_df

def build_filters():
    """Build filter conditions for optimization"""
    filters = {}
    
    # Dunkin Gravity Zones (the key filters!)
    filters['Coffee Gravity'] = {
        'Dunkin Safe Zone': "gravity_zone = 'Dunkin Safe Zone'",
        'Dunkin Stronghold': "gravity_zone = 'Dunkin Stronghold'",
        'High Dunkin (Net > 3)': "net_gravity >= 3",
        'Any Dunkin Zone (Net > 0)': "net_gravity > 0",
    }
    
    # Opponent characteristics
    filters['Opponent'] = {
        'Bird Teams': "opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA')",
        'Hat Teams': "opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK')",
        'Mammal Teams': "opponent IN ('CHI', 'DET', 'JAX', 'CAR', 'LAR', 'CIN', 'DEN', 'IND', 'MIA', 'BUF')",
    }
    
    return filters

def process_chunk(args):
    """Process a chunk of permutations (for parallel processing)"""
    perms, parquet_path, target_entity, entity_type = args
    con = duckdb.connect(database=':memory:')
    con.execute(f"CREATE VIEW data AS SELECT * FROM parquet_scan('{parquet_path}')")
    
    hits = []
    
    if entity_type == 'defense':
        metrics = DEFENSE_METRICS
    else:
        metrics = OFFENSE_METRICS
    
    for perm in perms:
        metric_name = perm['metric']
        if metric_name not in metrics:
            continue
        
        col_sql, default_sort_dir, min_att_col, min_att_val = metrics[metric_name]
        
        filter_sql = "1=1"
        for cat, name, sql in perm['filters']:
            filter_sql += f" AND {sql}"
        
        directions = [
            ('Best', default_sort_dir),
            ('Worst', 'ASC' if default_sort_dir == 'DESC' else 'DESC')
        ]
        
        for rank_type, sort_dir in directions:
            try:
                query = f"""
                    SELECT 
                        player,
                        {col_sql} as val,
                        {min_att_col} as opps
                    FROM data
                    WHERE {filter_sql}
                    GROUP BY player
                    HAVING opps >= {min_att_val}
                    ORDER BY val {sort_dir}
                    LIMIT 5
                """
                
                df = con.execute(query).fetchdf()
                if not df.empty:
                    top_player = df.iloc[0]['player']
                    if target_entity.lower() in str(top_player).lower():
                        perm_copy = perm.copy()
                        perm_copy['rank_type'] = rank_type
                        perm_copy['value'] = df.iloc[0]['val']
                        perm_copy['query'] = query
                        hits.append(perm_copy)
            except Exception as e:
                pass
    
    con.close()
    return hits

def process_offense_chunk(args):
    """Process offensive play-by-play data"""
    perms, parquet_path = args
    con = duckdb.connect(database=':memory:')
    con.execute(f"CREATE VIEW data AS SELECT * FROM parquet_scan('{parquet_path}')")
    
    hits = []
    
    for perm in perms:
        metric_name = perm['metric']
        if metric_name not in OFFENSE_METRICS:
            continue
        
        col_sql, default_sort_dir, min_att_col, min_att_val = OFFENSE_METRICS[metric_name]
        
        # Build filter
        filter_sql = "1=1"
        for cat, name, sql in perm['filters']:
            filter_sql += f" AND {sql}"
        
        # Determine play type filter
        play_type_filter = ""
        if 'Rush' in metric_name:
            play_type_filter = "AND play_type = 'run'"
        elif 'Pass' in metric_name or 'Sack' in metric_name:
            play_type_filter = "AND play_type = 'pass'"
        
        filter_sql += f" {play_type_filter}"
        
        directions = [
            ('Best', default_sort_dir),
            ('Worst', 'ASC' if default_sort_dir == 'DESC' else 'DESC')
        ]
        
        for rank_type, sort_dir in directions:
            try:
                query = f"""
                    SELECT 
                        'NE' as player,
                        {col_sql} as val,
                        {min_att_col} as opps
                    FROM data
                    WHERE {filter_sql}
                    HAVING opps >= {min_att_val}
                    ORDER BY val {sort_dir}
                    LIMIT 1
                """
                
                df = con.execute(query).fetchdf()
                if not df.empty and df.iloc[0]['val'] is not None:
                    perm_copy = perm.copy()
                    perm_copy['rank_type'] = rank_type
                    perm_copy['value'] = df.iloc[0]['val']
                    perm_copy['opps'] = df.iloc[0]['opps']
                    perm_copy['query'] = query
                    hits.append(perm_copy)
            except Exception as e:
                pass
    
    con.close()
    return hits

def run_optimization(df, target, type_, filters, forced_filter=None):
    """Run optimization to find winning stats"""
    import tempfile
    import shutil
    
    temp_dir = tempfile.mkdtemp()
    parquet_path = os.path.join(temp_dir, f'{type_}.parquet')
    df.to_parquet(parquet_path, index=False)
    
    permutations = []
    adhoc_filters = []
    
    for cat, opts in filters.items():
        for name, sql in opts.items():
            if forced_filter and forced_filter[1] == name:
                continue
            adhoc_filters.append((cat, name, sql))
    
    if type_ == 'defense':
        metrics = DEFENSE_METRICS
    else:
        metrics = OFFENSE_METRICS
    
    # Generate permutations
    for metric in metrics:
        base_filters = [forced_filter] if forced_filter else []
        
        # Just the base metric with forced filter
        permutations.append({'metric': metric, 'filters': base_filters})
        
        # Add single additional filters
        for f in adhoc_filters:
            new_filters = base_filters + [f]
            permutations.append({'metric': metric, 'filters': new_filters})
        
        # Add combinations of 2 filters
        for f1, f2 in itertools.combinations(adhoc_filters, 2):
            if f1[0] != f2[0]:  # Different categories
                new_filters = base_filters + [f1, f2]
                permutations.append({'metric': metric, 'filters': new_filters})
    
    print(f"Testing {len(permutations)} permutations...")
    
    # Parallel processing
    num_cores = multiprocessing.cpu_count()
    chunk_size = max(1, len(permutations) // (num_cores * 4))
    chunks = [permutations[i:i + chunk_size] for i in range(0, len(permutations), chunk_size)]
    
    if type_ == 'defense':
        worker_args = [(c, parquet_path, target, type_) for c in chunks]
        with multiprocessing.Pool(num_cores) as pool:
            results = list(tqdm(pool.imap_unordered(process_chunk, worker_args), 
                               total=len(chunks), desc="Processing"))
    else:
        worker_args = [(c, parquet_path) for c in chunks]
        with multiprocessing.Pool(num_cores) as pool:
            results = list(tqdm(pool.imap_unordered(process_offense_chunk, worker_args),
                               total=len(chunks), desc="Processing"))
    
    winning_perms = []
    for result in results:
        if result:
            winning_perms.extend(result)
    
    shutil.rmtree(temp_dir)
    
    return winning_perms

def generate_report(perms, target, type_, gravity_df):
    """Generate markdown report"""
    output_dir = os.path.dirname(__file__)
    if type_ == 'defense':
        filename = os.path.join(output_dir, "patriots_defense_dunkin.md")
    else:
        filename = os.path.join(output_dir, "patriots_offense_dunkin.md")
    
    # Sort by absolute value (most extreme correlations first)
    perms_sorted = sorted(perms, key=lambda x: abs(float(x['value'])), reverse=True)
    
    perms_by_type = {'Best': [], 'Worst': []}
    for p in perms_sorted:
        perms_by_type[p.get('rank_type', 'Best')].append(p)
    
    with open(filename, 'w') as f:
        f.write(f"# Patriots {type_.upper()} Performance by Dunkin Gravity\n\n")
        f.write(f"**Analysis Period:** 2025 Season\n\n")
        f.write(f"This analysis shows how the New England Patriots {'defense' if type_ == 'defense' else 'offense'} performs under different **Coffee Gravity** conditions.\n\n")
        
        # Add gravity context
        f.write("## Coffee Gravity Zones\n\n")
        f.write("Based on the Coffee Wars gravitational model:\n\n")
        gravity_summary = gravity_df.groupby('gravity_zone')['net_gravity'].agg(['min', 'max', 'count'])
        f.write(gravity_summary.to_markdown())
        f.write("\n\n")
        f.write("**Key Insight:** Patriots performance in Dunkin-dominated territories (Net Gravity > 0).\n\n")
        f.write("---\n\n")
        
        for rank_type, p_list in perms_by_type.items():
            if not p_list:
                continue
            
            f.write(f"# {rank_type} Stuperlatives\n\n")
            
            for i, perm in enumerate(p_list[:15]):  # Top 15
                metric_name = perm['metric']
                filter_descs = [f[1] for f in perm['filters']]
                filters_str = ", ".join(filter_descs) if filter_descs else "All Games"
                
                f.write(f"## {i+1}. {metric_name} ({rank_type})\n")
                f.write(f"**Conditions:** {filters_str}\n")
                f.write(f"**Value:** {perm['value']:.3f}\n\n")
                
                f.write(f"```sql\n{perm['query'].strip()}\n```\n\n")
                f.write("---\n\n")
    
    print(f"✅ Report saved: {filename}")

def main():
    """Main execution"""
    client = get_bq_client()
    if not client:
        print("❌ Could not create BigQuery client")
        return
    
    # Calculate coffee gravity
    gravity_df = calculate_coffee_gravity(client)
    print(f"\n📊 Coffee Gravity Summary:")
    print(gravity_df.groupby('gravity_zone').size())
    print("\n🏈 Gillette Stadium (NE) Gravity:")
    ne_gravity = gravity_df[gravity_df['team_abbr'] == 'NE']
    print(ne_gravity)
    
    filters = build_filters()
    
    # Analysis 1: NE Defense in Dunkin Zones
    print("\n\n🔍 ANALYZING: NE Defense Performance by Dunkin Gravity")
    print("=" * 70)
    def_df = load_defense_data(client, gravity_df)
    
    # Force filter: any Dunkin condition
    dunkin_filter = ('Coffee Gravity', 'Any Dunkin Zone (Net > 0)', 
                        filters['Coffee Gravity']['Any Dunkin Zone (Net > 0)'])
    
    def_perms = run_optimization(def_df, 'NE', 'defense', filters, 
                                 forced_filter=dunkin_filter)
    
    print(f"\n✅ Found {len(def_perms)} defensive stuperlatives")
    if def_perms:
        generate_report(def_perms, 'NE', 'defense', gravity_df)
    
    # Analysis 2: NE Offense in Dunkin Zones  
    print("\n\n🔍 ANALYZING: NE Offense Performance by Dunkin Gravity")
    print("=" * 70)
    off_df = load_offense_data(client, gravity_df)
    
    off_perms = run_optimization(off_df, 'NE', 'offense', filters,
                                 forced_filter=dunkin_filter)
    
    print(f"\n✅ Found {len(off_perms)} offensive stuperlatives")
    if off_perms:
        generate_report(off_perms, 'NE', 'offense', gravity_df)
    
    print("\n\n🎉 ANALYSIS COMPLETE!")
    print("=" * 70)

if __name__ == "__main__":
    main()
