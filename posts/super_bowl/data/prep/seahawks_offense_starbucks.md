# Seahawks OFFENSE Performance by Starbucks Gravity

**Analysis Period:** 2025 Season

This analysis shows how the Seattle Seahawks offense performs under different **Coffee Gravity** conditions.

## Coffee Gravity Zones

Based on the Coffee Wars gravitational model:

| gravity_zone           |       min |        max |   count |
|:-----------------------|----------:|-----------:|--------:|
| Dunkin Safe Zone       |   3.0928  |   5.74354  |       3 |
| Extreme Starbucks Zone | -11.4562  | -11.4562   |       1 |
| Mild Dunkin Zone       |   1.15958 |   2.95478  |       7 |
| Mild Starbucks Zone    |  -4.05686 |  -1.27731  |      10 |
| Neutral Zone           |  -0.87689 |   0.969007 |       7 |
| Starbucks Death Zone   |  -5.79918 |  -4.57381  |       4 |

**Key Insight:** Seattle benefits from high Starbucks gravity, Patriots from high Dunkin' gravity.

---

# Best Stuperlatives

## 1. Total Yards (Best)
**Conditions:** Any Starbucks Zone (Net < 0)
**Value:** 4791.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 2. Total Yards (Best)
**Conditions:** Any Starbucks Zone (Net < 0), High Starbucks (Net < -4)
**Value:** 3723.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND net_gravity <= -4 
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 3. Total Yards (Best)
**Conditions:** Any Starbucks Zone (Net < 0), Extreme Starbucks Zone
**Value:** 2946.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND gravity_zone = 'Extreme Starbucks Zone' 
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 4. Total Yards (Best)
**Conditions:** Any Starbucks Zone (Net < 0), Hat Teams
**Value:** 1951.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK') 
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 5. Total Rush Yards (Best)
**Conditions:** Any Starbucks Zone (Net < 0)
**Value:** 1895.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND play_type = 'run'
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 6. Total Yards (Best)
**Conditions:** Any Starbucks Zone (Net < 0), High Starbucks (Net < -4), Hat Teams
**Value:** 1556.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND net_gravity <= -4 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK') 
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 7. Total Rush Yards (Best)
**Conditions:** Any Starbucks Zone (Net < 0), High Starbucks (Net < -4)
**Value:** 1459.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND net_gravity <= -4 AND play_type = 'run'
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 8. Total Yards (Best)
**Conditions:** Any Starbucks Zone (Net < 0), Extreme Starbucks Zone, Hat Teams
**Value:** 1193.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND gravity_zone = 'Extreme Starbucks Zone' AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK') 
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 9. Total Rush Yards (Best)
**Conditions:** Any Starbucks Zone (Net < 0), Extreme Starbucks Zone
**Value:** 1142.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND gravity_zone = 'Extreme Starbucks Zone' AND play_type = 'run'
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 10. Total Rush Yards (Best)
**Conditions:** Any Starbucks Zone (Net < 0), Hat Teams
**Value:** 805.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK') AND play_type = 'run'
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 11. Total Yards (Best)
**Conditions:** Any Starbucks Zone (Net < 0), Starbucks Death Zone
**Value:** 777.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND gravity_zone = 'Starbucks Death Zone' 
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 12. Total Yards (Best)
**Conditions:** Any Starbucks Zone (Net < 0), Bird Teams
**Value:** 762.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA') 
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 13. Total Rush Yards (Best)
**Conditions:** Any Starbucks Zone (Net < 0), High Starbucks (Net < -4), Hat Teams
**Value:** 688.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND net_gravity <= -4 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK') AND play_type = 'run'
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 14. Total Yards (Best)
**Conditions:** Any Starbucks Zone (Net < 0), Mammal Teams
**Value:** 604.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND opponent IN ('CHI', 'DET', 'JAX', 'CAR', 'LAR', 'CIN', 'DEN', 'IND', 'MIA', 'BUF') 
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

## 15. Total Rush Yards (Best)
**Conditions:** Any Starbucks Zone (Net < 0), Extreme Starbucks Zone, Hat Teams
**Value:** 506.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND gravity_zone = 'Extreme Starbucks Zone' AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK') AND play_type = 'run'
                    HAVING opps >= 10
                    ORDER BY val DESC
                    LIMIT 1
```

---

# Worst Stuperlatives

## 1. Total Yards (Worst)
**Conditions:** Any Starbucks Zone (Net < 0)
**Value:** 4791.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 2. Total Yards (Worst)
**Conditions:** Any Starbucks Zone (Net < 0), High Starbucks (Net < -4)
**Value:** 3723.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND net_gravity <= -4 
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 3. Total Yards (Worst)
**Conditions:** Any Starbucks Zone (Net < 0), Extreme Starbucks Zone
**Value:** 2946.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND gravity_zone = 'Extreme Starbucks Zone' 
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 4. Total Yards (Worst)
**Conditions:** Any Starbucks Zone (Net < 0), Hat Teams
**Value:** 1951.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK') 
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 5. Total Rush Yards (Worst)
**Conditions:** Any Starbucks Zone (Net < 0)
**Value:** 1895.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND play_type = 'run'
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 6. Total Yards (Worst)
**Conditions:** Any Starbucks Zone (Net < 0), High Starbucks (Net < -4), Hat Teams
**Value:** 1556.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND net_gravity <= -4 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK') 
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 7. Total Rush Yards (Worst)
**Conditions:** Any Starbucks Zone (Net < 0), High Starbucks (Net < -4)
**Value:** 1459.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND net_gravity <= -4 AND play_type = 'run'
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 8. Total Yards (Worst)
**Conditions:** Any Starbucks Zone (Net < 0), Extreme Starbucks Zone, Hat Teams
**Value:** 1193.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND gravity_zone = 'Extreme Starbucks Zone' AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK') 
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 9. Total Rush Yards (Worst)
**Conditions:** Any Starbucks Zone (Net < 0), Extreme Starbucks Zone
**Value:** 1142.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND gravity_zone = 'Extreme Starbucks Zone' AND play_type = 'run'
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 10. Total Rush Yards (Worst)
**Conditions:** Any Starbucks Zone (Net < 0), Hat Teams
**Value:** 805.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK') AND play_type = 'run'
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 11. Total Yards (Worst)
**Conditions:** Any Starbucks Zone (Net < 0), Starbucks Death Zone
**Value:** 777.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND gravity_zone = 'Starbucks Death Zone' 
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 12. Total Yards (Worst)
**Conditions:** Any Starbucks Zone (Net < 0), Bird Teams
**Value:** 762.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA') 
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 13. Total Rush Yards (Worst)
**Conditions:** Any Starbucks Zone (Net < 0), High Starbucks (Net < -4), Hat Teams
**Value:** 688.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND net_gravity <= -4 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK') AND play_type = 'run'
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 14. Total Yards (Worst)
**Conditions:** Any Starbucks Zone (Net < 0), Mammal Teams
**Value:** 604.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND opponent IN ('CHI', 'DET', 'JAX', 'CAR', 'LAR', 'CIN', 'DEN', 'IND', 'MIA', 'BUF') 
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

## 15. Total Rush Yards (Worst)
**Conditions:** Any Starbucks Zone (Net < 0), Extreme Starbucks Zone, Hat Teams
**Value:** 506.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        'SEA' as player,
                        SUM(yards_gained) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND gravity_zone = 'Extreme Starbucks Zone' AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK') AND play_type = 'run'
                    HAVING opps >= 10
                    ORDER BY val ASC
                    LIMIT 1
```

---

