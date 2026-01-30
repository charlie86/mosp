/*
Reproducible SQL Queries for "Robust Coffee Metrics" Analysis
Target Season: 2025 (Regular + Playoffs)
Date: 2026-01-28

METHODOLOGY:
1.  Gravity Calculation: Exponential decay model (gravity ~ exp(-0.5 * distance)) with interference.
2.  Filters: "Away Games Only" to remove home field advantage bias.
3.  Zones:
    - Starbucks Zone: Net Gravity < 0
    - Dunkin Zone: Net Gravity > 0
    - Death Zone: Net Gravity <= -4 (Extreme Starbucks)
*/

-- ------------------------------------------------------------------
-- CTE: Stadium Gravity Mapping (Pre-calculated via Python model)
-- ------------------------------------------------------------------
WITH stadium_gravity AS (
    SELECT * FROM UNNEST([
        STRUCT('Empower Field at Mile High' AS stadium_name, 'Denver Broncos' AS team_name, -1.9701 AS net_gravity),
        STRUCT('GEHA Field at Arrowhead Stadium', 'Kansas City Chiefs', 0.0000),
        STRUCT('Ford Field', 'Detroit Lions', 2.3793),
        STRUCT('Lambeau Field', 'Green Bay Packers', 0.0000),
        STRUCT('Lumen Field', 'Seattle Seahawks', -11.4589),
        STRUCT('Levi\'s Stadium', 'San Francisco 49ers', -5.7955),
        STRUCT('AT&T Stadium', 'Dallas Cowboys', 0.8654),
        STRUCT('Lucas Oil Stadium', 'Indianapolis Colts', -3.9995),
        STRUCT('Nissan Stadium', 'Tennessee Titans', -2.8767),
        STRUCT('NRG Stadium', 'Houston Texans', -1.2599),
        STRUCT('Highmark Stadium', 'Buffalo Bills', 2.8715),
        STRUCT('U.S. Bank Stadium', 'Minnesota Vikings', -4.2413),
        STRUCT('Caesars Superdome', 'New Orleans Saints', -6.3475),
        STRUCT('SoFi Stadium', 'Los Angeles Chargers', -4.9277),
        STRUCT('SoFi Stadium', 'Los Angeles Rams', -4.9277),
        STRUCT('State Farm Stadium', 'Arizona Cardinals', -1.8730),
        STRUCT('Cleveland Browns Stadium', 'Cleveland Browns', 1.1596),
        STRUCT('EverBank Stadium', 'Jacksonville Jaguars', 0.1170),
        STRUCT('Bank of America Stadium', 'Carolina Panthers', -2.8215),
        STRUCT('Acrisure Stadium', 'Pittsburgh Steelers', -0.8769),
        STRUCT('Allegiant Stadium', 'Las Vegas Raiders', -2.1399),
        STRUCT('Paycor Stadium', 'Cincinnati Bengals', 2.4352),
        STRUCT('Raymond James Stadium', 'Tampa Bay Buccaneers', 0.4659),
        STRUCT('Mercedes-Benz Stadium', 'Atlanta Falcons', 2.9548),
        STRUCT('Commanders Field', 'Washington Commanders', 0.0320),
        STRUCT('MetLife Stadium', 'New York Giants', 2.3755),
        STRUCT('MetLife Stadium', 'New York Jets', 2.3755),
        STRUCT('Gillette Stadium', 'New England Patriots', 4.3520),
        STRUCT('Soldier Field', 'Chicago Bears', 1.2688),
        STRUCT('M&T Bank Stadium', 'Baltimore Ravens', 5.7435),
        STRUCT('Hard Rock Stadium', 'Miami Dolphins', 2.8371),
        STRUCT('Lincoln Financial Field', 'Philadelphia Eagles', 0.9690)
    ])
),

