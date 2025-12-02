import pandas as pd
import os

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_DATA_FILE = os.path.join(SCRIPT_DIR, '../data/pff_ihop_analysis_results_with_draft_year.csv')
TEAM_STATS_FILE = os.path.join(SCRIPT_DIR, '../data/pff_team_defense_grades.csv')
OUTPUT_FILE = os.path.join(SCRIPT_DIR, '../data/pff_ihop_analysis_results_final.csv')

def main():
    if not os.path.exists(MAIN_DATA_FILE):
        print(f"Error: {MAIN_DATA_FILE} not found.")
        return
    if not os.path.exists(TEAM_STATS_FILE):
        print(f"Error: {TEAM_STATS_FILE} not found.")
        return

    print(f"Loading main data from {MAIN_DATA_FILE}...")
    df = pd.read_csv(MAIN_DATA_FILE)
    
    print(f"Loading team stats from {TEAM_STATS_FILE}...")
    team_df = pd.read_csv(TEAM_STATS_FILE)
    
    # Ensure Season is int
    df['Season'] = pd.to_numeric(df['Season'], errors='coerce').astype('Int64')
    team_df['Season'] = pd.to_numeric(team_df['Season'], errors='coerce').astype('Int64')
    
    # Ensure Team/Opponent are strings
    df['Opponent'] = df['Opponent'].astype(str)
    team_df['Team'] = team_df['Team'].astype(str)
    
    print("Dtypes - Main:")
    print(df[['Season', 'Opponent']].dtypes)
    print("Dtypes - Team:")
    print(team_df[['Season', 'Team']].dtypes)
    
    # Merge
    # Main Data has 'Opponent' and 'Season'
    # Team Stats has 'Team' and 'Season'
    
    print("Merging data...")
    merged_df = df.merge(
        team_df, 
        left_on=['Opponent', 'Season'], 
        right_on=['Team', 'Season'], 
        how='left'
    )
    
    # Check match rate
    total_rows = len(merged_df)
    matched_rows = merged_df['OppRunDefGrade'].notna().sum()
    print(f"Matched {matched_rows} / {total_rows} rows ({matched_rows/total_rows:.1%})")
    
    if matched_rows < total_rows:
        print("\nSample Unmatched Opponents:")
        unmatched = merged_df[merged_df['OppRunDefGrade'].isna()][['Opponent', 'Season']].drop_duplicates().head(10)
        print(unmatched)
    
    # Save
    merged_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved final dataset to {OUTPUT_FILE}")

if __name__ == "__main__":
    main()
