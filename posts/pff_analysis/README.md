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
All scraped data is stored directly in a secure **Google Sheet** (`PFF Run Blocking Data`). No scraped data is stored locally.
*   **PFF Grades:** `etl/pff_position_scraper.py` (Scrapes 2006-2025 Player Grades -> Google Sheets)
*   **Team Defense:** `etl/pff_team_scraper.py` (Scrapes 2006-2025 Team Grades -> Google Sheets)
*   **Images/Plots:** Uploaded to **Google Cloud Storage** bucket `mosp-pff-analysis`.
    > **Note:** All future plots and visualizations MUST be stored in this GCS bucket. Do not commit image files to the repository. The `reporting/plots/` directory is gitignored.

### 2. ETL Pipeline
*   **Master Script:** `etl/run_analysis.py`
*   **Input:** Reads raw data tabs from Google Sheets.
*   **Processing:** Cleans data, restores historical stadium names, merges IHOP metrics, calculates experience (rookie year + aging curve), and merges team defense stats.
*   **Output:** Writes the final dataset to the **`Merged Analysis Data`** tab in the Google Sheet.

### 3. Analysis & Reporting
*   **Standardized Loading:** All analysis scripts use `analysis/production/utils.py` to fetch the merged data directly from Google Sheets.
*   **Scripts:** Located in `analysis/production/`.
    *   `analyze_global_controlled_regression.py`: Global MV Regressions.
    *   `analyze_controlled_regression.py`: Individual player regressions.
    *   `generate_global_regression_plot.py`: Visualization.

## Directory Structure

*   `etl/`: Extract, Transform, Load scripts.
    *   `pff_position_scraper.py`: Scrapes player grades to Sheets.
    *   `run_analysis.py`: Cleans and merges data within Sheets.
    *   `tests/`: Unit tests and debug scripts.
    *   `PFF_SCRAPING_WALKTHROUGH.md`: Detailed scraping guide.
*   `analysis/`:
    *   `production/`: **Core analysis scripts.** Robust, peer-reviewed code.
        *   `utils.py`: Shared data loading logic.
        *   `analyze_*.py`: Statistical models.
        *   `generate_*.py`: Plot generation.
    *   `exploration/`: Experimental scripts and notebooks.
*   `reporting/`: Artifacts for publication.
    *   `paper/`: LaTeX source and PDF for the research paper.
    *   `plots/`: Generated figures and charts.
    *   `*.html/csv`: Regression reports and tables.

## How to Run

### 1. Install Dependencies
```bash
pip install -r requirements.txt
playwright install
```

### 2. Scrape Data
```bash
# Scrape positions (Handles auth, resumes dynamically, saves to Sheets)
python3 etl/pff_position_scraper.py
```

### 3. Run ETL (Merge & Clean)
```bash
# Merges raw scraping + schedule + IHOP data -> 'Merged Analysis Data' tab
python3 etl/run_analysis.py
```

### 4. Run Analysis
```bash
# Run global regression
python3 analysis/production/analyze_global_controlled_regression.py

# Generate plots
python3 analysis/production/generate_global_regression_plot.py
```
