
import os
import sys
from google.cloud import bigquery
# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from posts.stuperlatives.etl.bq_utils import get_bq_client

# --- Configuration ---
TARGET_SEASON = 2025
BLOCKING_SUMMARY = f"pff_blocking_summary_{TARGET_SEASON}"

client = get_bq_client()

print("Checking Position Groups...")
groups = client.query(f"""
    SELECT DISTINCT position_group FROM `pff_analysis.{BLOCKING_SUMMARY}`
""").to_dataframe()
print("Groups:", groups['position_group'].unique())

print("Checking Positions...")
pos = client.query(f"""
    SELECT DISTINCT position FROM `pff_analysis.{BLOCKING_SUMMARY}`
""").to_dataframe()
print("Positions:", pos['position'].unique())
