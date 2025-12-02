# PFF Run Blocking Scraper Walkthrough

I have successfully implemented a robust, automated scraper for PFF Run Blocking stats.

## Solution Overview

The solution uses a standalone Python script (`posts/pff_analysis/scripts/pff_auto_scraper.py`) powered by **Playwright**. This approach was chosen to handle PFF's complex React-based DOM and authentication requirements.

### Key Features
-   **Persistent Authentication**: Uses `pff_auth.json` to save your login session, so you only need to log in manually once.
-   **Game-Specific URLs**: Iterates through each team's specific game page for the requested week (e.g., `.../minnesota-vikings/offense-run-blocking`) to ensure accurate data.
-   **Robust Selector Logic**: Uses an "Index Matching" strategy to correctly map player names to their Run Blocking grades, handling the split-table structure of the PFF website.
-   **CSV Export**: Saves all data to `pff_run_blocking_data_2025_by_game.csv`.

## How to Run

1.  **Install Dependencies** (if not already done):
    ```bash
    pip install playwright pandas
    playwright install chromium
    ```

2.  **Run the Script**:
    ```bash
    python3 posts/pff_analysis/scripts/pff_auto_scraper.py
    ```

3.  **First Run (Authentication)**:
    -   The script will open a browser window and navigate to the PFF login page.
    -   **Log in manually** with your credentials.
    -   Wait for the redirect to the dashboard. The script will detect the login, save the session to `pff_auth.json`, and proceed automatically.

4.  **Subsequent Runs**:
    -   The script will load the saved session and run fully automatically without user intervention.

## Output

The data is saved to `pff_run_blocking_data_2025_by_game.csv` with the following columns:
-   `Week`: The NFL week (e.g., 12).
-   `Team`: The team slug (e.g., `minnesota-vikings`).
-   `Player`: The player's name.
-   `Grade`: The PFF Run Blocking grade (0-100).

## Configuration

You can adjust the `SEASON` and `START_WEEK` / `END_WEEK` variables at the top of `posts/pff_analysis/scripts/pff_auto_scraper.py` to scrape different time periods.

### Example: Full Season Scrape
To scrape the entire regular season so far (e.g., Weeks 1-12):
```python
SEASON = 2025
START_WEEK = 1
END_WEEK = 12
```

### Example: Single Week Scrape
To scrape just the latest week:
```python
SEASON = 2025
START_WEEK = 12
END_WEEK = 12
```

## Legal & Ethical Considerations

Before using this scraper, please be aware of PFF's policies:

1.  **Robots.txt**:
    *   `premium.pff.com/robots.txt` disallows `/api/`, but does **not** disallow the game pages (`/nfl/games/...`) accessed by this script.
2.  **Terms of Use**:
    *   PFF grants permission to "download one copy of the materials... for your **personal use**".
    *   **Mirroring** (republishing) any material is strictly prohibited.
    *   **Do not** share the raw CSV data publicly or use it for commercial purposes without PFF's permission.
3.  **Rate Limiting**:
    *   The script runs sequentially to be respectful of PFF's servers. Do not attempt to parallelize it aggressively, as this may trigger IP bans.

    *   The script runs sequentially to be respectful of PFF's servers. Do not attempt to parallelize it aggressively, as this may trigger IP bans.

## Google Sheets Integration

To upload the scraped data to Google Sheets:

1.  **Set up Google Cloud**:
    *   Go to the [Google Cloud Console](https://console.cloud.google.com/).
    *   Create a new project.
    *   Enable the **Google Sheets API** and **Google Drive API**.
    *   Create a **Service Account**.
    *   Create a JSON key for that service account and download it.
    *   **Rename** the key file to `service_account.json` and place it in the `shhhh/` directory.

2.  **Prepare the Sheet**:
    *   Create a new Google Sheet named **"PFF Run Blocking Data 2025"**.
    *   **Share** the sheet with the email address found inside your `shhhh/service_account.json` file (look for `client_email`). Give it "Editor" access.

3.  **Run the Upload Script**:
    ```bash
    pip install gspread oauth2client
    python3 posts/pff_analysis/scripts/pff_to_sheets.py
    ```

4.  **Cleanup**:
    *   Once verified in Google Sheets, **delete the local CSV file** to prevent accidental upload to GitHub.
    ```bash
    rm pff_run_blocking_data_2025_by_game.csv
    ```

## Technical Details

### The "Split Table" Challenge
During development, we discovered that the PFF data table is split into two parts:
1.  **Sticky Columns**: Contains Player Name, Team, etc.
2.  **Scrollable Data**: Contains the actual grades.

These two parts are not nested in a single row container. Instead, they are rendered separately.

### The Solution: Index Matching
To solve this, the script:
1.  Finds all **Player Names** in the sticky column.
2.  Finds all **Grade Badges** in the data column.
3.  Matches them by index (assuming a 1-to-1 correspondence and consistent sort order).
4.  Extracts the **Run Blocking Grade**, which is consistently the first grade in the triplet of grades shown for each player on the "Run Blocking" page.

### Browser Inspection
The following recording demonstrates the browser subagent inspecting the DOM to discover this structure:

![Browser Inspection](/Users/charliethompson/.gemini/antigravity/brain/fbf0c722-cab1-41ba-9c4e-dc2e8fb73483/inspect_pff_stats_container_1764557947870.webp)
