import pandas as pd
import nfl_data_py as nfl
import os

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, '../data/pff_ihop_analysis_results.csv')
OUTPUT_FILE = os.path.join(SCRIPT_DIR, '../data/pff_ihop_analysis_results_with_experience.csv')

def main():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return

    print(f"Loading PFF data from {DATA_FILE}...")
    df = pd.read_csv(DATA_FILE)
    
    # Calculate Years in PFF (Proxy for Experience)
    # YearsInPFF = Season - First Season in Dataset
    
    print("Calculating Years in PFF...")
    
    # Ensure Season is numeric
    df['Season'] = pd.to_numeric(df['Season'], errors='coerce')
    
    # Find first season for each player
    first_seasons = df.groupby('Player')['Season'].min().reset_index()
    first_seasons.rename(columns={'Season': 'FirstSeason'}, inplace=True)
    
    # Merge back
    merged_df = df.merge(first_seasons, on='Player', how='left')
    
    # Calculate YearsInPFF
    merged_df['YearsInPFF'] = merged_df['Season'] - merged_df['FirstSeason']
    
    # Save
    merged_df.to_csv(OUTPUT_FILE, index=False)
    print(f"Saved data with YearsInPFF to {OUTPUT_FILE}")
    
    # Preview
    print(merged_df[['Player', 'Season', 'FirstSeason', 'YearsInPFF']].head(10))
    
    # Check distribution
    print("\nYearsInPFF Distribution:")
    print(merged_df['YearsInPFF'].value_counts().sort_index().head(10))

if __name__ == "__main__":
    main()
