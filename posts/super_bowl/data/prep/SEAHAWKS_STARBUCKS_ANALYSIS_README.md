# Seahawks Starbucks Gravity Analysis

This project analyzes the performance of the Seattle Seahawks based on the "Coffee Gravity" of the stadium they are playing in. It uses a **Mass Interference Model** to calculate the gravitational pull of Starbucks vs. Dunkin' Donuts and correlates it with offensive and defensive metrics.

## 📂 Project Structure

### Analysis & Scripts
*   **`seahawks_starbucks_optimizer.py`**: The main powerhouse script. It calculates coffee gravity for every NFL stadium and runs a permutation analysis to find the strongest correlations between high Starbucks gravity and Seahawks performance. It generates the detailed reports.

### Generated Reports
*   **`seahawks_starbucks_summary.md`**: The master narrative report. Summarizes the findings, explains the "Starbucks Death Zone" concept, and provides a prediction for Super Bowl LX.
*   **`seahawks_top_10_starbucks_stats.md`**: A "greatest hits" list of the most creative and statistically accurate (yet absurd) findings, perfect for social media or quick digest.
*   **`seahawks_defense_starbucks.md`**: Comprehensive data dump of the top defensive correlations (Stops, Pressures, etc.) in various Starbucks zones.
*   **`seahawks_offense_starbucks.md`**: Comprehensive data dump of the top offensive correlations (Total Yards, Rush Yards) in various Starbucks zones.

### Supporting Files (Existing)
*   **`coffee_narrative_report.md`**: The original foundational report establishing the Physics of Coffee and the "Runs on Dunkin'" theory for the Patriots.
*   **`validate_coffee_report.py`**: Used to verify the gravity calculations and stadium coordinates.

## ☕ The Coffee Gravity Model

We calculate "Net Gravity" using an exponential decay model with interference:

$$ Net Gravity = \sum (Dunkin \cdot e^{-0.5d}) - \sum (Starbucks \cdot e^{-0.5d}) $$

*   **Interference:** If a Dunkin' and Starbucks are within 0.5 miles of each other, their masses cancel out.
*   **Interpretation:** 
    *   **Positive Score (+)** = Dunkin' Dominance (Patriots Territory)
    *   **Negative Score (-)** = Starbucks Dominance (Seahawks Territory)

## 🚀 How to Reproduce

1.  **Run the Optimizer:**
    ```bash
    cd posts/stuperlatives/super_bowl
    python3 seahawks_starbucks_optimizer.py
    ```
    *This will recalculate gravity scores and regenerate the defense and offense markdown reports from scratch.*

2.  **View the Results:**
    Open `seahawks_starbucks_summary.md` for the narrative overview.

## 📊 Key Findings (Sneak Peek)

*   **Lumen Field (-11.46 Gravity):** The "Extreme Starbucks Zone" where the Seahawks defense records **330 stops**.
*   **Levi's Stadium (-5.80 Gravity):** A "Starbucks Death Zone" for the Patriots (rush EPA -0.160), but a playground for the Seahawks (1,459 rush yards in similar zones).
*   **Inverse Correlation:** The exact environmental conditions that destroy the Patriots' run game are statistically significant boosters for the Seahawks.

---
*Analysis generated for the Super Bowl Stuperlatives project.*
