# Stuperlatives: The Ministry of Silly Plots Analysis

This project explores "Stupid Superlatives" for NFL players, finding correlations between performance and arbitrary, humorous criteria like mascot taxonomy or facial hair.

## Structure (Cloud-Native)
- `etl/`: Scripts to fetch NFL data and manage GCS assets.
- `analysis/`: Logic to compute the superlatives using data from GCS.
- `sql/`: Raw SQL queries for BigQuery analysis.
- `data/`: Minimal local config (`team_taxonomy.py`).

## Analyses

### Mascot-Based
- **Bird Hunters:** Passes deflected against bird teams.
- **Circus Tamers:** Rushing defense against circus animal teams.
- **Social Justice Warriors:** Record against teams with controversial branding.
- **Deadliest Catch:** Interceptions against aquatic/nautical teams.

### Appearance-Based
- **Grizzly Adams:** Tackling performance of bearded defenders.
- **Yosemite Sam:** QB ratings of mustachioed quarterbacks.
- **Rooster Fever:** Sack production against redheaded quarterbacks.

## Criteria & Metrics (2022-2024 Data)

### Mascot Taxonomy
*Reference: `data/team_taxonomy.py`*

- **Bird Teams:** Cardinals (ARI), Falcons (ATL), Ravens (BAL), Eagles (PHI), Seahawks (SEA).
- **Circus Teams** (Animals found in a circus): Lions (DET), Bears (CHI), Bengals (CIN), Jaguars (JAX).
- **Social Justice Teams** (Controversial/Problematic mascots): Chiefs (KC), Commanders (WAS).
- **Aquatic Teams:** Dolphins (MIA), Seahawks (SEA), Chargers (LAC).

### Metrics Defined

#### Mascot-Based
- **Bird Hunters:** Total Passes Defended (PDs) + Interceptions (INTs) recorded by a defender *against* Bird Teams.
- **Circus Tamers:** Fewest Rushing Yards Allowed per Game by a team defense in games *against* Circus Teams (min. 2 games).
- **Social Justice Warriors:** Highest Win Percentage *against* Social Justice Teams (min. 3 games).
- **Deadliest Catch:** Total Interceptions recorded by a defender *against* Aquatic Teams.
- **Deadliest Catch:** Total Interceptions recorded by a defender *against* Aquatic Teams.
- **Pirate's Booty:** Total Takeaways (INTs + Fumble Recoveries) by a defender *against* **Pirate Teams**.
- **Schoolyard Bullies:** Total Tackles recorded by a defender *against* players who attended an **Ivy League** school.

#### Appearance-Based (Automated Computer Vision)
*Labels generated via Gemini Vision API analysis of official roster headshots (`etl/gemini_label.py`).*

- **Grizzly Adams:** Total Tackles (Solo + Assist) by defenders identified as having a **Beard**.
- **Yosemite Sam:** EPA per Play for Quarterbacks identified as having a **Strict Mustache** (Mustache=True, Beard=False).
- **Rooster Fever:** Total Sacks recorded by a defender *against* **Redheaded Quarterbacks** (Andy Dalton, Sam Darnold, Cooper Rush, C.J. Beathard).

- `data/`: Contains `team_taxonomy.py`. Headshots and labels are stored in Google Cloud Storage (`mosp-stuperlatives-data`).

### Selection Criteria
- **Dataset:** Active players from the 2023-2024 seasons.
- **Filtering:** Players included if they played **> 50 Snaps** or recorded **> 10** statistics (Attempts/Tackles).
- **Headshots:** Sourced via `nfl_data_py` and stored in GCS.


## Data Storage & Access

### Google Cloud Storage (GCS)
- **Bucket:** `mosp-stuperlatives-data`
- **Contents:**
    - `headshots/{player_id}.png`: Source images for appearance analysis.
    - `appearance_labels.csv`: Master dataset of Gemini-generated classifications.

### BigQuery
- **Dataset:** `stuperlatives`
- **Tables:**
    - **Intermediary:**
        - `appearance_labels`: Copy of the GCS CSV (Player ID, Beard, Mustache, Redhead status).
        - `ivy_league_players`: List of active players from Ivy League schools.
    - **Calculated Metrics:**
        - `metric_bird_hunters`
        - `metric_circus_tamers`
        - `metric_deadliest_catch`
        - `metric_pirates_booty`
        - `metric_schoolyard_bullies`
        - `metric_grizzly_adams`
        - `metric_yosemite_sam`
        - `metric_rooster_fever`
        - `metric_social_justice_warriors`

All analysis scripts can be re-run to update these tables via `etl/upload_to_bq.py`.
