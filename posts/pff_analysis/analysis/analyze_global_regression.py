import pandas as pd
from scipy import stats
import os

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, '../data/pff_ihop_analysis_results.csv')

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
    df['RelativeDrivingDist'] = pd.to_numeric(df['RelativeDrivingDist'], errors='coerce')
    df['RelativeDrivingTimeSeconds'] = pd.to_numeric(df['RelativeDrivingTimeSeconds'], errors='coerce')
    df['SnapCount_RunBlock'] = pd.to_numeric(df['SnapCount_RunBlock'], errors='coerce')
    
    # Filter 1: Observation Level (Snaps >= 10)
    df = df[df['SnapCount_RunBlock'] >= 10]
    print(f"Rows after Snap Count Filter (>= 10): {len(df)}")
    
    # Identify Veterans (>= 100 Total Games)
    player_counts = df['Player'].value_counts()
    veterans = player_counts[player_counts >= 100].index
    print(f"Identified {len(veterans)} veterans with >= 100 total games.")
    
    # Filter for Veterans
    df = df[df['Player'].isin(veterans)]
    
    # Filter 2: Remove Home Games
    df = df[df['IsHome'] == False]
    print(f"Rows after Removing Home Games (Veterans Only): {len(df)}")
    
    print(f"Rows after Game Count Filter (>= 100 games): {len(df)}")
    print(f"Unique Players: {len(df['Player'].unique())}")
    
    metrics = [
        ('RelativeDistToIHOP', 'Haversine Distance'),
        ('RelativeDrivingDist', 'Driving Distance'),
        ('RelativeDrivingTimeSeconds', 'Driving Time')
    ]
    
    print("\n" + "="*60)
    print("GLOBAL REGRESSION ANALYSIS (Veterans: 100+ Games)")
    print("="*60)
    
    for metric_col, metric_name in metrics:
        # Drop NaNs for this specific metric
        metric_df = df.dropna(subset=['Grade', metric_col])
        
        x = metric_df[metric_col]
        y = metric_df['Grade']
        
        slope, intercept, r_value, p_value, std_err = stats.linregress(x, y)
        
        print(f"\nMETRIC: {metric_name}")
        print(f"Observations: {len(metric_df)}")
        print(f"Slope:        {slope:.6f}")
        print(f"Intercept:    {intercept:.6f}")
        print(f"R-Squared:    {r_value**2:.6f}")
        print(f"P-Value:      {p_value:.6f}")
        print(f"Std Error:    {std_err:.6f}")
        
        if p_value <= 0.05:
            direction = "CLOSER is Better" if slope < 0 else "FARTHER is Better"
            print(f"Result:       SIGNIFICANT ({direction})")
        else:
            print(f"Result:       NOT Significant")

if __name__ == "__main__":
    main()
