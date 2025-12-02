import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os
from adjustText import adjust_text

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, '../data/pff_ihop_analysis_results.csv')
OUTPUT_PLOT = os.path.join(SCRIPT_DIR, '../plots/stadium_impact_scatter.png')

def main():
    # 1. Load Data
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return
    
    df = pd.read_csv(DATA_FILE)
    
    # 2. Filter for All Players (Home & Away)
    # User requested to include home team players.
    # away_df = df[df['IsHome'] == False].copy()
    analysis_df = df.copy()
    
    print(f"Analyzing {len(analysis_df)} player-games (Home & Away).")
    
    # 3. Group by Stadium
    # We want 80th Percentile Grade per Stadium for ALL players
    
    def q80(x):
        return x.quantile(0.8)

    stadium_stats = analysis_df.groupby('Stadium').agg({
        'Grade': q80,
        'DistToIHOP': 'first',
        'DrivingDist': 'first',
        'DrivingTimeSeconds': 'first'
    }).reset_index()
    
    print(f"Aggregated data for {len(stadium_stats)} stadiums.")
    
    # 4. Create Plots
    fig, axes = plt.subplots(1, 3, figsize=(20, 8))
    sns.set_theme(style="whitegrid")
    
    metrics = [
        ('DistToIHOP', 'Haversine Distance (mi)'),
        ('DrivingDist', 'Driving Distance (mi)'),
        ('DrivingTimeSeconds', 'Driving Time (s)')
    ]
    
    for i, (col, label) in enumerate(metrics):
        ax = axes[i]
        
        # Scatterplot
        sns.regplot(
            x=col, y='Grade', data=stadium_stats, ax=ax,
            scatter_kws={'s': 50, 'alpha': 0.7},
            line_kws={'color': 'red', 'alpha': 0.5}
        )
        
        # Labels
        texts = []
        for _, row in stadium_stats.iterrows():
            texts.append(ax.text(row[col], row['Grade'], row['Stadium'], fontsize=8))
            
        # Adjust text to avoid overlap
        try:
            adjust_text(texts, ax=ax, arrowprops=dict(arrowstyle='-', color='gray', lw=0.5))
        except Exception as e:
            print(f"Warning: adjust_text failed for {label}: {e}")
        
        ax.set_title(f'80th Percentile Player Grade (All) vs {label}')
        ax.set_xlabel(label)
        ax.set_ylabel('80th Percentile Player PFF Grade')
        
        # Add correlation
        corr = stadium_stats[col].corr(stadium_stats['Grade'])
        ax.text(0.05, 0.95, f'r = {corr:.2f}', transform=ax.transAxes, 
                bbox=dict(facecolor='white', alpha=0.8))

    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT, dpi=300)
    print(f"Saved stadium impact plot to {OUTPUT_PLOT}")

if __name__ == "__main__":
    main()
