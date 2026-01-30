# Stuperlatives: Sam Darnold

**Season:** 2025

## BTT Rate
**Conditions:** Night Game, in NorthEast

| player         |       val |   opps |
|:---------------|----------:|-------:|
| Sam Darnold    | 0.125     |     24 |
| Dak Prescott   | 0.117647  |     34 |
| Joe Burrow     | 0.0869565 |     46 |
| Jayden Daniels | 0.0625    |     48 |
| Aaron Rodgers  | 0.047619  |     63 |

```sql
SELECT 
                        player,
                        CAST(SUM(big_time_throws) AS FLOAT) / NULLIF(SUM(attempts), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour >= 19 AND home_team IN ('NE', 'NYJ', 'NYG', 'BUF', 'PHI', 'PIT', 'BAL', 'WAS')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## BTT Rate
**Conditions:** Night Game, Home

| player         |       val |   opps |
|:---------------|----------:|-------:|
| Sam Darnold    | 0.107692  |     65 |
| Malik Willis   | 0.0952381 |     21 |
| Jalen Hurts    | 0.0784314 |     51 |
| Jayden Daniels | 0.0625    |     48 |
| Baker Mayfield | 0.0588235 |     34 |

```sql
SELECT 
                        player,
                        CAST(SUM(big_time_throws) AS FLOAT) / NULLIF(SUM(attempts), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour >= 19 AND venue = 'Home'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Big Time Throws
**Conditions:** Outdoors

| player         |   val |   opps |
|:---------------|------:|-------:|
| Sam Darnold    |    27 |    351 |
| Bo Nix         |    24 |    459 |
| Drake Maye     |    22 |    448 |
| Caleb Williams |    22 |    436 |
| Jordan Love    |    21 |    337 |

```sql
SELECT 
                        player,
                        SUM(big_time_throws) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## BTT Rate
**Conditions:** Outdoors, in South

| player           |       val |   opps |
|:-----------------|----------:|-------:|
| Sam Darnold      | 0.1125    |     80 |
| Joe Burrow       | 0.09375   |     32 |
| Drake Maye       | 0.0909091 |     77 |
| Matthew Stafford | 0.0851064 |     94 |
| Kirk Cousins     | 0.0784314 |     51 |

```sql
SELECT 
                        player,
                        CAST(SUM(big_time_throws) AS FLOAT) / NULLIF(SUM(attempts), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND home_team IN ('DAL', 'HOU', 'NO', 'ATL', 'CAR', 'TB', 'MIA', 'JAX', 'TEN')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## BTT Rate
**Conditions:** Outdoors, Away

| player         |       val |   opps |
|:---------------|----------:|-------:|
| Sam Darnold    | 0.0948905 |    137 |
| Joe Burrow     | 0.0875912 |    137 |
| Jaxson Dart    | 0.0818182 |    110 |
| Marcus Mariota | 0.0759494 |     79 |
| J.J. McCarthy  | 0.0754717 |     53 |

```sql
SELECT 
                        player,
                        CAST(SUM(big_time_throws) AS FLOAT) / NULLIF(SUM(attempts), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND venue = 'Away'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## BTT Rate
**Conditions:** in West, Home

| player         |       val |   opps |
|:---------------|----------:|-------:|
| Sam Darnold    | 0.0654206 |    214 |
| Bo Nix         | 0.0651466 |    307 |
| Justin Herbert | 0.0365449 |    301 |
| Brock Purdy    | 0.0300752 |    133 |
| Geno Smith     | 0.0191571 |    261 |

```sql
SELECT 
                        player,
                        CAST(SUM(big_time_throws) AS FLOAT) / NULLIF(SUM(attempts), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD') AND venue = 'Home'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## BTT Rate
**Conditions:** in NorthEast, Near IHOP

| player         |       val |   opps |
|:---------------|----------:|-------:|
| Jordan Love    | 0.125     |     24 |
| Sam Darnold    | 0.125     |     24 |
| Marcus Mariota | 0.0873016 |    126 |
| Joe Burrow     | 0.0869565 |     46 |
| Aaron Rodgers  | 0.078125  |     64 |

```sql
SELECT 
                        player,
                        CAST(SUM(big_time_throws) AS FLOAT) / NULLIF(SUM(attempts), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('NE', 'NYJ', 'NYG', 'BUF', 'PHI', 'PIT', 'BAL', 'WAS') AND home_team IN ('ATL', 'TB', 'LAC', 'PHI', 'MIA', 'JAX', 'WAS', 'ARI', 'DAL', 'NYG', 'NO', 'BAL', 'CAR', 'CIN', 'LV', 'SF', 'DEN', 'DET', 'HOU', 'LAR', 'GB', 'NYJ', 'SEA')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## YPA
**Conditions:** in NorthEast

| player      |      val |   opps |
|:------------|---------:|-------:|
| Sam Darnold | 10.9649  |     57 |
| Geno Smith  | 10.3333  |     63 |
| Mac Jones   |  9.79167 |     24 |
| Jordan Love |  8.7541  |     61 |
| Drake Maye  |  8.70833 |    336 |

```sql
SELECT 
                        player,
                        CAST(SUM(yards) AS FLOAT) / NULLIF(SUM(attempts), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('NE', 'NYJ', 'NYG', 'BUF', 'PHI', 'PIT', 'BAL', 'WAS')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## YPA
**Conditions:** Bird Teams, Day Game

| player       |      val |   opps |
|:-------------|---------:|-------:|
| Sam Darnold  | 10.1667  |     42 |
| Dak Prescott |  9.83333 |     36 |
| Drake Maye   |  8.93103 |     29 |
| Daniel Jones |  8.33929 |     56 |
| Jaxson Dart  |  8.04167 |     24 |

```sql
SELECT 
                        player,
                        CAST(SUM(yards) AS FLOAT) / NULLIF(SUM(attempts), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA') AND start_hour < 19
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## YPA
**Conditions:** Bird Teams, Dome

| player          |     val |   opps |
|:----------------|--------:|-------:|
| Sam Darnold     | 8.76786 |     56 |
| Trevor Lawrence | 8.53333 |     30 |
| Daniel Jones    | 8.33929 |     56 |
| Dak Prescott    | 8.05333 |     75 |
| Tua Tagovailoa  | 7.88462 |     26 |

```sql
SELECT 
                        player,
                        CAST(SUM(yards) AS FLOAT) / NULLIF(SUM(attempts), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA') AND roof IN ('dome', 'closed')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## YPA
**Conditions:** Bird Teams, in South

| player           |     val |   opps |
|:-----------------|--------:|-------:|
| Sam Darnold      | 8.3     |     30 |
| Dak Prescott     | 8.05333 |     75 |
| Matthew Stafford | 7.07895 |     38 |
| Tua Tagovailoa   | 7.06061 |     66 |
| Josh Allen       | 6.92308 |     26 |

```sql
SELECT 
                        player,
                        CAST(SUM(yards) AS FLOAT) / NULLIF(SUM(attempts), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA') AND home_team IN ('DAL', 'HOU', 'NO', 'ATL', 'CAR', 'TB', 'MIA', 'JAX', 'TEN')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## YPA
**Conditions:** Bird Teams, Away

| player          |     val |   opps |
|:----------------|--------:|-------:|
| Sam Darnold     | 8.76786 |     56 |
| Drake Maye      | 8.63636 |     44 |
| Trevor Lawrence | 8.53333 |     30 |
| Baker Mayfield  | 8.4     |     65 |
| Aaron Rodgers   | 8.35294 |     34 |

```sql
SELECT 
                        player,
                        CAST(SUM(yards) AS FLOAT) / NULLIF(SUM(attempts), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA') AND venue = 'Away'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## YPA
**Conditions:** Division Rivals, in West

| player           |     val |   opps |
|:-----------------|--------:|-------:|
| Sam Darnold      | 8.8421  |     95 |
| Matthew Stafford | 8.77586 |    116 |
| Justin Herbert   | 7.89844 |    128 |
| Brock Purdy      | 7.81967 |     61 |
| Mac Jones        | 7.5375  |     80 |

```sql
SELECT 
                        player,
                        CAST(SUM(yards) AS FLOAT) / NULLIF(SUM(attempts), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND div_game = 1 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## YPA
**Conditions:** Night Game, in NorthEast

| player         |      val |   opps |
|:---------------|---------:|-------:|
| Sam Darnold    | 13.75    |     24 |
| Jordan Love    |  9.72973 |     37 |
| Drake Maye     |  8.7482  |    139 |
| Caleb Williams |  8.68966 |     29 |
| Josh Allen     |  8.19048 |    105 |

```sql
SELECT 
                        player,
                        CAST(SUM(yards) AS FLOAT) / NULLIF(SUM(attempts), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour >= 19 AND home_team IN ('NE', 'NYJ', 'NYG', 'BUF', 'PHI', 'PIT', 'BAL', 'WAS')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## YPA
**Conditions:** Night Game, Away

| player         |      val |   opps |
|:---------------|---------:|-------:|
| Sam Darnold    | 11.44    |     50 |
| Justin Herbert |  8.96296 |     27 |
| J.J. McCarthy  |  8.93182 |     44 |
| Drake Maye     |  8.82432 |     74 |
| Brock Purdy    |  8.67647 |     34 |

```sql
SELECT 
                        player,
                        CAST(SUM(yards) AS FLOAT) / NULLIF(SUM(attempts), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour >= 19 AND venue = 'Away'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## YPA
**Conditions:** Dome, in West

| player           |     val |   opps |
|:-----------------|--------:|-------:|
| Sam Darnold      | 9.30769 |     26 |
| Matthew Stafford | 9.06452 |     31 |
| Jayden Daniels   | 8.88461 |     26 |
| Daniel Jones     | 8.47059 |     34 |
| Dak Prescott     | 8.12121 |     33 |

```sql
SELECT 
                        player,
                        CAST(SUM(yards) AS FLOAT) / NULLIF(SUM(attempts), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof IN ('dome', 'closed') AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## YPA
**Conditions:** Outdoors, in NorthEast

| player      |      val |   opps |
|:------------|---------:|-------:|
| Sam Darnold | 10.9649  |     57 |
| Geno Smith  | 10.3333  |     63 |
| Mac Jones   |  9.79167 |     24 |
| Jordan Love |  8.7541  |     61 |
| Drake Maye  |  8.70833 |    336 |

```sql
SELECT 
                        player,
                        CAST(SUM(yards) AS FLOAT) / NULLIF(SUM(attempts), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND home_team IN ('NE', 'NYJ', 'NYG', 'BUF', 'PHI', 'PIT', 'BAL', 'WAS')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## YPA
**Conditions:** Outdoors, Away

| player       |     val |   opps |
|:-------------|--------:|-------:|
| Sam Darnold  | 9.56934 |    137 |
| Drake Maye   | 9.29952 |    207 |
| Mac Jones    | 9.2381  |     63 |
| Tyler Shough | 8.75439 |    114 |
| Geno Smith   | 8.2     |    105 |

```sql
SELECT 
                        player,
                        CAST(SUM(yards) AS FLOAT) / NULLIF(SUM(attempts), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND venue = 'Away'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Big Time Throws
**Conditions:** Night Game, in West

| player           |   val |   opps |
|:-----------------|------:|-------:|
| Sam Darnold      |     8 |     91 |
| Matthew Stafford |     5 |     49 |
| Caleb Williams   |     4 |     42 |
| Justin Herbert   |     4 |    145 |
| Patrick Mahomes  |     3 |     39 |

```sql
SELECT 
                        player,
                        SUM(big_time_throws) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour >= 19 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Big Time Throws
**Conditions:** Night Game, Home

| player          |   val |   opps |
|:----------------|------:|-------:|
| Sam Darnold     |     7 |     65 |
| Patrick Mahomes |     5 |     97 |
| Josh Allen      |     5 |    105 |
| Jalen Hurts     |     4 |     51 |
| Jordan Love     |     3 |     67 |

```sql
SELECT 
                        player,
                        SUM(big_time_throws) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour >= 19 AND venue = 'Home'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Big Time Throws
**Conditions:** Night Game, Near IHOP

| player           |   val |   opps |
|:-----------------|------:|-------:|
| Sam Darnold      |    11 |    115 |
| Matthew Stafford |    10 |     87 |
| Dak Prescott     |    10 |    231 |
| Baker Mayfield   |     7 |    122 |
| Jalen Hurts      |     7 |    150 |

```sql
SELECT 
                        player,
                        SUM(big_time_throws) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour >= 19 AND home_team IN ('ATL', 'TB', 'LAC', 'PHI', 'MIA', 'JAX', 'WAS', 'ARI', 'DAL', 'NYG', 'NO', 'BAL', 'CAR', 'CIN', 'LV', 'SF', 'DEN', 'DET', 'HOU', 'LAR', 'GB', 'NYJ', 'SEA')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Big Time Throws
**Conditions:** Outdoors, Near IHOP

| player           |   val |   opps |
|:-----------------|------:|-------:|
| Sam Darnold      |    23 |    292 |
| Bo Nix           |    22 |    421 |
| Jordan Love      |    19 |    262 |
| Baker Mayfield   |    18 |    330 |
| Matthew Stafford |    15 |    205 |

```sql
SELECT 
                        player,
                        SUM(big_time_throws) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND home_team IN ('ATL', 'TB', 'LAC', 'PHI', 'MIA', 'JAX', 'WAS', 'ARI', 'DAL', 'NYG', 'NO', 'BAL', 'CAR', 'CIN', 'LV', 'SF', 'DEN', 'DET', 'HOU', 'LAR', 'GB', 'NYJ', 'SEA')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## BTT Rate
**Conditions:** Night Game

| player           |       val |   opps |
|:-----------------|----------:|-------:|
| Sam Darnold      | 0.0956522 |    115 |
| Malik Willis     | 0.09375   |     32 |
| Joe Burrow       | 0.0869565 |     46 |
| Matthew Stafford | 0.0769231 |    169 |
| J.J. McCarthy    | 0.0769231 |     65 |

```sql
SELECT 
                        player,
                        CAST(SUM(big_time_throws) AS FLOAT) / NULLIF(SUM(attempts), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour >= 19
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## YPA
**Conditions:** in NorthEast, Away

| player      |      val |   opps |
|:------------|---------:|-------:|
| Sam Darnold | 10.9649  |     57 |
| Geno Smith  | 10.3333  |     63 |
| Mac Jones   |  9.79167 |     24 |
| Drake Maye  |  9.56842 |     95 |
| Jordan Love |  8.7541  |     61 |

```sql
SELECT 
                        player,
                        CAST(SUM(yards) AS FLOAT) / NULLIF(SUM(attempts), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('NE', 'NYJ', 'NYG', 'BUF', 'PHI', 'PIT', 'BAL', 'WAS') AND venue = 'Away'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## YPA
**Conditions:** in NorthEast, Near IHOP

| player        |      val |   opps |
|:--------------|---------:|-------:|
| Sam Darnold   | 13.75    |     24 |
| Geno Smith    |  9.96552 |     29 |
| Mac Jones     |  9.79167 |     24 |
| Drake Maye    |  9.78462 |     65 |
| Aaron Rodgers |  8.25    |     64 |

```sql
SELECT 
                        player,
                        CAST(SUM(yards) AS FLOAT) / NULLIF(SUM(attempts), 0) as val,
                        SUM(attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('NE', 'NYJ', 'NYG', 'BUF', 'PHI', 'PIT', 'BAL', 'WAS') AND home_team IN ('ATL', 'TB', 'LAC', 'PHI', 'MIA', 'JAX', 'WAS', 'ARI', 'DAL', 'NYG', 'NO', 'BAL', 'CAR', 'CIN', 'LV', 'SF', 'DEN', 'DET', 'HOU', 'LAR', 'GB', 'NYJ', 'SEA')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep Yards
**Conditions:** Night Game, in West

| player         |   val |   opps |
|:---------------|------:|-------:|
| Sam Darnold    |   168 |     10 |
| Justin Herbert |   151 |     17 |
| Geno Smith     |    51 |     11 |

```sql
SELECT 
                        player,
                        SUM(deep_yards) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour >= 19 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep Yards
**Conditions:** Outdoors, Near IHOP

| player         |   val |   opps |
|:---------------|------:|-------:|
| Bo Nix         |   671 |     52 |
| Sam Darnold    |   671 |     30 |
| Baker Mayfield |   658 |     40 |
| Jordan Love    |   615 |     44 |
| Jalen Hurts    |   570 |     43 |

```sql
SELECT 
                        player,
                        SUM(deep_yards) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND home_team IN ('ATL', 'TB', 'LAC', 'PHI', 'MIA', 'JAX', 'WAS', 'ARI', 'DAL', 'NYG', 'NO', 'BAL', 'CAR', 'CIN', 'LV', 'SF', 'DEN', 'DET', 'HOU', 'LAR', 'GB', 'NYJ', 'SEA')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep Yards
**Conditions:** in South, Away

| player           |   val |   opps |
|:-----------------|------:|-------:|
| Sam Darnold      |   339 |     14 |
| Drake Maye       |   314 |     15 |
| Matthew Stafford |   279 |     24 |
| Russell Wilson   |   264 |     11 |
| Tyler Shough     |   264 |     17 |

```sql
SELECT 
                        player,
                        SUM(deep_yards) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('DAL', 'HOU', 'NO', 'ATL', 'CAR', 'TB', 'MIA', 'JAX', 'TEN') AND venue = 'Away'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep TDs
**Conditions:** Outdoors, Away

| player         |   val |   opps |
|:---------------|------:|-------:|
| Sam Darnold    |     6 |     17 |
| Aaron Rodgers  |     4 |     20 |
| Joe Burrow     |     4 |     20 |
| Tyler Shough   |     4 |     18 |
| Caleb Williams |     4 |     25 |

```sql
SELECT 
                        player,
                        SUM(deep_touchdowns) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND venue = 'Away'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep BTT
**Conditions:** Outdoors

| player          |   val |   opps |
|:----------------|------:|-------:|
| Sam Darnold     |    20 |     37 |
| Caleb Williams  |    19 |     57 |
| Jordan Love     |    18 |     48 |
| Bo Nix          |    17 |     55 |
| Trevor Lawrence |    15 |     56 |

```sql
SELECT 
                        player,
                        SUM(deep_big_time_throws) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep BTT
**Conditions:** Night Game, in West

| player         |   val |   opps |
|:---------------|------:|-------:|
| Sam Darnold    |     5 |     10 |
| Justin Herbert |     3 |     17 |
| Geno Smith     |     2 |     11 |

```sql
SELECT 
                        player,
                        SUM(deep_big_time_throws) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour >= 19 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep BTT
**Conditions:** Outdoors, Away

| player           |   val |   opps |
|:-----------------|------:|-------:|
| Sam Darnold      |    11 |     17 |
| Matthew Stafford |    11 |     33 |
| Caleb Williams   |    10 |     25 |
| Dak Prescott     |     9 |     24 |
| Aaron Rodgers    |     8 |     20 |

```sql
SELECT 
                        player,
                        SUM(deep_big_time_throws) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND venue = 'Away'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep BTT Rate
**Conditions:** Night Game

| player           |      val |   opps |
|:-----------------|---------:|-------:|
| Sam Darnold      | 0.615385 |     13 |
| Caleb Williams   | 0.444444 |     18 |
| J.J. McCarthy    | 0.416667 |     12 |
| Josh Allen       | 0.35     |     20 |
| Matthew Stafford | 0.333333 |     24 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_big_time_throws) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour >= 19
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep BTT Rate
**Conditions:** Outdoors

| player         |      val |   opps |
|:---------------|---------:|-------:|
| Sam Darnold    | 0.540541 |     37 |
| Kirk Cousins   | 0.4      |     10 |
| Tyler Shough   | 0.388889 |     18 |
| Bryce Young    | 0.387097 |     31 |
| Jayden Daniels | 0.384615 |     13 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_big_time_throws) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep BTT Rate
**Conditions:** Division Rivals, in West

| player           |      val |   opps |
|:-----------------|---------:|-------:|
| Sam Darnold      | 0.5      |     10 |
| Matthew Stafford | 0.4375   |     16 |
| Patrick Mahomes  | 0.4      |     10 |
| Bo Nix           | 0.294118 |     17 |
| Justin Herbert   | 0.266667 |     15 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_big_time_throws) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND div_game = 1 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep BTT Rate
**Conditions:** Night Game, in West

| player         |      val |   opps |
|:---------------|---------:|-------:|
| Sam Darnold    | 0.5      |     10 |
| Geno Smith     | 0.181818 |     11 |
| Justin Herbert | 0.176471 |     17 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_big_time_throws) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour >= 19 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep BTT Rate
**Conditions:** Night Game, Near IHOP

| player           |      val |   opps |
|:-----------------|---------:|-------:|
| Sam Darnold      | 0.615385 |     13 |
| Kirk Cousins     | 0.333333 |     12 |
| Matthew Stafford | 0.333333 |     15 |
| Baker Mayfield   | 0.315789 |     19 |
| Jalen Hurts      | 0.3      |     20 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_big_time_throws) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour >= 19 AND home_team IN ('ATL', 'TB', 'LAC', 'PHI', 'MIA', 'JAX', 'WAS', 'ARI', 'DAL', 'NYG', 'NO', 'BAL', 'CAR', 'CIN', 'LV', 'SF', 'DEN', 'DET', 'HOU', 'LAR', 'GB', 'NYJ', 'SEA')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep BTT Rate
**Conditions:** Outdoors, in West

| player           |      val |   opps |
|:-----------------|---------:|-------:|
| Sam Darnold      | 0.45     |     20 |
| Bo Nix           | 0.355556 |     45 |
| Matthew Stafford | 0.333333 |     12 |
| Brock Purdy      | 0.263158 |     19 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_big_time_throws) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep BTT Rate
**Conditions:** Outdoors, in South

| player         |      val |   opps |
|:---------------|---------:|-------:|
| Sam Darnold    | 0.636364 |     11 |
| Bryce Young    | 0.423077 |     26 |
| Tyler Shough   | 0.411765 |     17 |
| Drake Maye     | 0.4      |     10 |
| Tua Tagovailoa | 0.37037  |     27 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_big_time_throws) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND home_team IN ('DAL', 'HOU', 'NO', 'ATL', 'CAR', 'TB', 'MIA', 'JAX', 'TEN')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep BTT Rate
**Conditions:** Outdoors, Away

| player        |      val |   opps |
|:--------------|---------:|-------:|
| Sam Darnold   | 0.647059 |     17 |
| Jordan Love   | 0.466667 |     15 |
| Aaron Rodgers | 0.4      |     20 |
| Joe Burrow    | 0.4      |     20 |
| Kirk Cousins  | 0.4      |     10 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_big_time_throws) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND venue = 'Away'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep BTT Rate
**Conditions:** in West, Home

| player         |      val |   opps |
|:---------------|---------:|-------:|
| Sam Darnold    | 0.45     |     20 |
| Bo Nix         | 0.355556 |     45 |
| Justin Herbert | 0.243243 |     37 |
| Geno Smith     | 0.15     |     20 |
| Brock Purdy    | 0.142857 |     14 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_big_time_throws) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD') AND venue = 'Home'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep YPA
**Conditions:** All Games

| player         |     val |   opps |
|:---------------|--------:|-------:|
| Sam Darnold    | 20.34   |     50 |
| Drake Maye     | 17.2586 |     58 |
| Brock Purdy    | 17.1333 |     30 |
| Russell Wilson | 17.0588 |     17 |
| Dak Prescott   | 15.7534 |     73 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_yards) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep YPA
**Conditions:** Night Game

