# Super Bowl Preview: Drake Maye (PASSING)

**Season:** 2025

# Best Stuperlatives

## Median Clean YPA (Best)
**Conditions:** Bird Teams

| player          |   val |   opps |
|:----------------|------:|-------:|
| Drake Maye      | 10.3  |     46 |
| Sam Darnold     | 10.3  |     54 |
| Brock Purdy     |  9.75 |     40 |
| Jared Goff      |  9    |     41 |
| Patrick Mahomes |  8.6  |     48 |

```sql
SELECT 
                            player,
                            MEDIAN(no_pressure_ypa) as val,
                            SUM(no_pressure_attempts) as opps
                        FROM data
                        WHERE 1=1 AND opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA')
                        GROUP BY player
                        HAVING opps >= 20
                        ORDER BY val DESC
                        LIMIT 5
```

---

