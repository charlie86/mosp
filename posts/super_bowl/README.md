# Home Brew Advantage: Coffee Gravity Analysis

**The Gravitational Influence of Regional Coffee Chains on Super Bowl LX**

This project analyzes the correlation between coffee chain density (Starbucks vs. Dunkin') around NFL stadiums and team performance, specifically for the New England Patriots and Seattle Seahawks.

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Set up BigQuery credentials (optional - uses cached data by default)
export GOOGLE_APPLICATION_CREDENTIALS="path/to/service_account.json"

# 3. Run the analysis
python analysis/robust_coffee_check.py

# 4. Generate visualizations
python visualization/plot_gravity_chart.py
python visualization/generate_map.py
```

## Project Structure

```
posts/super_bowl/
├── README.md                 # This file
├── requirements.txt          # Python dependencies
│
├── etl/                      # Data extraction & loading
│   ├── scrape_coffee_locations.py  # Scrapes Starbucks/Dunkin' via Google Maps API
│   ├── load_data.py              # Loads PBP data to BigQuery via nflverse
│   ├── bq_utils.py               # BigQuery utility functions
│   └── coffee_data_cache.json    # Pre-computed coffee location data
│
├── analysis/                 # Core analysis
│   ├── robust_coffee_check.py   # Main analysis script
│   └── reproduce_robust_metrics.sql  # Reproducible SQL queries
│
├── visualization/            # Output generation
│   ├── generate_map.py       # Interactive Folium map
│   └── plot_gravity_chart.py # Net gravity ranking chart
│
├── assets/                   # Generated outputs (maps, charts, logos)
├── screenshots/              # Stadium screenshots for report
└── docs/                     # LaTeX report & documentation
```

## ETL Pipeline

### 1. Scrape Coffee Locations (Optional - uses cached data)

```bash
# Requires Google Maps API key
python etl/scrape_coffee_locations.py
```

This scrapes all Starbucks and Dunkin' locations within 10 miles of each NFL stadium and saves to `etl/coffee_data_cache.json`.

### 2. Load PBP Data to BigQuery (Optional)

```bash
python etl/load_data.py
```

Loads nflverse play-by-play data (1999-2025) to BigQuery for analysis.

## Methodology

### Coffee Gravity Model

We use an **Interference-Adjusted Exponential Decay Model** to calculate the "gravitational pull" of each coffee chain:

```
G_chain = Σ M_i × e^(-0.5 × d_i)
```

Where:
- `d_i` = Haversine distance (miles) from stadium to location `i`
- `M_i` = "Mass" of location (reduced if competitor nearby)

**Net Gravity** = G_dunkin - G_starbucks
- Positive → Dunkin'-dominant
- Negative → Starbucks-dominant

### Key Finding

Using **Away Games Only** to control for home field advantage:
- **Patriots offense** performs significantly better in Dunkin' zones (+7.3 PPG)
- **Seahawks defense** forces 80% more turnovers in Starbucks zones

## Data Sources

- **Play-by-Play Data**: [nflverse](https://nflverse.nflverse.com/) via BigQuery
- **Coffee Locations**: Geocoded Starbucks & Dunkin' coordinates
- **Season**: 2025 (Regular + Playoffs)

## Outputs

| File | Description |
|------|-------------|
| `assets/coffee_force_field_map_all.html` | Interactive gravity field map |
| `assets/coffee_gravity_ranking_publication.jpeg` | Net gravity ranking chart |
| `docs/robust_coffee_metrics.pdf` | Full scientific report |

## License

MIT
