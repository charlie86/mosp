import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import os

# --- Configuration ---
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
DATA_FILE = os.path.join(SCRIPT_DIR, '../data/nfl_stadium_ihop_distances.csv')



def create_bar_chart(df, col, title, ylabel, filename):
    plt.figure(figsize=(12, 10))
    
    # Sort by the metric
    df_sorted = df.sort_values(by=col, ascending=True)
    
    sns.barplot(x=col, y='Stadium', data=df_sorted, palette='viridis')
    
    plt.title(title, fontsize=16)
    plt.xlabel(ylabel, fontsize=12)
    plt.ylabel('Stadium', fontsize=12)
    plt.tight_layout()
    
    output_path = os.path.join(SCRIPT_DIR, '../plots', filename)
    plt.savefig(output_path, dpi=300)
    print(f"Saved {filename}")

def main():
    if not os.path.exists(DATA_FILE):
        print(f"Error: {DATA_FILE} not found.")
        return

    df = pd.read_csv(DATA_FILE)
    

    
    # 1. Haversine Distance
    create_bar_chart(
        df.dropna(subset=['HaversineDist']), 
        'HaversineDist', 
        'Distance to Nearest IHOP (Haversine)', 
        'Distance (Miles)', 
        'stadium_haversine_distances.png'
    )
    
    # 2. Driving Distance
    create_bar_chart(
        df.dropna(subset=['DrivingDist']), 
        'DrivingDist', 
        'Driving Distance to Nearest IHOP', 
        'Distance (Miles)', 
        'stadium_driving_distances.png'
    )
    
    # 3. Driving Time (Seconds)
    create_bar_chart(
        df.dropna(subset=['DrivingTimeSeconds']), 
        'DrivingTimeSeconds', 
        'Driving Time to Nearest IHOP', 
        'Time (Seconds)', 
        'stadium_driving_times.png'
    )

if __name__ == "__main__":
    main()
