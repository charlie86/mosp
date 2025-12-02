import os
import pandas as pd
import nfl_data_py as nfl
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../"))
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')
SHEET_NAME = 'PFF Run Blocking Data'
RAW_PLAYER_TAB = 'Raw Player Data'
OUTPUT_CSV = os.path.join(SCRIPT_DIR, '..', 'data', 'pff_ihop_analysis_results.csv')

# --- Helper Functions ---

def fetch_from_sheets(tab_name):
    print(f"Fetching data from Google Sheet '{SHEET_NAME}', tab '{tab_name}'...")
    
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"Error: {SERVICE_ACCOUNT_FILE} not found.")
        return None

    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
        client = gspread.authorize(creds)
        
        sheet = client.open(SHEET_NAME)
        worksheet = sheet.worksheet(tab_name)
        
        data = worksheet.get_all_records()
        df = pd.DataFrame(data)
        print(f"  -> Loaded {len(df)} rows from Sheets.")
        return df
    except Exception as e:
        print(f"Error fetching from Sheets: {e}")
        return None

def map_pff_team_to_abbr(pff_abbr):
    # Map PFF abbreviations to nfl_data_py abbreviations
    # PFF uses some non-standard ones like ARZ, BLT, CLV, HST
    mapping = {
        'ARZ': 'ARI',
        'BLT': 'BAL',
        'CLV': 'CLE',
        'HST': 'HOU',
        'SL': 'STL',   # St. Louis Rams
        'SD': 'SD',    # San Diego Chargers
        'OAK': 'OAK',  # Oakland Raiders
        'LA': 'LA',    # Los Angeles Rams (nfl_data_py uses LA for Rams)
        'LAC': 'LAC',  # Los Angeles Chargers
        'LV': 'LV',    # Las Vegas Raiders
        'JAX': 'JAX',
        'TEN': 'TEN',
        'WAS': 'WAS',
        'NYG': 'NYG',
        'NYJ': 'NYJ',
        'PHI': 'PHI',
        'DAL': 'DAL',
        'CHI': 'CHI',
        'DET': 'DET',
        'GB': 'GB',
        'MIN': 'MIN',
        'TB': 'TB',
        'NO': 'NO',
        'ATL': 'ATL',
        'CAR': 'CAR',
        'SF': 'SF',
        'SEA': 'SEA',
        'KC': 'KC',
        'DEN': 'DEN',
        'PIT': 'PIT',
        'CIN': 'CIN',
        'BUF': 'BUF',
        'MIA': 'MIA',
        'NE': 'NE',
        'IND': 'IND'
    }
    # Return mapped value, or original if not in map (assuming standard)
    return mapping.get(pff_abbr, pff_abbr)