-- ------------------------------------------------------------------
-- CTE: Team Abbreviation Mapping (Normalizing names)
-- ------------------------------------------------------------------
team_mapping AS (
    SELECT 'Denver Broncos' as name, 'DEN' as abbr UNION ALL
    SELECT 'Kansas City Chiefs', 'KC' UNION ALL
    SELECT 'Detroit Lions', 'DET' UNION ALL
    SELECT 'Green Bay Packers', 'GB' UNION ALL
    SELECT 'Seattle Seahawks', 'SEA' UNION ALL
    SELECT 'San Francisco 49ers', 'SF' UNION ALL
    SELECT 'Dallas Cowboys', 'DAL' UNION ALL
    SELECT 'Indianapolis Colts', 'IND' UNION ALL
    SELECT 'Tennessee Titans', 'TEN' UNION ALL
    SELECT 'Houston Texans', 'HOU' UNION ALL
    SELECT 'Buffalo Bills', 'BUF' UNION ALL
    SELECT 'Minnesota Vikings', 'MIN' UNION ALL
    SELECT 'New Orleans Saints', 'NO' UNION ALL
    SELECT 'Los Angeles Chargers', 'LAC' UNION ALL
    SELECT 'Los Angeles Rams', 'LA' UNION ALL
    SELECT 'Arizona Cardinals', 'ARI' UNION ALL
    SELECT 'Cleveland Browns', 'CLE' UNION ALL
    SELECT 'Jacksonville Jaguars', 'JAX' UNION ALL
    SELECT 'Bank of America Stadium', 'CAR' UNION ALL -- Handled via join usually, mapping here for safety
    SELECT 'Carolina Panthers', 'CAR' UNION ALL
    SELECT 'Pittsburgh Steelers', 'PIT' UNION ALL
    SELECT 'Las Vegas Raiders', 'LV' UNION ALL
    SELECT 'Cincinnati Bengals', 'CIN' UNION ALL
    SELECT 'Tampa Bay Buccaneers', 'TB' UNION ALL
    SELECT 'Atlanta Falcons', 'ATL' UNION ALL
    SELECT 'Washington Commanders', 'WAS' UNION ALL
    SELECT 'New York Giants', 'NYG' UNION ALL
    SELECT 'New York Jets', 'NYJ' UNION ALL
    SELECT 'New England Patriots', 'NE' UNION ALL
    SELECT 'Chicago Bears', 'CHI' UNION ALL
    SELECT 'Baltimore Ravens', 'BAL' UNION ALL
    SELECT 'Miami Dolphins', 'MIA' UNION ALL
    SELECT 'Philadelphia Eagles', 'PHI'
),

-- ------------------------------------------------------------------
-- CTE: Joined PBP Data with Gravity (Away Games Only)
-- ------------------------------------------------------------------
joined_data AS (
    SELECT 
        pbp.*,
        sg.net_gravity,
        CASE 
            WHEN sg.net_gravity < -4 THEN 'Starbucks Death Zone'
            WHEN sg.net_gravity < 0 THEN 'Starbucks Zone'
            ELSE 'Dunkin Zone' 
        END as gravity_zone
    FROM `stuperlatives.pbp_data` pbp
    -- Join Gravity to Home Team (Environmental Factor)
    JOIN team_mapping tm ON tm.abbr = pbp.home_team
    JOIN stadium_gravity sg ON sg.team_name = tm.name
    WHERE pbp.season = 2025
      AND pbp.season_type IN ('REG', 'POST')
),

