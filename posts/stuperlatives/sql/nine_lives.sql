SELECT
    fumbled_1_player_name as player,
    posteam,
    COUNT(*) as nine_lives_used
FROM
    `stuperlatives.pbp_data`
WHERE
    posteam IN ('DET', 'JAX', 'CAR', 'CIN')
    AND fumble = 1
    AND fumble_lost = 0
GROUP BY
    1,
    2
ORDER BY
    nine_lives_used DESC
LIMIT
    10