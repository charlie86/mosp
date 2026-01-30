WITH
    sjw_games AS (
        SELECT
            *,
            CASE
            -- Identify if Home is SJW
                WHEN home_team = 'KC'
                OR (
                    home_team = 'WAS'
                    AND season <= 2019
                ) THEN 1
                ELSE 0
            END as home_is_sjw,
            CASE
            -- Identify if Away is SJW
                WHEN away_team = 'KC'
                OR (
                    away_team = 'WAS'
                    AND season <= 2019
                ) THEN 1
                ELSE 0
            END as away_is_sjw
        FROM
            `stuperlatives.schedules`
    ),
    filtered_games AS (
        SELECT
            *,
            CASE
                WHEN home_is_sjw = 1 THEN away_team -- Home is SJW, so opponent is Away
                ELSE home_team -- Away is SJW, so opponent is Home
            END as opponent_team,
            CASE
                WHEN home_is_sjw = 1 THEN -1 * result -- Result is Home - Away. If Home is SJW, we want Away perspective (opp)
                ELSE result -- If Away is SJW, Home is Opponent, result is good
            END as opponent_point_diff,
            CASE
                WHEN home_is_sjw = 1 THEN CASE
                    WHEN result < 0 THEN 1
                    ELSE 0
                END -- Home lost (res<0) -> Away (Opp) Won
                ELSE CASE
                    WHEN result > 0 THEN 1
                    ELSE 0
                END -- Home won (res>0) -> Home (Opp) Won
            END as opponent_win
        FROM
            sjw_games
        WHERE
            (
                home_is_sjw = 1
                OR away_is_sjw = 1
            )
            AND NOT (
                home_is_sjw = 1
                AND away_is_sjw = 1
            ) -- Exclude SJW vs SJW
    )
SELECT
    opponent_team as team,
    SUM(opponent_win) as wins,
    COUNT(*) as games,
    SUM(opponent_point_diff) as total_point_diff,
    SUM(opponent_win) / COUNT(*) as win_pct
FROM
    filtered_games
GROUP BY
    team
HAVING
    games >= 3
ORDER BY
    win_pct DESC,
    total_point_diff DESC
LIMIT
    10