# Stuperlatives: Kenneth Walker

**Season:** 2025
**Generated:** 2026-01-27 09:43:44.293495

## Rushing Yards
**Conditions:** Division Rivals, in West

### Leaderboard
| player              |   val |   opps |
|:--------------------|------:|-------:|
| Kenneth Walker III  |   268 |     54 |
| Blake Corum         |   232 |     39 |
| Christian McCaffrey |   232 |     64 |
| Kyren Williams      |   227 |     50 |
| Zach Charbonnet     |   201 |     47 |

### SQL Query
```sql
SELECT 
                        player,
                        SUM(yards) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND div_game = 1 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Rushing Yards
**Conditions:** in West, Home

### Leaderboard
| player              |   val |   opps |
|:--------------------|------:|-------:|
| Kenneth Walker III  |   450 |    100 |
| J.K. Dobbins        |   433 |     79 |
| Christian McCaffrey |   422 |    116 |
| Kimani Vidal        |   420 |    100 |
| Ashton Jeanty       |   385 |    101 |

### SQL Query
```sql
SELECT 
                        player,
                        SUM(yards) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD') AND venue = 'Home'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Rushing Yards
**Conditions:** Pirate Teams, Outdoors

### Leaderboard
| player             |   val |   opps |
|:-------------------|------:|-------:|
| Kenneth Walker III |   142 |     23 |
| Saquon Barkley     |   121 |     41 |
| Emanuel Wilson     |   107 |     28 |
| Zach Charbonnet    |    88 |     23 |

### SQL Query
```sql
SELECT 
                        player,
                        SUM(yards) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('TB', 'MIN', 'LV', 'OAK') AND roof = 'outdoors'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Breakaway Yards
**Conditions:** in West

### Leaderboard
| player             |   val |   opps |
|:-------------------|------:|-------:|
| Kenneth Walker III |   230 |    119 |
| J.K. Dobbins       |   203 |     90 |
| Travis Etienne Jr. |   155 |     72 |
| RJ Harvey          |   143 |     91 |
| Blake Corum        |    98 |     39 |

### SQL Query
```sql
SELECT 
                        player,
                        SUM(breakaway_yards) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Breakaway Yards
**Conditions:** Outdoors, in West

### Leaderboard
| player              |   val |   opps |
|:--------------------|------:|-------:|
| Kenneth Walker III  |   189 |    100 |
| J.K. Dobbins        |   143 |     79 |
| RJ Harvey           |   128 |     72 |
| Travis Etienne Jr.  |    90 |     35 |
| Christian McCaffrey |    62 |    138 |

### SQL Query
```sql
SELECT 
                        player,
                        SUM(breakaway_yards) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Breakaway Yards
**Conditions:** in West, Home

### Leaderboard
| player             |   val |   opps |
|:-------------------|------:|-------:|
| Kenneth Walker III |   189 |    100 |
| J.K. Dobbins       |   143 |     79 |
| RJ Harvey          |   128 |     72 |
| Kimani Vidal       |    98 |    100 |
| Ashton Jeanty      |    64 |    101 |

### SQL Query
```sql
SELECT 
                        player,
                        SUM(breakaway_yards) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD') AND venue = 'Home'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Breakaway Yards
**Conditions:** in West, Near IHOP

### Leaderboard
| player             |   val |   opps |
|:-------------------|------:|-------:|
| Kenneth Walker III |   230 |    119 |
| J.K. Dobbins       |   203 |     90 |
| Travis Etienne Jr. |   155 |     72 |
| RJ Harvey          |   143 |     91 |
| Kimani Vidal       |    98 |    100 |

### SQL Query
```sql
SELECT 
                        player,
                        SUM(breakaway_yards) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD') AND home_team IN ('CAR', 'LV', 'DAL', 'TB', 'HOU', 'NO', 'GB', 'MIA', 'DET', 'CIN', 'NYG', 'ATL', 'NYJ', 'LAC', 'SF', 'DEN', 'LAR', 'SEA', 'WAS', 'JAX', 'BAL', 'ARI', 'PHI')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Breakaway Yards
**Conditions:** Division Rivals, Night Game

### Leaderboard
| player             |   val |   opps |
|:-------------------|------:|-------:|
| Kenneth Walker III |   113 |     30 |
| Chase Brown        |    82 |     26 |
| Saquon Barkley     |    52 |     30 |
| James Cook         |    42 |     34 |
| Breece Hall        |    40 |     28 |

### SQL Query
```sql
SELECT 
                        player,
                        SUM(breakaway_yards) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND div_game = 1 AND start_hour >= 19
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Breakaway Yards
**Conditions:** Division Rivals, in West

