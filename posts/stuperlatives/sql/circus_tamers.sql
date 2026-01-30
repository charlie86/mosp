WITH
    stats AS (
        SELECT
            defteam,
            SUM(yards_gained) as total_rush_yards,
            COUNT(*) as rushes_faced,
            COUNT(DISTINCT game_id) as games_played
        FROM
            `stuperlatives.pbp_data`
        WHERE
            posteam IN ('DET', 'CHI', 'CIN', 'JAX')
            AND rush = 1
        GROUP BY
            defteam
    )
SELECT
    defteam,
    total_rush_yards,
    rushes_faced,
    games_played,
    total_rush_yards / games_played as yards_per_game
FROM
    stats
WHERE
    games_played >= 2
ORDER BY
    yards_per_game ASC
LIMIT
    10