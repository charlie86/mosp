# Patriots DEFENSE Performance by Dunkin Gravity

**Analysis Period:** 2025 Season

This analysis shows how the New England Patriots defense performs under different **Coffee Gravity** conditions.

## Coffee Gravity Zones

Based on the Coffee Wars gravitational model:

| gravity_zone      |       min |       max |   count |
|:------------------|----------:|----------:|--------:|
| Dunkin Safe Zone  |   5.74354 |  5.74354  |       1 |
| Dunkin Stronghold |   3.0928  |  4.35203  |       2 |
| Mild Dunkin Zone  |   1.15958 |  2.95478  |       7 |
| Neutral Zone      |  -0.87689 |  0.969007 |       7 |
| Starbucks Zone    | -11.4562  | -1.27731  |      15 |

**Key Insight:** Patriots performance in Dunkin-dominated territories (Net Gravity > 0).

---

# Best Stuperlatives

## 1. Stops (Best)
**Conditions:** Any Dunkin Zone (Net > 0)
**Value:** 510.000

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 2. Total Pressures (Best)
**Conditions:** Any Dunkin Zone (Net > 0)
**Value:** 383.000

```sql
SELECT 
                        player,
                        SUM(total_pressures) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 3. Stops (Best)
**Conditions:** Any Dunkin Zone (Net > 0), High Dunkin (Net > 3)
**Value:** 321.000

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND net_gravity >= 3
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 4. Stops (Best)
**Conditions:** Any Dunkin Zone (Net > 0), Dunkin Stronghold
**Value:** 288.000

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND gravity_zone = 'Dunkin Stronghold'
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 5. Total Pressures (Best)
**Conditions:** Any Dunkin Zone (Net > 0), High Dunkin (Net > 3)
**Value:** 246.000

```sql
SELECT 
                        player,
                        SUM(total_pressures) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND net_gravity >= 3
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 6. Total Pressures (Best)
**Conditions:** Any Dunkin Zone (Net > 0), Dunkin Stronghold
**Value:** 218.000

```sql
SELECT 
                        player,
                        SUM(total_pressures) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND gravity_zone = 'Dunkin Stronghold'
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 7. Stops (Best)
**Conditions:** Any Dunkin Zone (Net > 0), Mammal Teams
**Value:** 173.000

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND opponent IN ('CHI', 'DET', 'JAX', 'CAR', 'LAR', 'CIN', 'DEN', 'IND', 'MIA', 'BUF')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 8. Total Pressures (Best)
**Conditions:** Any Dunkin Zone (Net > 0), Mammal Teams
**Value:** 121.000

```sql
SELECT 
                        player,
                        SUM(total_pressures) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND opponent IN ('CHI', 'DET', 'JAX', 'CAR', 'LAR', 'CIN', 'DEN', 'IND', 'MIA', 'BUF')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 9. Stops (Best)
**Conditions:** Any Dunkin Zone (Net > 0), Hat Teams
**Value:** 107.000

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 10. Total Pressures (Best)
**Conditions:** Any Dunkin Zone (Net > 0), Hat Teams
**Value:** 90.000

```sql
SELECT 
                        player,
                        SUM(total_pressures) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 11. Stops (Best)
**Conditions:** Any Dunkin Zone (Net > 0), Dunkin Stronghold, Mammal Teams
**Value:** 90.000

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND gravity_zone = 'Dunkin Stronghold' AND opponent IN ('CHI', 'DET', 'JAX', 'CAR', 'LAR', 'CIN', 'DEN', 'IND', 'MIA', 'BUF')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 12. Stops (Best)
**Conditions:** Any Dunkin Zone (Net > 0), High Dunkin (Net > 3), Mammal Teams
**Value:** 90.000

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND net_gravity >= 3 AND opponent IN ('CHI', 'DET', 'JAX', 'CAR', 'LAR', 'CIN', 'DEN', 'IND', 'MIA', 'BUF')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 13. Stops (Best)
**Conditions:** Any Dunkin Zone (Net > 0), Bird Teams
**Value:** 74.000

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 14. Stops (Best)
**Conditions:** Any Dunkin Zone (Net > 0), High Dunkin (Net > 3), Bird Teams
**Value:** 74.000

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND net_gravity >= 3 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 15. Total Pressures (Best)
**Conditions:** Any Dunkin Zone (Net > 0), High Dunkin (Net > 3), Bird Teams
**Value:** 65.000

```sql
SELECT 
                        player,
                        SUM(total_pressures) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND net_gravity >= 3 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

