import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, '../data/pff_run_blocking_data_2006_2025_positions.csv')
OUTPUT_PLOT = os.path.join(SCRIPT_DIR, '../plots/games_played_distribution.png')

def main():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return

    print(f"Loading data from {DATA_FILE}...")
    df = pd.read_csv(DATA_FILE)
    
    # Apply the same filter as the main analysis
    if 'SnapCount_RunBlock' in df.columns:
        df['SnapCount_RunBlock'] = pd.to_numeric(df['SnapCount_RunBlock'], errors='coerce')
        original_len = len(df)
        df = df[df['SnapCount_RunBlock'] >= 10]
        print(f"Filtered from {original_len} to {len(df)} rows (RunBlock Snaps >= 10).")
    
    # Calculate Games Played per Player
    games_per_player = df.groupby('Player').size()
    
    # Descriptive Statistics
    stats = games_per_player.describe()
    print("\n--- Games Played per Player Distribution ---")
    print(stats)
    
    # Percentiles
    percentiles = [0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]
    print("\n--- Percentiles ---")
    print(games_per_player.quantile(percentiles))

    # Visualization
    plt.figure(figsize=(10, 6))
    sns.histplot(games_per_player, binwidth=1, kde=True) # Binwidth 1 for granular view
    plt.title('Distribution of Games Played per Player (Run Block Snaps >= 10)')
    plt.xlabel('Games Played')
    plt.ylabel('Frequency (Players)')
    plt.grid(True, alpha=0.3)
    
    os.makedirs(os.path.dirname(OUTPUT_PLOT), exist_ok=True)
    plt.savefig(OUTPUT_PLOT, dpi=300)
    print(f"\nSaved distribution plot to {OUTPUT_PLOT}")

if __name__ == "__main__":
    main()
