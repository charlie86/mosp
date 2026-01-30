# Stuperlative Optimizer: The Methodology

This tool is designed to find "Stupid Superlatives" for NFL players by aggressively filtering data until they rank #1 in a specific metric.

## The Concept

Standard analysis looks at "All Games" or "Last 5 Weeks". The **Stuperlative Optimizer** looks at *800+* specific scenarios to find where a player dominates.

We combine **PFF Metrics** (Grades, Breakaway Yards, etc.) with **Game Context** (Time of Day, Stadium Roof, Opponent Mascots) to find niche statistical dominance.

## Data Sources

The optimizer joins two datasets:
1.  **PFF Summary Data**: `pff_rushing_summary_{YEAR}` (BigQuery)
    -   *Metrics:* Yards, Touchdowns, Breakaway Yards, Avoided Tackles, Explosive Runs.
2.  **Schedule Context**: Derived from `pbp_data` (BigQuery)
    -   *Environment:* Roof (Dome/Outdoors), Time (Night/Day).
    -   *Opponent:* Team Abbreviation, Division Rivalry.
    -   *Derived Categories:* "Bird Teams", "Pirate Teams", "Near IHOP", "West Coast".

## The Algorithm

1.  **Load & Join**: Fetches PFF stats and joins them with the schedule context for every game.
2.  **Generate Permutations**: Creates a list of all possible filter combinations.
    -   *Opponent:* All, Bird Teams, Cat Teams, Pirate Teams, Division Rivals.
    -   *Environment:* Night Games, Day Games, Domes, Outdoors.
    -   *Geography:* West Coast, East Coast, Near IHOP.
    -   *Combinations:* "Night Games vs Bird Teams", "Outdoors in the West", etc.
3.  **Parallel Optimization**:
    -   For every permutation (e.g., "Night Games vs Rivals"), it aggregates stats for ALL players.
    -   Calculates rankings for every metric (e.g., "Breakaway %").
    -   Checks if the **Target Player** is Rank #1.
4.  **Verification**: ensure the sample size is sufficient (e.g., >20 attempts) to avoid "1 attempt, 10 yards = #1 YPC" noise.

## How to Run

To run the optimizer for any player (currently configured for 2025/2026 Season):

```bash
python3 posts/stuperlatives/optimizer/pff_optimizer.py --player "Player Name"
```

**Example:**
```bash
python3 posts/stuperlatives/optimizer/pff_optimizer.py --player "Kenneth Walker"
```

## Output

The script generates a Markdown report (`pff_stuperlatives_{player_name}.md`) containing:
-   **The "Winning" Conditions**: (e.g., "Outdoors vs Pirate Teams").
-   **The Metric**: (e.g., "Explosive Run Rate").
-   **Leaderboard**: Top 5 players in that specific split to prove the rank.
-   **SQL Query**: The exact SQL used to verify this stat in BigQuery.

## Customization

To add new "silly" filters, edit `posts/stuperlatives/optimizer/pff_optimizer.py`:
-   **`METRICS`**: Add new PFF columns (e.g., `fumbles`, `grades_offense`).
-   **`build_filters()`**: Define new groups (e.g., "Teams with Red Logos").
