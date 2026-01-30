import nfl_data_py as nfl
import pandas as pd
import os

def fetch_pbp_data(years):
    """Fetches play-by-play data for the specified years."""
    print(f"Fetching PBP data for {years}...")
    pbp = nfl.import_pbp_data(years)
    return pbp

def fetch_rosters(years):
    """Fetches roster data for the specified years (includes headshot URLs)."""
    print(f"Fetching rosters for {years}...")
    rosters = nfl.import_seasonal_rosters(years)
    return rosters

def fetch_schedules(years):
    """Fetches schedule data to determine opponents."""
    print(f"Fetching schedules for {years}...")
    schedules = nfl.import_schedules(years)
    return schedules

if __name__ == "__main__":
    # Default to recent years for analysis
    YEARS = [2022, 2023, 2024]
    
    # Ensure data directory exists
    os.makedirs("posts/stuperlatives/data", exist_ok=True)
    
    # Fetch and save sample data if needed, or just print status
    print("Testing data fetch...")
    try:
        df_pbp = fetch_pbp_data([2024])
        print(f"Successfully fetched {len(df_pbp)} plays from 2024.")
        
        df_roster = fetch_rosters([2024])
        print(f"Successfully fetched {len(df_roster)} roster entries from 2024.")
    except Exception as e:
        print(f"Error fetching data: {e}")
