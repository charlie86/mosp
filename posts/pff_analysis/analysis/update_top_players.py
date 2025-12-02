import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import os
from scipy import stats
import numpy as np
import shutil

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, '../data/pff_ihop_analysis_results_final.csv')
REGRESSION_FILE = os.path.join(SCRIPT_DIR, '../data/player_controlled_regression_results.csv')
PLOT_DIR = os.path.join(SCRIPT_DIR, '../plots/top_players_driving_time')
HTML_FILE = os.path.join(SCRIPT_DIR, 'top_players_report.html')

def cleanup_plots():
    if os.path.exists(PLOT_DIR):
        print(f"Cleaning up {PLOT_DIR}...")
        shutil.rmtree(PLOT_DIR)
    os.makedirs(PLOT_DIR, exist_ok=True)

def generate_html_table(negative_df, positive_df):
    html = """
    <html>
    <head>
        <style>
            body { font-family: sans-serif; }
            table { border-collapse: collapse; width: 100%; margin-bottom: 20px; }
            th, td { border: 1px solid #ddd; padding: 8px; text-align: left; }
            th { background-color: #f2f2f2; }
            h2 { color: #333; }
            .negative { color: #D50A0A; }
            .positive { color: #008000; }
        </style>
    </head>
    <body>
        <h1>Top Players: IHOP Proximity Impact (Driving Time)</h1>
        <p>Regression Model: Grade ~ DrivingTime + IsHome + YearsInLeague + YearsInLeague^2 + OppRunDefGrade</p>
        
        <h2 class="negative">Top 5: Closer is Better (Negative Slope)</h2>
        <table>
            <tr>
                <th>Player</th>
                <th>Dist Coef</th>
                <th>P-Value</th>
                <th>IsHome Coef</th>
                <th>Exp Coef</th>
                <th>Exp^2 Coef</th>
                <th>OppRunDef Coef</th>
                <th>Games</th>
            </tr>
    """
    
    for _, row in negative_df.iterrows():
        html += f"""
            <tr>
                <td>{row['Player']}</td>
                <td>{row['Dist_Coef']:.4f}</td>
                <td>{row['Dist_PValue']:.4f}</td>
                <td>{row['IsHome_Coef']:.2f}</td>
                <td>{row['Exp_Coef']:.2f}</td>
                <td>{row.get('Exp_Sq_Coef', 0):.4f}</td>
                <td>{row['OppRunDefGrade_Coef']:.4f}</td>
                <td>{row['N_Games']}</td>
            </tr>
        """
        
    html += """
        </table>
        
        <h2 class="positive">Top 5: Farther is Better (Positive Slope)</h2>
        <table>
            <tr>
                <th>Player</th>
                <th>Dist Coef</th>
                <th>P-Value</th>
                <th>IsHome Coef</th>
                <th>Exp Coef</th>
                <th>Exp^2 Coef</th>
                <th>OppRunDef Coef</th>
                <th>Games</th>
            </tr>
    """
    
    for _, row in positive_df.iterrows():
        html += f"""
            <tr>
                <td>{row['Player']}</td>
                <td>{row['Dist_Coef']:.4f}</td>
                <td>{row['Dist_PValue']:.4f}</td>
                <td>{row['IsHome_Coef']:.2f}</td>
                <td>{row['Exp_Coef']:.2f}</td>
                <td>{row.get('Exp_Sq_Coef', 0):.4f}</td>
                <td>{row['OppRunDefGrade_Coef']:.4f}</td>
                <td>{row['N_Games']}</td>
            </tr>
        """
        
    html += """
        </table>
    </body>
    </html>
    """
    
    with open(HTML_FILE, 'w') as f:
        f.write(html)
    print(f"Saved HTML report to {HTML_FILE}")

def plot_player(df, player_name, metric_col, metric_name, unit, filename_prefix):
    plt.figure(figsize=(12, 8))
    
    # 1. Global Data (Background)
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
    output_path = os.path.join(PLOT_DIR, filename)
    plt.savefig(output_path, dpi=300, bbox_inches='tight')
    print(f"Saved plot to {output_path}")
    plt.close()

def main():
    if not os.path.exists(DATA_FILE) or not os.path.exists(REGRESSION_FILE):
        print(f"Error: Data files not found.")
        return

    # Cleanup
    cleanup_plots()

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
    top_negative = subset.sort_values(by='Dist_Coef', ascending=True).head(5)
    print(f"Top 5 Negative: {top_negative['Player'].tolist()}")
    
    # Top 5 Positive (Farther is Better)
    top_positive = subset.sort_values(by='Dist_Coef', ascending=False).head(5)
    print(f"Top 5 Positive: {top_positive['Player'].tolist()}")
    
    # Generate HTML
    generate_html_table(top_negative, top_positive)
    
    # Generate Plots
    for player in top_negative['Player']:
        plot_player(df, player, 'DrivingTimeMinutes', 'Driving Time', 'Minutes', 'negative_slope')
        
    for player in top_positive['Player']:
        plot_player(df, player, 'DrivingTimeMinutes', 'Driving Time', 'Minutes', 'positive_slope')

if __name__ == "__main__":
    main()