-- ------------------------------------------------------------------
-- ANALYSIS 1: PATRIOTS OFFENSE (AWAY GAMES)
-- ------------------------------------------------------------------
metrics_pats AS (
    SELECT
        'Patriots Offense (Away)' as segment,
        CASE WHEN net_gravity > 0 THEN 'Dunkin Zone' ELSE 'Starbucks Zone' END as zone,
        COUNT(DISTINCT game_id) as games,
        ROUND(AVG(CAST(complete_pass AS INT64)) / NULLIF(AVG(pass_attempt),0) * 100, 1) as comp_pct,
        ROUND(SUM(CASE WHEN play_type='pass' AND sack=0 THEN yards_gained ELSE 0 END) / NULLIF(SUM(pass_attempt),0), 2) as ypa,
        ROUND(SUM(epa) / COUNT(*), 3) as epa_per_play,
        ROUND(AVG(home_score + away_score), 1) as game_ev_ppg -- Approx
        -- Note: For exact PPG we need game-level aggregation first
    FROM joined_data
    WHERE posteam = 'NE' 
      AND home_team != 'NE' -- Away Only
      AND play_type IN ('run', 'pass')
    GROUP BY 1, 2
)

SELECT * FROM metrics_pats ORDER BY zone;


-- ------------------------------------------------------------------
-- ANALYSIS 2: SEAHAWKS DEFENSE (AWAY GAMES)
-- ------------------------------------------------------------------
-- Calculate PPG Allowed properly
SELECT 
    'Seahawks Defense (Away)' as segment,
    CASE 
        WHEN net_gravity < -4 THEN 'Starbucks Death Zone'
        WHEN net_gravity < 0 THEN 'Starbucks Zone'
        ELSE 'Dunkin Zone' 
    END as zone,
    COUNT(DISTINCT game_id) as games,
    ROUND(AVG(away_score), 1) as ppg_allowed, -- In away games, SEA allows 'home_score'? No, SEA is away, so they allow 'home_score'.
    -- Wait: if SEA is Away (defteam='SEA', home_team!='SEA'), then SEA allows the HOME score.
    -- My previous python script used: "if g['home_team'] == team: allowed = away_score".
    -- Here SEA is AWAY. So they allow HOME score.
    ROUND(AVG(home_score), 1) as ppg_allowed_corrected,
    
    -- Opponent Passer Rating Calculation Components
    SUM(pass_touchdown) as opp_tds,
    SUM(interception) as opp_ints,
    ROUND(SUM(CASE WHEN play_type='pass' AND sack=0 THEN yards_gained ELSE 0 END) / NULLIF(SUM(pass_attempt),0), 2) as opp_ypa,
    
    -- Sack Rate
    ROUND(SUM(sack) / NULLIF(SUM(pass_attempt + sack), 0) * 100, 1) as sack_rate_pct
    
FROM joined_data
WHERE defteam = 'SEA'
  AND home_team != 'SEA' -- Away Only
GROUP BY 1, 2
ORDER BY zone;


-- ------------------------------------------------------------------
-- ANALYSIS 3: SAM DARNOLD (SEA QB) PARADOX (AWAY GAMES)
-- ------------------------------------------------------------------
SELECT
    'Sam Darnold (Away)' as segment,
    CASE WHEN net_gravity > 0 THEN 'Dunkin Zone' ELSE 'Starbucks Zone' END as zone,
    COUNT(DISTINCT game_id) as games,
    SUM(pass_touchdown) as tds,
    SUM(interception) as ints,
    ROUND(SUM(pass_touchdown) / NULLIF(SUM(interception), 0.01), 2) as td_int_ratio,
    
    -- Passer Rating Formula Components
    ROUND(
        (
            GREATEST(0, LEAST(2.375, (SUM(complete_pass)/SUM(pass_attempt) - 0.3) * 5)) +
            GREATEST(0, LEAST(2.375, (SUM(CASE WHEN play_type='pass' AND sack=0 THEN yards_gained ELSE 0 END)/SUM(pass_attempt) - 3) * 0.25)) +
            GREATEST(0, LEAST(2.375, (SUM(pass_touchdown)/SUM(pass_attempt)) * 20)) +
            GREATEST(0, LEAST(2.375, 2.375 - (SUM(interception)/SUM(pass_attempt) * 25)))
        ) / 6 * 100
    , 1) as rating
    
FROM joined_data
WHERE passer_player_name = 'S.Darnold'
  AND home_team != posteam -- Away Only
GROUP BY 1, 2
ORDER BY zone;
