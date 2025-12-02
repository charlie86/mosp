import pandas as pd
import os
import ast
import gspread
from oauth2client.service_account import ServiceAccountCredentials

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../"))
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')
SHEET_NAME = 'PFF Run Blocking Data'
RAW_TEAM_TAB = 'Raw Team Data'
OUTPUT_FILE = os.path.join(SCRIPT_DIR, '../data/pff_team_defense_grades.csv')

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

def clean_team_name(name):
    """Normalize team names to match the main dataset."""
    name_map = {
        'Arizona Cardinals': 'ARZ',
        'Atlanta Falcons': 'ATL',
        'Baltimore Ravens': 'BLT',
        'Buffalo Bills': 'BUF',
        'Carolina Panthers': 'CAR',
        'Chicago Bears': 'CHI',
        'Cincinnati Bengals': 'CIN',
        'Cleveland Browns': 'CLV',
        'Dallas Cowboys': 'DAL',
        'Denver Broncos': 'DEN',
        'Detroit Lions': 'DET',
        'Green Bay Packers': 'GB',
        'Houston Texans': 'HST',
        'Indianapolis Colts': 'IND',
        'Jacksonville Jaguars': 'JAX',
        'Kansas City Chiefs': 'KC',
        'Las Vegas Raiders': 'LV',
        'Los Angeles Chargers': 'LAC',
        'Los Angeles Rams': 'LA',
        'Miami Dolphins': 'MIA',
        'Minnesota Vikings': 'MIN',
        'New England Patriots': 'NE',
        'New Orleans Saints': 'NO',
        'New York Giants': 'NYG',
        'New York Jets': 'NYJ',
        'Oakland Raiders': 'LV', # Map to LV for consistency
        'Philadelphia Eagles': 'PHI',
        'Pittsburgh Steelers': 'PIT',
        'San Diego Chargers': 'LAC', # Map to LAC
        'San Francisco 49ers': 'SF',
        'Seattle Seahawks': 'SEA',
        'St. Louis Rams': 'LA', # Map to LA
        'Tampa Bay Buccaneers': 'TB',
        'Tennessee Titans': 'TEN',
        'Washington Commanders': 'WAS',
        'Washington Football Team': 'WAS',
        'Washington Redskins': 'WAS'
    }
    return name_map.get(name, name)

def main():
    # 1. Fetch Data from Sheets
    df = fetch_from_sheets(RAW_TEAM_TAB)
    if df is None: return
    
    processed_data = []
    
    for idx, row in df.iterrows():
        season = row['Season']
        team_name = row['Team']
        raw_stats_str = row['RawStats']
        
        try:
            # Parse the string representation of the list
            parts = ast.literal_eval(raw_stats_str)
            
            # Expected structure based on inspection of stats row:
            # Headers: ['RANK', 'RANK', 'TEAM', 'RECORD', 'PF', 'PA', 'OVER', 'OFF', 'PASS', 'PBLK', 'RECV', 'RUN', 'RBLK', 'DEF', 'RDEF', 'TACK', 'PRSH', 'COV', 'SPEC', '']
            # The 'RawStats' likely starts from 'RECORD' or 'PF' depending on how split happened.
            # In position scraper, stat row contained everything except name/rank.
            # But here, let's look at the parts.
            
            # If we assume the split was clean:
            # Name Row: Rank, Team
            # Stat Row: Record, PF, PA, ...
            
            # Let's try to map by index relative to end or start.
            # RDEF is usually near the middle-end.
            
            # If we look at headers again:
            # ... RUN, RBLK, DEF, RDEF, TACK ...
            
            # Let's try to find it by position.
            # RDEF is typically the 14th column overall.
            # If Name row took 2-3 columns (Rank, Team), then Stat row has the rest.
            # So RDEF should be around index 10-12 in parts.
            
            # Let's try index 11 (0-based) from parts?
            # Or better, let's look for a value that looks like a grade (0-100 float).
            
            # Actually, let's just use a fixed index based on standard PFF table layout for teams.
            # Based on previous debug:
            # 8-9, 400, 379, ...
            # Record, PF, PA ...
            
            # Headers: RECORD(3), PF(4), PA(5), OVER(6), OFF(7), PASS(8), PBLK(9), RECV(10), RUN(11), RBLK(12), DEF(13), RDEF(14)
            # If parts starts at RECORD, then RDEF is index 14-3 = 11.
            
            rdef_grade = None
            if len(parts) > 11:
                rdef_grade = parts[11]
            
            # Clean Team Name
            clean_team = clean_team_name(team_name)
            
            processed_data.append({
                'Season': season,
                'Team': clean_team,
                'OppRunDefGrade': rdef_grade
            })
            
        except Exception as e:
            print(f"Error processing row {idx}: {e}")
            continue
            
    # Create DataFrame
    proc_df = pd.DataFrame(processed_data)
    
    # Clean Grade
    proc_df['OppRunDefGrade'] = pd.to_numeric(proc_df['OppRunDefGrade'], errors='coerce')
    
    # Save
    proc_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved processed team stats to {OUTPUT_FILE}")
    print(proc_df.head())
    print(f"Total rows: {len(proc_df)}")

if __name__ == "__main__":
    main()
