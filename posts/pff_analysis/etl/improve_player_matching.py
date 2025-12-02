import pandas as pd
import nfl_data_py as nfl
import os
import re

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, '../data/pff_ihop_analysis_results.csv')
OUTPUT_FILE = os.path.join(SCRIPT_DIR, '../data/pff_ihop_analysis_results_with_draft_year.csv')

def clean_name(name):
    if not isinstance(name, str):
        return ""
    # Lowercase, remove punctuation, remove suffixes like ' Jr', ' III'
    name = name.lower()
    name = re.sub(r'[^\w\s]', '', name)
    name = re.sub(r'\sjr$', '', name)
    name = re.sub(r'\ssr$', '', name)
    name = re.sub(r'\siii$', '', name)
    name = re.sub(r'\sii$', '', name)
    name = re.sub(r'\siv$', '', name)
    name = name.replace(' ', '')
    return name

def main():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return

    print(f"Loading PFF data from {DATA_FILE}...")
    df = pd.read_csv(DATA_FILE)
    
    print("Loading NFL Player data (import_players)...")
    # import_players() might have better historical coverage than import_ids()
    # It returns columns like: 'display_name', 'first_name', 'last_name', 'birth_date', 'college', 'position_group', 'position', 'jersey_number', 'height', 'weight', 'team', 'status', 'esb_id', 'gsis_id', 'pff_id', 'sleeper_id', 'yahoo_id', 'espn_id', 'nfl_id', 'smart_id', 'entry_year', 'rookie_year', 'draft_number', 'draft_round', 'draft_year'
    
    ids_df = nfl.import_players()
    
    # Check columns
    print("Columns in players df:", ids_df.columns.tolist())
    
    # We want draft_year.
    # Use 'display_name' as name
    ids_df['name'] = ids_df['display_name']
    
    # Filter to relevant columns
    ids_df = ids_df[['name', 'draft_year', 'position']]
    
    # Create clean names for matching
    print("Cleaning names...")
    df['clean_name'] = df['Player'].apply(clean_name)
    ids_df['clean_name'] = ids_df['name'].apply(clean_name)
    
    # Strategy:
    # 1. Match on clean_name -> clean_name
    
    # Create a lookup dictionary from IDs
    id_lookup = {}
    
    # Populate lookup
    for idx, row in ids_df.iterrows():
        if row['clean_name']:
            id_lookup[row['clean_name']] = row
            
    # Apply lookup
    def get_draft_year(clean_n):
        if clean_n in id_lookup:
            return id_lookup[clean_n]['draft_year']
        return None

    print("Matching players...")
    df['draft_year'] = df['clean_name'].apply(get_draft_year)
    
    # Check match rate
    total_players = len(df['Player'].unique())
    matched_players = df.dropna(subset=['draft_year'])['Player'].nunique()
    print(f"Matched {matched_players} / {total_players} players ({matched_players/total_players:.1%})")
    
    # Calculate YearsInLeague
    df['Season'] = pd.to_numeric(df['Season'], errors='coerce')
    df['draft_year'] = pd.to_numeric(df['draft_year'], errors='coerce')
    df['YearsInLeague'] = df['Season'] - df['draft_year']
    
    # For unmatched, we can't calculate.
    # We will filter the regression to only those with valid YearsInLeague.
    
    # Save
    df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved data with YearsInLeague to {OUTPUT_FILE}")
    
    # Debug: Show some unmatched players
    unmatched = df[df['draft_year'].isna()]['Player'].unique()
    print(f"\nSample Unmatched Players ({len(unmatched)}):")
    print(unmatched[:20])

if __name__ == "__main__":
    main()
