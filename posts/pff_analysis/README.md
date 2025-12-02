# The IHOP Effect: Do NFL Offensive Linemen Play Better Near Pancakes?

**Hypothesis:** Offensive Linemen perform better when they are in close proximity to an IHOP (International House of Pancakes), presumably due to the psychological boost of being near "pancakes".

## Findings (Updated Dec 2025)

### 1. The "Closer is Better" Effect (Confirmed)
After controlling for **Home Field Advantage**, **Player Experience** (Quadratic), and **Opposing Run Defense**, we found a statistically significant relationship between proximity to IHOP and Run Blocking Grades.

*   **Metric:** Driving Time to nearest IHOP (Minutes)
*   **Global Result:** **-0.0010** coefficient (p=0.0019). For every minute closer to an IHOP, run blocking grades increase.
*   **Robustness:** The effect persists even when accounting for:
    *   **Home/Away:** Home field advantage is controlled.
    *   **Experience:** A quadratic "aging curve" (`YearsInLeague` + `YearsInLeague^2`) accounts for improvement and decline.
    *   **Opponent:** The quality of the opposing Run Defense (`OppRunDefGrade`) is controlled.

### 2. Top Player Spotlights
Certain elite linemen show a massive sensitivity to IHOP proximity.

#### Mitchell Schwartz (The King of Pancakes)
*   **Effect:** **-0.0204** Grade Points per Minute (p=0.002)
*   **Detail:** Schwartz's performance drops significantly as he gets farther from an IHOP, even after adjusting for all other factors.

#### Bradley Bozeman
*   **Effect:** **-0.0183** Grade Points per Minute (p=0.015)
*   **Detail:** A consistent "Closer is Better" performer across his career.

### 3. Stadium Rankings
*   **Closest IHOP (Haversine):** Detroit Lions (Ford Field) - 0.68 miles
*   **Closest IHOP (Driving):** New Orleans Saints (Caesars Superdome) - 1.44 miles
*   **Furthest IHOP:** Buffalo Bills (Highmark Stadium) - > 9 miles

## Methodology & Process

### 1. Data Collection & Storage
*   **PFF Grades:** Scraped run blocking grades for all Offensive Linemen (2006-2025) using `etl/pff_position_scraper.py`.
*   **Team Defense:** Scraped Run Defense grades for all teams (2006-2025) using `etl/pff_team_scraper.py`.
*   **Cloud Storage:** All raw scraped data is uploaded to a secure Google Sheet (`PFF Run Blocking Data`) using `etl/pff_to_sheets.py`. This ensures no proprietary data is stored in the repo.

### 2. ETL Pipeline
1.  **`etl/run_analysis.py`**: Reads **Raw Player Data** from Google Sheets. Merges with Schedule and IHOP Distances.
2.  **`etl/process_team_stats.py`**: Reads **Raw Team Data** from Google Sheets. Cleans and normalizes Team Defense data.
3.  **`etl/merge_team_stats.py`**: Merges Team Defense grades into the main dataset.
4.  **`etl/add_years_in_league.py`**: Calculates `YearsInLeague` based on Draft Year.

### 3. Analysis Models
*   **Global Controlled Regression:** `Grade ~ DrivingTime + IsHome + YearsInLeague + YearsInLeague^2 + OppRunDefGrade`
    *   Script: `analysis/analyze_global_controlled_regression.py` (Reads **Merged Analysis Data** from Google Sheets)
*   **Individual Player Regression:** Same model applied to individual players (Min 30 games).
    *   Script: `analysis/analyze_controlled_regression.py` (Reads **Merged Analysis Data** from Google Sheets)

## Directory Structure

*   `data/`: CSV data files.
    *   `pff_ihop_analysis_results_final.csv`: The master dataset.
    *   `pff_team_defense_grades.csv`: Cleaned team defense stats.
*   `plots/`: Generated visualizations.
*   `etl/`: Extract, Transform, Load scripts.
    *   `pff_position_scraper.py`: Scrapes player grades.
    *   `pff_team_scraper.py`: Scrapes team defense grades.
    *   `process_team_stats.py`: Cleans team data.
    *   `merge_team_stats.py`: Merges datasets.
*   `analysis/`: Core analysis scripts.
    *   `analyze_global_controlled_regression.py`: Global model.
    *   `analyze_controlled_regression.py`: Individual player models.
    *   `update_top_players.py`: Generates top player reports and plots.
    *   `plot_experience_curve.py`: Visualizes the aging curve.
