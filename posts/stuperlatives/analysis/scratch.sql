SELECT
    passer_player_name as player,
    SUM(success) as successful_plays,
    COUNT(*) as attempts,
    CAST(SUM(success) AS FLOAT64) / COUNT(*) as value
FROM
    `stuperlatives.pbp_data`
WHERE
    season >= 2018
    AND score_differential = 0
    AND pass_location = 'left'
    AND (
        pass_attempt = 1
        OR sack = 1
    )
GROUP BY
    1
HAVING
    attempts >= 20
ORDER BY
    value DESC
LIMIT
    10