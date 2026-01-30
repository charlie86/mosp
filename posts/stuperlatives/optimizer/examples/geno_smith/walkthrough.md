
# Geno Smith: The "Midnight Snack" King

## Executive Summary
Using the **Stuperlative Optimizer**, we conducted a brute-force statistical search to identify specific scenarios where **Geno Smith** is the #1 Quarterback. 

*   **Total Permutations Tested**: ~67,000
*   **Data Source**: BigQuery PBP Data (1999-2025)
*   **Processing Time**: ~8 minutes (Parallelized)

We discovered that Geno Smith excels in highly specific, high-pressure environments—specifically when playing deep in enemy territory in the South, or when playing in Overtime near a pancake house.

---

## The Discoveries

### 1. The "IHOP Clutch God" (Active Players)
**The Stat**: Highest EPA/Play in Overtime games played within 5 miles of an IHOP.
*   **Value**: **0.466 EPA/Play**
*   **Rank**: **#1** among Active Players (Min 5 attempts)

> [!NOTE]
> **Interpretation**: This finding validates our "IHOP Proximity" hypothesis. When the game goes late (Overtime) and the gravitational pull of the Rooty Tooty Fresh 'N Fruity is strongest (Within 5mi), Geno Smith becomes the most efficient quarterback in the league.

**The Filter**:
*   `Environment`: Within 5mi of IHOP
*   `Game Context`: Overtime

---

### 2. The "Southern Slayer" (All-Time Record)
**The Stat**: Highest Yards/Attempt in Division Rivalry Games played in the "South" region.
*   **Value**: **10.2 Yards/Attempt**
*   **Rank**: **#1 All-Time** (Since 1999)

> [!TIP]
> **Context**: This covers games played in stadiums belonging to: DAL, HOU, NO, ATL, CAR, TB, MIA, JAX, TEN.
> Geno's efficiency here likely stems from his time with the Jets (playing @ MIA) and Seahawks (playing @ NFC South teams), where he has historically torched division rivals on the road in the humidity.

---

### 3. The "Deep End" Safety Valve
**The Stat**: Highest Completion % Over Expected (CPOE) in Tied Games when backed up inside his own 20.
*   **Value**: **+13.2% CPOE**
*   **Rank**: **#1 Active Player**

> [!IMPORTANT]
> **Why this matters**: In the most dangerous part of the field (Deep Own Territory), in the tensest game state (Tied), Geno doesn't just manage the game—he completes passes at a rate 13% higher than the mathematical expectation. He is the ultimate safety valve.

---

## Technical Appendix

### SQL Logic Verification
To verify these stats in BigQuery, you can use the following derived queries.


#### Query 1: The IHOP Overtime Stat
```sql
SELECT
    p.passer_player_name as player,
    COUNT(*) as plays,
    AVG(p.epa) as epa_per_play
FROM `stuperlatives.pbp_data` p
JOIN `stuperlatives.rosters` r
  ON p.passer_player_name = r.player_name
WHERE p.qtr = 5 -- Overtime
  AND p.home_team IN (
      SELECT Team FROM `stuperlatives.ihop_data` WHERE DistanceMiles < 5
  )
  AND r.season = (SELECT MAX(season) FROM `stuperlatives.rosters`) -- Strictly Active Players
GROUP BY 1
HAVING plays >= 5
ORDER BY epa_per_play DESC
LIMIT 5
```

#### Query 2: The Southern Slayer
```sql
SELECT
    passer_player_name as player,
    SUM(yards_gained) / COUNT(*) as yards_per_att
FROM `stuperlatives.pbp_data`
WHERE div_game = 1
  AND home_team IN ('DAL', 'HOU', 'NO', 'ATL', 'CAR', 'TB', 'MIA', 'JAX', 'TEN')
  AND (pass_attempt = 1 OR sack = 1)
GROUP BY 1
HAVING COUNT(*) >= 20
ORDER BY yards_per_att DESC
LIMIT 5
```

### Reproduction
You can replicate this search using the CLI tool:

```bash
python3 posts/stuperlatives/optimizer/stuperlative_finder.py --player "G.Smith" --position "QB"
```
