import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, '../data/pff_run_blocking_data_2006_2025_positions.csv')
OUTPUT_PLOT = os.path.join(SCRIPT_DIR, '../plots/run_block_snaps_distribution.png')

def main():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return

    print(f"Loading data from {DATA_FILE}...")
    df = pd.read_csv(DATA_FILE)
    
    if 'SnapCount_RunBlock' not in df.columns:
        print("Error: 'SnapCount_RunBlock' column not found.")
        return

    # Ensure numeric
    df['SnapCount_RunBlock'] = pd.to_numeric(df['SnapCount_RunBlock'], errors='coerce')
    df = df.dropna(subset=['SnapCount_RunBlock'])

    # Descriptive Statistics
    stats = df['SnapCount_RunBlock'].describe()
    print("\n--- Run Block Snaps Distribution ---")
    print(stats)
    
    # Percentiles
    percentiles = [0.1, 0.25, 0.5, 0.75, 0.9, 0.95, 0.99]
    print("\n--- Percentiles ---")
    print(df['SnapCount_RunBlock'].quantile(percentiles))

    # Visualization
    plt.figure(figsize=(10, 6))
    sns.histplot(df['SnapCount_RunBlock'], binwidth=1, kde=True)
    plt.title('Distribution of Run Block Snaps (2006-2025)')
    plt.xlabel('Run Block Snaps')
    plt.ylabel('Frequency')
    plt.grid(True, alpha=0.3)
    
    os.makedirs(os.path.dirname(OUTPUT_PLOT), exist_ok=True)
    plt.savefig(OUTPUT_PLOT, dpi=300)
    print(f"\nSaved distribution plot to {OUTPUT_PLOT}")

if __name__ == "__main__":
    main()