### Leaderboard
| player             |   val |   opps |
|:-------------------|------:|-------:|
| Kenneth Walker III |   137 |     54 |
| Blake Corum        |    98 |     39 |
| J.K. Dobbins       |    60 |     29 |
| Kimani Vidal       |    59 |     25 |
| Zach Charbonnet    |    45 |     47 |

### SQL Query
```sql
SELECT 
                        player,
                        SUM(breakaway_yards) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND div_game = 1 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Breakaway Yards
**Conditions:** Night Game, in West

### Leaderboard
| player              |   val |   opps |
|:--------------------|------:|-------:|
| Kenneth Walker III  |   129 |     47 |
| Saquon Barkley      |    71 |     20 |
| Omarion Hampton     |    48 |     36 |
| Christian McCaffrey |    47 |     48 |
| Kimani Vidal        |    39 |     62 |

### SQL Query
```sql
SELECT 
                        player,
                        SUM(breakaway_yards) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour >= 19 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Breakaway Yards
**Conditions:** Pirate Teams, Day Game

### Leaderboard
| player             |   val |   opps |
|:-------------------|------:|-------:|
| Kenneth Walker III |    77 |     23 |
| Kimani Vidal       |    59 |     25 |
| Travis Etienne Jr. |    20 |     22 |
| Saquon Barkley     |    17 |     59 |
| Zach Charbonnet    |    17 |     23 |

### SQL Query
```sql
SELECT 
                        player,
                        SUM(breakaway_yards) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('TB', 'MIN', 'LV', 'OAK') AND start_hour < 19
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Breakaway Yards
**Conditions:** Pirate Teams, Outdoors

### Leaderboard
| player             |   val |   opps |
|:-------------------|------:|-------:|
| Kenneth Walker III |    77 |     23 |
| Zach Charbonnet    |    17 |     23 |
| Saquon Barkley     |    17 |     41 |
| Emanuel Wilson     |     0 |     28 |

### SQL Query
```sql
SELECT 
                        player,
                        SUM(breakaway_yards) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('TB', 'MIN', 'LV', 'OAK') AND roof = 'outdoors'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Breakaway %
**Conditions:** Division Rivals

### Leaderboard
| player             |      val |   opps |
|:-------------------|---------:|-------:|
| Kenneth Walker III | 0.483582 |     70 |
| TreVeyon Henderson | 0.479508 |     42 |
| Saquon Barkley     | 0.457346 |     75 |
| De'Von Achane      | 0.43326  |     72 |
| Jahmyr Gibbs       | 0.417476 |     50 |

