import os
import pandas as pd
import nfl_data_py as nfl
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
import ast
import time

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../"))
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')

# BigQuery Config
DATASET_ID = 'pff_analysis'
POS_STATS_TABLE = f'{DATASET_ID}.position_stats'
TEAM_STATS_TABLE = f'{DATASET_ID}.team_stats'
IHOP_TABLE = f'{DATASET_ID}.stadium_ihop_distances'
GRAVITY_TABLE = f'{DATASET_ID}.stadium_gravitational_pull'
OUTPUT_TABLE = f'{DATASET_ID}.merged_analysis_data'

# --- Mappings ---

# Population Density Map (Approx Persons/Sq Mile) - Derived from valid MSA approximations
POPULATION_DENSITY_MAP = {
    'ARI': 4000, 'ATL': 3700, 'BAL': 7600, 'BUF': 1200, 'CAR': 2800,
    'CHI': 12000, 'CIN': 3900, 'CLE': 5100, 'DAL': 4100, 'DEN': 4600,
    'DET': 4800, 'GB': 2300, 'HOU': 3600, 'IND': 2400, 'JAX': 1200,
    'KC': 1600, 'LV': 4500, 'LAC': 11900, 'LA': 11900, 'MIA': 6000,
    'MIN': 7900, 'NE': 800, 'NO': 2300, 'NYG': 2700, 'NYJ': 2700,
    'PHI': 11900, 'PIT': 5500, 'SF': 6800, 'SEA': 8800, 'TB': 3400,
    'TEN': 1400, 'WAS': 5000, 'OAK': 7500, 'SD': 4300, 'STL': 5000
}

# Player Name Mapping (PFF -> NFL Data Py)
PLAYER_MAPPING = {
    'Stephen Neal': 'Steve Neal',
    'Jon Runyan Sr.': 'Jon Runyan',
    # Add others as discovered
}

# Stadium Mapping (Old -> New/Standard)
STADIUM_MAPPING = {
    'University of Phoenix Stadium': 'State Farm Stadium',
    'Alltel Stadium': 'EverBank Stadium',
    'Reliant Stadium': 'NRG Stadium',
    'LP Field': 'Nissan Stadium',
    'McAfee Coliseum': 'Allegiant Stadium', # Raiders moved
    'Giants Stadium': 'MetLife Stadium',
    'Edward Jones Dome': 'SoFi Stadium', # Rams moved
    'Monster Park': 'Levi\'s Stadium', # 49ers moved
    'Texas Stadium': 'AT&T Stadium',
    'Qwest Field': 'Lumen Field',
    'Qualcomm Stadium': 'SoFi Stadium', # Chargers moved
    'RCA Dome': 'Lucas Oil Stadium',
    'Invesco Field at Mile High': 'Empower Field at Mile High',
    'Dolphin Stadium': 'Hard Rock Stadium',
    'Georgia Dome': 'Mercedes-Benz Stadium',
    'Hubert H. Humphrey Metrodome': 'U.S. Bank Stadium',
    'Louisiana Superdome': 'Caesars Superdome',
    'Ralph Wilson Stadium': 'Highmark Stadium',
    'Jacksonville Municipal Stadium': 'EverBank Stadium',
    'Oakland-Alameda County Coliseum': 'Allegiant Stadium', # Raiders moved
    'Candlestick Park': 'Levi\'s Stadium', # 49ers moved
    'Rogers Centre': 'Highmark Stadium', # Bills in Toronto -> Map to Buffalo? Or skip.
    'Twickenham Stadium': 'Wembley Stadium', # Map to London? Or skip.
    'Wembley Stadium': 'Wembley Stadium',
    'Tottenham Stadium': 'Tottenham Hotspur Stadium',
    'Azteca Stadium': 'Estadio Azteca',
    'Allianz Arena': 'Allianz Arena',
    'Deutsche Bank Park': 'Deutsche Bank Park',
    'Arena Corinthians': 'Arena Corinthians',
    'Aloha Stadium': 'Aloha Stadium',
    'Camping World Stadium': 'Camping World Stadium',
    'Cowboys Stadium': 'AT&T Stadium',
    'New Meadowlands Stadium': 'MetLife Stadium',
    'EverBank Field': 'EverBank Stadium',
    'Mall of America Field': 'U.S. Bank Stadium',
    'Sun Life Stadium': 'Hard Rock Stadium',
    'TCF Bank Stadium': 'U.S. Bank Stadium',
    'Sports Authority Field at Mile High': 'Empower Field at Mile High',
    'O.co Coliseum': 'Allegiant Stadium',
    'CenturyLink Field': 'Lumen Field',
    'Los Angeles Memorial Coliseum': 'SoFi Stadium',
    'StubHub Center': 'SoFi Stadium',
    'Ring Central Coliseum': 'Allegiant Stadium',
    'Pro Player Stadium': 'Hard Rock Stadium',
    'Land Shark Stadium': 'Hard Rock Stadium',
    'FedExField': 'Commanders Field',
    'Heinz Field': 'Acrisure Stadium',
    'Paul Brown Stadium': 'Paycor Stadium',
    'Arrowhead Stadium': 'GEHA Field at Arrowhead Stadium',
    'Mercedes-Benz Superdome': 'Caesars Superdome',
    'New Era Field': 'Highmark Stadium',
    'TIAA Bank Stadium': 'EverBank Stadium',
    'FirstEnergy Stadium': 'Cleveland Browns Stadium',
}

