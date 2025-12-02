import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, '../data/pff_ihop_analysis_results.csv')
OUTPUT_BAR_CHART = os.path.join(SCRIPT_DIR, '../plots/ihop_effect_top_players.png')
OUTPUT_SCATTER = os.path.join(SCRIPT_DIR, '../plots/ihop_dist_vs_performance_delta.png')
OUTPUT_SCATTER_RAW = os.path.join(SCRIPT_DIR, '../plots/ihop_dist_vs_raw_grade.png')

IHOP_CLOSE_THRESHOLD = 2.0 # Miles

def parse_driving_time(time_str):
    if pd.isna(time_str):
        return None
    try:
        # Format is usually "X mins" or "X hours Y mins"
        total_mins = 0
        parts = time_str.split()
        for i, part in enumerate(parts):
            if 'hour' in part:
                total_mins += int(parts[i-1]) * 60
            elif 'min' in part:
                total_mins += int(parts[i-1])
        return total_mins
    except:
        return None

def calculate_effect(df, metric_col, threshold, metric_name):
    print(f"\n--- Calculating Effect for {metric_name} (Threshold: {threshold}) ---")
    
    # Filter for Away Games Only
    away_df = df[df['IsHome'] == False].copy()
    print(f"  -> Analyzing {len(away_df)} away games.")
    
    # Define "Better Access" (Closer than home) vs "Worse/Same Access"
    # RelativeDist < -Threshold means significantly closer than home (Better)
    # RelativeDist > Threshold means significantly farther (Worse)
    # Let's try a simple split: Is it closer than home?
    # Or stick to the user's "relative difference" request.
    # "distances to ihop to only be calculated for away games, based on the relative difference"
    
    # Let's define "IsClose" as "Is Closer Than Home" (Relative < 0)
    # Or maybe "Is Significantly Closer" (Relative < -1 mile)
    # Let's use the threshold as a "Better by X" metric.
    # If threshold is 0, then any improvement counts.
    
    away_df['IsBetterAccess'] = away_df[metric_col] < -threshold
    
    player_split = away_df.groupby(['Player', 'IsBetterAccess'])['Grade'].mean().unstack()
    
    if True in player_split.columns and False in player_split.columns:
        # Effect = Grade(Better Access) - Grade(Worse/Same Access)
        player_split['Effect'] = player_split[True] - player_split[False]
        
        player_counts = away_df.groupby(['Player', 'IsBetterAccess'])['Grade'].count().unstack()
        valid_players = player_counts[(player_counts[True] >= 1) & (player_counts[False] >= 1)].index
        
        effect_df = player_split.loc[valid_players].reset_index()
        effect_df = effect_df.sort_values(by='Effect', ascending=False)
        
        print(f"Found {len(effect_df)} valid players.")
        return effect_df
    else:
        print("Not enough data.")
        return None