| player         |     val |   opps |
|:---------------|--------:|-------:|
| Sam Darnold    | 18.8462 |     13 |
| J.J. McCarthy  | 17.25   |     12 |
| Caleb Williams | 17.1111 |     18 |
| Brock Purdy    | 14.9091 |     11 |
| Drake Maye     | 14.2381 |     21 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_yards) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour >= 19
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep YPA
**Conditions:** Outdoors

| player         |     val |   opps |
|:---------------|--------:|-------:|
| Sam Darnold    | 23.4324 |     37 |
| Geno Smith     | 20.8462 |     13 |
| Brock Purdy    | 17.6364 |     22 |
| Drake Maye     | 16.4717 |     53 |
| Baker Mayfield | 16.2381 |     42 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_yards) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep YPA
**Conditions:** in West

| player           |     val |   opps |
|:-----------------|--------:|-------:|
| Sam Darnold      | 21.2174 |     23 |
| Brock Purdy      | 17.8261 |     23 |
| Matthew Stafford | 17.25   |     16 |
| Patrick Mahomes  | 14.8    |     10 |
| Cam Ward         | 14.0556 |     18 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_yards) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep YPA
**Conditions:** in South

| player          |     val |   opps |
|:----------------|--------:|-------:|
| Sam Darnold     | 24.2143 |     14 |
| Russell Wilson  | 24      |     11 |
| Drake Maye      | 20.9333 |     15 |
| Dak Prescott    | 16.8293 |     41 |
| Spencer Rattler | 14.9444 |     18 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_yards) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('DAL', 'HOU', 'NO', 'ATL', 'CAR', 'TB', 'MIA', 'JAX', 'TEN')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep YPA
**Conditions:** Home

