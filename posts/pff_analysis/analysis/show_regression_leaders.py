import pandas as pd
import os

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, '../data/player_controlled_regression_results.csv')

def main():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return

    df = pd.read_csv(DATA_FILE)
    
    metrics = [
        ('Haversine', 'Haversine Distance'),
        ('DrivingDist', 'Driving Distance'),
        ('DrivingTime', 'Driving Time')
    ]
    
    for metric_key, metric_name in metrics:
        print(f"\n{'='*60}")
        print(f"METRIC: {metric_name}")
        print(f"{'='*60}")
        
        subset = df[(df['Metric'] == metric_key) & (df['Dist_PValue'] <= 0.05)]
        
        if subset.empty:
            print(f"No significant data (p<=0.05) found for metric: {metric_key}")
            continue
            
        # Top 5 "Closer is Better" (Most Negative Slope)
        print(f"\n--- Top 5: Closer to IHOP = Better Grade (Negative Slope, p<=0.05) ---")
        top_closer = subset.sort_values(by='Dist_Coef', ascending=True).head(5)
        print(top_closer[['Player', 'Dist_Coef', 'Dist_PValue', 'IsHome_Coef', 'Exp_Coef', 'OppRunDefGrade_Coef', 'N_Games']].to_string(index=False))
        
        # Top 5 "Farther is Better" (Most Positive Slope)
        print(f"\n--- Top 5: Farther from IHOP = Better Grade (Positive Slope, p<=0.05) ---")
        top_farther = subset.sort_values(by='Dist_Coef', ascending=False).head(5)
        print(top_farther[['Player', 'Dist_Coef', 'Dist_PValue', 'IsHome_Coef', 'Exp_Coef', 'OppRunDefGrade_Coef', 'N_Games']].to_string(index=False))

if __name__ == "__main__":
    main()
