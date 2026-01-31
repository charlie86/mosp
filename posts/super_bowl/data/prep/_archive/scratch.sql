SELECT
    game_id,
    home_team,
    posteam,
    epa,
    success
FROM
    `stuperlatives.pbp_data`
WHERE
    season >= 2015
    AND posteam = 'NE'
    AND play_type = 'run'