| player           |     val |   opps |
|:-----------------|--------:|-------:|
| Sam Darnold      | 21      |     20 |
| Joe Flacco       | 17.8824 |     17 |
| Dak Prescott     | 17.6923 |     39 |
| Matthew Stafford | 16.9412 |     34 |
| Baker Mayfield   | 16.9259 |     27 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_yards) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND venue = 'Home'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep YPA
**Conditions:** Near IHOP

| player         |     val |   opps |
|:---------------|--------:|-------:|
| Sam Darnold    | 21.4444 |     36 |
| Drake Maye     | 19.6522 |     23 |
| Aaron Rodgers  | 18.1    |     20 |
| Brock Purdy    | 17.8261 |     23 |
| Russell Wilson | 17.0588 |     17 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_yards) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('ATL', 'TB', 'LAC', 'PHI', 'MIA', 'JAX', 'WAS', 'ARI', 'DAL', 'NYG', 'NO', 'BAL', 'CAR', 'CIN', 'LV', 'SF', 'DEN', 'DET', 'HOU', 'LAR', 'GB', 'NYJ', 'SEA')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep YPA
**Conditions:** in West, Near IHOP

| player           |     val |   opps |
|:-----------------|--------:|-------:|
| Sam Darnold      | 21.2174 |     23 |
| Brock Purdy      | 17.8261 |     23 |
| Matthew Stafford | 17.25   |     16 |
| Patrick Mahomes  | 14.8    |     10 |
| Cam Ward         | 14.0556 |     18 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_yards) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD') AND home_team IN ('ATL', 'TB', 'LAC', 'PHI', 'MIA', 'JAX', 'WAS', 'ARI', 'DAL', 'NYG', 'NO', 'BAL', 'CAR', 'CIN', 'LV', 'SF', 'DEN', 'DET', 'HOU', 'LAR', 'GB', 'NYJ', 'SEA')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep YPA
**Conditions:** in South, Away

| player         |     val |   opps |
|:---------------|--------:|-------:|
| Sam Darnold    | 24.2143 |     14 |
| Russell Wilson | 24      |     11 |
| Drake Maye     | 20.9333 |     15 |
| Tyler Shough   | 15.5294 |     17 |
| Bryce Young    | 15.2    |     10 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_yards) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('DAL', 'HOU', 'NO', 'ATL', 'CAR', 'TB', 'MIA', 'JAX', 'TEN') AND venue = 'Away'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep YPA
**Conditions:** Home, Near IHOP

| player         |     val |   opps |
|:---------------|--------:|-------:|
| Sam Darnold    | 21      |     20 |
| Joe Flacco     | 17.8824 |     17 |
| Dak Prescott   | 17.6923 |     39 |
| Baker Mayfield | 16.9259 |     27 |
| Brock Purdy    | 16.7857 |     14 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_yards) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND venue = 'Home' AND home_team IN ('ATL', 'TB', 'LAC', 'PHI', 'MIA', 'JAX', 'WAS', 'ARI', 'DAL', 'NYG', 'NO', 'BAL', 'CAR', 'CIN', 'LV', 'SF', 'DEN', 'DET', 'HOU', 'LAR', 'GB', 'NYJ', 'SEA')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep Completion %
**Conditions:** Night Game

