import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, '../data/pff_ihop_analysis_results.csv')
OUTPUT_PLOT = os.path.join(SCRIPT_DIR, '../plots/ihop_vs_grade_scatter.png')

def main():
    # 1. Load Data
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return
    
    df = pd.read_csv(DATA_FILE)
    
    # Filter out missing data
    df = df.dropna(subset=['DistToIHOP', 'Grade'])
    
    # 2. Setup Plot
    plt.figure(figsize=(10, 6))
    sns.set_theme(style="whitegrid")
    
    # 3. Create Scatterplot
    sns.regplot(
        x='DistToIHOP', 
        y='Grade', 
        data=df, 
        scatter_kws={'alpha':0.5, 's': 20}, 
        line_kws={'color': 'red'}
    )
    
    # 4. Styling
    plt.title('PFF Run Blocking Grade vs. Proximity to IHOP', fontsize=16)
    plt.xlabel('Distance to Nearest IHOP (Miles)', fontsize=12)
    plt.ylabel('PFF Run Blocking Grade', fontsize=12)
    
    # Add correlation coefficient to plot
    corr = df['DistToIHOP'].corr(df['Grade'])
    plt.text(
        0.05, 0.95, 
        f'Correlation: {corr:.3f}', 
        transform=plt.gca().transAxes, 
        fontsize=12, 
        verticalalignment='top', 
        bbox=dict(boxstyle='round', facecolor='white', alpha=0.5)
    )
    
    # 5. Save
    plt.tight_layout()
    plt.savefig(OUTPUT_PLOT, dpi=300)
    print(f"Plot saved to {OUTPUT_PLOT}")

if __name__ == "__main__":
    main()