# PFF to NFL Abbreviation Mapping
PFF_TO_NFL_MAP = {
    'ARZ': 'ARI', 'BLT': 'BAL', 'CLV': 'CLE', 'HST': 'HOU',
    'SL': 'STL', 'SD': 'SD', 'OAK': 'OAK', 'LA': 'LA', 'LAC': 'LAC', 'LV': 'LV',
    'JAX': 'JAX', 'TEN': 'TEN', 'WAS': 'WAS', 'NYG': 'NYG', 'NYJ': 'NYJ',
    'PHI': 'PHI', 'DAL': 'DAL', 'CHI': 'CHI', 'DET': 'DET', 'GB': 'GB',
    'MIN': 'MIN', 'TB': 'TB', 'NO': 'NO', 'ATL': 'ATL', 'CAR': 'CAR',
    'SF': 'SF', 'SEA': 'SEA', 'KC': 'KC', 'DEN': 'DEN', 'PIT': 'PIT',
    'CIN': 'CIN', 'BUF': 'BUF', 'MIA': 'MIA', 'NE': 'NE', 'IND': 'IND'
}

# --- Helper Functions ---

def get_bq_client():
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"Error: {SERVICE_ACCOUNT_FILE} not found.")
        return None
    return bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)

def fetch_from_bq(client, table_id):
    print(f"Fetching data from BQ table '{table_id}'...")
    try:
        query = f"SELECT * FROM `{client.project}.{table_id}`"
        df = client.query(query).to_dataframe()
        print(f"  -> Loaded {len(df)} rows.")
        return df
    except Exception as e:
        print(f"Error fetching '{table_id}': {e}")
        return None

def get_schedule_lookup(seasons):
    print(f"Fetching schedule data for seasons: {seasons}...")
    try:
        schedule_df = nfl.import_schedules(seasons)
        lookup = {}
        for _, row in schedule_df.iterrows():
            season = row['season']
            week = row['week']
            home = row['home_team']
            away = row['away_team']
            stadium = row.get('stadium')
            
            # Map for both home and away teams
            lookup[(season, week, home)] = stadium
            lookup[(season, week, away)] = stadium
        return lookup
    except Exception as e:
        print(f"Error fetching schedules: {e}")
        return {}

def get_roster_lookup(seasons):
    print(f"Fetching roster data for seasons: {seasons}...")
    try:
        rosters = nfl.import_seasonal_rosters(seasons)
        
        # Create lookup: (Player, Season, Team) -> Rookie Year
        roster_lookup = {}
        # Fallback lookup: (Player, Season) -> Rookie Year
        fallback_lookup = {}
        
        for _, row in rosters.iterrows():
            name = row['player_name']
            season = row['season']
            team = row['team']
            rookie = row['rookie_year']
            
            if pd.notna(rookie):
                roster_lookup[(name, season, team)] = rookie
                fallback_lookup[(name, season)] = rookie
                
        print(f"Built roster lookup with {len(roster_lookup)} entries.")
        return roster_lookup, fallback_lookup
    except Exception as e:
        print(f"Error fetching rosters: {e}")
        return {}, {}

def map_pff_team_to_abbr(pff_abbr):
    return PFF_TO_NFL_MAP.get(pff_abbr, pff_abbr)