| player         |      val |   opps |
|:---------------|---------:|-------:|
| Sam Darnold    | 0.692308 |     13 |
| Caleb Williams | 0.555556 |     18 |
| Brock Purdy    | 0.545455 |     11 |
| Drake Maye     | 0.52381  |     21 |
| J.J. McCarthy  | 0.5      |     12 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_completions) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour >= 19
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep Completion %
**Conditions:** Outdoors

| player      |      val |   opps |
|:------------|---------:|-------:|
| Sam Darnold | 0.675676 |     37 |
| Geno Smith  | 0.615385 |     13 |
| Brock Purdy | 0.590909 |     22 |
| Drake Maye  | 0.528302 |     53 |
| Jordan Love | 0.479167 |     48 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_completions) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep Completion %
**Conditions:** in West

| player           |      val |   opps |
|:-----------------|---------:|-------:|
| Sam Darnold      | 0.652174 |     23 |
| Brock Purdy      | 0.608696 |     23 |
| Matthew Stafford | 0.5625   |     16 |
| Bo Nix           | 0.45098  |     51 |
| Cam Ward         | 0.444444 |     18 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_completions) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep Completion %
**Conditions:** Home

| player       |      val |   opps |
|:-------------|---------:|-------:|
| Sam Darnold  | 0.65     |     20 |
| Joe Flacco   | 0.588235 |     17 |
| Brock Purdy  | 0.571429 |     14 |
| Daniel Jones | 0.545455 |     22 |
| Dak Prescott | 0.538462 |     39 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_completions) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND venue = 'Home'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep Completion %
**Conditions:** Near IHOP

| player        |      val |   opps |
|:--------------|---------:|-------:|
| Sam Darnold   | 0.638889 |     36 |
| Brock Purdy   | 0.608696 |     23 |
| Drake Maye    | 0.608696 |     23 |
| Joe Flacco    | 0.526316 |     19 |
| Aaron Rodgers | 0.5      |     20 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_completions) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('ATL', 'TB', 'LAC', 'PHI', 'MIA', 'JAX', 'WAS', 'ARI', 'DAL', 'NYG', 'NO', 'BAL', 'CAR', 'CIN', 'LV', 'SF', 'DEN', 'DET', 'HOU', 'LAR', 'GB', 'NYJ', 'SEA')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep YPA
**Conditions:** Division Rivals, in West

| player           |     val |   opps |
|:-----------------|--------:|-------:|
| Sam Darnold      | 19.8    |     10 |
| Matthew Stafford | 17.25   |     16 |
| Patrick Mahomes  | 14.8    |     10 |
| Bo Nix           | 14.7647 |     17 |
| Justin Herbert   | 10.2    |     15 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_yards) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND div_game = 1 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep YPA
**Conditions:** Night Game, in West

| player         |      val |   opps |
|:---------------|---------:|-------:|
| Sam Darnold    | 16.8     |     10 |
| Justin Herbert |  8.88235 |     17 |
| Geno Smith     |  4.63636 |     11 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_yards) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour >= 19 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep YPA
**Conditions:** Night Game, Near IHOP

| player           |     val |   opps |
|:-----------------|--------:|-------:|
| Sam Darnold      | 18.8462 |     13 |
| Patrick Mahomes  | 12.1176 |     17 |
| Jalen Hurts      | 11.6    |     20 |
| Dak Prescott     | 11.4545 |     33 |
| Matthew Stafford | 10.4    |     15 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_yards) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour >= 19 AND home_team IN ('ATL', 'TB', 'LAC', 'PHI', 'MIA', 'JAX', 'WAS', 'ARI', 'DAL', 'NYG', 'NO', 'BAL', 'CAR', 'CIN', 'LV', 'SF', 'DEN', 'DET', 'HOU', 'LAR', 'GB', 'NYJ', 'SEA')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep YPA
**Conditions:** Day Game, in West

| player           |     val |   opps |
|:-----------------|--------:|-------:|
| Sam Darnold      | 24.6154 |     13 |
| Brock Purdy      | 19.8125 |     16 |
| Matthew Stafford | 17.4    |     10 |
| Cam Ward         | 14.0556 |     18 |
| Bo Nix           | 13.3556 |     45 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_yards) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour < 19 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep YPA
**Conditions:** Day Game, in South

| player           |     val |   opps |
|:-----------------|--------:|-------:|
| Sam Darnold      | 24.2143 |     14 |
| Russell Wilson   | 24      |     11 |
| Drake Maye       | 20.9333 |     15 |
| Dak Prescott     | 18.92   |     25 |
| Matthew Stafford | 15      |     15 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_yards) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour < 19 AND home_team IN ('DAL', 'HOU', 'NO', 'ATL', 'CAR', 'TB', 'MIA', 'JAX', 'TEN')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep YPA
**Conditions:** Day Game, Home

| player           |     val |   opps |
|:-----------------|--------:|-------:|
| Sam Darnold      | 24.6154 |     13 |
| Dak Prescott     | 20.5652 |     23 |
| Matthew Stafford | 18.16   |     25 |
| Joe Flacco       | 17.0714 |     14 |
| Marcus Mariota   | 17      |     12 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_yards) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour < 19 AND venue = 'Home'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep YPA
**Conditions:** Day Game, Near IHOP

| player         |     val |   opps |
|:---------------|--------:|-------:|
| Sam Darnold    | 22.913  |     23 |
| Russell Wilson | 22      |     12 |
| Aaron Rodgers  | 21.4545 |     11 |
| Drake Maye     | 21.4    |     15 |
| Brock Purdy    | 19.8125 |     16 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_yards) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour < 19 AND home_team IN ('ATL', 'TB', 'LAC', 'PHI', 'MIA', 'JAX', 'WAS', 'ARI', 'DAL', 'NYG', 'NO', 'BAL', 'CAR', 'CIN', 'LV', 'SF', 'DEN', 'DET', 'HOU', 'LAR', 'GB', 'NYJ', 'SEA')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep YPA
**Conditions:** Outdoors, in West

| player           |     val |   opps |
|:-----------------|--------:|-------:|
| Sam Darnold      | 21      |     20 |
| Brock Purdy      | 18.6842 |     19 |
| Bo Nix           | 14.2222 |     45 |
| Matthew Stafford | 13.0833 |     12 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_yards) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep YPA
**Conditions:** Outdoors, in South

| player           |     val |   opps |
|:-----------------|--------:|-------:|
| Sam Darnold      | 27.8182 |     11 |
| Drake Maye       | 18.6    |     10 |
| Tyler Shough     | 15.5294 |     17 |
| Baker Mayfield   | 15.1429 |     35 |
| Matthew Stafford | 15      |     15 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_yards) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND home_team IN ('DAL', 'HOU', 'NO', 'ATL', 'CAR', 'TB', 'MIA', 'JAX', 'TEN')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep YPA
**Conditions:** Outdoors, Home

| player         |     val |   opps |
|:---------------|--------:|-------:|
| Sam Darnold    | 21      |     20 |
| Joe Flacco     | 17.8824 |     17 |
| Baker Mayfield | 16.9259 |     27 |
| Brock Purdy    | 16.7857 |     14 |
| Josh Allen     | 15      |     29 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_yards) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND venue = 'Home'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep YPA
**Conditions:** Outdoors, Away

| player         |     val |   opps |
|:---------------|--------:|-------:|
| Sam Darnold    | 26.2941 |     17 |
| Geno Smith     | 20.8462 |     13 |
| Drake Maye     | 20.1304 |     23 |
| Aaron Rodgers  | 17.85   |     20 |
| Caleb Williams | 16.16   |     25 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_yards) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND venue = 'Away'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep YPA
**Conditions:** in West, Home

| player         |     val |   opps |
|:---------------|--------:|-------:|
| Sam Darnold    | 21      |     20 |
| Brock Purdy    | 16.7857 |     14 |
| Bo Nix         | 14.2222 |     45 |
| Justin Herbert |  9.7027 |     37 |
| Geno Smith     |  4.25   |     20 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_yards) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD') AND venue = 'Home'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep Completion %
**Conditions:** Division Rivals, in West

| player           |      val |   opps |
|:-----------------|---------:|-------:|
| Sam Darnold      | 0.6      |     10 |
| Matthew Stafford | 0.5625   |     16 |
| Bo Nix           | 0.411765 |     17 |
| Justin Herbert   | 0.333333 |     15 |
| Patrick Mahomes  | 0.3      |     10 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_completions) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND div_game = 1 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep Completion %
**Conditions:** Night Game, in West

| player         |      val |   opps |
|:---------------|---------:|-------:|
| Sam Darnold    | 0.6      |     10 |
| Justin Herbert | 0.235294 |     17 |
| Geno Smith     | 0.181818 |     11 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_completions) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour >= 19 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep Completion %
**Conditions:** Night Game, Near IHOP

| player           |      val |   opps |
|:-----------------|---------:|-------:|
| Sam Darnold      | 0.692308 |     13 |
| Dak Prescott     | 0.393939 |     33 |
| Patrick Mahomes  | 0.352941 |     17 |
| Jalen Hurts      | 0.35     |     20 |
| Matthew Stafford | 0.333333 |     15 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_completions) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour >= 19 AND home_team IN ('ATL', 'TB', 'LAC', 'PHI', 'MIA', 'JAX', 'WAS', 'ARI', 'DAL', 'NYG', 'NO', 'BAL', 'CAR', 'CIN', 'LV', 'SF', 'DEN', 'DET', 'HOU', 'LAR', 'GB', 'NYJ', 'SEA')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep Completion %
**Conditions:** Day Game, in West

| player           |      val |   opps |
|:-----------------|---------:|-------:|
| Sam Darnold      | 0.692308 |     13 |
| Brock Purdy      | 0.6875   |     16 |
| Matthew Stafford | 0.6      |     10 |
| Bo Nix           | 0.444444 |     45 |
| Cam Ward         | 0.444444 |     18 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_completions) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour < 19 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep Completion %
**Conditions:** Day Game, Home

