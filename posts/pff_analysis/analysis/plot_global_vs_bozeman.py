import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from scipy import stats
import numpy as np

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, '../data/pff_ihop_analysis_results.csv')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '../plots')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def plot_metric(df, metric_col, metric_name, unit, filename):
    plt.figure(figsize=(12, 8))
    
    # 1. Global Data (Background)
    # Filter for valid data
    global_data = df.dropna(subset=['Grade', metric_col])
    
    # Scatter
    plt.scatter(global_data[metric_col], global_data['Grade'], 
                color='lightgray', alpha=0.3, s=10, label='All Players (Snaps >= 10)')
    
    # Global Regression Line (Univariate for Visualization)
    slope_g, intercept_g, r_g, p_g, std_err_g = stats.linregress(global_data[metric_col], global_data['Grade'])
    x_vals_g = np.array([global_data[metric_col].min(), global_data[metric_col].max()])
    y_vals_g = intercept_g + slope_g * x_vals_g
    plt.plot(x_vals_g, y_vals_g, color='gray', linestyle='--', linewidth=2, 
             label=f'Global Trend (Slope: {slope_g:.4f})')
    
    # 2. Bradley Bozeman Data (Foreground)
    bozeman_data = global_data[global_data['Player'] == 'Bradley Bozeman']
    
    if not bozeman_data.empty:
        # Scatter
        plt.scatter(bozeman_data[metric_col], bozeman_data['Grade'], 
                    color='#D50A0A', alpha=0.9, s=60, edgecolor='black', label='Bradley Bozeman')
        
        # Bozeman Regression Line
        slope_b, intercept_b, r_b, p_b, std_err_b = stats.linregress(bozeman_data[metric_col], bozeman_data['Grade'])
        x_vals_b = np.array([bozeman_data[metric_col].min(), bozeman_data[metric_col].max()])
        y_vals_b = intercept_b + slope_b * x_vals_b
        plt.plot(x_vals_b, y_vals_b, color='#D50A0A', linestyle='-', linewidth=3, 
                 label=f'Bozeman Trend (Slope: {slope_b:.4f})')
    
    # Formatting
    plt.title(f'Impact of IHOP Proximity: Global vs. Bradley Bozeman\nMetric: {metric_name}', fontsize=16, fontweight='bold')
    plt.xlabel(f'{metric_name} ({unit})', fontsize=12)
    plt.ylabel('PFF Run Block Grade', fontsize=12)
    plt.legend(fontsize=10, loc='upper right')
    plt.grid(True, alpha=0.3)
    
    # Annotations
    plt.text(0.02, 0.98, f"Global N: {len(global_data)}\nBozeman N: {len(bozeman_data)}", 
             transform=plt.gca().transAxes, verticalalignment='top', fontsize=10, 
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Save
    output_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved plot to {output_path}")
    plt.close()

def main():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return

    print(f"Loading data from {DATA_FILE}...")
    df = pd.read_csv(DATA_FILE)
    
    # Ensure numeric
    cols = ['Grade', 'DistToIHOP', 'DrivingDist', 'DrivingTimeSeconds', 'SnapCount_RunBlock']
    for col in cols:
        df[col] = pd.to_numeric(df[col], errors='coerce')
    
    # Filter: Snaps >= 10
    df = df[df['SnapCount_RunBlock'] >= 10]
    
    # Convert Driving Time to Minutes
    df['DrivingTimeMinutes'] = df['DrivingTimeSeconds'] / 60.0
    
    print(f"Filtered data (Snaps >= 10): {len(df)} rows")
    
    # Plot 1: Haversine
    plot_metric(df, 'DistToIHOP', 'Haversine Distance', 'Miles', 'global_vs_bozeman_haversine.png')
    
    # Plot 2: Driving Distance
    plot_metric(df, 'DrivingDist', 'Driving Distance', 'Miles', 'global_vs_bozeman_driving_dist.png')
    
    # Plot 3: Driving Time (Minutes)
    plot_metric(df, 'DrivingTimeMinutes', 'Driving Time', 'Minutes', 'global_vs_bozeman_driving_time.png')

if __name__ == "__main__":
    main()