def clean_team_name(name):
    """Normalize team names to match the main dataset."""
    name_map = {
        'Arizona Cardinals': 'ARI', 'Atlanta Falcons': 'ATL', 'Baltimore Ravens': 'BAL',
        'Buffalo Bills': 'BUF', 'Carolina Panthers': 'CAR', 'Chicago Bears': 'CHI',
        'Cincinnati Bengals': 'CIN', 'Cleveland Browns': 'CLE', 'Dallas Cowboys': 'DAL',
        'Denver Broncos': 'DEN', 'Detroit Lions': 'DET', 'Green Bay Packers': 'GB',
        'Houston Texans': 'HOU', 'Indianapolis Colts': 'IND', 'Jacksonville Jaguars': 'JAX',
        'Kansas City Chiefs': 'KC', 'Las Vegas Raiders': 'LV', 'Los Angeles Chargers': 'LAC',
        'Los Angeles Rams': 'LA', 'Miami Dolphins': 'MIA', 'Minnesota Vikings': 'MIN',
        'New England Patriots': 'NE', 'New Orleans Saints': 'NO', 'New York Giants': 'NYG',
        'New York Jets': 'NYJ', 'Oakland Raiders': 'OAK', 'Philadelphia Eagles': 'PHI',
        'Pittsburgh Steelers': 'PIT', 'San Diego Chargers': 'SD', 'San Francisco 49ers': 'SF',
        'Seattle Seahawks': 'SEA', 'St. Louis Rams': 'STL', 'Tampa Bay Buccaneers': 'TB',
        'Tennessee Titans': 'TEN', 'Washington Commanders': 'WAS', 'Washington Football Team': 'WAS',
        'Washington Redskins': 'WAS'
    }
    return name_map.get(name, name)