| player       |      val |   opps |
|:-------------|---------:|-------:|
| Sam Darnold  | 0.692308 |     13 |
| Joe Flacco   | 0.571429 |     14 |
| Dak Prescott | 0.565217 |     23 |
| Jared Goff   | 0.555556 |     18 |
| Daniel Jones | 0.545455 |     22 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_completions) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour < 19 AND venue = 'Home'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep Completion %
**Conditions:** Outdoors, in West

| player           |      val |   opps |
|:-----------------|---------:|-------:|
| Sam Darnold      | 0.65     |     20 |
| Brock Purdy      | 0.631579 |     19 |
| Bo Nix           | 0.488889 |     45 |
| Matthew Stafford | 0.416667 |     12 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_completions) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep Completion %
**Conditions:** Outdoors, in South

| player           |      val |   opps |
|:-----------------|---------:|-------:|
| Sam Darnold      | 0.636364 |     11 |
| Drake Maye       | 0.5      |     10 |
| Matthew Stafford | 0.466667 |     15 |
| Bryce Young      | 0.423077 |     26 |
| Tyler Shough     | 0.411765 |     17 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_completions) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND home_team IN ('DAL', 'HOU', 'NO', 'ATL', 'CAR', 'TB', 'MIA', 'JAX', 'TEN')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep Completion %
**Conditions:** Outdoors, Home

| player      |      val |   opps |
|:------------|---------:|-------:|
| Sam Darnold | 0.65     |     20 |
| Joe Flacco  | 0.588235 |     17 |
| Brock Purdy | 0.571429 |     14 |
| Josh Allen  | 0.517241 |     29 |
| Bryce Young | 0.5      |     22 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_completions) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND venue = 'Home'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep Completion %
**Conditions:** Outdoors, Away

| player        |      val |   opps |
|:--------------|---------:|-------:|
| Sam Darnold   | 0.705882 |     17 |
| Drake Maye    | 0.652174 |     23 |
| Geno Smith    | 0.615385 |     13 |
| Jordan Love   | 0.6      |     15 |
| Aaron Rodgers | 0.55     |     20 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_completions) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND venue = 'Away'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep Completion %
**Conditions:** in West, Home

| player         |      val |   opps |
|:---------------|---------:|-------:|
| Sam Darnold    | 0.65     |     20 |
| Brock Purdy    | 0.571429 |     14 |
| Bo Nix         | 0.488889 |     45 |
| Justin Herbert | 0.324324 |     37 |
| Geno Smith     | 0.15     |     20 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_completions) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD') AND venue = 'Home'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep Completion %
**Conditions:** in West, Near IHOP

| player           |      val |   opps |
|:-----------------|---------:|-------:|
| Sam Darnold      | 0.652174 |     23 |
| Brock Purdy      | 0.608696 |     23 |
| Matthew Stafford | 0.5625   |     16 |
| Bo Nix           | 0.45098  |     51 |
| Cam Ward         | 0.444444 |     18 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_completions) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD') AND home_team IN ('ATL', 'TB', 'LAC', 'PHI', 'MIA', 'JAX', 'WAS', 'ARI', 'DAL', 'NYG', 'NO', 'BAL', 'CAR', 'CIN', 'LV', 'SF', 'DEN', 'DET', 'HOU', 'LAR', 'GB', 'NYJ', 'SEA')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep Completion %
**Conditions:** Home, Near IHOP

| player       |      val |   opps |
|:-------------|---------:|-------:|
| Sam Darnold  | 0.65     |     20 |
| Joe Flacco   | 0.588235 |     17 |
| Brock Purdy  | 0.571429 |     14 |
| Dak Prescott | 0.538462 |     39 |
| Bryce Young  | 0.5      |     22 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_completions) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND venue = 'Home' AND home_team IN ('ATL', 'TB', 'LAC', 'PHI', 'MIA', 'JAX', 'WAS', 'ARI', 'DAL', 'NYG', 'NO', 'BAL', 'CAR', 'CIN', 'LV', 'SF', 'DEN', 'DET', 'HOU', 'LAR', 'GB', 'NYJ', 'SEA')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Deep Completion %
**Conditions:** Away, Near IHOP

| player         |      val |   opps |
|:---------------|---------:|-------:|
| Sam Darnold    | 0.625    |     16 |
| Drake Maye     | 0.608696 |     23 |
| Geno Smith     | 0.583333 |     12 |
| Russell Wilson | 0.583333 |     12 |
| Aaron Rodgers  | 0.5      |     20 |

