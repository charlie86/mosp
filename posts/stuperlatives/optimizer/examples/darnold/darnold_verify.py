
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
            print(f"--- {description} ---")
            print(df.head(10))
            
            top_player = df.iloc[0][0]
            if 'Darnold' in str(top_player):
                print(">>> CONFIRMED #1 <<<")
            else:
                darnold_rows = df[df.iloc[:,0].astype(str).str.contains('Darnold')]
                if not darnold_rows.empty:
                    print(f"Darnold Rank: {darnold_rows.index[0] + 1}")
                else:
                    print("Darnold not in top list")
            print("\n")
    except Exception as e:
        print(f"Error querying {description}: {e}")

if __name__ == "__main__":
    print("--- VERIFYING OPTIMIZER HITS (ACTIVE PLAYERS COHORT) ---")
    
    # Common Subquery for Active Players
    # We define active generally as played in 2024 or 2025 (latest season)
    # The optimizer used the MAX season in DB. We will use a subquery.
    
    active_player_filter = """
    passer_player_name IN (
        SELECT DISTINCT passer_player_name 
        FROM `stuperlatives.pbp_data` 
        WHERE season = (SELECT MAX(season) FROM `stuperlatives.pbp_data`)
    )
    """

    # Hit 1: [Active] Success Rate | Tied, Left
    check_stat("Success Rate (Active, Tied, Left)", f"""
        SELECT
            passer_player_name as player,
            SUM(success) as successes,
            COUNT(*) as attempts,
            CAST(SUM(success) AS FLOAT64)/COUNT(*) as value
        FROM `stuperlatives.pbp_data`
        WHERE {active_player_filter}
          AND score_differential = 0
          AND pass_location = 'left'
          AND (pass_attempt = 1 OR sack = 1)
        GROUP BY 1
        HAVING attempts >= 20
        ORDER BY value DESC
        LIMIT 10
    """)

    # Hit 2: [Active] Passing Yards/Game | Deep Own Terr, Night Game
    # Deep Own Terr: yardline_100 > 80
    # Night Game: start_time > '19:00:00'
    check_stat("Passing Yards/Game (Active, Deep Own, Night)", f"""
        SELECT
            passer_player_name as player,
            SUM(yards_gained) as total_yards,
            COUNT(DISTINCT game_id) as games,
            CAST(SUM(yards_gained) AS FLOAT64)/COUNT(DISTINCT game_id) as value
        FROM `stuperlatives.pbp_data`
        WHERE {active_player_filter}
          AND yardline_100 > 80
          AND start_time > '19:00:00'
          AND (pass_attempt = 1 OR sack = 1)
        GROUP BY 1
        HAVING games >= 5
        ORDER BY value DESC
        LIMIT 10
    """)

    # Hit 3: [Active] Success Rate | Tied, Opponent Territory
    # Tied, yardline_100 <= 50
    check_stat("Success Rate (Active, Tied, Opp Terr)", f"""
        SELECT
            passer_player_name as player,
            SUM(success) as successes,
            COUNT(*) as attempts,
            CAST(SUM(success) AS FLOAT64)/COUNT(*) as value
        FROM `stuperlatives.pbp_data`
        WHERE {active_player_filter}
          AND score_differential = 0
          AND yardline_100 <= 50
          AND (pass_attempt = 1 OR sack = 1)
        GROUP BY 1
        HAVING attempts >= 20
        ORDER BY value DESC
        LIMIT 10
    """)
    

    
    print("--- VERIFYING OPTIMIZER HITS (ALL TIME COHORT) ---")

    # Hit 6: [All Time] Lowest INT Rate | Night Game, West
    # Night: > 19:00, West: SEA, SF, LAR, LAC, ARI, LV, DEN, OAK, SD
    # Min Atts: 20
    check_stat("Lowest INT Rate (All Time, Night, West)", """
        SELECT
            passer_player_name as player,
            SUM(interception) as ints,
            COUNT(*) as attempts,
            CAST(SUM(interception) AS FLOAT64)/COUNT(*) as value
        FROM `stuperlatives.pbp_data`
        WHERE start_time > '19:00:00'
          AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
          AND (pass_attempt = 1 OR sack = 1)
        GROUP BY 1
        HAVING attempts >= 20
        ORDER BY value ASC
        LIMIT 10
    """)

    # Hit 7: [All Time] Completion % | Tied, Red Zone
    check_stat("Comp % (All Time, Tied, Red Zone)", """
        SELECT
            passer_player_name as player,
            SUM(complete_pass) as completions,
            COUNT(*) as attempts,
            CAST(SUM(complete_pass) AS FLOAT64)/COUNT(*) as value
        FROM `stuperlatives.pbp_data`
        WHERE score_differential = 0
          AND yardline_100 <= 20
          AND (pass_attempt = 1 OR sack = 1)
        GROUP BY 1
        HAVING attempts >= 20
        ORDER BY value DESC
        LIMIT 10
    """)