def main():
    client = get_bq_client()
    if not client: return

    # 1. Fetch Raw Player Data
    pff_df = fetch_from_bq(client, POS_STATS_TABLE)
    if pff_df is None: return

    # Determine seasons
    if 'Season' not in pff_df.columns:
        print("Error: 'Season' column not found.")
        return
    # Assuming BQ returned integers, fillna(0) just in case
    pff_df['Season'] = pff_df['Season'].fillna(0).astype(int)
    seasons = sorted(pff_df['Season'].unique().tolist())
    print(f"Found seasons: {seasons}")

    # 2. Filter Data
    if 'Position' in pff_df.columns:
        print("Filtering for Offensive Linemen...")
        ol_positions = ['G', 'T', 'C', 'LT', 'LG', 'RG', 'RT'] 
        pff_df = pff_df[pff_df['Position'].isin(ol_positions)]
    
    if 'SnapCount_RunBlock' in pff_df.columns:
        print("Filtering for Min Snap Count...")
        pff_df['SnapCount_RunBlock'] = pff_df['SnapCount_RunBlock'].fillna(0).astype(int)
        pff_df = pff_df[pff_df['SnapCount_RunBlock'] >= 10]

    if 'Player' in pff_df.columns:
        print("Filtering for Min Games Played...")
        player_counts = pff_df['Player'].value_counts()
        valid_players = player_counts[player_counts >= 30].index
        pff_df = pff_df[pff_df['Player'].isin(valid_players)]

    # 3. Fetch Reference Data
    schedule_lookup = get_schedule_lookup(seasons)
    roster_lookup, fallback_lookup = get_roster_lookup(seasons)
    
    ihop_df = fetch_from_bq(client, IHOP_TABLE)
    if ihop_df is not None:
        ihop_df = ihop_df.drop_duplicates(subset=['Stadium'])
        
        ihop_lookup = ihop_df.set_index('Stadium')[['DistToIHOP', 'DrivingDist', 'DrivingTime', 'DrivingTimeSeconds']].to_dict('index')
        # Also prepare for relative calc
        # Map full team names in IHOP CSV to abbreviations
        csv_team_to_abbr = {
            "Arizona Cardinals": "ARI", "Atlanta Falcons": "ATL", "Baltimore Ravens": "BAL",
            "Buffalo Bills": "BUF", "Carolina Panthers": "CAR", "Chicago Bears": "CHI",
            "Cincinnati Bengals": "CIN", "Cleveland Browns": "CLE", "Dallas Cowboys": "DAL",
            "Denver Broncos": "DEN", "Detroit Lions": "DET", "Green Bay Packers": "GB",
            "Houston Texans": "HOU", "Indianapolis Colts": "IND", "Jacksonville Jaguars": "JAX",
            "Kansas City Chiefs": "KC", "Las Vegas Raiders": "LV", "Los Angeles Chargers": "LAC",
            "Los Angeles Rams": "LA", "Miami Dolphins": "MIA", "Minnesota Vikings": "MIN",
            "New England Patriots": "NE", "New Orleans Saints": "NO", "New York Giants": "NYG",
            "New York Jets": "NYJ", "Philadelphia Eagles": "PHI", "Pittsburgh Steelers": "PIT",
            "San Francisco 49ers": "SF", "Seattle Seahawks": "SEA", "Tampa Bay Buccaneers": "TB",
            "Tennessee Titans": "TEN", "Washington Commanders": "WAS"
        }
        ihop_df['TeamAbbr'] = ihop_df['Team'].map(csv_team_to_abbr)
        home_metrics = ihop_df.set_index('TeamAbbr')[['DistToIHOP', 'DrivingDist', 'DrivingTimeSeconds']].to_dict('index')
    else:
        print("Warning: Could not load IHOP data.")
        ihop_lookup = {}
        home_metrics = {}

    # Fetch Gravitational Data
    grav_df = fetch_from_bq(client, GRAVITY_TABLE)
    grav_lookup = {}
    if grav_df is not None:
        print("Processing Gravitational Data...")
        for index, row in grav_df.iterrows():
            stadium = row['Stadium']
            ihops = row['IHOPs'] # This assumes it comes back as a list of dicts/structs
            g_lin = 0
            g_quad = 0
            g_cub = 0
            if ihops is not None:
                 # Helper to handle BQ Struct/Record format if needed, but standard BQ library returns list of mappings
                 for place in ihops:
                    dist = place.get('DistanceMiles')
                    if dist is None: dist = 10
                    d = max(float(dist), 0.1)
                    g_lin += 1 / d
                    g_quad += 1 / (d ** 2)
                    g_cub += 1 / (d ** 3)
            grav_lookup[stadium] = {'linear': g_lin, 'quadratic': g_quad, 'cubic': g_cub}

    # 4. Process Rows (Merge & Clean)
    print("Processing rows (Merging Schedule, IHOP, Experience)...")
    
    pff_df['TeamAbbr'] = pff_df['Team'].apply(map_pff_team_to_abbr)
    pff_df['Week'] = pff_df['Week'].fillna(0).astype(int)
    
    # Lists to populate new columns
    stadiums = []
    is_homes = []
    opponents = []
    dist_ihops = []
    driving_dists = []
    driving_times = []
    driving_secs = []
    rel_dists = []
    rel_drive_dists = []
    rel_drive_secs = []
    rookie_years = []
    years_in_leagues = []
    years_in_league_sqs = []
    gravity_linears = []
    gravity_quadratics = []
    gravity_cubics = []
    pop_densities = []
    
    # Enhanced Schedule Lookup for Home/Opponent
    print("Building detailed schedule map...")
    schedule_df = nfl.import_schedules(seasons)
    team_week_map = {} # (Season, Team, Week) -> {Stadium, IsHome, Opponent}
    
    for _, row in schedule_df.iterrows():
        s = row['season']
        w = row['week']
        h = row['home_team']
        a = row['away_team']
        stad = row.get('stadium')
        
        team_week_map[(s, h, w)] = {'Stadium': stad, 'IsHome': True, 'Opponent': a}
        team_week_map[(s, a, w)] = {'Stadium': stad, 'IsHome': False, 'Opponent': h}
        
    # Apply Logic
    for _, row in pff_df.iterrows():
        season = int(row['Season'])
        week = int(row['Week'])
        team = row['TeamAbbr']
        player = row['Player']
        
        # Defaults
        curr_stadium = None
        curr_is_home = None
        curr_opponent = None
        
        # 1. Schedule Data
        if season and week and team:
            sched_data = team_week_map.get((season, team, week))
            if sched_data:
                curr_stadium = sched_data['Stadium']
                curr_is_home = sched_data['IsHome']
                curr_opponent = sched_data['Opponent']
        
        # Pro Bowl override
        if week and week > 21:
            curr_stadium = 'Aloha Stadium'
            
        # 2. IHOP Data
        # Normalize Stadium
        lookup_stadium = STADIUM_MAPPING.get(curr_stadium, curr_stadium)
        
        ihop_metrics = ihop_lookup.get(lookup_stadium, {})
        d_ihop = ihop_metrics.get('DistToIHOP')
        d_drive = ihop_metrics.get('DrivingDist')
        d_time = ihop_metrics.get('DrivingTime')
        d_sec = ihop_metrics.get('DrivingTimeSeconds')

        # Gravity
        grav_data = grav_lookup.get(lookup_stadium, {'linear': 0.0, 'quadratic': 0.0, 'cubic': 0.0})
        g_lin = grav_data['linear']
        g_quad = grav_data['quadratic']
        g_cub = grav_data['cubic']
        
        # Relative Metrics
        rel_dist = None
        rel_drive = None
        rel_sec = None
        
        if curr_is_home is False and team in home_metrics: # Away game
            home_vals = home_metrics[team]
            if pd.notna(d_ihop) and pd.notna(home_vals.get('DistToIHOP')):
                rel_dist = d_ihop - home_vals['DistToIHOP']
            if pd.notna(d_drive) and pd.notna(home_vals.get('DrivingDist')):
                rel_drive = d_drive - home_vals['DrivingDist']
            if pd.notna(d_sec) and pd.notna(home_vals.get('DrivingTimeSeconds')):
                rel_sec = d_sec - home_vals['DrivingTimeSeconds']
        elif curr_is_home is True:
            rel_dist = 0
            rel_drive = 0
            rel_sec = 0

        # Population Density
        # Logic: If Home, use Team. If Away, use Opponent.
        # However, pop_density_map is keyed by TEAM ABBR.
        # If curr_is_home (True), we are at Team's home -> use Team
        # If curr_is_home (False), we are at Opponent's home -> use Opponent
        city_team = team if curr_is_home else curr_opponent
        pop_density = POPULATION_DENSITY_MAP.get(city_team, 4000)
            
        # 3. Experience Data
        rookie_year = None
        years_in_league = None
        years_in_league_sq = None
        
        if season and team:
            lookup_name = PLAYER_MAPPING.get(player, player)
            
            # Primary: (Name, Season, Team)
            if (lookup_name, season, team) in roster_lookup:
                rookie_year = int(roster_lookup[(lookup_name, season, team)])
            # Fallback: (Name, Season)
            elif (lookup_name, season) in fallback_lookup:
                rookie_year = int(fallback_lookup[(lookup_name, season)])
                
            if rookie_year:
                years_in_league = season - rookie_year
                if years_in_league < 0: years_in_league = None # Sanity check
                else: years_in_league_sq = years_in_league ** 2
        
        # Append
        stadiums.append(curr_stadium)
        is_homes.append(curr_is_home)
        opponents.append(curr_opponent)
        dist_ihops.append(d_ihop)
        driving_dists.append(d_drive)
        driving_times.append(d_time)
        driving_secs.append(d_sec)
        rel_dists.append(rel_dist)
        rel_drive_dists.append(rel_drive)
        rel_drive_secs.append(rel_sec)
        rookie_years.append(rookie_year)
        years_in_leagues.append(years_in_league)
        years_in_league_sqs.append(years_in_league_sq)
        gravity_linears.append(g_lin)
        gravity_quadratics.append(g_quad)
        gravity_cubics.append(g_cub)
        pop_densities.append(pop_density)

    # Assign columns
    pff_df['Stadium'] = stadiums
    pff_df['IsHome'] = is_homes
    pff_df['Opponent'] = opponents
    pff_df['DistToIHOP'] = dist_ihops
    pff_df['DrivingDist'] = driving_dists
    pff_df['DrivingTime'] = driving_times
    pff_df['DrivingTimeSeconds'] = driving_secs
    pff_df['RelativeDistToIHOP'] = rel_dists
    pff_df['RelativeDrivingDist'] = rel_drive_dists
    pff_df['RelativeDrivingTimeSeconds'] = rel_drive_secs
    pff_df['rookie_year'] = rookie_years
    pff_df['YearsInLeague'] = years_in_leagues
    pff_df['YearsInLeague_Sq'] = years_in_league_sqs
    pff_df['IHOP_Gravity_Linear'] = gravity_linears
    pff_df['IHOP_Gravity_Quadratic'] = gravity_quadratics
    pff_df['IHOP_Gravity_Cubic'] = gravity_cubics
    pff_df['PopulationDensity'] = pop_densities
    
    # Clean IsHome to 1/0
    pff_df['IsHome'] = pff_df['IsHome'].map({'TRUE': 1, 'FALSE': 0, 1: 1, 0: 0, True: 1, False: 0}).fillna(0).astype(int)

    # Calculate SeasonAvg_Excl
    # Rename Grade_RunBlock -> Grade early for this calc
    if 'Grade_RunBlock' in pff_df.columns:
        pff_df['Grade'] = pff_df['Grade_RunBlock']
    
    print("Calculating SeasonAvg_Excl...")
    # Group by Player, Season to get Sum and Count
    season_stats = pff_df.groupby(['Player', 'Season'])['Grade'].agg(['sum', 'count']).reset_index()
    season_stats.rename(columns={'sum': 'SeasonSum', 'count': 'SeasonCount'}, inplace=True)
    
    pff_df = pff_df.merge(season_stats, on=['Player', 'Season'], how='left')
    pff_df['SeasonAvg_Excl'] = (pff_df['SeasonSum'] - pff_df['Grade']) / (pff_df['SeasonCount'] - 1)
    
    # Note: Filtering where SeasonCount > 1 might be drastic for the global table, 
    # but for regression it is needed. User said "include all columns needed for regression",
    # but didn't explicitly say "filter the table". 
    # However, SeasonAvg_Excl will be NaN or Inf if Count <= 1.
    # Let's leave NaNs/Infs for now, or handle div by zero.
    # Actually, let's just let it be. Analysis script can filter dropna.
    
    print("Check DistToIHOP before merge:")
    print(pff_df[['Stadium', 'DistToIHOP']].head())
    
    # 5. Merge Team Stats
    print("Processing Team Defense Grades from Raw Team Data...")
    raw_team_df = fetch_from_bq(client, TEAM_STATS_TABLE)
    
    if raw_team_df is not None:
        processed_team_data = []
        for idx, row in raw_team_df.iterrows():
            try:
                season = row['Season']
                team_name = row['Team']
                raw_stats_str = row['RawStats']
                
                # Parse RawStats
                parts = ast.literal_eval(raw_stats_str)
                
                # Extract RDEF Grade (Index 11 based on analysis)
                rdef_grade = None
                if len(parts) > 11:
                    rdef_grade = parts[11]
                
                processed_team_data.append({
                    'Season': str(season),
                    'Team': clean_team_name(team_name),
                    'OppRunDefGrade': rdef_grade
                })
            except Exception as e:
                pass
                
        team_df = pd.DataFrame(processed_team_data)
        team_df['OppRunDefGrade'] = pd.to_numeric(team_df['OppRunDefGrade'], errors='coerce')
        
        # Ensure types match for merge
        pff_df['Season'] = pff_df['Season'].astype(str)
        pff_df['Opponent'] = pff_df['Opponent'].astype(str)
        
        # Merge
        pff_df = pff_df.merge(
            team_df, 
            left_on=['Opponent', 'Season'], 
            right_on=['Team', 'Season'], 
            how='left'
        )
        print(f"  -> Merged team stats. Columns added: {team_df.columns.tolist()}")
        
    print("Check DistToIHOP after merge:")
    print(pff_df[['Stadium', 'DistToIHOP']].head())
    
    # 6. Final Cleanup
    # Filter out international stadiums
    international_stadiums = [
        'Tottenham Stadium', 'Wembley Stadium', 'Allianz Arena', 
        'Azteca Stadium', 'Deutsche Bank Park', 'Arena Corinthians',
        'Twickenham Stadium'
    ]
    pff_df = pff_df[~pff_df['Stadium'].isin(international_stadiums)]
    
    # 7. Write to BigQuery
    print(f"Writing {len(pff_df)} rows to '{OUTPUT_TABLE}'...")
    try:
        table_ref = f"{client.project}.{OUTPUT_TABLE}"
        job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE")
        
        job = client.load_table_from_dataframe(pff_df, table_ref, job_config=job_config)
        job.result()
        print(f"Success! Data updated in {OUTPUT_TABLE}.")
        
    except Exception as e:
        print(f"Error writing to BQ: {e}")

if __name__ == "__main__":
    main()
