import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
import numpy as np

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, '../data/pff_ihop_analysis_results_final.csv')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '../plots')

def main():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return

    print(f"Loading data from {DATA_FILE}...")
    df = pd.read_csv(DATA_FILE)
    
    # Ensure numeric
    df['Grade'] = pd.to_numeric(df['Grade'], errors='coerce')
    df['YearsInLeague'] = pd.to_numeric(df['YearsInLeague'], errors='coerce')
    df['SnapCount_RunBlock'] = pd.to_numeric(df['SnapCount_RunBlock'], errors='coerce')
    
    # Filter
    df = df.dropna(subset=['Grade', 'YearsInLeague'])
    df = df[df['SnapCount_RunBlock'] >= 10]
    
    # Remove outliers in YearsInLeague (e.g. > 20 is rare and noisy)
    df = df[df['YearsInLeague'] <= 20]
    df = df[df['YearsInLeague'] >= 0]
    
    print(f"Plotting {len(df)} data points...")
    
    # Setup Plot
    plt.figure(figsize=(12, 8))
    sns.set_theme(style="darkgrid")
    
    # Scatter plot with regression line (order=2 for quadratic)
    sns.regplot(
        x='YearsInLeague', 
        y='Grade', 
        data=df, 
        scatter_kws={'alpha': 0.1, 's': 10}, 
        line_kws={'color': 'red'},
        order=2,
        label='Quadratic Fit'
    )
    
    # Also plot mean grade per year for clarity
    mean_grades = df.groupby('YearsInLeague')['Grade'].mean().reset_index()
    plt.plot(mean_grades['YearsInLeague'], mean_grades['Grade'], 'o-', color='yellow', label='Mean Grade', linewidth=2)
    
    plt.title('Run Blocking Grade vs. Years in League (Aging Curve)', fontsize=16)
    plt.xlabel('Years in League', fontsize=12)
    plt.ylabel('PFF Run Block Grade', fontsize=12)
    plt.legend()
    
    output_path = os.path.join(OUTPUT_DIR, 'experience_curve.png')
    plt.savefig(output_path)
    print(f"Saved plot to {output_path}")

if __name__ == "__main__":
    main()
