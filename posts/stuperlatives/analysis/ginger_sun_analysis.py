
from posts.stuperlatives.etl.bq_utils import get_bq_client
import pandas as pd

def analyze_gingers_in_sun():
    client = get_bq_client()
    if not client: return

    # List of known Red Headed QBs (The "Ginger Avengers")
    # Andy Dalton, Carson Wentz, Sam Darnold, Cooper Rush, Mike Glennon
    redheads = [
        'A.Dalton', 
        'C.Wentz', 
        'S.Darnold', 
        'C.Rush', 
        'M.Glennon'
    ]
    
    names_str = "', '".join(redheads)
    
    query = f"""
    SELECT
        passer_player_name as player,
        CASE 
            WHEN LOWER(weather) LIKE '%sunny%' OR LOWER(weather) LIKE '%clear%' THEN 'Sunny'
            WHEN roof = 'dome' or roof = 'closed' THEN 'Indoors'
            ELSE 'Cloudy/Rain/Other'
        END as weather_condition,
        COUNT(*) as attempts,
        Round(AVG(success), 3) as success_rate,
        Round(AVG(epa), 3) as avg_epa,
        Round(AVG(cpoe), 1) as avg_cpoe
    FROM
        `stuperlatives.pbp_data`
    WHERE
        passer_player_name IN ('{names_str}')
        AND season >= 2016
        AND pass_attempt = 1
    GROUP BY
        1, 2
    ORDER BY
        player, weather_condition
    """
    
    print("Running Ginger Analysis...")
    df = client.query(query).to_dataframe()
    
    print("\n--- Red Headed QBs Weather Report ---")
    print(df.to_string())
    
    # Aggregate View
    agg_query = f"""
    SELECT
        CASE 
            WHEN LOWER(weather) LIKE '%sunny%' OR LOWER(weather) LIKE '%clear%' THEN 'Sunny'
            ELSE 'Not Sunny'
        END as weather_condition,
        COUNT(*) as attempts,
        Round(AVG(success), 3) as success_rate,
        Round(AVG(epa), 3) as avg_epa
    FROM
        `stuperlatives.pbp_data`
    WHERE
        passer_player_name IN ('{names_str}')
        AND season >= 2016
        AND pass_attempt = 1
    GROUP BY
        1
    ORDER BY
        1 DESC
    """
    print("\n--- Aggregate Ginger Stats (Sunny vs Not) ---")
    agg_df = client.query(agg_query).to_dataframe()
    print(agg_df.to_string())

if __name__ == "__main__":
    analyze_gingers_in_sun()
