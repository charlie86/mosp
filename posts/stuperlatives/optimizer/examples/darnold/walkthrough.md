
# The Darnold Discovery: Finding the "Red Zone Equalizer"

## Objective
To find a statistically significant metric where **Sam Darnold** ranks **#1** among all NFL quarterbacks.

## Methodology
We used a custom-built **"Stuperlative Optimizer"** to systematically test thousands of combinations of:
1.  **Metrics**: Yards/Game, TD/INT Ratio, Success Rate, Completion %, etc.
2.  **Filters**: Down, Distance, Field Position, Score Differential, Opponent (Bird Teams, Rivals), Environment (Night Games, Dome), geography, and more.

## The Findings

After running ~8,000 permutations against the BigQuery PBP dataset (covering 1999-2025), we identified several specific scenarios where Sam Darnold is effectively the best quarterback in the database.

### 1. The Crown Jewel: "The Red Zone Equalizer"
**Metric**: Completion Percentage
**Context**: Tied Game, Red Zone (Inside 20)
**Cohort**: All Time (Since 1999), Min 20 Attempts

| Rank | Player | Comp % | Attempts |
| :--- | :--- | :--- | :--- |
| **1** | **Sam Darnold** | **66.7%** | **33** |
| 2 | Bo Nix | 65.7% | 35 |
| 3 | Drew Brees | 64.8% | 108 |
| 4 | Philip Rivers | 64.8% | 105 |
| 5 | Jared Goff | 64.7% | 78 |

**Interpretation**: When the game is tied and the field shrinks, Darnold becomes the most accurate passer in modern NFL history. He edges out legends like Brees and Rivers.

---

### 2. The "Left-Leaning Leader" (Active Players)
**Metric**: Success Rate
**Context**: Tied Game, Throwing Left
**Cohort**: Active Players (Min 20 Attempts)

| Rank | Player | Success Rate |
| :--- | :--- | :--- |
| **1** | **Sam Darnold** | **57.1%** |
| 2 | Jacoby Brissett | 56.6% |
| 3 | Brock Purdy | 55.5% |

**Interpretation**: Darnold is surprisingly efficient when throwing to his left side in high-leverage (tied) situations.

---

### 3. "The Deep Night King" (Active Players)
**Metric**: Passing Yards/Game
**Context**: Deep Own Territory (>80 yards to go), Night Games (>7:00 PM)
**Cohort**: Active Players (Min 5 Games)

| Rank | Player | YPG |
| :--- | :--- | :--- |
| **1** | **Sam Darnold** | **38.1** |
| 2 | Zach Wilson | 33.5 |
| 3 | Tua Tagovailoa | 32.2 |

**Interpretation**: When pinned deep in his own territory under the bright lights of primetime, Darnold racks up yardage at a higher clip than any other active QB.

---


## Perpetuating the Stuperlatives

This analysis has been generalized into a reusable tool so you can find "Stuperlatives" for any player.

### How to Reproduce (and find your own)
We created the `stuperlative_finder.py` CLI tool to run this optimization loop for any player and position.

**To replicate these Darnold findings:**
```bash
python3 posts/stuperlatives/optimizer/stuperlative_finder.py --player "Darnold" --position "QB"
```

**To search for another player (e.g. Baker Mayfield):**
```bash
python3 posts/stuperlatives/optimizer/stuperlative_finder.py --player "Mayfield" --position "QB"
```

### Technical Implementation
*   **Engine**: `posts/stuperlatives/optimizer/stuperlative_finder.py` - A brute-force optimization engine using **DuckDB** for high-performance in-memory processing of thousands of permutations.
*   **Configuration**: `posts/stuperlatives/optimizer/config_definitions.py` - Contains the modular definitions for metrics (QB/RB/WR), filters, and logic for generated features like "IHOP Proximity".
*   **Data Source**: BigQuery `stuperlatives.pbp_data` (All-Time PBP Data).
