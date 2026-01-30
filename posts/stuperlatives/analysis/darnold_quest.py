
from google.cloud import bigquery
import pandas as pd
from posts.stuperlatives.etl.bq_utils import get_bq_client

def run_query(query):
    client = get_bq_client()
    return client.query(query).to_dataframe()

def check_stat(description, query):
    try:
        df = run_query(query)
        if not df.empty:
            # Handle possible column name differences if alias not used
            if 'player' in df.columns:
                top_player = df.iloc[0]['player']
            else:
                top_player = df.iloc[0][0] # Fallback to first column

            print(f"--- {description} ---")
            print(df.head(10))
            
            if top_player and 'Darnold' in str(top_player):
                print(">>> FOUND ONE! <<<")
            else:
                if 'player' in df.columns:
                    darnold_rank = df[df['player'].astype(str).str.contains('Darnold')].index
                else: 
                     darnold_rank = [] # Fallback

                if len(darnold_rank) > 0:
                    print(f"Darnold Rank: {darnold_rank[0] + 1}")
                else:
                    print("Darnold not in top list")
            print("\n")
    except Exception as e:
        print(f"Error querying {description}: {e}")

if __name__ == "__main__":
    print("--- VERIFYING OPTIMIZER HITS ---")
    
    # Hit 1: INT Rate | 4th Down, Division Rivals
    check_stat("INT Rate (4th Down, Division Rivals)", """
        SELECT
            passer_player_name as player,
            SUM(interception) as total_ints,
            COUNT(*) as attempts,
            CAST(SUM(interception) AS FLOAT64)/COUNT(*) as value,
            ARRAY_AGG(DISTINCT defteam) as opponents
        FROM `stuperlatives.pbp_data`
        WHERE season >= 2018
          AND down = 4
          AND div_game = 1
          AND (pass_attempt = 1 OR sack = 1)
        GROUP BY 1
        HAVING attempts >= 20
        ORDER BY value DESC
        LIMIT 10
    """)

    # Hit 2: INT Rate | Deep Own Terr, Bird Teams
    check_stat("INT Rate (Deep Own Terr, Bird Teams)", """
        SELECT
            passer_player_name as player,
            SUM(interception) as total_ints,
            COUNT(*) as attempts,
            CAST(SUM(interception) AS FLOAT64)/COUNT(*) as value
        FROM `stuperlatives.pbp_data`
        WHERE season >= 2018
          AND yardline_100 > 80
          AND defteam IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA')
          AND (pass_attempt = 1 OR sack = 1)
        GROUP BY 1
        HAVING attempts >= 20
        ORDER BY value DESC
        LIMIT 10
    """)

    # Hit 3: TDs/Game | Bird Teams, Midwest
    check_stat("TDs/Game (Bird Teams @ Midwest)", """
        SELECT
            passer_player_name as player,
            SUM(touchdown) as total_tds,
            COUNT(DISTINCT game_id) as games,
            CAST(SUM(touchdown) AS FLOAT64)/COUNT(DISTINCT game_id) as value
        FROM `stuperlatives.pbp_data`
        WHERE season >= 2018
          AND defteam IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA')
          AND home_team IN ('GB', 'CHI', 'MIN', 'DET', 'IND', 'CIN', 'CLE', 'KC', 'STL')
          AND (pass_attempt = 1 OR sack = 1)
        GROUP BY 1
        HAVING games >= 2
        ORDER BY value DESC
        LIMIT 10
    """)
    
    # Hit 4: Success Rate | Tied, Left
    check_stat("Success Rate (Tied, Left)", """
        SELECT
            passer_player_name as player,
            SUM(success) as successful_plays,
            COUNT(*) as attempts,
            CAST(SUM(success) AS FLOAT64)/COUNT(*) as value
        FROM `stuperlatives.pbp_data`
        WHERE season >= 2018
          AND score_differential = 0
          AND pass_location = 'left'
          AND (pass_attempt = 1 OR sack = 1)
        GROUP BY 1
        HAVING attempts >= 20
        ORDER BY value DESC
        LIMIT 10
    """)
