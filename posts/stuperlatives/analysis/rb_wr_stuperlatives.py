
import pandas as pd
from posts.stuperlatives.etl.bq_utils import get_bq_client
from posts.stuperlatives.data.team_taxonomy import BIRD_TEAMS, MAILMAN_TEAMS

def analyze_rb_wr():
    client = get_bq_client()
    print("--- Running Super Bowl RB/WR Stuperlatives ---")
    
    # 1. K9 vs The Mailman (Patriots, etc)
    mailman_teams_str = "', '".join(MAILMAN_TEAMS)
    print("\n1. 'K9 Chasing The Mailman' (Kenneth Walker vs Uniformed Human Mascots):")
    query_k9_mailman = f"""
    SELECT
        rusher_player_name as player,
        CASE 
            WHEN defteam IN ('{mailman_teams_str}') THEN 'vs Mailman Team'
            ELSE 'vs Non-Mailman Team'
        END as opponent_type,
        COUNT(*) as rushes,
        Round(AVG(yards_gained), 2) as ypc,
        Round(AVG(epa), 3) as avg_epa_rush,
        -- Need Yards After Contact if available, or just EPA/YPC as proxy for "Aggression"
        -- PBP doesn't always have accurate YCO. Let's use 'yards_gained' and 'success'
        Round(AVG(success), 3) as success_rate
    FROM `stuperlatives.pbp_data`
    WHERE
        (rusher_player_name = 'K.Walker' OR rusher_player_name = 'K.Walker III')
        AND rush = 1
        AND season >= 2022
    GROUP BY 1, 2
    """
    try:
        df_k9 = client.query(query_k9_mailman).to_dataframe()
        print(df_k9.to_string())
    except Exception as e:
        print(e)


    # 2. 'The Good Boy' (Walker on Grass vs Turf)
    print("\n2. 'The Good Boy' (Walker on Grass vs Turf):")
    query_kw3 = """
    SELECT
        rusher_player_name as player,
        CASE 
            WHEN LOWER(surface) LIKE '%grass%' THEN 'Natural Grass'
            ELSE 'Artificial Turf'
        END as surface_type,
        COUNT(*) as rushes,
        Round(AVG(epa), 3) as avg_epa_rush,
        Round(AVG(yards_gained), 2) as ypc,
        SUM(fumble) as fumbles
    FROM `stuperlatives.pbp_data`
    WHERE
        (rusher_player_name = 'K.Walker' OR rusher_player_name = 'K.Walker III') -- Verify naming
        AND rush = 1
        AND season >= 2022
    GROUP BY 1, 2
    """
    try:
        df_kw3 = client.query(query_kw3).to_dataframe()
        print(df_kw3.to_string())
    except Exception as e:
        print(e)


    # 2. DK Metcalf: Night vs Day
    # Night: Start Time > 6pm local? Or just broadly based on `start_time`.
    # PBP `start_time` format is usually HH:MM:SS (24hr).
    print("\n2. 'Decaf Metcalf' (DK Metcalf Day vs Night):")
    query_dk = """
    SELECT
        receiver_player_name as player,
        CASE 
            WHEN CAST(SPLIT(start_time, ':')[OFFSET(0)] AS INT64) >= 18 THEN 'Night Game (>6pm)'
            ELSE 'Day Game'
        END as time_of_day,
        COUNT(*) as targets,
        Round(AVG(epa), 3) as avg_epa_target,
        Round(AVG(yards_gained), 2) as ypt,
        SUM(touchdown) as tds
    FROM `stuperlatives.pbp_data`
    WHERE
        receiver_player_name = 'D.Metcalf'
        AND pass_attempt = 1
        AND season >= 2019
    GROUP BY 1, 2
    """
    try:
        df_dk = client.query(query_dk).to_dataframe()
        print(df_dk.to_string())
    except Exception as e:
        print(e)
        

    # 3. Rhamondre Stevenson vs Bird Teams
    bird_teams_str = "', '".join(BIRD_TEAMS)
    print("\n3. 'Rhamondre vs The Birds':")
    query_rhamondre = f"""
    SELECT
        player,
        CASE 
            WHEN defteam IN ('{bird_teams_str}') THEN 'vs Bird Team'
            ELSE 'vs Non-Bird Team'
        END as opponent_type,
        COUNT(*) as rushes,
        Round(AVG(epa), 3) as avg_epa_rush,
        Round(AVG(yards_gained), 2) as ypc,
        SUM(touchdown) as tds
    FROM `stuperlatives.pbp_data`
    WHERE
        player = 'R.Stevenson'
        AND rush = 1
        AND season >= 2021
    GROUP BY 1, 2
    """
    try:
        df_r = client.query(query_rhamondre).to_dataframe()
        print(df_r.to_string())
    except Exception as e:
        print(e)

if __name__ == "__main__":
    analyze_rb_wr()
