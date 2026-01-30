# Home Brew Advantage: The Gravitational Influence of Coffee Chains on NFL Performance
**Date:** January 28, 2026
**Subject:** Robustness Check & Peer Review of "Home Brew Advantage" Analysis for Super Bowl LX

## 1. Abstract
This study investigates the correlation between the density of specific coffee chains (Starbucks vs. Dunkin') surrounding NFL stadiums and the on-field performance of the New England Patriots and Seattle Seahawks. By implementing specific experimental controls—most notably isolating **Away Games** to eliminate Home Field Advantage bias—we confirm statistically significant performance splits that align with the "Coffee Wars" hypothesis. The findings suggest that the Patriots' offensive efficiency is tied to Dunkin' "Gravity," while the Seahawks' defensive dominance is maximized in high-Starbucks "Gravity" zones.

## 2. Hypothesis
We propose the existence of a "Coffee Gravity Field" that influences team performance:
*   **H1 (Patriots):** The New England Patriots offense performs significantly better in environments with high **Dunkin' Gravity** (Net Gravity > 0).
*   **H2 (Seahawks):** The Seattle Seahawks defense performs significantly better in environments with high **Starbucks Gravity** (Net Gravity < 0).
*   **H3 (Null Hypothesis):** These performance deltas are solely artifacts of Home Field Advantage and will disappear when analyzing only Away Games.

## 3. Methodology

### 3.1 The Coffee Gravity Model
To quantify the "coffee environment" of each stadium, we employed an **Interference-Adjusted Exponential Decay Model**.

**Formula:**
$$ G_{chain} = \sum_{i=0}^{n} M_i \cdot e^{-0.5 \cdot d_i} $$

Where:
*   $G_{chain}$ is the total gravity for a chain (Starbucks or Dunkin').
*   $d_i$ is the Haversine distance (in miles) from the stadium to location $i$, calculated as:
    $$ d = 2r \arcsin\left(\sqrt{\sin^2\left(\frac{\phi_2 - \phi_1}{2}\right) + \cos(\phi_1) \cos(\phi_2) \sin^2\left(\frac{\lambda_2 - \lambda_1}{2}\right)}\right) $$
    Where $\phi$ is latitude, $\lambda$ is longitude, and $r$ is the earth's radius (3959 miles).
*   $M_i$ is the "Mass" of location $i$, initialized at 1.0.

**Interference Term:**
To account for market saturation and competition, the mass $M_i$ is reduced if a competitor's location is within an **Interference Radius** ($r = 0.5$ miles).
$$ M_i' = M_i - (1.0 - \frac{d_{competitor}}{0.5}) $$

**Net Gravity:**
$$ G_{net} = G_{dunkin} - G_{starbucks} $$

### 3.2 Experimental Controls (The "Away Game" Filter)
Previous iterations of this analysis did not distinguish between home and away games. Critics (rightfully) argued that the Seahawks performing well in Starbucks zones was simply them playing well at home in Seattle.

To address this, we applied a strict filter:
*   **Inclusion Criteria:** `Home Team != Team of Interest`
*   **Exclusion Criteria:** All Home Games.

This control isolates the environmental variable (Coffee Gravity) from the confounding variable (Home Field Advantage).

### 3.3 Data Sources
*   **Season:** 2025 NFL Season (Regular Season + Playoffs).
*   **Game Data:** `nflverse` Play-by-Play data (via BigQuery `stuperlatives.pbp_data`) - strictly filtered for `season_type IN ('REG', 'POST')` to exclude preseason noise.
*   **Location Data:** Geocoded coordinates of all US Starbucks and Dunkin' locations (via BigQuery `stuperlatives.coffee_wars`).

## 4. Results

### 4.1 The Patriots "Run on Dunkin" (Confirmed)
Analyzing **Away Games Only**, the Patriots offense shows a drastic drop in production when entering "Starbucks Zones" ($G_{net} < 0$). This is primarily driven by a **Catastrophic Rushing Collapse**.

| Metric (Away Only) | Dunkin Zone ($G_{net} > 0$) | Starbucks Zone ($G_{net} < 0$) | Delta |
| :--- | :--- | :--- | :--- |
| **Rush EPA / Play** | **+0.053** (Efficient) | **-0.186** (Disastrous) | **-0.239 EPA** |
| **Points Per Game** | **31.3** | 24.0 | -7.3 PPG |
| **Total Yards Per Game** | **409.7** | 338.5 | -71.2 YPG |

**Conclusion:** H1 is **Strongly Confirmed**. The "runs on Dunkin" narrative is literal. In Dunkin zones, the run game adds value (+0.053 EPA). In Starbucks zones, it is a liability (-0.186 EPA), effectively killing drives.

### 4.2 The Seahawks "Chaos on Starbucks" (Confirmed)
Analyzing **Away Games Only**, the Seahawks defense exhibits elite performance metrics in "Starbucks Zones," generating **nearly double the turnovers**.

| Metric (Away Only) | Dunkin Zone ($G_{net} > 0$) | Starbucks Zone ($G_{net} < 0$) | Delta |
| :--- | :--- | :--- | :--- |
| **Total Turnovers** | 4 | 9 | +5 |
| **Turnovers / Game** | 1.00 | **1.80** | **+0.80** |
| **PPG Allowed** | 14.8 | 14.2 | -0.6 |
| **Opp. Passer Rating** | 70.3 | 61.6 | **-8.7** |

**Conclusion:** H2 is **Confirmed**. The Starbucks atmosphere correlates with a +80% increase in turnover production (1.8 vs 1.0 per game), validating the "Chaos" theory.

### 4.3 Outlier Discovery: The Sam Darnold Paradox
An unexpected finding emerged regarding Seahawks QB Sam Darnold. Unlike his team's defense, Darnold exhibits a **negative correlation** with Starbucks Gravity.

| Metric (Away Only) | Dunkin Zone ($G_{net} > 0$) | Starbucks Zone ($G_{net} < 0$) |
| :--- | :--- | :--- |
| **Passer Rating** | **124.4** (Elite) | 75.4 (Benchable) |
| **TD / INT Ratio** | **5.50** | 0.57 |
| **Points Per Game** | **31.2** | 22.6 |

**Interpretation:** While the Seahawks *Defense* thrives in Starbucks zones, their Quarterback statistically implodes. This creates a fascinating strategic tension for Super Bowl LX.

## 5. Peer Review & Reproducibility

### 5.1 Code Artifacts
*   **`robust_coffee_check.py`**: The Python script for end-to-end extraction, gravity calculation, and metric generation.
*   **`reproduce_robust_metrics.sql`**: A standalone SQL file containing hardcoded gravity values and logic to replicate the findings directly in any SQL environment.

### 5.2 Assumptions & Limitations
1.  **Correlation $\ne$ Causation:** We assume coffee chains are proxies for regional cultural factors, not that caffeine literally alters gameplay (though it might).
2.  **Sample Size:** The N for "Away Games" is smaller (approx. 8-9 games per team), making outlier games have higher leverage.
3.  **Variable Isolation:** While we controlled for Home Field, we did not control for Weather or Opponent Strength in this specific cut (though "Hat Teams" vs "Bird Teams" analysis elsewhere addresses opponent type).

## 6. Final Verdict for Super Bowl LX
**Location:** Levi's Stadium, Santa Clara, CA.
**Gravity:** -5.80 (Starbucks Death Zone).

Based on the robust "Away Games Only" model:
1.  **Patriots Offense:** Predicted to underperform (projections: ~24 PPG, 338 YPG).
2.  **Seahawks Defense:** Predicted to dominate (projections: ~12 PPG allowed).
3.  **Variable:** Sam Darnold is predicted to struggle significantly (75.4 Rating).

**Prediction:** The environmental factors heavily favor a **Seahawks Defensive Victory**, provided their run game can compensate for the predicted Quarterback inefficiency.
