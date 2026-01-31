SELECT
    -- game_id,
    -- home_team,
    -- posteam,
    avg(epa) as epa_play,
    avg(success) as success_play,
    -- epa,
    -- success,
FROM
    `stuperlatives.pbp_data`
WHERE
    season >= 2015
    -- AND posteam = 'NE'
    AND play_type = 'run'