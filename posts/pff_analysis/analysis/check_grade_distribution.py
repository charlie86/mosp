import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, '../data/pff_ihop_analysis_results.csv')
OUTPUT_PLOT = os.path.join(SCRIPT_DIR, '../plots/grade_distribution.png')

def main():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return
    
    df = pd.read_csv(DATA_FILE)
    
    # Analyze 60.0 grades
    total_rows = len(df)
    exact_60 = df[df['Grade'] == 60.0]
    count_60 = len(exact_60)
    percent_60 = (count_60 / total_rows) * 100
    
    print(f"Total Grades: {total_rows}")
    print(f"Grades exactly 60.0: {count_60} ({percent_60:.2f}%)")
    
    # Plot Distribution of All Game Grades
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")
    
    sns.histplot(df['Grade'], bins=50, kde=True, color='skyblue', edgecolor='black')
    
    plt.title('Distribution of All PFF Run Blocking Grades (Game Level)', fontsize=16)
    plt.xlabel('Grade', fontsize=12)
    plt.ylabel('Frequency', fontsize=12)
    
    # Add text box with 60.0 stats
    plt.text(
        0.95, 0.95, 
        f'Total Games: {total_rows}\nExactly 60.0: {count_60} ({percent_60:.1f}%)', 
        transform=plt.gca().transAxes, 
        fontsize=12, 
        verticalalignment='top', 
        horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)
    )
    
    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT, dpi=300)
    print(f"Saved game-level distribution plot to {OUTPUT_PLOT}")

    # --- New: Player Median Distribution ---
    OUTPUT_PLOT_MEDIAN = os.path.join(SCRIPT_DIR, '../plots/player_median_grade_distribution.png')
    
    player_medians = df.groupby('Player')['Grade'].median()
    
    plt.figure(figsize=(10, 6))
    sns.histplot(player_medians, bins=50, kde=True, color='lightgreen', edgecolor='black')
    
    plt.title('Distribution of Median PFF Run Blocking Grades (Player Level)', fontsize=16)
    plt.xlabel('Median Grade', fontsize=12)
    plt.ylabel('Number of Players', fontsize=12)
    
    # Add stats
    mean_median = player_medians.mean()
    median_median = player_medians.median()
    
    plt.text(
        0.95, 0.95, 
        f'Total Players: {len(player_medians)}\nMean of Medians: {mean_median:.1f}\nMedian of Medians: {median_median:.1f}', 
        transform=plt.gca().transAxes, 
        fontsize=12, 
        verticalalignment='top', 
        horizontalalignment='right',
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.8)
    )
    
    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT_MEDIAN, dpi=300)
    print(f"Saved player median distribution plot to {OUTPUT_PLOT_MEDIAN}")

if __name__ == "__main__":
    main()
