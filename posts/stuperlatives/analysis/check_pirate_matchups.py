
import sys
import os
import pandas as pd

# Add path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from posts.stuperlatives.etl.fetch_data import fetch_schedules

# Include OAK for historical accuracy
PIRATE_TEAMS = ['TB', 'LV', 'MIN', 'OAK']

def check_matchups():
    print("Fetching schedules (1999-2025)...")
    df = fetch_schedules(list(range(1999, 2026)))
    
    pirate_games = df[
        (df['home_team'].isin(PIRATE_TEAMS)) & 
        (df['away_team'].isin(PIRATE_TEAMS))
    ].copy()
    
    print(f"\nTotal Pirate vs Pirate Games: {len(pirate_games)}\n")
    
    # Standardize matchups (alphabetical order) to count unique pairings
    matchups = []
    for _, game in pirate_games.iterrows():
        teams = sorted([game['home_team'], game['away_team']])
        matchups.append(f"{teams[0]} vs {teams[1]}")
        
    pirate_games['matchup'] = matchups
    
    counts = pirate_games['matchup'].value_counts()
    print(counts)
    
    # Detailed list by season
    print("\nRecent Games:")
    print(pirate_games[['season', 'week', 'home_team', 'away_team', 'result']].sort_values(['season', 'week'], ascending=False).head(20))

if __name__ == "__main__":
    check_matchups()
