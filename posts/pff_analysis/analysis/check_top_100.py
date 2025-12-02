import pandas as pd
import os

SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, '../data/pff_ihop_analysis_results.csv')

if not os.path.exists(DATA_FILE):
    print(f"Error: {DATA_FILE} not found.")
else:
    df = pd.read_csv(DATA_FILE)
    print(f"Data Shape: {df.shape}")
    if 'Season' in df.columns:
        print(f"Seasons: {sorted(df['Season'].unique())}")
    
    # Current Logic
    print("\n--- Current Top 10 (Median Grade) ---")
    player_medians = df.groupby('Player')['Grade'].median().sort_values(ascending=False)
    top_10 = player_medians.head(10)
    
    for player, grade in top_10.items():
        games = len(df[df['Player'] == player])
        print(f"{player}: {grade:.1f} ({games} games)")

    # Logic with Min Games
    print("\n--- Top 10 (Median Grade, Min 20 Games) ---")
    player_counts = df.groupby('Player')['Grade'].count()
    valid_players = player_counts[player_counts >= 20].index
    
    df_filtered = df[df['Player'].isin(valid_players)]
    player_medians_filtered = df_filtered.groupby('Player')['Grade'].median().sort_values(ascending=False)
    top_10_filtered = player_medians_filtered.head(10)
    
    for player, grade in top_10_filtered.items():
        games = len(df[df['Player'] == player])
        print(f"{player}: {grade:.1f} ({games} games)")
