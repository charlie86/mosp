SELECT
  interception_player_name as interception_player_name,
  defteam,
  COUNT(*) as aquatic_ints
FROM
  `stuperlatives.pbp_data`
WHERE
  posteam IN ('MIA', 'SEA', 'LAC', 'SD')
  AND interception = 1
GROUP BY
  1,
  2
ORDER BY
  aquatic_ints DESC
LIMIT
  10