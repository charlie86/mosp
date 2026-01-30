SELECT
    CASE
        WHEN interception = 1 THEN interception_player_name
        ELSE pass_defense_1_player_name
    END AS player,
    defteam,
    COUNT(*) as bird_plays_made,
    STRUCT(
        COUNTIF(posteam = 'ARI') AS cardinals,
        COUNTIF(posteam = 'ATL') AS falcons,
        COUNTIF(posteam = 'BAL') AS ravens,
        COUNTIF(posteam = 'PHI') AS eagles,
        COUNTIF(posteam = 'SEA') AS seahawks
    ) AS bird_breakdown
FROM
    `stuperlatives.pbp_data`
WHERE
    posteam IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA')
    AND (
        interception = 1
        OR pass_defense_1_player_name IS NOT NULL
    )
GROUP BY
    1,
    2
ORDER BY
    bird_plays_made DESC
LIMIT
    10