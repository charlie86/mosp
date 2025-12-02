import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from scipy import stats
import numpy as np

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, '../data/pff_ihop_analysis_results.csv')
REGRESSION_FILE = os.path.join(SCRIPT_DIR, '../data/player_controlled_regression_results.csv')
OUTPUT_DIR = os.path.join(SCRIPT_DIR, '../plots/top_players_driving_time')
os.makedirs(OUTPUT_DIR, exist_ok=True)

def plot_player(df, player_name, metric_col, metric_name, unit, filename_prefix):
    plt.figure(figsize=(12, 8))
    
    # 1. Global Data (Background)
    # Filter for valid data
    global_data = df.dropna(subset=['Grade', metric_col])
    
    # Scatter
    plt.scatter(global_data[metric_col], global_data['Grade'], 
                color='lightgray', alpha=0.3, s=10, label='All Players (Snaps >= 10)')
    
    # Global Regression Line
    slope_g, intercept_g, r_g, p_g, std_err_g = stats.linregress(global_data[metric_col], global_data['Grade'])
    x_vals_g = np.array([global_data[metric_col].min(), global_data[metric_col].max()])
    y_vals_g = intercept_g + slope_g * x_vals_g
    plt.plot(x_vals_g, y_vals_g, color='gray', linestyle='--', linewidth=2, 
             label=f'Global Trend (Slope: {slope_g:.4f})')
    
    # 2. Player Data (Foreground)
    player_data = global_data[global_data['Player'] == player_name]
    
    if not player_data.empty:
        # Scatter
        plt.scatter(player_data[metric_col], player_data['Grade'], 
                    color='#D50A0A', alpha=0.9, s=60, edgecolor='black', label=player_name)
        
        # Player Regression Line
        slope_b, intercept_b, r_b, p_b, std_err_b = stats.linregress(player_data[metric_col], player_data['Grade'])
        x_vals_b = np.array([player_data[metric_col].min(), player_data[metric_col].max()])
        y_vals_b = intercept_b + slope_b * x_vals_b
        plt.plot(x_vals_b, y_vals_b, color='#D50A0A', linestyle='-', linewidth=3, 
                 label=f'{player_name} Trend (Slope: {slope_b:.4f})')
    
    # Formatting
    plt.title(f'Impact of IHOP Proximity: Global vs. {player_name}\nMetric: {metric_name}', fontsize=16, fontweight='bold')
    plt.xlabel(f'{metric_name} ({unit})', fontsize=12)
    plt.ylabel('PFF Run Block Grade', fontsize=12)
    plt.legend(fontsize=10, loc='upper right')
    plt.grid(True, alpha=0.3)
    
    # Annotations
    plt.text(0.02, 0.98, f"Global N: {len(global_data)}\n{player_name} N: {len(player_data)}", 
             transform=plt.gca().transAxes, verticalalignment='top', fontsize=10, 
             bbox=dict(boxstyle='round', facecolor='white', alpha=0.8))
    
    # Save
    safe_name = player_name.replace(' ', '_').replace('.', '').lower()
    filename = f"{filename_prefix}_{safe_name}.png"
    output_path = os.path.join(OUTPUT_DIR, filename)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved plot to {output_path}")
    plt.close()

def main():
    if not os.path.exists(DATA_FILE) or not os.path.exists(REGRESSION_FILE):
        print(f"Error: Data files not found.")
        return

    print(f"Loading data...")
    df = pd.read_csv(DATA_FILE)
    reg_df = pd.read_csv(REGRESSION_FILE)
    
    # Prepare Data
    df['Grade'] = pd.to_numeric(df['Grade'], errors='coerce')
    df['DrivingTimeSeconds'] = pd.to_numeric(df['DrivingTimeSeconds'], errors='coerce')
    df['SnapCount_RunBlock'] = pd.to_numeric(df['SnapCount_RunBlock'], errors='coerce')
    
    # Filter: Snaps >= 10
    df = df[df['SnapCount_RunBlock'] >= 10]
    
    # Convert to Minutes
    df['DrivingTimeMinutes'] = df['DrivingTimeSeconds'] / 60.0
    
    # Identify Leaders (DrivingTime)
    metric_name = 'DrivingTime'
    subset = reg_df[(reg_df['Metric'] == metric_name) & (reg_df['Dist_PValue'] <= 0.05)]
    
    if subset.empty:
        print("No significant players found.")
        return

    # Top 5 Negative (Closer is Better)
    top_negative = subset.sort_values(by='Dist_Coef', ascending=True).head(5)['Player'].tolist()
    print(f"Top 5 Negative (Closer is Better): {top_negative}")
    
    # Top 5 Positive (Farther is Better)
    top_positive = subset.sort_values(by='Dist_Coef', ascending=False).head(5)['Player'].tolist()
    print(f"Top 5 Positive (Farther is Better): {top_positive}")
    
    # Generate Plots
    for player in top_negative:
        plot_player(df, player, 'DrivingTimeMinutes', 'Driving Time', 'Minutes', 'negative_slope')
        
    for player in top_positive:
        plot_player(df, player, 'DrivingTimeMinutes', 'Driving Time', 'Minutes', 'positive_slope')

if __name__ == "__main__":
    main()
