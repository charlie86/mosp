SELECT
    CASE
        WHEN interception = 1 THEN passer_player_name
        WHEN fumble_lost = 1 THEN fumbled_1_player_name
    END AS player,
    posteam,
    COUNT(*) AS turnovers_committed,
    STRUCT(
        COUNTIF(defteam = 'TB') AS bucs,
        COUNTIF(defteam = 'MIN') AS vikings,
        COUNTIF(defteam IN ('LV', 'OAK')) AS raiders
    ) AS pirate_breakdown
FROM
    `stuperlatives.pbp_data`
WHERE
    defteam IN ('TB', 'MIN', 'LV', 'OAK')
    AND (
        interception = 1
        OR fumble_lost = 1
    )
GROUP BY
    1,
    2
ORDER BY
    turnovers_committed DESC
LIMIT
    10