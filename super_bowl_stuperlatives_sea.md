# Super Bowl Preview: SEA (DEFENSE)

**Season:** 2025

# Best Stuperlatives

## Interceptions (Best)
**Conditions:** Hat Teams, Outdoors

| player   |   val |   opps |
|:---------|------:|-------:|
| SEA      |     9 |    101 |
| CHI      |     6 |     75 |
| CAR      |     4 |     75 |
| DEN      |     4 |     61 |
| CIN      |     3 |     38 |

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

## Sacks (Best)
**Conditions:** Hat Teams, Outdoors

| player   |   val |   opps |
|:---------|------:|-------:|
| SEA      |    17 |    101 |
| GB       |    15 |     54 |
| NYG      |    14 |     89 |
| DEN      |    13 |     61 |
| PIT      |    12 |     39 |

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