```sql
SELECT 
                        player,
                        CAST(SUM(deep_completions) AS FLOAT) / NULLIF(SUM(deep_attempts), 0) as val,
                        SUM(deep_attempts) as opps
                    FROM data
                    WHERE 1=1 AND venue = 'Away' AND home_team IN ('ATL', 'TB', 'LAC', 'PHI', 'MIA', 'JAX', 'WAS', 'ARI', 'DAL', 'NYG', 'NO', 'BAL', 'CAR', 'CIN', 'LV', 'SF', 'DEN', 'DET', 'HOU', 'LAR', 'GB', 'NYJ', 'SEA')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Pressure TDs
**Conditions:** Outdoors

| player           |   val |   opps |
|:-----------------|------:|-------:|
| Sam Darnold      |     9 |    110 |
| Caleb Williams   |     7 |    134 |
| Justin Fields    |     6 |     74 |
| Baker Mayfield   |     6 |     83 |
| Matthew Stafford |     5 |     74 |

```sql
SELECT 
                        player,
                        SUM(pressure_touchdowns) as val,
                        SUM(pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Pressure TDs
**Conditions:** Away

| player           |   val |   opps |
|:-----------------|------:|-------:|
| Sam Darnold      |     6 |     67 |
| Matthew Stafford |     5 |     89 |
| Drake Maye       |     5 |     72 |
| Tua Tagovailoa   |     5 |     51 |
| Jalen Hurts      |     5 |     85 |

```sql
SELECT 
                        player,
                        SUM(pressure_touchdowns) as val,
                        SUM(pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND venue = 'Away'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Pressure TDs
**Conditions:** Cat Teams, in South

| player            |   val |   opps |
|:------------------|------:|-------:|
| Tyler Shough      |     2 |     12 |
| Sam Darnold       |     2 |     18 |
| Matthew Stafford  |     2 |     14 |
| Patrick Mahomes   |     0 |     11 |
| Michael Penix Jr. |     0 |     14 |

```sql
SELECT 
                        player,
                        SUM(pressure_touchdowns) as val,
                        SUM(pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('DET', 'JAX', 'CAR', 'CIN') AND home_team IN ('DAL', 'HOU', 'NO', 'ATL', 'CAR', 'TB', 'MIA', 'JAX', 'TEN')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Pressure TDs
**Conditions:** Pirate Teams, Day Game

| player      |   val |   opps |
|:------------|------:|-------:|
| Sam Darnold |     2 |     20 |
| Drake Maye  |     1 |     27 |
| Bryce Young |     1 |     14 |
| Jalen Hurts |     1 |     19 |
| Josh Allen  |     1 |     11 |

```sql
SELECT 
                        player,
                        SUM(pressure_touchdowns) as val,
                        SUM(pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('TB', 'MIN', 'LV', 'OAK') AND start_hour < 19
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Pressure TDs
**Conditions:** Pirate Teams, Outdoors

| player       |   val |   opps |
|:-------------|------:|-------:|
| Sam Darnold  |     2 |     20 |
| Kirk Cousins |     1 |     18 |
| Josh Allen   |     1 |     11 |
| Tyrod Taylor |     1 |     14 |
| Jalen Hurts  |     1 |     12 |

```sql
SELECT 
                        player,
                        SUM(pressure_touchdowns) as val,
                        SUM(pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('TB', 'MIN', 'LV', 'OAK') AND roof = 'outdoors'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Pressure TDs
**Conditions:** Outdoors, in West

| player           |   val |   opps |
|:-----------------|------:|-------:|
| Brock Purdy      |     4 |     55 |
| Sam Darnold      |     4 |     68 |
| Bo Nix           |     3 |     95 |
| Mac Jones        |     3 |     33 |
| Matthew Stafford |     2 |     33 |

```sql
SELECT 
                        player,
                        SUM(pressure_touchdowns) as val,
                        SUM(pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Pressure TDs
**Conditions:** Outdoors, Away

| player           |   val |   opps |
|:-----------------|------:|-------:|
| Sam Darnold      |     5 |     42 |
| Matthew Stafford |     5 |     74 |
| Jalen Hurts      |     4 |     47 |
| Justin Fields    |     3 |     31 |
| Drake Maye       |     3 |     62 |

```sql
SELECT 
                        player,
                        SUM(pressure_touchdowns) as val,
                        SUM(pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND venue = 'Away'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Pressure TDs
**Conditions:** Outdoors, Near IHOP

| player           |   val |   opps |
|:-----------------|------:|-------:|
| Sam Darnold      |     7 |     89 |
| Baker Mayfield   |     6 |     80 |
| Matthew Stafford |     5 |     62 |
| Justin Fields    |     5 |     62 |
| Bryce Young      |     5 |     95 |

```sql
SELECT 
                        player,
                        SUM(pressure_touchdowns) as val,
                        SUM(pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND home_team IN ('ATL', 'TB', 'LAC', 'PHI', 'MIA', 'JAX', 'WAS', 'ARI', 'DAL', 'NYG', 'NO', 'BAL', 'CAR', 'CIN', 'LV', 'SF', 'DEN', 'DET', 'HOU', 'LAR', 'GB', 'NYJ', 'SEA')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Pressure TDs
**Conditions:** in South, Away

| player          |   val |   opps |
|:----------------|------:|-------:|
| Sam Darnold     |     4 |     32 |
| Patrick Mahomes |     3 |     24 |
| Tua Tagovailoa  |     3 |     12 |
| Drake Maye      |     3 |     25 |
| Josh Allen      |     2 |     39 |

```sql
SELECT 
                        player,
                        SUM(pressure_touchdowns) as val,
                        SUM(pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('DAL', 'HOU', 'NO', 'ATL', 'CAR', 'TB', 'MIA', 'JAX', 'TEN') AND venue = 'Away'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Pressure BTT Rate
**Conditions:** in West, Home

| player         |       val |   opps |
|:---------------|----------:|-------:|
| Sam Darnold    | 0.0882353 |     68 |
| Brock Purdy    | 0.0731707 |     41 |
| Justin Herbert | 0.0619469 |    113 |
| Bo Nix         | 0.0315789 |     95 |
| Geno Smith     | 0.0240964 |     83 |

```sql
SELECT 
                        player,
                        CAST(SUM(pressure_big_time_throws) AS FLOAT) / NULLIF(SUM(pressure_attempts), 0) as val,
                        SUM(pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD') AND venue = 'Home'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket YPA
**Conditions:** Night Game, in NorthEast

| player      |      val |   opps |
|:------------|---------:|-------:|
| Sam Darnold | 13.8571  |     21 |
| Drake Maye  |  9.75281 |     89 |
| Jordan Love |  9.68    |     25 |
| Jared Goff  |  9.17073 |     41 |
| Bo Nix      |  9       |     32 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_yards) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour >= 19 AND home_team IN ('NE', 'NYJ', 'NYG', 'BUF', 'PHI', 'PIT', 'BAL', 'WAS')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket YPA
**Conditions:** Night Game, Away

| player         |      val |   opps |
|:---------------|---------:|-------:|
| Sam Darnold    | 12.15    |     40 |
| Drake Maye     |  9.80851 |     47 |
| Justin Herbert |  9.69565 |     23 |
| Jordan Love    |  9.34921 |     63 |
| Kirk Cousins   |  8.84615 |     26 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_yards) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour >= 19 AND venue = 'Away'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket YPA
**Conditions:** Night Game, Near IHOP

| player      |      val |   opps |
|:------------|---------:|-------:|
| Sam Darnold | 10.1951  |     82 |
| Drake Maye  |  9.85185 |     27 |
| Jared Goff  |  9.58537 |     82 |
| Jordan Love |  9.2     |     65 |
| Brock Purdy |  9.10417 |     48 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_yards) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour >= 19 AND home_team IN ('ATL', 'TB', 'LAC', 'PHI', 'MIA', 'JAX', 'WAS', 'ARI', 'DAL', 'NYG', 'NO', 'BAL', 'CAR', 'CIN', 'LV', 'SF', 'DEN', 'DET', 'HOU', 'LAR', 'GB', 'NYJ', 'SEA')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket YPA
**Conditions:** Outdoors, Near IHOP

| player       |     val |   opps |
|:-------------|--------:|-------:|
| Sam Darnold  | 9.70936 |    203 |
| Brock Purdy  | 9.65487 |    113 |
| Geno Smith   | 9.58065 |     31 |
| Josh Johnson | 9.36364 |     22 |
| Mac Jones    | 9.35772 |    123 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_yards) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND home_team IN ('ATL', 'TB', 'LAC', 'PHI', 'MIA', 'JAX', 'WAS', 'ARI', 'DAL', 'NYG', 'NO', 'BAL', 'CAR', 'CIN', 'LV', 'SF', 'DEN', 'DET', 'HOU', 'LAR', 'GB', 'NYJ', 'SEA')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket YPA
**Conditions:** in NorthEast, Near IHOP

| player       |      val |   opps |
|:-------------|---------:|-------:|
| Sam Darnold  | 13.8571  |     21 |
| Mac Jones    | 10.4286  |     21 |
| Drake Maye   |  9.7     |     40 |
| Jared Goff   |  9.61539 |     65 |
| Josh Johnson |  9.36364 |     22 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_yards) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('NE', 'NYJ', 'NYG', 'BUF', 'PHI', 'PIT', 'BAL', 'WAS') AND home_team IN ('ATL', 'TB', 'LAC', 'PHI', 'MIA', 'JAX', 'WAS', 'ARI', 'DAL', 'NYG', 'NO', 'BAL', 'CAR', 'CIN', 'LV', 'SF', 'DEN', 'DET', 'HOU', 'LAR', 'GB', 'NYJ', 'SEA')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket BTT Rate
**Conditions:** Cat Teams

| player           |       val |   opps |
|:-----------------|----------:|-------:|
| Sam Darnold      | 0.138889  |     36 |
| Tua Tagovailoa   | 0.133333  |     30 |
| Jordan Love      | 0.108434  |     83 |
| Matthew Stafford | 0.108108  |     74 |
| Jameis Winston   | 0.0952381 |     21 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_big_time_throws) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('DET', 'JAX', 'CAR', 'CIN')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket YPA
**Conditions:** All Games

| player       |     val |   opps |
|:-------------|--------:|-------:|
| Sam Darnold  | 9.40506 |    316 |
| Josh Johnson | 9.36364 |     22 |
| Malik Willis | 9.22727 |     22 |
| Jordan Love  | 9.1614  |    285 |
| Brock Purdy  | 9.1345  |    171 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_yards) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket YPA
**Conditions:** Bird Teams

| player          |      val |   opps |
|:----------------|---------:|-------:|
| Sam Darnold     | 10.7963  |     54 |
| Drake Maye      | 10.1957  |     46 |
| Brock Purdy     |  9.775   |     40 |
| Jared Goff      |  9.17073 |     41 |
| Patrick Mahomes |  8.4375  |     48 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_yards) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket YPA
**Conditions:** Night Game

| player       |      val |   opps |
|:-------------|---------:|-------:|
| Sam Darnold  | 10.1951  |     82 |
| Drake Maye   |  9.75281 |     89 |
| Malik Willis |  9.55    |     20 |
| Jared Goff   |  9.16038 |    106 |
| Jordan Love  |  9       |    101 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_yards) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour >= 19
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket YPA
**Conditions:** Outdoors

| player       |     val |   opps |
|:-------------|--------:|-------:|
| Sam Darnold  | 9.60166 |    241 |
| Josh Johnson | 9.36364 |     22 |
| Mac Jones    | 9.35772 |    123 |
| Geno Smith   | 9.34286 |     70 |
| Brock Purdy  | 9.28346 |    127 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_yards) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket YPA
**Conditions:** Bird Teams, Day Game

| player       |      val |   opps |
|:-------------|---------:|-------:|
| Sam Darnold  | 11.0857  |     35 |
| Brock Purdy  |  9.775   |     40 |
| Joe Burrow   |  9.34615 |     52 |
| Dak Prescott |  8.875   |     24 |
| Mac Jones    |  8.75862 |     29 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_yards) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA') AND start_hour < 19
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket YPA
**Conditions:** Bird Teams, Dome

| player          |     val |   opps |
|:----------------|--------:|-------:|
| Sam Darnold     | 9.52273 |     44 |
| Trevor Lawrence | 8.3913  |     23 |
| Dak Prescott    | 7.96296 |     54 |
| Jordan Love     | 7.81818 |     22 |
| Carson Wentz    | 7.77778 |     27 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_yards) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA') AND roof IN ('dome', 'closed')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket YPA
**Conditions:** Bird Teams, in West

| player           |     val |   opps |
|:-----------------|--------:|-------:|
| Sam Darnold      | 12.3793 |     29 |
| Baker Mayfield   | 11      |     29 |
| Matthew Stafford | 10.8727 |     55 |
| Brock Purdy      |  9.775  |     40 |
| Trevor Lawrence  |  8.3913 |     23 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_yards) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA') AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket YPA
**Conditions:** Bird Teams, in South

| player         |     val |   opps |
|:---------------|--------:|-------:|
| Sam Darnold    | 8.96    |     25 |
| Dak Prescott   | 7.96296 |     54 |
| Baker Mayfield | 7.4382  |     89 |
| Bryce Young    | 7.18841 |     69 |
| Tua Tagovailoa | 7.03704 |     54 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_yards) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA') AND home_team IN ('DAL', 'HOU', 'NO', 'ATL', 'CAR', 'TB', 'MIA', 'JAX', 'TEN')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket YPA
**Conditions:** Bird Teams, Near IHOP

| player         |      val |   opps |
|:---------------|---------:|-------:|
| Sam Darnold    | 10.7963  |     54 |
| Drake Maye     |  9.85185 |     27 |
| Brock Purdy    |  9.775   |     40 |
| Jared Goff     |  9.17073 |     41 |
| Baker Mayfield |  8.31356 |    118 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_yards) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA') AND home_team IN ('ATL', 'TB', 'LAC', 'PHI', 'MIA', 'JAX', 'WAS', 'ARI', 'DAL', 'NYG', 'NO', 'BAL', 'CAR', 'CIN', 'LV', 'SF', 'DEN', 'DET', 'HOU', 'LAR', 'GB', 'NYJ', 'SEA')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket YPA
**Conditions:** Cat Teams, in South

| player           |     val |   opps |
|:-----------------|--------:|-------:|
| Sam Darnold      | 9.83333 |     36 |
| Quinn Ewers      | 9.82609 |     23 |
| Tyler Shough     | 9       |     47 |
| Matthew Stafford | 8.6383  |     47 |
| Tua Tagovailoa   | 7.96667 |     30 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_yards) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('DET', 'JAX', 'CAR', 'CIN') AND home_team IN ('DAL', 'HOU', 'NO', 'ATL', 'CAR', 'TB', 'MIA', 'JAX', 'TEN')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket YPA
**Conditions:** Pirate Teams, in West

| player         |     val |   opps |
|:---------------|--------:|-------:|
| Sam Darnold    | 8.375   |     40 |
| Dak Prescott   | 8.30435 |     23 |
| Justin Herbert | 7.95918 |     49 |
| Bo Nix         | 7       |     43 |
| Caleb Williams | 6.84615 |     26 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_yards) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('TB', 'MIN', 'LV', 'OAK') AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket BTT Rate
**Conditions:** in NorthEast

| player          |       val |   opps |
|:----------------|----------:|-------:|
| Sam Darnold     | 0.0952381 |     42 |
| Joe Burrow      | 0.09375   |     64 |
| Patrick Mahomes | 0.0888889 |     45 |
| Marcus Mariota  | 0.0833333 |     96 |
| Geno Smith      | 0.0769231 |     39 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_big_time_throws) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('NE', 'NYJ', 'NYG', 'BUF', 'PHI', 'PIT', 'BAL', 'WAS')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket BTT Rate
**Conditions:** Cat Teams, Day Game

| player           |       val |   opps |
|:-----------------|----------:|-------:|
| Sam Darnold      | 0.138889  |     36 |
| Tua Tagovailoa   | 0.133333  |     30 |
| Jordan Love      | 0.108434  |     83 |
| Matthew Stafford | 0.108108  |     74 |
| Jameis Winston   | 0.0952381 |     21 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_big_time_throws) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('DET', 'JAX', 'CAR', 'CIN') AND start_hour < 19
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket BTT Rate
**Conditions:** Cat Teams, Outdoors

| player           |       val |   opps |
|:-----------------|----------:|-------:|
| Sam Darnold      | 0.138889  |     36 |
| Tua Tagovailoa   | 0.133333  |     30 |
| Jordan Love      | 0.0923077 |     65 |
| Drake Maye       | 0.0857143 |     35 |
| Matthew Stafford | 0.0851064 |     47 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_big_time_throws) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('DET', 'JAX', 'CAR', 'CIN') AND roof = 'outdoors'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket BTT Rate
**Conditions:** Cat Teams, in South

| player           |       val |   opps |
|:-----------------|----------:|-------:|
| Sam Darnold      | 0.138889  |     36 |
| Tua Tagovailoa   | 0.133333  |     30 |
| Matthew Stafford | 0.0851064 |     47 |
| Bryce Young      | 0.0384615 |     26 |
| Dak Prescott     | 0.0357143 |     28 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_big_time_throws) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('DET', 'JAX', 'CAR', 'CIN') AND home_team IN ('DAL', 'HOU', 'NO', 'ATL', 'CAR', 'TB', 'MIA', 'JAX', 'TEN')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket BTT Rate
**Conditions:** Cat Teams, Away

| player           |       val |   opps |
|:-----------------|----------:|-------:|
| Sam Darnold      | 0.138889  |     36 |
| Tua Tagovailoa   | 0.133333  |     30 |
| Jameis Winston   | 0.0952381 |     21 |
| Drake Maye       | 0.0869565 |     23 |
| Matthew Stafford | 0.0851064 |     47 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_big_time_throws) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('DET', 'JAX', 'CAR', 'CIN') AND venue = 'Away'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket BTT Rate
**Conditions:** Cat Teams, Near IHOP

| player         |       val |   opps |
|:---------------|----------:|-------:|
| Sam Darnold    | 0.138889  |     36 |
| Tua Tagovailoa | 0.133333  |     30 |
| Jordan Love    | 0.108434  |     83 |
| Jameis Winston | 0.0952381 |     21 |
| Drake Maye     | 0.0869565 |     23 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_big_time_throws) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('DET', 'JAX', 'CAR', 'CIN') AND home_team IN ('ATL', 'TB', 'LAC', 'PHI', 'MIA', 'JAX', 'WAS', 'ARI', 'DAL', 'NYG', 'NO', 'BAL', 'CAR', 'CIN', 'LV', 'SF', 'DEN', 'DET', 'HOU', 'LAR', 'GB', 'NYJ', 'SEA')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket BTT Rate
**Conditions:** Pirate Teams, in West

| player          |       val |   opps |
|:----------------|----------:|-------:|
| Sam Darnold     | 0.05      |     40 |
| Trevor Lawrence | 0.04      |     25 |
| Caleb Williams  | 0.0384615 |     26 |
| Justin Herbert  | 0.0204082 |     49 |
| Dak Prescott    | 0         |     23 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_big_time_throws) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('TB', 'MIN', 'LV', 'OAK') AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket BTT Rate
**Conditions:** Pirate Teams, Home

| player           |       val |   opps |
|:-----------------|----------:|-------:|
| Sam Darnold      | 0.05      |     40 |
| Tyler Shough     | 0.0434783 |     23 |
| Caleb Williams   | 0.0416667 |     24 |
| Matthew Stafford | 0.0333333 |     30 |
| Drake Maye       | 0.0333333 |     30 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_big_time_throws) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('TB', 'MIN', 'LV', 'OAK') AND venue = 'Home'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket BTT Rate
**Conditions:** Night Game, in NorthEast

| player         |       val |   opps |
|:---------------|----------:|-------:|
| Sam Darnold    | 0.142857  |     21 |
| Dak Prescott   | 0.0909091 |     22 |
| Joe Burrow     | 0.0833333 |     36 |
| Jayden Daniels | 0.0571429 |     35 |
| Jaxson Dart    | 0.0555556 |     36 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_big_time_throws) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND start_hour >= 19 AND home_team IN ('NE', 'NYJ', 'NYG', 'BUF', 'PHI', 'PIT', 'BAL', 'WAS')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket BTT Rate
**Conditions:** Outdoors, in NorthEast

| player          |       val |   opps |
|:----------------|----------:|-------:|
| Sam Darnold     | 0.0952381 |     42 |
| Joe Burrow      | 0.09375   |     64 |
| Patrick Mahomes | 0.0888889 |     45 |
| Marcus Mariota  | 0.0833333 |     96 |
| Geno Smith      | 0.0769231 |     39 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_big_time_throws) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND home_team IN ('NE', 'NYJ', 'NYG', 'BUF', 'PHI', 'PIT', 'BAL', 'WAS')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket BTT Rate
**Conditions:** Outdoors, Away

| player           |       val |   opps |
|:-----------------|----------:|-------:|
| Sam Darnold      | 0.105263  |     95 |
| Joe Burrow       | 0.0865385 |    104 |
| Brock Purdy      | 0.0857143 |     35 |
| Max Brosmer      | 0.08      |     25 |
| Matthew Stafford | 0.0792683 |    164 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_big_time_throws) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND venue = 'Away'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket BTT Rate
**Conditions:** in NorthEast, Away

| player          |       val |   opps |
|:----------------|----------:|-------:|
| Sam Darnold     | 0.0952381 |     42 |
| Joe Burrow      | 0.09375   |     64 |
| Patrick Mahomes | 0.0888889 |     45 |
| Geno Smith      | 0.0769231 |     39 |
| Jaxson Dart     | 0.0588235 |     34 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_big_time_throws) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('NE', 'NYJ', 'NYG', 'BUF', 'PHI', 'PIT', 'BAL', 'WAS') AND venue = 'Away'
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Clean Pocket BTT Rate
**Conditions:** in NorthEast, Near IHOP

| player         |       val |   opps |
|:---------------|----------:|-------:|
| Sam Darnold    | 0.142857  |     21 |
| Joe Burrow     | 0.0833333 |     36 |
| Marcus Mariota | 0.0833333 |     96 |
| Dak Prescott   | 0.0512821 |     78 |
| Drake Maye     | 0.05      |     40 |

```sql
SELECT 
                        player,
                        CAST(SUM(no_pressure_big_time_throws) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0) as val,
                        SUM(no_pressure_attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('NE', 'NYJ', 'NYG', 'BUF', 'PHI', 'PIT', 'BAL', 'WAS') AND home_team IN ('ATL', 'TB', 'LAC', 'PHI', 'MIA', 'JAX', 'WAS', 'ARI', 'DAL', 'NYG', 'NO', 'BAL', 'CAR', 'CIN', 'LV', 'SF', 'DEN', 'DET', 'HOU', 'LAR', 'GB', 'NYJ', 'SEA')
                    GROUP BY player
                    HAVING opps >= 20
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Blitz YPA
**Conditions:** Bird Teams

| player        |      val |   opps |
|:--------------|---------:|-------:|
| Sam Darnold   | 11.1034  |     29 |
| Joe Burrow    | 10.85    |     20 |
| Dak Prescott  | 10.5333  |     30 |
| Carson Wentz  | 10.1538  |     13 |
| J.J. McCarthy |  9.61905 |     21 |

```sql
SELECT 
                        player,
                        CAST(SUM(blitz_yards) AS FLOAT) / NULLIF(SUM(blitz_attempts), 0) as val,
                        SUM(blitz_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Blitz YPA
**Conditions:** Bird Teams, Night Game

| player           |      val |   opps |
|:-----------------|---------:|-------:|
| Sam Darnold      | 11.9091  |     11 |
| Matthew Stafford |  9.375   |     24 |
| Dak Prescott     |  9.05    |     20 |
| Josh Allen       |  7.72    |     25 |
| Jaxson Dart      |  7.61538 |     13 |

```sql
SELECT 
                        player,
                        CAST(SUM(blitz_yards) AS FLOAT) / NULLIF(SUM(blitz_attempts), 0) as val,
                        SUM(blitz_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA') AND start_hour >= 19
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Blitz YPA
**Conditions:** Bird Teams, Dome

| player        |      val |   opps |
|:--------------|---------:|-------:|
| Sam Darnold   | 10.9167  |     24 |
| Dak Prescott  | 10.4783  |     23 |
| Carson Wentz  | 10.1538  |     13 |
| J.J. McCarthy |  9.61905 |     21 |
| Daniel Jones  |  8.08696 |     23 |

```sql
SELECT 
                        player,
                        CAST(SUM(blitz_yards) AS FLOAT) / NULLIF(SUM(blitz_attempts), 0) as val,
                        SUM(blitz_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA') AND roof IN ('dome', 'closed')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Blitz YPA
**Conditions:** Bird Teams, in West

| player           |      val |   opps |
|:-----------------|---------:|-------:|
| Sam Darnold      | 11.9375  |     16 |
| Matthew Stafford |  9.04762 |     21 |
| Brock Purdy      |  7.73684 |     19 |
| Kirk Cousins     |  7.66667 |     12 |
| Trevor Lawrence  |  7.09091 |     11 |

```sql
SELECT 
                        player,
                        CAST(SUM(blitz_yards) AS FLOAT) / NULLIF(SUM(blitz_attempts), 0) as val,
                        SUM(blitz_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA') AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Blitz YPA
**Conditions:** Bird Teams, Away

| player         |      val |   opps |
|:---------------|---------:|-------:|
| Sam Darnold    | 10.9167  |     24 |
| Aaron Rodgers  |  9.91667 |     12 |
| Tyrod Taylor   |  8.81818 |     11 |
| Tua Tagovailoa |  7.91667 |     12 |
| Brock Purdy    |  7.73684 |     19 |

```sql
SELECT 
                        player,
                        CAST(SUM(blitz_yards) AS FLOAT) / NULLIF(SUM(blitz_attempts), 0) as val,
                        SUM(blitz_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA') AND venue = 'Away'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Blitz YPA
**Conditions:** Bird Teams, Near IHOP

| player        |      val |   opps |
|:--------------|---------:|-------:|
| Sam Darnold   | 11.1034  |     29 |
| Joe Burrow    | 10.85    |     20 |
| Dak Prescott  | 10.5333  |     30 |
| Aaron Rodgers |  9.91667 |     12 |
| Jaxson Dart   |  8.42105 |     19 |

```sql
SELECT 
                        player,
                        CAST(SUM(blitz_yards) AS FLOAT) / NULLIF(SUM(blitz_attempts), 0) as val,
                        SUM(blitz_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA') AND home_team IN ('ATL', 'TB', 'LAC', 'PHI', 'MIA', 'JAX', 'WAS', 'ARI', 'DAL', 'NYG', 'NO', 'BAL', 'CAR', 'CIN', 'LV', 'SF', 'DEN', 'DET', 'HOU', 'LAR', 'GB', 'NYJ', 'SEA')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Blitz YPA
**Conditions:** Division Rivals, in West

| player           |     val |   opps |
|:-----------------|--------:|-------:|
| Sam Darnold      | 9.5     |     32 |
| Matthew Stafford | 9.26829 |     41 |
| Justin Herbert   | 8.77778 |     45 |
| Bo Nix           | 8.66667 |     36 |
| Brock Purdy      | 7.73684 |     19 |

```sql
SELECT 
                        player,
                        CAST(SUM(blitz_yards) AS FLOAT) / NULLIF(SUM(blitz_attempts), 0) as val,
                        SUM(blitz_attempts) as opps
                    FROM data
                    WHERE 1=1 AND div_game = 1 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Blitz YPA
**Conditions:** Dome, in West

| player         |      val |   opps |
|:---------------|---------:|-------:|
| Sam Darnold    | 11.9091  |     11 |
| Justin Herbert |  8.50443 |    113 |
| Bo Nix         |  7.94444 |     18 |
| Kirk Cousins   |  7.66667 |     12 |
| Geno Smith     |  7.5     |     98 |

```sql
SELECT 
                        player,
                        CAST(SUM(blitz_yards) AS FLOAT) / NULLIF(SUM(blitz_attempts), 0) as val,
                        SUM(blitz_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof IN ('dome', 'closed') AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Blitz YPA
**Conditions:** Outdoors, Away

| player          |     val |   opps |
|:----------------|--------:|-------:|
| Sam Darnold     | 9.24528 |     53 |
| Jared Goff      | 9.22581 |     62 |
| Jaxson Dart     | 9.06977 |     43 |
| Jordan Love     | 8.76364 |     55 |
| Trevor Lawrence | 8.72727 |     33 |

```sql
SELECT 
                        player,
                        CAST(SUM(blitz_yards) AS FLOAT) / NULLIF(SUM(blitz_attempts), 0) as val,
                        SUM(blitz_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof = 'outdoors' AND venue = 'Away'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Blitz YPA
**Conditions:** in West, Away

| player           |      val |   opps |
|:-----------------|---------:|-------:|
| Sam Darnold      | 11.9091  |     11 |
| Justin Herbert   |  9.7     |     10 |
| Matthew Stafford |  9.26829 |     41 |
| Trevor Lawrence  |  8.46341 |     41 |
| Jordan Love      |  8.22727 |     22 |

```sql
SELECT 
                        player,
                        CAST(SUM(blitz_yards) AS FLOAT) / NULLIF(SUM(blitz_attempts), 0) as val,
                        SUM(blitz_attempts) as opps
                    FROM data
                    WHERE 1=1 AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD') AND venue = 'Away'
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Blitz TDs
**Conditions:** Bird Teams, Day Game

| player           |   val |   opps |
|:-----------------|------:|-------:|
| Sam Darnold      |     4 |     18 |
| Matthew Stafford |     4 |     46 |
| Trevor Lawrence  |     3 |     18 |
| Dak Prescott     |     2 |     10 |
| Marcus Mariota   |     2 |     20 |

```sql
SELECT 
                        player,
                        SUM(blitz_touchdowns) as val,
                        SUM(blitz_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA') AND start_hour < 19
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Blitz TDs
**Conditions:** Bird Teams, Dome

| player           |   val |   opps |
|:-----------------|------:|-------:|
| Sam Darnold      |     4 |     24 |
| Trevor Lawrence  |     3 |     11 |
| Matthew Stafford |     3 |     32 |
| Marcus Mariota   |     2 |     16 |
| Tua Tagovailoa   |     2 |     12 |

```sql
SELECT 
                        player,
                        SUM(blitz_touchdowns) as val,
                        SUM(blitz_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA') AND roof IN ('dome', 'closed')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Blitz TDs
**Conditions:** Bird Teams, in South

| player         |   val |   opps |
|:---------------|------:|-------:|
| Baker Mayfield |     3 |     51 |
| Sam Darnold    |     3 |     13 |
| Tua Tagovailoa |     2 |     23 |
| Dak Prescott   |     2 |     23 |
| Marcus Mariota |     2 |     16 |

```sql
SELECT 
                        player,
                        SUM(blitz_touchdowns) as val,
                        SUM(blitz_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA') AND home_team IN ('DAL', 'HOU', 'NO', 'ATL', 'CAR', 'TB', 'MIA', 'JAX', 'TEN')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Blitz TDs
**Conditions:** Bird Teams, Near IHOP

| player           |   val |   opps |
|:-----------------|------:|-------:|
| Sam Darnold      |     5 |     29 |
| Matthew Stafford |     4 |     57 |
| Trevor Lawrence  |     3 |     18 |
| Baker Mayfield   |     3 |     59 |
| Tua Tagovailoa   |     2 |     23 |

```sql
SELECT 
                        player,
                        SUM(blitz_touchdowns) as val,
                        SUM(blitz_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA') AND home_team IN ('ATL', 'TB', 'LAC', 'PHI', 'MIA', 'JAX', 'WAS', 'ARI', 'DAL', 'NYG', 'NO', 'BAL', 'CAR', 'CIN', 'LV', 'SF', 'DEN', 'DET', 'HOU', 'LAR', 'GB', 'NYJ', 'SEA')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Blitz TDs
**Conditions:** Dome, in South

| player         |   val |   opps |
|:---------------|------:|-------:|
| Sam Darnold    |     3 |     13 |
| Dak Prescott   |     2 |    105 |
| Marcus Mariota |     2 |     22 |
| Baker Mayfield |     2 |     41 |
| Tua Tagovailoa |     2 |     12 |

```sql
SELECT 
                        player,
                        SUM(blitz_touchdowns) as val,
                        SUM(blitz_attempts) as opps
                    FROM data
                    WHERE 1=1 AND roof IN ('dome', 'closed') AND home_team IN ('DAL', 'HOU', 'NO', 'ATL', 'CAR', 'TB', 'MIA', 'JAX', 'TEN')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

## Blitz BTT Rate
**Conditions:** Pirate Teams, in West

| player         |       val |   opps |
|:---------------|----------:|-------:|
| Sam Darnold    | 0.0357143 |     28 |
| Justin Herbert | 0.0333333 |     30 |
| Bo Nix         | 0         |     19 |

```sql
SELECT 
                        player,
                        CAST(SUM(blitz_big_time_throws) AS FLOAT) / NULLIF(SUM(blitz_attempts), 0) as val,
                        SUM(blitz_attempts) as opps
                    FROM data
                    WHERE 1=1 AND opponent IN ('TB', 'MIN', 'LV', 'OAK') AND home_team IN ('SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD')
                    GROUP BY player
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 5
```

---