def main():
    # 1. Fetch Data from Sheets
    pff_df = fetch_from_sheets(RAW_PLAYER_TAB)
    if pff_df is None: return

    # Determine seasons from data
    if 'Season' not in pff_df.columns:
        print("Error: 'Season' column not found in PFF data.")
        return
    
    seasons = pff_df['Season'].unique()
    seasons = sorted(seasons)
    print(f"Found seasons: {seasons}")

    # Fetch Schedule for all seasons
    print(f"Fetching schedule data for {len(seasons)} seasons...")
    try:
        schedule_df = nfl.import_schedules(seasons)
    except Exception as e:
        print(f"Error fetching schedules: {e}")
        return

    # 2. Filter for Offensive Linemen
    if 'Position' in pff_df.columns:
        print("Filtering for Offensive Linemen using 'Position' column...")
        # Correct OL positions based on PFF data (G, T, C)
        ol_positions = ['G', 'T', 'C', 'LT', 'LG', 'RG', 'RT'] 
        
        original_count = len(pff_df)
        pff_df = pff_df[pff_df['Position'].isin(ol_positions)]
        filtered_count = len(pff_df)
        print(f"  -> Filtered from {original_count} to {filtered_count} rows (kept OL only).")
    else:
        print("Warning: 'Position' column not found in PFF data.")

    # Filter for Minimum Snap Count (Run Block >= 10)
    if 'SnapCount_RunBlock' in pff_df.columns:
        print("Filtering for Minimum Snap Count (Run Block >= 10)...")
        pff_df['SnapCount_RunBlock'] = pd.to_numeric(pff_df['SnapCount_RunBlock'], errors='coerce')
        
        before_snap_filter = len(pff_df)
        pff_df = pff_df[pff_df['SnapCount_RunBlock'] >= 10]
        after_snap_filter = len(pff_df)
        print(f"  -> Filtered from {before_snap_filter} to {after_snap_filter} rows (kept RunBlock Snaps >= 10).")
    else:
        print("Warning: 'SnapCount_RunBlock' column not found.")

    # Filter for Minimum Games Played (>= 30)
    if 'Player' in pff_df.columns:
        print("Filtering for Minimum Games Played (>= 30)...")
        player_counts = pff_df['Player'].value_counts()
        valid_players = player_counts[player_counts >= 30].index
        
        before_game_filter = len(pff_df)
        pff_df = pff_df[pff_df['Player'].isin(valid_players)]
        after_game_filter = len(pff_df)
        print(f"  -> Filtered from {before_game_filter} to {after_game_filter} rows (kept Players with >= 30 games).")
        print(f"  -> {len(valid_players)} unique players remaining.")

    # 3. Prepare Data for Merge
    print("Processing data...")
    pff_df['TeamAbbr'] = pff_df['Team'].apply(map_pff_team_to_abbr)
    
    # Ensure Week is int
    pff_df['Week'] = pd.to_numeric(pff_df['Week'], errors='coerce')
    schedule_df['week'] = pd.to_numeric(schedule_df['week'], errors='coerce')
    schedule_df['season'] = pd.to_numeric(schedule_df['season'], errors='coerce')

    # 4. Merge PFF with Schedule to get Stadium and Home/Away info
    
    team_week_stadium_map = {}
    team_week_is_home_map = {}
    team_week_opponent_map = {}
    
    for _, row in schedule_df.iterrows():
        season = row['season']
        week = row['week']
        home = row['home_team']
        away = row['away_team']
        stadium = row.get('stadium')
        
        # Add to map with Season key
        team_week_stadium_map[(season, home, week)] = stadium
        team_week_stadium_map[(season, away, week)] = stadium
        
        # Track if it's a home game for the team
        team_week_is_home_map[(season, home, week)] = True
        team_week_is_home_map[(season, away, week)] = False
        
        # Track Opponent
        team_week_opponent_map[(season, home, week)] = away
        team_week_opponent_map[(season, away, week)] = home

    pff_df['Stadium'] = pff_df.apply(lambda x: team_week_stadium_map.get((x['Season'], x['TeamAbbr'], x['Week'])), axis=1)
    pff_df['IsHome'] = pff_df.apply(lambda x: team_week_is_home_map.get((x['Season'], x['TeamAbbr'], x['Week'])), axis=1)
    pff_df['Opponent'] = pff_df.apply(lambda x: team_week_opponent_map.get((x['Season'], x['TeamAbbr'], x['Week'])), axis=1)
    
    print(f"  -> Merged stadium info. Found {pff_df['Stadium'].notna().sum()} matches out of {len(pff_df)} rows.")
    
    # Normalize stadium names
    stadium_mapping = {
        'Mercedes-Benz Superdome': 'Caesars Superdome',
        'New Era Field': 'Highmark Stadium',
        'TIAA Bank Stadium': 'EverBank Stadium',
        'FirstEnergy Stadium': 'Cleveland Browns Stadium',
        'FedExField': 'Commanders Field',
        'Heinz Field': 'Acrisure Stadium',
        'Paul Brown Stadium': 'Paycor Stadium',
        'Arrowhead Stadium': 'GEHA Field at Arrowhead Stadium'
    }
    pff_df['Stadium'] = pff_df['Stadium'].replace(stadium_mapping)

    # Filter out International Stadiums
    international_stadiums = [
        'Tottenham Stadium', 'Wembley Stadium', 'Allianz Arena', 
        'Azteca Stadium', 'Deutsche Bank Park', 'Arena Corinthians'
    ]
    pff_df = pff_df[~pff_df['Stadium'].isin(international_stadiums)]
    
    # 5. Load IHOP Distances from CSV
    ihop_csv_path = os.path.join(SCRIPT_DIR, '..', 'data', 'nfl_stadium_ihop_distances.csv')
    if os.path.exists(ihop_csv_path):
        print(f"Loading IHOP distances from {ihop_csv_path}...")
        ihop_df = pd.read_csv(ihop_csv_path)
        
        ihop_df = ihop_df.rename(columns={'HaversineDist': 'DistToIHOP'})
        
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
        
        # Create Home Metrics Map
        home_metrics = ihop_df.set_index('TeamAbbr')[['DistToIHOP', 'DrivingDist', 'DrivingTimeSeconds']].to_dict('index')
        
        # Merge with main DF on Stadium
        ihop_cols = ['Stadium', 'DistToIHOP', 'DrivingDist', 'DrivingTime', 'DrivingTimeSeconds']
        merged_df = pff_df.merge(ihop_df[ihop_cols], on='Stadium', how='left')
        
        # Calculate Relative Metrics
        def get_relative_metric(row, metric):
            if row['IsHome']:
                return 0 
            
            team = row['TeamAbbr']
            if team in home_metrics:
                home_val = home_metrics[team].get(metric)
                current_val = row[metric]
                
                if pd.notna(home_val) and pd.notna(current_val):
                    return current_val - home_val
            return None

        print("Calculating relative distances...")
        merged_df['RelativeDistToIHOP'] = merged_df.apply(lambda x: get_relative_metric(x, 'DistToIHOP'), axis=1)
        merged_df['RelativeDrivingDist'] = merged_df.apply(lambda x: get_relative_metric(x, 'DrivingDist'), axis=1)
        merged_df['RelativeDrivingTimeSeconds'] = merged_df.apply(lambda x: get_relative_metric(x, 'DrivingTimeSeconds'), axis=1)
        
        print(f"  -> Merged IHOP data. Found {merged_df['DistToIHOP'].notna().sum()} matches.")
    else:
        print(f"Error: {ihop_csv_path} not found.")
        return

    # 6. Save Results
    # Rename Grade_RunBlock to Grade for compatibility with analysis scripts
    if 'Grade_RunBlock' in merged_df.columns:
        merged_df['Grade'] = merged_df['Grade_RunBlock']
    
    # Ensure Grade is numeric
    merged_df['Grade'] = pd.to_numeric(merged_df['Grade'], errors='coerce')
        
    merged_df.to_csv(OUTPUT_CSV, index=False)
    print(f"Done. Saved to {OUTPUT_CSV}")

if __name__ == "__main__":
    main()
