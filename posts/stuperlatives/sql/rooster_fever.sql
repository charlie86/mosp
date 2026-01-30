WITH
    redhead_qbs AS (
        SELECT
            player_id
        FROM
            `stuperlatives.appearance_labels`
        WHERE
            is_redhead = TRUE
        UNION DISTINCT
        SELECT
            '00-0034869' as player_id
    ),
    sacks AS (
        SELECT
            -- Try to find sacker name. sack_player_name is often available.
            -- If not, we might need ID. But report uses name.
            sack_player_name,
            defteam
        FROM
            `stuperlatives.pbp_data`
        WHERE
            sack = 1
            AND passer_player_id IN (
                SELECT
                    player_id
                FROM
                    redhead_qbs
            )
    )
SELECT
    sack_player_name,
    COUNT(*) as redhead_sacks
FROM
    sacks
WHERE
    sack_player_name IS NOT NULL
GROUP BY
    1
ORDER BY
    redhead_sacks DESC
LIMIT
    10