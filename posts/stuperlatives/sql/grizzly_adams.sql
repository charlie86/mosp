WITH
    bearded_players AS (
        SELECT
            player_id
        FROM
            `stuperlatives.appearance_labels`
        WHERE
            has_beard = TRUE
    ),
    tackles AS (
        -- Solo Tackles
        SELECT
            solo_tackle_1_player_id as player_id
        FROM
            `stuperlatives.pbp_data`
        WHERE
            solo_tackle = 1
        UNION ALL
        -- Assist Tackles
        SELECT
            assist_tackle_1_player_id as player_id
        FROM
            `stuperlatives.pbp_data`
        WHERE
            assist_tackle = 1
    )
SELECT
    t.player_id,
    COUNT(*) as tackles,
    ANY_VALUE (name_lookup.player_name) as player_name
FROM
    tackles t
    JOIN bearded_players b ON t.player_id = b.player_id
    LEFT JOIN (
        SELECT
            player_id,
            MAX(player_name) as player_name
        FROM
            `stuperlatives.rosters`
        GROUP BY
            1
    ) name_lookup ON t.player_id = name_lookup.player_id
GROUP BY
    1
ORDER BY
    tackles DESC
LIMIT
    10