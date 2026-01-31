# Seahawks DEFENSE Performance by Starbucks Gravity

**Analysis Period:** 2025 Season

This analysis shows how the Seattle Seahawks defense performs under different **Coffee Gravity** conditions.

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

## 1. Stops (Best)
**Conditions:** Any Starbucks Zone (Net < 0)
**Value:** 471.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 2. Total Pressures (Best)
**Conditions:** Any Starbucks Zone (Net < 0)
**Value:** 426.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        player,
                        SUM(total_pressures) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 3. Stops (Best)
**Conditions:** Any Starbucks Zone (Net < 0), High Starbucks (Net < -4)
**Value:** 373.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND net_gravity <= -4
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 4. Stops (Best)
**Conditions:** Any Starbucks Zone (Net < 0), Extreme Starbucks Zone
**Value:** 330.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND gravity_zone = 'Extreme Starbucks Zone'
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 5. Total Pressures (Best)
**Conditions:** Any Starbucks Zone (Net < 0), High Starbucks (Net < -4)
**Value:** 327.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        player,
                        SUM(total_pressures) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND net_gravity <= -4
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 6. Total Pressures (Best)
**Conditions:** Any Starbucks Zone (Net < 0), Extreme Starbucks Zone
**Value:** 284.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        player,
                        SUM(total_pressures) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND gravity_zone = 'Extreme Starbucks Zone'
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 7. Stops (Best)
**Conditions:** Any Starbucks Zone (Net < 0), Hat Teams
**Value:** 189.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 8. Total Pressures (Best)
**Conditions:** Any Starbucks Zone (Net < 0), Hat Teams
**Value:** 146.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        player,
                        SUM(total_pressures) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 9. Stops (Best)
**Conditions:** Any Starbucks Zone (Net < 0), High Starbucks (Net < -4), Hat Teams
**Value:** 142.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND net_gravity <= -4 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 10. Stops (Best)
**Conditions:** Any Starbucks Zone (Net < 0), Extreme Starbucks Zone, Hat Teams
**Value:** 121.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND gravity_zone = 'Extreme Starbucks Zone' AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 11. Total Pressures (Best)
**Conditions:** Any Starbucks Zone (Net < 0), High Starbucks (Net < -4), Hat Teams
**Value:** 107.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        player,
                        SUM(total_pressures) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND net_gravity <= -4 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 12. Total Pressures (Best)
**Conditions:** Any Starbucks Zone (Net < 0), Extreme Starbucks Zone, Hat Teams
**Value:** 79.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        player,
                        SUM(total_pressures) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND gravity_zone = 'Extreme Starbucks Zone' AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 13. Stops (Best)
**Conditions:** Any Starbucks Zone (Net < 0), Mammal Teams
**Value:** 78.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND opponent IN ('CHI', 'DET', 'JAX', 'CAR', 'LAR', 'CIN', 'DEN', 'IND', 'MIA', 'BUF')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 14. Median Pass Rush Grade (Best)
**Conditions:** Any Starbucks Zone (Net < 0), Starbucks Death Zone, Hat Teams
**Value:** 66.450

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        player,
                        MEDIAN(grades_pass_rush_defense) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND gravity_zone = 'Starbucks Death Zone' AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

## 15. Total Pressures (Best)
**Conditions:** Any Starbucks Zone (Net < 0), Mammal Teams
**Value:** 66.000

✅ **NARRATIVE WIN:** Seahawks excel in Starbucks territory!

```sql
SELECT 
                        player,
                        SUM(total_pressures) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND opponent IN ('CHI', 'DET', 'JAX', 'CAR', 'LAR', 'CIN', 'DEN', 'IND', 'MIA', 'BUF')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val DESC
                    LIMIT 5
```

---

# Worst Stuperlatives

## 1. Stops (Worst)
**Conditions:** Any Starbucks Zone (Net < 0)
**Value:** 471.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 2. Total Pressures (Worst)
**Conditions:** Any Starbucks Zone (Net < 0)
**Value:** 426.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        player,
                        SUM(total_pressures) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 3. Stops (Worst)
**Conditions:** Any Starbucks Zone (Net < 0), High Starbucks (Net < -4)
**Value:** 373.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND net_gravity <= -4
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 4. Stops (Worst)
**Conditions:** Any Starbucks Zone (Net < 0), Extreme Starbucks Zone
**Value:** 330.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND gravity_zone = 'Extreme Starbucks Zone'
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 5. Total Pressures (Worst)
**Conditions:** Any Starbucks Zone (Net < 0), High Starbucks (Net < -4)
**Value:** 327.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        player,
                        SUM(total_pressures) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND net_gravity <= -4
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 6. Total Pressures (Worst)
**Conditions:** Any Starbucks Zone (Net < 0), Extreme Starbucks Zone
**Value:** 284.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        player,
                        SUM(total_pressures) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND gravity_zone = 'Extreme Starbucks Zone'
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 7. Stops (Worst)
**Conditions:** Any Starbucks Zone (Net < 0), Hat Teams
**Value:** 189.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 8. Total Pressures (Worst)
**Conditions:** Any Starbucks Zone (Net < 0), Hat Teams
**Value:** 146.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        player,
                        SUM(total_pressures) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 9. Stops (Worst)
**Conditions:** Any Starbucks Zone (Net < 0), High Starbucks (Net < -4), Hat Teams
**Value:** 142.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND net_gravity <= -4 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 10. Stops (Worst)
**Conditions:** Any Starbucks Zone (Net < 0), Extreme Starbucks Zone, Hat Teams
**Value:** 121.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND gravity_zone = 'Extreme Starbucks Zone' AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 11. Total Pressures (Worst)
**Conditions:** Any Starbucks Zone (Net < 0), High Starbucks (Net < -4), Hat Teams
**Value:** 107.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        player,
                        SUM(total_pressures) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND net_gravity <= -4 AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 12. Total Pressures (Worst)
**Conditions:** Any Starbucks Zone (Net < 0), Extreme Starbucks Zone, Hat Teams
**Value:** 79.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        player,
                        SUM(total_pressures) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND gravity_zone = 'Extreme Starbucks Zone' AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 13. Stops (Worst)
**Conditions:** Any Starbucks Zone (Net < 0), Mammal Teams
**Value:** 78.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        player,
                        SUM(stops) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND opponent IN ('CHI', 'DET', 'JAX', 'CAR', 'LAR', 'CIN', 'DEN', 'IND', 'MIA', 'BUF')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 14. Median Pass Rush Grade (Worst)
**Conditions:** Any Starbucks Zone (Net < 0), Starbucks Death Zone, Hat Teams
**Value:** 66.450

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        player,
                        MEDIAN(grades_pass_rush_defense) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND gravity_zone = 'Starbucks Death Zone' AND opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

## 15. Total Pressures (Worst)
**Conditions:** Any Starbucks Zone (Net < 0), Mammal Teams
**Value:** 66.000

⚠️ This is a worst-case scenario in Starbucks land.

```sql
SELECT 
                        player,
                        SUM(total_pressures) as val,
                        COUNT(*) as opps
                    FROM data
                    WHERE 1=1 AND net_gravity < 0 AND opponent IN ('CHI', 'DET', 'JAX', 'CAR', 'LAR', 'CIN', 'DEN', 'IND', 'MIA', 'BUF')
                    GROUP BY player
                    HAVING opps >= 1
                    ORDER BY val ASC
                    LIMIT 5
```

---

