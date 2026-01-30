
# Coffee Gravity Map Visualization

This document explains how to reproduce the "Coffee Force Field" maps, which visualize the gravitational pull of Dunkin' vs. Starbucks around NFL stadiums.

## Overview
The goal is to create interactive maps:
1.  **Gravity Field**: A heatmap showing the net gravitational influence (Dunkin' vs. Starbucks) across the geography.
2.  **Interference Model**: Stores within 0.5 miles of an opposing chain "cancel out" each other's mass.
3.  **Active Stadiums**: Only map the 30 active NFL stadiums for the 2024/2025 season.

## Scripts

### 1. `generate_gravity_field_all.py`
This is the main script that generates the comprehensive map.

**Key Features:**
*   **Data Source**: BigQuery `stuperlatives.coffee_wars`.
*   **Stadium Validation**: Uses a hardcoded mapping of current 2024 stadiums (verified via Web Search and PBP data) to ensure we map the correct physical location, ignoring historical stadiums like "Candlestick Park".
*   **Display Overrides**: Handles stadium renames (e.g., Cleveland Browns Stadium -> Huntington Bank Field) for display purposes while maintaining data integrity with the BigQuery records.
*   **Interference Logic**: 
    -   Radius: 0.5 miles.
    -   Strength: 1.0 (Linear reduction).
    -   Formula: Mass reduced by `(1 - distance/0.5)`.
*   **Field Calculation**: 
    -   Grid resolution: 100x100 per stadium.
    -   Gravity Model: `Mass * exp(-0.5 * distance_miles)`.
    -   Net Gravity: `Sum(Dunkin) - Sum(Starbucks)`.
*   **Visualization**: Folium map with `folium.raster_layers.ImageOverlay` to project the calculated numpy grid as a colored PNG (Orange for Dunkin', Green for Starbucks).

**Usage:**
```bash
python3 generate_gravity_field_all.py
```
**Output:** `coffee_force_field_map_all.html`

### 2. `generate_gravity_field.py` (Single Stadium)
A variant of the main script focused on generating a high-resolution map for a single specific stadium (e.g., Gillette Stadium).
**Usage:** Edit `STADIUM_FILTER` in the script.

### 3. `generate_gravity_map.py` (Circle Markers)
An older visualization script that plots simple circles scaled by gravity, rather than a continuous force field. Useful for debugging specific store locations.

## Data Schema
The BigQuery table `stuperlatives.coffee_wars` contains:
*   `team_name`: NFL Team (e.g., "New England Patriots").
*   `stadium_name`: Stadium Name (e.g., "Gillette Stadium").
*   `dunkin`: STRUCT containing `locations` (ARRAY of STRUCTs with `lat`, `lng`, `distance_miles`).
*   `starbucks`: Same structure as Dunkin.

## Reproducibility Steps
1.  **Setup Environment**: Ensure Python environment has `folium`, `pandas`, `numpy`, `matplotlib`, and `google-cloud-bigquery`.
2.  **Authenticate**: Ensure `shhhh/service_account.json` is present.
3.  **Run Script**: Execute `python3 generate_gravity_field_all.py`.
4.  **View Output**: Open the resulting HTML file in a browser.

## Logic Implementation Details
*   **Stadium Selection**: The script iterates through the BigQuery rows. It **skips** any row where the literal `stadium_name` does not match the `CURRENT_STADIUM_NAMES` dictionary. This is critical for teams like the 49ers who have rows for both Candlestick (Old) and Levi's (New).
*   **Coordinate Precision**: Coordinates are strictly defined in `STADIUM_COORDS` to ensure the map centers on the current stadium turf, regardless of the centroid of nearby coffee shops.
