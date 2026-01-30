/*
Ginger Sun Analysis

analyzes the performance of known Red Headed QBs (The "Ginger Avengers")
in "Sunny" vs other weather conditions.

Cohort: 
- Andy Dalton
- Carson Wentz
- Sam Darnold
- Cooper Rush
- Mike Glennon

Weather Definition:
- Sunny: description contains 'sunny' or 'clear'
- Indoors: roof is 'dome' or 'closed'
- Other: everything else
*/
SELECT
    passer_player_name as player,
    CASE
        WHEN LOWER(weather) LIKE '%sunny%'
        OR LOWER(weather) LIKE '%clear%' THEN 'Sunny'
        WHEN roof = 'dome'
        or roof = 'closed' THEN 'Indoors'
        ELSE 'Cloudy/Rain/Other'
    END as weather_condition,
    COUNT(*) as attempts,
    Round(AVG(success), 3) as success_rate,
    Round(AVG(epa), 3) as avg_epa,
    Round(AVG(cpoe), 1) as avg_cpoe
FROM
    `stuperlatives.pbp_data`
WHERE
    passer_player_name IN (
        'A.Dalton',
        'C.Wentz',
        'S.Darnold',
        'C.Rush',
        'M.Glennon'
    )
    AND season >= 2016
    AND pass_attempt = 1
GROUP BY
    1,
    2
ORDER BY
    player,
    weather_condition