### SQL Query
```sql
SELECT 
                        player,
                        CAST(SUM(breakaway_yards) AS FLOAT) / NULLIF(SUM(yards), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND div_game = 1
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Breakaway %
**Conditions:** in West, Home

### Leaderboard
| player             |      val |   opps |
|:-------------------|---------:|-------:|
| Kenneth Walker III | 0.42     |    100 |
| RJ Harvey          | 0.390244 |     72 |
| J.K. Dobbins       | 0.330254 |     79 |
| Jaret Patterson    | 0.258824 |     23 |
| Kimani Vidal       | 0.233333 |    100 |

### SQL Query
```sql
SELECT 
                        player,
                        CAST(SUM(breakaway_yards) AS FLOAT) / NULLIF(SUM(yards), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD') AND venue = 'Home'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Breakaway %
**Conditions:** Division Rivals, Night Game

### Leaderboard
| player             |      val |   opps |
|:-------------------|---------:|-------:|
| Kenneth Walker III | 0.624309 |     30 |
| Chase Brown        | 0.44086  |     26 |
| Saquon Barkley     | 0.440678 |     30 |
| Breece Hall        | 0.28777  |     28 |
| James Cook         | 0.267516 |     34 |

### SQL Query
```sql
SELECT 
                        player,
                        CAST(SUM(breakaway_yards) AS FLOAT) / NULLIF(SUM(yards), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND div_game = 1 AND start_hour >= 19
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Breakaway %
**Conditions:** Division Rivals, in West

### Leaderboard
| player             |      val |   opps |
|:-------------------|---------:|-------:|
| Kenneth Walker III | 0.511194 |     54 |
| Kimani Vidal       | 0.468254 |     25 |
| Blake Corum        | 0.422414 |     39 |
| J.K. Dobbins       | 0.375    |     29 |
| Zach Charbonnet    | 0.223881 |     47 |

### SQL Query
```sql
SELECT 
                        player,
                        CAST(SUM(breakaway_yards) AS FLOAT) / NULLIF(SUM(yards), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND div_game = 1 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Breakaway %
**Conditions:** Division Rivals, Near IHOP

### Leaderboard
| player             |      val |   opps |
|:-------------------|---------:|-------:|
| Kenneth Walker III | 0.511194 |     54 |
| De'Von Achane      | 0.501266 |     60 |
| Kimani Vidal       | 0.468254 |     25 |
| Saquon Barkley     | 0.457346 |     75 |
| Jaylen Warren      | 0.435714 |     24 |

### SQL Query
```sql
SELECT 
                        player,
                        CAST(SUM(breakaway_yards) AS FLOAT) / NULLIF(SUM(yards), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND div_game = 1 AND home_team IN ('CAR', 'LV', 'DAL', 'TB', 'HOU', 'NO', 'GB', 'MIA', 'DET', 'CIN', 'NYG', 'ATL', 'NYJ', 'LAC', 'SF', 'DEN', 'LAR', 'SEA', 'WAS', 'JAX', 'BAL', 'ARI', 'PHI')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Breakaway %
**Conditions:** Pirate Teams, Day Game

### Leaderboard
| player              |      val |   opps |
|:--------------------|---------:|-------:|
| Kenneth Walker III  | 0.542253 |     23 |
| Kimani Vidal        | 0.468254 |     25 |
| Travis Etienne Jr.  | 0.238095 |     22 |
| Zach Charbonnet     | 0.193182 |     23 |
| Chris Rodriguez Jr. | 0.164835 |     21 |

### SQL Query
```sql
SELECT 
                        player,
                        CAST(SUM(breakaway_yards) AS FLOAT) / NULLIF(SUM(yards), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('TB', 'MIN', 'LV', 'OAK') AND start_hour < 19
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Breakaway %
**Conditions:** Pirate Teams, Outdoors

### Leaderboard
| player             |      val |   opps |
|:-------------------|---------:|-------:|
| Kenneth Walker III | 0.542253 |     23 |
| Zach Charbonnet    | 0.193182 |     23 |
| Saquon Barkley     | 0.140496 |     41 |
| Emanuel Wilson     | 0        |     28 |

### SQL Query
```sql
SELECT 
                        player,
                        CAST(SUM(breakaway_yards) AS FLOAT) / NULLIF(SUM(yards), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('TB', 'MIN', 'LV', 'OAK') AND roof = 'outdoors'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Breakaway %
**Conditions:** Pirate Teams, in West

### Leaderboard
| player             |      val |   opps |
|:-------------------|---------:|-------:|
| Kenneth Walker III | 0.542253 |     23 |
| Kimani Vidal       | 0.403292 |     48 |
| Jaret Patterson    | 0.261905 |     22 |
| Travis Etienne Jr. | 0.238095 |     22 |
| Zach Charbonnet    | 0.193182 |     23 |

### SQL Query
```sql
SELECT 
                        player,
                        CAST(SUM(breakaway_yards) AS FLOAT) / NULLIF(SUM(yards), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('TB', 'MIN', 'LV', 'OAK') AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Missed Tackles Forced
**Conditions:** Night Game, in West

### Leaderboard
| player             |   val |   opps |
|:-------------------|------:|-------:|
| Kenneth Walker III |    12 |     47 |
| Zach Charbonnet    |    10 |     33 |
| Kimani Vidal       |    10 |     62 |
| Ashton Jeanty      |     9 |     36 |
| J.K. Dobbins       |     8 |     34 |

### SQL Query
```sql
SELECT 
                        player,
                        SUM(avoided_tackles) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour >= 19 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Explosive Runs (10+ yds)
**Conditions:** Pirate Teams, Day Game

### Leaderboard
| player              |   val |   opps |
|:--------------------|------:|-------:|
| Emanuel Wilson      |     4 |     28 |
| Kenneth Walker III  |     4 |     23 |
| Chris Rodriguez Jr. |     3 |     21 |
| Travis Etienne Jr.  |     3 |     22 |
| Saquon Barkley      |     3 |     59 |

### SQL Query
```sql
SELECT 
                        player,
                        SUM(explosive) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('TB', 'MIN', 'LV', 'OAK') AND start_hour < 19
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Explosive Runs (10+ yds)
**Conditions:** Pirate Teams, Outdoors

### Leaderboard
| player             |   val |   opps |
|:-------------------|------:|-------:|
| Kenneth Walker III |     4 |     23 |
| Emanuel Wilson     |     4 |     28 |
| Saquon Barkley     |     3 |     41 |
| Zach Charbonnet    |     1 |     23 |

### SQL Query
```sql
SELECT 
                        player,
                        SUM(explosive) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('TB', 'MIN', 'LV', 'OAK') AND roof = 'outdoors'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Explosive Runs (10+ yds)
**Conditions:** Pirate Teams, in West

### Leaderboard
| player             |   val |   opps |
|:-------------------|------:|-------:|
| Kenneth Walker III |     4 |     23 |
| Kimani Vidal       |     4 |     48 |
| Javonte Williams   |     3 |     22 |
| Travis Etienne Jr. |     3 |     22 |
| RJ Harvey          |     2 |     21 |

### SQL Query
```sql
SELECT 
                        player,
                        SUM(explosive) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('TB', 'MIN', 'LV', 'OAK') AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Explosive Rate
**Conditions:** Pirate Teams, Day Game

### Leaderboard
| player              |       val |   opps |
|:--------------------|----------:|-------:|
| Kenneth Walker III  | 0.173913  |     23 |
| Chris Rodriguez Jr. | 0.142857  |     21 |
| Emanuel Wilson      | 0.142857  |     28 |
| Travis Etienne Jr.  | 0.136364  |     22 |
| D'Andre Swift       | 0.0571429 |     35 |

### SQL Query
```sql
SELECT 
                        player,
                        CAST(SUM(explosive) AS FLOAT) / NULLIF(SUM(attempts), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('TB', 'MIN', 'LV', 'OAK') AND start_hour < 19
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Explosive Rate
**Conditions:** Pirate Teams, Outdoors

### Leaderboard
| player             |       val |   opps |
|:-------------------|----------:|-------:|
| Kenneth Walker III | 0.173913  |     23 |
| Emanuel Wilson     | 0.142857  |     28 |
| Saquon Barkley     | 0.0731707 |     41 |
| Zach Charbonnet    | 0.0434783 |     23 |

### SQL Query
```sql
SELECT 
                        player,
                        CAST(SUM(explosive) AS FLOAT) / NULLIF(SUM(attempts), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('TB', 'MIN', 'LV', 'OAK') AND roof = 'outdoors'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Explosive Rate
**Conditions:** Pirate Teams, in West

### Leaderboard
| player             |       val |   opps |
|:-------------------|----------:|-------:|
| Kenneth Walker III | 0.173913  |     23 |
| Travis Etienne Jr. | 0.136364  |     22 |
| Javonte Williams   | 0.136364  |     22 |
| RJ Harvey          | 0.0952381 |     21 |
| Kimani Vidal       | 0.0833333 |     48 |

### SQL Query
```sql
SELECT 
                        player,
                        CAST(SUM(explosive) AS FLOAT) / NULLIF(SUM(attempts), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('TB', 'MIN', 'LV', 'OAK') AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Explosive Rate
**Conditions:** Pirate Teams, Home

### Leaderboard
| player             |       val |   opps |
|:-------------------|----------:|-------:|
| Kenneth Walker III | 0.173913  |     23 |
| Emanuel Wilson     | 0.142857  |     28 |
| Jahmyr Gibbs       | 0.115385  |     26 |
| Saquon Barkley     | 0.0909091 |     22 |
| David Montgomery   | 0.0833333 |     24 |

### SQL Query
```sql
SELECT 
                        player,
                        CAST(SUM(explosive) AS FLOAT) / NULLIF(SUM(attempts), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('TB', 'MIN', 'LV', 'OAK') AND venue = 'Home'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Explosive Rate
**Conditions:** Outdoors, Away

### Leaderboard
| player             |      val |   opps |
|:-------------------|---------:|-------:|
| Kenneth Walker III | 0.244444 |     45 |
| D'Andre Swift      | 0.178571 |     56 |
| Blake Corum        | 0.171875 |     64 |
| James Cook         | 0.154472 |    123 |
| De'Von Achane      | 0.148148 |     54 |

### SQL Query
```sql
SELECT 
                        player,
                        CAST(SUM(explosive) AS FLOAT) / NULLIF(SUM(attempts), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND venue = 'Away'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

## Explosive Rate
**Conditions:** in NorthEast, Away

### Leaderboard
| player             |      val |   opps |
|:-------------------|---------:|-------:|
| Kenneth Walker III | 0.25     |     24 |
| D'Andre Swift      | 0.232558 |     43 |
| De'Von Achane      | 0.193548 |     31 |
| Saquon Barkley     | 0.181818 |     33 |
| Bijan Robinson     | 0.171429 |     35 |

### SQL Query
```sql
SELECT 
                        player,
                        CAST(SUM(explosive) AS FLOAT) / NULLIF(SUM(attempts), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('NE', 'NYJ', 'NYG', 'BUF', 'PHI', 'PIT', 'BAL', 'WAS') AND venue = 'Away'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```
---