# Worst Stuperlatives

## 1. Stops (Worst)
**Conditions:** Any Dunkin Zone (Net > 0)
**Value:** 510.000

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 2. Total Pressures (Worst)
**Conditions:** Any Dunkin Zone (Net > 0)
**Value:** 383.000

```sql
SELECT 
                        player,
                        SUM(total_pressures) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 3. Stops (Worst)
**Conditions:** Any Dunkin Zone (Net > 0), High Dunkin (Net > 3)
**Value:** 321.000

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND net_gravity >= 3
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 4. Stops (Worst)
**Conditions:** Any Dunkin Zone (Net > 0), Dunkin Stronghold
**Value:** 288.000

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND gravity_zone = 'Dunkin Stronghold'
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 5. Total Pressures (Worst)
**Conditions:** Any Dunkin Zone (Net > 0), High Dunkin (Net > 3)
**Value:** 246.000

```sql
SELECT 
                        player,
                        SUM(total_pressures) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND net_gravity >= 3
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 6. Total Pressures (Worst)
**Conditions:** Any Dunkin Zone (Net > 0), Dunkin Stronghold
**Value:** 218.000

```sql
SELECT 
                        player,
                        SUM(total_pressures) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND gravity_zone = 'Dunkin Stronghold'
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 7. Stops (Worst)
**Conditions:** Any Dunkin Zone (Net > 0), Mammal Teams
**Value:** 173.000

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND opponent IN ('CHI', 'DET', 'JAX', 'CAR', 'LAR', 'CIN', 'DEN', 'IND', 'MIA', 'BUF')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 8. Total Pressures (Worst)
**Conditions:** Any Dunkin Zone (Net > 0), Mammal Teams
**Value:** 121.000

```sql
SELECT 
                        player,
                        SUM(total_pressures) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND opponent IN ('CHI', 'DET', 'JAX', 'CAR', 'LAR', 'CIN', 'DEN', 'IND', 'MIA', 'BUF')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 9. Stops (Worst)
**Conditions:** Any Dunkin Zone (Net > 0), Hat Teams
**Value:** 107.000

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 10. Total Pressures (Worst)
**Conditions:** Any Dunkin Zone (Net > 0), Hat Teams
**Value:** 90.000

```sql
SELECT 
                        player,
                        SUM(total_pressures) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 11. Stops (Worst)
**Conditions:** Any Dunkin Zone (Net > 0), Dunkin Stronghold, Mammal Teams
**Value:** 90.000

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND gravity_zone = 'Dunkin Stronghold' AND opponent IN ('CHI', 'DET', 'JAX', 'CAR', 'LAR', 'CIN', 'DEN', 'IND', 'MIA', 'BUF')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 12. Stops (Worst)
**Conditions:** Any Dunkin Zone (Net > 0), High Dunkin (Net > 3), Mammal Teams
**Value:** 90.000

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND net_gravity >= 3 AND opponent IN ('CHI', 'DET', 'JAX', 'CAR', 'LAR', 'CIN', 'DEN', 'IND', 'MIA', 'BUF')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 13. Stops (Worst)
**Conditions:** Any Dunkin Zone (Net > 0), Bird Teams
**Value:** 74.000

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 14. Stops (Worst)
**Conditions:** Any Dunkin Zone (Net > 0), High Dunkin (Net > 3), Bird Teams
**Value:** 74.000

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND net_gravity >= 3 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 15. Total Pressures (Worst)
**Conditions:** Any Dunkin Zone (Net > 0), High Dunkin (Net > 3), Bird Teams
**Value:** 65.000

```sql
SELECT 
                        player,
                        SUM(total_pressures) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND net_gravity >= 3 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

