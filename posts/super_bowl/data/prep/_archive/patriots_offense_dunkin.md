# Patriots OFFENSE Performance by Dunkin Gravity

**Analysis Period:** 2025 Season

This analysis shows how the New England Patriots offense performs under different **Coffee Gravity** conditions.

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

## 1. Total Yards (Best)
**Conditions:** Any Dunkin Zone (Net > 0)
**Value:** 6444.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 2. Total Yards (Best)
**Conditions:** Any Dunkin Zone (Net > 0), High Dunkin (Net > 3)
**Value:** 4447.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND net_gravity >= 3 
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 3. Total Yards (Best)
**Conditions:** Any Dunkin Zone (Net > 0), Dunkin Stronghold
**Value:** 3988.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND gravity_zone = 'Dunkin Stronghold' 
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 4. Total Rush Yards (Best)
**Conditions:** Any Dunkin Zone (Net > 0)
**Value:** 2335.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND play_type = 'run'
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 5. Total Yards (Best)
**Conditions:** Any Dunkin Zone (Net > 0), Mammal Teams
**Value:** 1884.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND opponent IN ('CHI', 'DET', 'JAX', 'CAR', 'LAR', 'CIN', 'DEN', 'IND', 'MIA', 'BUF') 
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 6. Total Rush Yards (Best)
**Conditions:** Any Dunkin Zone (Net > 0), High Dunkin (Net > 3)
**Value:** 1600.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND net_gravity >= 3 AND play_type = 'run'
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 7. Total Rush Yards (Best)
**Conditions:** Any Dunkin Zone (Net > 0), Dunkin Stronghold
**Value:** 1515.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND gravity_zone = 'Dunkin Stronghold' AND play_type = 'run'
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 8. Total Yards (Best)
**Conditions:** Any Dunkin Zone (Net > 0), Dunkin Stronghold, Mammal Teams
**Value:** 1153.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND gravity_zone = 'Dunkin Stronghold' AND opponent IN ('CHI', 'DET', 'JAX', 'CAR', 'LAR', 'CIN', 'DEN', 'IND', 'MIA', 'BUF') 
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 9. Total Yards (Best)
**Conditions:** Any Dunkin Zone (Net > 0), High Dunkin (Net > 3), Mammal Teams
**Value:** 1153.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND net_gravity >= 3 AND opponent IN ('CHI', 'DET', 'JAX', 'CAR', 'LAR', 'CIN', 'DEN', 'IND', 'MIA', 'BUF') 
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 10. Total Yards (Best)
**Conditions:** Any Dunkin Zone (Net > 0), Hat Teams
**Value:** 1141.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK') 
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 11. Total Rush Yards (Best)
**Conditions:** Any Dunkin Zone (Net > 0), Mammal Teams
**Value:** 832.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND opponent IN ('CHI', 'DET', 'JAX', 'CAR', 'LAR', 'CIN', 'DEN', 'IND', 'MIA', 'BUF') AND play_type = 'run'
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 12. Total Yards (Best)
**Conditions:** Any Dunkin Zone (Net > 0), Bird Teams
**Value:** 793.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA') 
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 13. Total Yards (Best)
**Conditions:** Any Dunkin Zone (Net > 0), High Dunkin (Net > 3), Bird Teams
**Value:** 793.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND net_gravity >= 3 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA') 
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 14. Total Yards (Best)
**Conditions:** Any Dunkin Zone (Net > 0), Dunkin Stronghold, Hat Teams
**Value:** 705.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND gravity_zone = 'Dunkin Stronghold' AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK') 
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 15. Total Yards (Best)
**Conditions:** Any Dunkin Zone (Net > 0), High Dunkin (Net > 3), Hat Teams
**Value:** 705.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND net_gravity >= 3 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK') 
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

# Worst Stuperlatives

## 1. Total Yards (Worst)
**Conditions:** Any Dunkin Zone (Net > 0)
**Value:** 6444.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 2. Total Yards (Worst)
**Conditions:** Any Dunkin Zone (Net > 0), High Dunkin (Net > 3)
**Value:** 4447.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND net_gravity >= 3 
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 3. Total Yards (Worst)
**Conditions:** Any Dunkin Zone (Net > 0), Dunkin Stronghold
**Value:** 3988.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND gravity_zone = 'Dunkin Stronghold' 
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 4. Total Rush Yards (Worst)
**Conditions:** Any Dunkin Zone (Net > 0)
**Value:** 2335.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND play_type = 'run'
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 5. Total Yards (Worst)
**Conditions:** Any Dunkin Zone (Net > 0), Mammal Teams
**Value:** 1884.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND opponent IN ('CHI', 'DET', 'JAX', 'CAR', 'LAR', 'CIN', 'DEN', 'IND', 'MIA', 'BUF') 
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 6. Total Rush Yards (Worst)
**Conditions:** Any Dunkin Zone (Net > 0), High Dunkin (Net > 3)
**Value:** 1600.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND net_gravity >= 3 AND play_type = 'run'
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 7. Total Rush Yards (Worst)
**Conditions:** Any Dunkin Zone (Net > 0), Dunkin Stronghold
**Value:** 1515.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND gravity_zone = 'Dunkin Stronghold' AND play_type = 'run'
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 8. Total Yards (Worst)
**Conditions:** Any Dunkin Zone (Net > 0), Dunkin Stronghold, Mammal Teams
**Value:** 1153.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND gravity_zone = 'Dunkin Stronghold' AND opponent IN ('CHI', 'DET', 'JAX', 'CAR', 'LAR', 'CIN', 'DEN', 'IND', 'MIA', 'BUF') 
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 9. Total Yards (Worst)
**Conditions:** Any Dunkin Zone (Net > 0), High Dunkin (Net > 3), Mammal Teams
**Value:** 1153.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND net_gravity >= 3 AND opponent IN ('CHI', 'DET', 'JAX', 'CAR', 'LAR', 'CIN', 'DEN', 'IND', 'MIA', 'BUF') 
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 10. Total Yards (Worst)
**Conditions:** Any Dunkin Zone (Net > 0), Hat Teams
**Value:** 1141.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK') 
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 11. Total Rush Yards (Worst)
**Conditions:** Any Dunkin Zone (Net > 0), Mammal Teams
**Value:** 832.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND opponent IN ('CHI', 'DET', 'JAX', 'CAR', 'LAR', 'CIN', 'DEN', 'IND', 'MIA', 'BUF') AND play_type = 'run'
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 12. Total Yards (Worst)
**Conditions:** Any Dunkin Zone (Net > 0), Bird Teams
**Value:** 793.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA') 
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 13. Total Yards (Worst)
**Conditions:** Any Dunkin Zone (Net > 0), High Dunkin (Net > 3), Bird Teams
**Value:** 793.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND net_gravity >= 3 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA') 
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 14. Total Yards (Worst)
**Conditions:** Any Dunkin Zone (Net > 0), Dunkin Stronghold, Hat Teams
**Value:** 705.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND gravity_zone = 'Dunkin Stronghold' AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK') 
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 15. Total Yards (Worst)
**Conditions:** Any Dunkin Zone (Net > 0), High Dunkin (Net > 3), Hat Teams
**Value:** 705.000

```sql
SELECT 
                        'NE' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity > 0 AND net_gravity >= 3 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK') 
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

