
import pandas as pd
from posts.stuperlatives.etl.bq_utils import get_bq_client
from posts.stuperlatives.data.team_taxonomy import HAT_TEAMS, BIRD_TEAMS

def analyze_super_bowl_stuperlatives():
    client = get_bq_client()
    if not client: return

    print("--- Running Super Bowl LIX Stuperlatives Analysis ---\n")

    # 1. Hat Metric: Seahawks Defense vs Hat Teams
    hat_teams_str = "', '".join(HAT_TEAMS)
    query_hat = f"""
    SELECT
        defteam,
        CASE 
            WHEN posteam IN ('{hat_teams_str}') THEN 'vs Hat Team'
            ELSE 'vs Non-Hat Team'
        END as opponent_type,
        COUNT(*) as plays,
        Round(AVG(epa), 3) as avg_epa_allowed,
        Round(AVG(success), 3) as success_rate_allowed
    FROM
        `stuperlatives.pbp_data`
    WHERE
        defteam = 'SEA'
        AND season >= 2020
    GROUP BY
        1, 2
    ORDER BY
        2 DESC
    """
    df_hat = client.query(query_hat).to_dataframe()
    print("1. Seahawks D vs Hat Teams (Lower EPA is better for Defense):")
    print(df_hat.to_string())
    print("\n")

    # 2. Drake Maye vs Bird Teams
    # Drake Maye is a rookie in 2024. He played vs:
    # SEA (Bird), ARI (Bird), maybe others?
    bird_teams_str = "', '".join(BIRD_TEAMS)
    query_maye = f"""
    SELECT
        passer_player_name,
        CASE 
            WHEN defteam IN ('{bird_teams_str}') THEN 'vs Bird Team'
            ELSE 'vs Non-Bird Team'
        END as opponent_type,
        COUNT(*) as attempts,
        Round(AVG(epa), 3) as avg_epa,
        Round(AVG(cpoe), 1) as avg_cpoe,
        SUM(interception) as ints
    FROM
        `stuperlatives.pbp_data`
    WHERE
        passer_player_name = 'D.Maye'
        AND season = 2024
        AND pass_attempt = 1
    GROUP BY
        1, 2
    """
    df_maye = client.query(query_maye).to_dataframe()
    print("2. Drake Maye vs Bird Teams:")
    print(df_maye.to_string())
    print("\n")

    # 3. IHOP Effect for O-Lines
    # Using pff_blocking_summary_2024 and stadium_gravitational_pull
    # Joining on (home_team = team) for home games, or game_id? 
    # PFF data is by player/game. Stadium pull is by stadium. 
    # We need to link game -> stadium -> ihop distance.
    # PBP data has `game_stadium` and `home_team`. 
    # Let's simplify: Check if we have stadium info in PFF or bridge it via PBP.
    
    # Actually, simpler: define 'IHOP Proximity' based on home field advantage for SEA/NE?
    # Or generically for all teams?
    # User asked: "both o lines when the stadium is within 2mi of an ihop"
    
    # We will look at NE and SEA O-Line blocking grades in games where the stadium 
    # has an IHOP < 2 miles.
    
    query_ihop = """
    WITH stadium_ihop AS (
        SELECT 
            stadium_id, 
            min_distance_ihop_miles 
        FROM `pff_analysis.stadium_gravitational_pull`
    ),
    game_map AS (
        SELECT DISTINCT game_id, home_team, stadium_id 
        FROM `stuperlatives.pbp_data`
        WHERE season >= 2022
    )
    
    -- This part is tricky because we need to link PFF data (which doesn't have stadium_id)
    -- to the stadium data.
    -- Alternative: Use PBP EPA for "Blocking" (Rush EPA?) or Sack Rate.
    -- Let's use Sack Rate for NE and SEA O-lines (Offense) split by IHOP distance.
    
    SELECT
        posteam,
        CASE 
            WHEN s.min_distance_ihop_miles <= 2.0 THEN 'Near IHOP (<2mi)'
            ELSE 'Far from IHOP'
        END as ihop_proximity,
        COUNT(*) as pass_plays,
        SUM(sack) as sacks_allowed,
        Round(SUM(sack)/COUNT(*)*100, 2) as sack_rate_pct,
        Round(AVG(epa), 3) as avg_epa_per_pass
    FROM
        `stuperlatives.pbp_data` p
    JOIN
        game_map g ON p.game_id = g.game_id
    JOIN
        stadium_ihop s ON g.stadium_id = s.stadium_id
    WHERE
        posteam IN ('NE', 'SEA')
        AND p.pass_attempt = 1
        AND p.season >= 2022
    GROUP BY
        1, 2
    ORDER BY
        1, 2
    """
    
    try:
        df_ihop = client.query(query_ihop).to_dataframe()
        print("3. O-Line Performance (Sack Rate) vs IHOP Proximity (Since 2022):")
        print(df_ihop.to_string())
    except Exception as e:
        print(f"IHOP Query Error: {e}")

if __name__ == "__main__":
    analyze_super_bowl_stuperlatives()
