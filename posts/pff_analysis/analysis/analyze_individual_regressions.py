import pandas as pd
import numpy as np
from scipy import stats
import os

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, '../data/pff_ihop_analysis_results.csv')
OUTPUT_CSV = os.path.join(SCRIPT_DIR, '../data/player_regression_results.csv')

def main():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return

    print(f"Loading data from {DATA_FILE}...")
    df = pd.read_csv(DATA_FILE)
    
    # Required columns
    req_cols = ['Player', 'Grade', 'RelativeDistToIHOP', 'SnapCount_RunBlock', 'IsHome']
    if not all(col in df.columns for col in req_cols):
        print(f"Error: Missing columns. Need {req_cols}")
        return

    # Ensure numeric
    df['Grade'] = pd.to_numeric(df['Grade'], errors='coerce')
    df['RelativeDistToIHOP'] = pd.to_numeric(df['RelativeDistToIHOP'], errors='coerce')
    df['SnapCount_RunBlock'] = pd.to_numeric(df['SnapCount_RunBlock'], errors='coerce')
    
    # Filter 1: Observation Level (Snaps >= 10)
    df = df[df['SnapCount_RunBlock'] >= 10]
    
    # Identify Veterans (>= 100 Total Games)
    player_counts = df['Player'].value_counts()
    veterans = player_counts[player_counts >= 100].index
    print(f"Identified {len(veterans)} veterans with >= 100 total games.")
    
    # Filter for Veterans
    df = df[df['Player'].isin(veterans)]
    
    # Filter 2: Remove Home Games (Analyze Away Performance)
    df = df[df['IsHome'] == False]
    print(f"Data loaded and filtered (Snaps >= 10, Veterans Only, Away Games Only): {len(df)} rows.")
    
    # Metrics to analyze
    metrics = [
        ('RelativeDistToIHOP', 'Haversine'),
        ('RelativeDrivingDist', 'DrivingDist'),
        ('RelativeDrivingTimeSeconds', 'DrivingTime')
    ]
    
    results = []
    
    players = df['Player'].unique()
    print(f"Analyzing {len(players)} veterans across {len(metrics)} metrics...")
    
    for metric_col, metric_name in metrics:
        print(f"  -> Processing {metric_name}...")
        
        # Drop NaNs for this specific metric
        metric_df = df.dropna(subset=['Grade', metric_col])
        
        for player in players:
            player_df = metric_df[metric_df['Player'] == player]
            
            n = len(player_df)
            
            # Ensure enough data points for regression (e.g., >= 20 away games)
            if n < 20:
                continue
                
            x = player_df[metric_col]
            y = player_df['Grade']
            
            # Check for variance in X
            if x.nunique() < 2:
                continue
                
            # Linear Regression
            try:
                slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
                
                results.append({
                    'Player': player,
                    'Metric': metric_name,
                    'Slope': slope,
                    'Intercept': intercept,
                    'R_Squared': r_value**2,
                    'P_Value': p_value,
                    'Std_Err': std_err,
                    'N_Games': n,
                    'Mean_Grade': y.mean(),
                    'Mean_Metric_Val': x.mean()
                })
            except Exception:
                continue
        
    results_df = pd.DataFrame(results)
    
    # Sort by Slope (Most Negative first = Strongest "Closer is Better" effect)
    results_df = results_df.sort_values(by=['Metric', 'Slope'], ascending=[True, True])
    
    # Save
    results_df.to_csv(OUTPUT_CSV, index=False)
    print(f"Saved regression results to {OUTPUT_CSV}")
    
    # Preview for each metric
    for _, metric_name in metrics:
        print(f"\n--- Top 5 'Closer is Better' (Negative Slope) - {metric_name} ---")
        subset = results_df[results_df['Metric'] == metric_name].sort_values(by='Slope')
        print(subset.head(5)[['Player', 'Slope', 'P_Value', 'N_Games']])

if __name__ == "__main__":
    main()
