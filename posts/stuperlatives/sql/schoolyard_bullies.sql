WITH
    ivy_targets AS (
        SELECT DISTINCT
            player_id
        FROM
            `stuperlatives.ivy_league_players`
    ),
    plays AS (
        SELECT
            *
        FROM
            `stuperlatives.pbp_data` p
            JOIN ivy_targets i ON (
                p.rusher_player_id = i.player_id
                OR p.receiver_player_id = i.player_id
            )
    ),
    tacklers AS (
        -- Solo Tackles
        SELECT
            solo_tackle_1_player_id as player_id,
            defteam
        FROM
            plays
        WHERE
            solo_tackle = 1
        UNION ALL
        -- Assist Tackles
        SELECT
            assist_tackle_1_player_id as player_id,
            defteam
        FROM
            plays
        WHERE
            assist_tackle = 1
    )
SELECT
    t.player_id,
    t.defteam,
    COUNT(*) as ivy_league_tackles,
    ANY_VALUE (name_lookup.player_name) as player_name
FROM
    tacklers t
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
    1,
    2
ORDER BY
    ivy_league_tackles DESC
LIMIT
    10