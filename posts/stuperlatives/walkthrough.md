# Stuperlatives Analysis Walkthrough

This guide explains how to run the Stuperlatives analysis and generate the report.

## Prerequisites

1.  **Python Environment**: Ensure you have Python installed.
2.  **Dependencies**: Install the required packages:
    ```bash
    pip install -r requirements.txt
    ```

## Data Setup

The analysis relies on play-by-play data (handled automatically via `nfl_data_py`) and manual appearance labels (e.g. who has a beard).

-   **Public Usage**: Ensure `posts/stuperlatives/data/appearance_labels.csv` exists.
-   **Internal Usage (with Credentials)**: If `shhhh/service_account.json` is present, the script will automatically download the latest labels from Google Cloud Storage.

## Initial Setup (One-Time)

If you have BigQuery credentials configured in `shhhh/service_account.json`, run the data loader to persist all raw data to BigQuery. **You only need to run this once** (or when you want to refresh the data).

```bash
python -m posts.stuperlatives.etl.load_data
```

This will create/populate the `stuperlatives` dataset with:
-   `pbp_data`: All ~1.2M plays
-   `appearance_labels`: Manual appearance tagging
-   `ivy_league_players`: Roster subset
-   `rosters`: Full roster data
-   `schedules`: Game schedules

## Running the Analysis

From the **root directory** of the project (`mosp/`), run the report generator as a module:

```bash
python -m posts.stuperlatives.analysis.generate_report
```

**Note**: The analysis now runs SQL queries directly against the BigQuery tables populated in the previous step. Ensure `load_data.py` has been run at least once.

## Output

The script will generate a Markdown report at:
`posts/stuperlatives/report.md`

## Troubleshooting

-   **ModuleNotFoundError**: Ensure you are running the command from the project root (`mosp/` folder), NOT from inside `posts/stuperlatives/analysis/`.
-   **Missing Appearance Data**: If you see empty tables for "Grizzly Adams" or "Yosemite Sam", ensure `posts/stuperlatives/data/appearance_labels.csv` is populated.
