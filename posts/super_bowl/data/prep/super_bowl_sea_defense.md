# Super Bowl Preview: SEA (DEFENSE)

**Season:** 2025

# Best Stuperlatives

## Interceptions (Best)
**Conditions:** Hat Teams, Outdoors

| player   |   val |   opps |
|:---------|------:|-------:|
| SEA      |     9 |    101 |
| CHI      |     6 |     75 |
| DEN      |     4 |     61 |
| CAR      |     4 |     75 |
| PIT      |     3 |     39 |

```sql
SELECT 
                            player,
                            SUM(interceptions) as val,
                            COUNT(*) as opps
                        FROM data
                        WHERE 1=1 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK') AND roof = 'outdoors'
                        GROUP BY player
                        HAVING opps >= 1
                        ORDER BY val DESC
                        LIMIT 5
```

---

## Interceptions (Best)
**Conditions:** Hat Teams, Near IHOP (< 2mi)

| player   |   val |   opps |
|:---------|------:|-------:|
| SEA      |     7 |     81 |
| LAC      |     4 |    102 |
| PHI      |     4 |    103 |
| DET      |     4 |     99 |
| TB       |     3 |     39 |

```sql
SELECT 
                            player,
                            SUM(interceptions) as val,
                            COUNT(*) as opps
                        FROM data
                        WHERE 1=1 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK') AND dist_to_ihop <= 2.0
                        GROUP BY player
                        HAVING opps >= 1
                        ORDER BY val DESC
                        LIMIT 5
```

---

## Interceptions (Best)
**Conditions:** Hat Teams

| player   |   val |   opps |
|:---------|------:|-------:|
| CHI      |     9 |     94 |
| SEA      |     9 |    101 |
| LAC      |     7 |    120 |
| ATL      |     6 |    109 |
| PHI      |     6 |    122 |

```sql
SELECT 
                            player,
                            SUM(interceptions) as val,
                            COUNT(*) as opps
                        FROM data
                        WHERE 1=1 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK')
                        GROUP BY player
                        HAVING opps >= 1
                        ORDER BY val DESC
                        LIMIT 5
```

---

## Sacks (Best)
**Conditions:** Hat Teams, Outdoors

| player   |   val |   opps |
|:---------|------:|-------:|
| SEA      |    17 |    101 |
| GB       |    15 |     54 |
| NYG      |    14 |     89 |
| DEN      |    13 |     61 |
| ATL      |    12 |     56 |

```sql
SELECT 
                            player,
                            SUM(sacks) as val,
                            COUNT(*) as opps
                        FROM data
                        WHERE 1=1 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK') AND roof = 'outdoors'
                        GROUP BY player
                        HAVING opps >= 1
                        ORDER BY val DESC
                        LIMIT 5
```

---

## Total Pressures (Best)
**Conditions:** Hat Teams, Outdoors

| player   |   val |   opps |
|:---------|------:|-------:|
| SEA      |   100 |    101 |
| PHI      |    74 |     84 |
| GB       |    69 |     54 |
| ATL      |    68 |     56 |
| NYG      |    67 |     89 |

```sql
SELECT 
                            player,
                            SUM(total_pressures) as val,
                            COUNT(*) as opps
                        FROM data
                        WHERE 1=1 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK') AND roof = 'outdoors'
                        GROUP BY player
                        HAVING opps >= 1
                        ORDER BY val DESC
                        LIMIT 5
```

---

## Stops (Best)
**Conditions:** Hat Teams, Outdoors

| player   |   val |   opps |
|:---------|------:|-------:|
| SEA      |   124 |    101 |
| NYG      |   106 |     89 |
| CAR      |    96 |     75 |
| CHI      |    91 |     75 |
| PHI      |    78 |     84 |

```sql
SELECT 
                            player,
                            SUM(stops) as val,
                            COUNT(*) as opps
                        FROM data
                        WHERE 1=1 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK') AND roof = 'outdoors'
                        GROUP BY player
                        HAVING opps >= 1
                        ORDER BY val DESC
                        LIMIT 5
```

---

## Median PRP (Best)
**Conditions:** Hat Teams, Near IHOP (< 2mi)

| player   |     val |   opps |
|:---------|--------:|-------:|
| SEA      | 16.0357 |     81 |
| TB       | 14.8059 |     39 |
| ATL      | 13.8692 |     20 |
| MIN      | 11.1286 |     20 |
| NO       | 10.8333 |     77 |

```sql
SELECT 
                            player,
                            MEDIAN(prp) as val,
                            COUNT(*) as opps
                        FROM data
                        WHERE 1=1 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK') AND dist_to_ihop <= 2.0
                        GROUP BY player
                        HAVING opps >= 1
                        ORDER BY val DESC
                        LIMIT 5
```

---

