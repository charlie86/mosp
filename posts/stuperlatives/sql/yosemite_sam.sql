WITH
    mustache_qbs AS (
        SELECT
            player_id
        FROM
            `stuperlatives.appearance_labels`
        WHERE
            has_mustache = TRUE
            AND has_beard = FALSE
        UNION DISTINCT
        SELECT
            '00-0035289' as player_id
    ),
    qb_stats AS (
        SELECT
            passer_player_id,
            AVG(epa) as epa,
            COUNT(*) as plays
        FROM
            `stuperlatives.pbp_data`
        WHERE
            passer_player_id IN (
                SELECT
                    player_id
                FROM
                    mustache_qbs
            )
        GROUP BY
            1
    )
SELECT
    passer_player_id,
    epa,
    plays,
    passer_player_id as player_id,
    name_lookup.player_name as player_name
FROM
    qb_stats
    LEFT JOIN (
        SELECT
            player_id,
            MAX(player_name) as player_name
        FROM
            `stuperlatives.rosters`
        GROUP BY
            1
    ) name_lookup ON qb_stats.passer_player_id = name_lookup.player_id
WHERE
    plays > 50
ORDER BY
    epa DESC