def main():
    # 1. Load Data
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return
    
    df = pd.read_csv(DATA_FILE)
    
    # Parse Driving Time (if needed, but we have Seconds now)
    # df['DrivingTimeMins'] = df['DrivingTime'].apply(parse_driving_time)
    
    # Filter for valid data
    # We need Relative metrics now
    required_cols = ['RelativeDistToIHOP', 'RelativeDrivingDist', 'RelativeDrivingTimeSeconds', 'Grade', 'IsHome']
    # Check if columns exist
    if not all(col in df.columns for col in required_cols):
        print(f"Error: Missing required columns. Found: {df.columns.tolist()}")
        return

    df = df.dropna(subset=required_cols)
    
    # 2. Calculate Player Baselines (using ONLY Away games as requested)
    # Filter for away games to calculate the baseline
    away_only_df = df[df['IsHome'] == False]
    player_stats = away_only_df.groupby('Player')['Grade'].agg(['mean', 'count']).reset_index()
    player_stats.rename(columns={'mean': 'BaselineGrade', 'count': 'TotalGames'}, inplace=True)
    
    # Merge baseline back to the main df
    df = df.merge(player_stats, on='Player', how='left')
    
    # Calculate GradeDelta (Performance vs Their Average Away Performance)
    df['GradeDelta'] = df['Grade'] - df['BaselineGrade']
    
    # 3. Calculate Effects (Away Games Only)
    # Thresholds: How much *closer* than home to count as "Better"?
    # Let's say 0 for now (any improvement).
    # Or maybe a small buffer.
    
    effects = {}
    effects['Haversine'] = calculate_effect(df, 'RelativeDistToIHOP', 0.5, 'Relative Haversine (< -0.5mi)')
    effects['DrivingDist'] = calculate_effect(df, 'RelativeDrivingDist', 1.0, 'Relative Driving Dist (< -1.0mi)')
    effects['DrivingTime'] = calculate_effect(df, 'RelativeDrivingTimeSeconds', 300, 'Relative Driving Time (< -5min)')
    
    # 4. Visualization: Top 5 for each metric
    fig, axes = plt.subplots(1, 3, figsize=(18, 8))
    
    metrics = [('Haversine', 'Better Haversine Access'), 
               ('DrivingDist', 'Better Driving Dist Access'), 
               ('DrivingTime', 'Better Driving Time Access')]
    
    for i, (key, title) in enumerate(metrics):
        if effects[key] is not None:
            top_5 = effects[key].head(5)
            sns.barplot(x='Effect', y='Player', data=top_5, ax=axes[i], palette='viridis')
            axes[i].set_title(title)
            axes[i].set_xlabel('Grade Boost (vs Worse Access)')
            axes[i].set_ylabel('')
    
    plt.tight_layout()
    plt.savefig(OUTPUT_BAR_CHART, dpi=300)
    print(f"Saved combined bar chart to {OUTPUT_BAR_CHART}")

    # 5. Scatterplots (Normalized) - Away Games Only
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    scatter_metrics = [('RelativeDistToIHOP', 'Relative Haversine (mi)'), 
                       ('RelativeDrivingDist', 'Relative Driving Dist (mi)'), 
                       ('RelativeDrivingTimeSeconds', 'Relative Driving Time (s)')]
    
    away_df = df[df['IsHome'] == False]
    
    for i, (col, title) in enumerate(scatter_metrics):
        sns.regplot(x=col, y='GradeDelta', data=away_df, ax=axes[i], 
                    scatter_kws={'alpha':0.3, 's': 15}, line_kws={'color': 'red'})
        axes[i].set_title(f'Performance vs {title}')
        axes[i].set_xlabel(title + ' (Negative = Closer than Home)')
        axes[i].set_ylabel('Grade Delta')
        axes[i].axhline(0, color='black', linestyle='--', linewidth=1)
        axes[i].axvline(0, color='black', linestyle=':', linewidth=1)

    plt.tight_layout()
    plt.savefig(OUTPUT_SCATTER, dpi=300)
    print(f"Saved combined scatterplot to {OUTPUT_SCATTER}")

    # 6. Scatterplots (Raw Grade) - Away Games Only
    fig, axes = plt.subplots(1, 3, figsize=(18, 6))
    
    for i, (col, title) in enumerate(scatter_metrics):
        sns.regplot(x=col, y='Grade', data=away_df, ax=axes[i], 
                    scatter_kws={'alpha':0.3, 's': 15}, line_kws={'color': 'blue'})
        axes[i].set_title(f'Raw Grade vs {title}')
        axes[i].set_xlabel(title + ' (Negative = Closer than Home)')
        axes[i].set_ylabel('Raw PFF Grade')
        axes[i].axvline(0, color='black', linestyle=':', linewidth=1)

    plt.tight_layout()
    plt.savefig(OUTPUT_SCATTER_RAW, dpi=300)
    print(f"Saved raw grade scatterplot to {OUTPUT_SCATTER_RAW}")

if __name__ == "__main__":
    main()
