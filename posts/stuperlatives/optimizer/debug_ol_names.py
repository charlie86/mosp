
import os
import sys
import pandas as pd
from google.cloud import bigquery
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from posts.stuperlatives.etl.bq_utils import get_bq_client

# --- Configuration ---
TARGET_SEASON = 2025
BLOCKING_SUMMARY = f"pff_blocking_summary_{TARGET_SEASON}"

client = get_bq_client()

print("Checking PFF Blocking Teams...")
pff_teams = client.query(f"""
    SELECT DISTINCT team_name FROM `pff_analysis.{BLOCKING_SUMMARY}` ORDER BY 1
""").to_dataframe()
print("PFF Teams:", pff_teams['team_name'].unique())

print("\nChecking Schedule Teams...")
sched_teams = client.query(f"""
    SELECT DISTINCT posteam as team_name FROM `stuperlatives.pbp_data` WHERE season = {TARGET_SEASON} ORDER BY 1
""").to_dataframe()
print("Schedule Teams:", sched_teams['team_name'].unique())

print("\nChecking IHOP Teams...")
ihop_teams = client.query(f"SELECT DISTINCT Team FROM `stuperlatives.ihop_data` ORDER BY 1").to_dataframe()
print("IHOP Teams:", ihop_teams['Team'].unique())
