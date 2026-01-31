import os
import math
import pandas as pd
from google.cloud import bigquery
from google.oauth2 import service_account

# --- Configuration ---
BQ_PROJECT = "gen-lang-client-0400686052"
BQ_TABLE = "stuperlatives.coffee_wars"
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
GRAVITY_CONSTANT = 1.0 # Arbitrary scalar
EPSILON_MILES = 0.1 # Minimum distance to prevent division by zero (and cap max gravity)
POWER = 2 # Inverse Square Law

def get_bq_client():
    try:
        possible_keys = [
            'shhhh/service_account.json',
            '../../../shhhh/service_account.json',
            os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')
        ]
        key_path = next((p for p in possible_keys if os.path.exists(p)), None)
        
        if key_path:
            credentials = service_account.Credentials.from_service_account_file(key_path)
            return bigquery.Client(credentials=credentials, project=credentials.project_id)
        else:
            return bigquery.Client()
    except Exception as e:
        print(f"Error creating BQ client: {e}")
        return None

def calculate_gravity(client):
    print("Fetching location data...")
    # Fetch nested data. 
    # We can unnest in SQL or Python. Python is easier for the loop math.
    query = f"""
    SELECT 
        team_name,
        stadium_name,
        dunkin,
        starbucks
    FROM `{BQ_TABLE}`
    """
    df = client.query(query).to_dataframe()
    
    stadium_gravity = []
    
    for _, row in df.iterrows():
        # Dunkin Pull
        d_pull = 0.0
        for loc in row['dunkin']['locations']:
            dist = loc['distance_miles']
            # Exponential Decay: I = e^(-lambda * d)
            # Lambda = 0.5 (Halves influence every ~1.4 miles, 10% remaining at 4.6 miles)
            # This models consumer willingness to travel for coffee more realistically than gravity.
            g = math.exp(-0.5 * dist)
            d_pull += g
            
        # Starbucks Pull
        s_pull = 0.0
        for loc in row['starbucks']['locations']:
            dist = loc['distance_miles']
            g = math.exp(-0.5 * dist)
            s_pull += g
            
        stadium_gravity.append({
            'Team': row['team_name'],
            'Stadium': row['stadium_name'],
            'Dunkin_Gravity': d_pull,
            'Starbucks_Gravity': s_pull,
            'Net_Gravity': d_pull - s_pull
        })
        
    results_df = pd.DataFrame(stadium_gravity)
    results_df.sort_values(by='Net_Gravity', ascending=False, inplace=True)
    
    # Save Report
    report_path = os.path.join(os.path.dirname(__file__), "coffee_gravity_report.md")
    with open(report_path, "w") as f:
        f.write("# NFL Coffee Gravity Rankings (Exponential Decay)\n\n")
        f.write(f"**Methodology**: Exponential Decay ($e^{{-0.5d}}$). This model assumes influence decays by 50% every 1.4 miles.\n")
        f.write("Positive Net Gravity = Dunkin Dominance. Negative = Starbucks Dominance.\n\n")
        f.write("| Rank | Team | Stadium | Net Score | Dunkin Score | Starbucks Score | Territory |\n")
        f.write("| :--- | :--- | :--- | :---: | :---: | :---: | :--- |\n")
        
        for i, row in enumerate(results_df.to_dict('records')):
            net = row['Net_Gravity']
            icon = "☕️" if net < 0 else "🍩"
            winner = "Starbucks" if net < 0 else "Dunkin'"
            f.write(f"| {i+1} | {row['Team']} | {row['Stadium']} | {net:.2f} | {row['Dunkin_Gravity']:.2f} | {row['Starbucks_Gravity']:.2f} | {icon} {winner} |\n")
            
    print(f"Report saved to {report_path}")
    
    # Print Top 5 and Bottom 5
    print("\nTop 5 Dunkin Gravity:")
    print(results_df.head(5)[['Team', 'Net_Gravity']])
    print("\nTop 5 Starbucks Gravity:")
    print(results_df.tail(5)[['Team', 'Net_Gravity']])

if __name__ == "__main__":
    client = get_bq_client()
    if client:
        calculate_gravity(client)
