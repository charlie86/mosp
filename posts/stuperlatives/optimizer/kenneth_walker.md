# The Kenneth Walker "Stuperlative" Summary

## 1. The "K9 vs. Cats" Phenomenon
Kenneth "K9" Walker III has a bone to pick with felines, especially after dark. When the sun goes down and a cat-themed team is on the prowl, K9 turns into a touchdown machine.

**The Stat:** Most Touchdowns vs. Cat Teams (Lions, Panthers, Jaguars, Bengals) in Night Games (Start Time > 7:00 PM) among all active RBs.

### The Leaderboard
| Rank | Player | Touchdowns |
| :--- | :--- | :--- |
| **#1** | **K. Walker** | **7** |
| #2 | J. Jacobs | 4 |
| #3 | D. Henry | 3 |
| #4 | C. Brown | 3 |
| #5 | A. Jones | 3 |

### The Query
For the data nerds who want to verify this canine dominance:

```sql
WITH active_players AS (
    SELECT DISTINCT rusher_player_name AS name
    FROM `stuperlatives.pbp_data`
    WHERE season = (SELECT MAX(season) FROM `stuperlatives.pbp_data`)
)

SELECT
    rusher_player_name AS player,
    COUNT(*) AS opportunities,
    SUM(touchdown) AS touchdowns
FROM `stuperlatives.pbp_data`
WHERE
    defteam IN ('DET', 'JAX', 'CAR', 'CIN') -- Cat Teams
    AND start_time > '19:00:00'             -- Night Game
    AND season_type != 'PRE'
    AND rush_attempt = 1                    -- Opportunity Filter
    AND rusher_player_name IN (SELECT name FROM active_players)
GROUP BY
    1
HAVING
    opportunities >= 20
ORDER BY
    touchdowns DESC
LIMIT
    5
```

## Other Notable Stuperlatives

### 2. 4th Quarter Dome Dominance
- **Metric:** Rushing Yards Per Game (28.3)
- **Conditions:** **4th Quarter**, in a **Dome** Stadium
- **Rank:** #1

### 3. Home Cookin' in the West
- **Metric:** Total Touchdowns (2.0)
- **Conditions:** **Own Territory** (Yardline > 50), in **Western Division** Games (NFC West, AFC West teams)
- **Rank:** #1

### 4. Red Zone Bird Watcher
- **Metric:** Rushing Yards Per Game (16.1)
- **Conditions:** **Red Zone** (Yardline <= 20), VS **Bird Teams** (Eagles, Falcons, Cardinals, Ravens, Seahawks - though he plays for one!)
- **Rank:** #1

