
import os
import requests
import pandas as pd
import sys

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from posts.stuperlatives.etl.fetch_data import fetch_rosters


from google.cloud import storage

# GCS Config
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')
BUCKET_NAME = 'mosp-stuperlatives-data'

def get_bucket():
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"Service account not found at {SERVICE_ACCOUNT_FILE}")
        return None
    client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)
    return client.bucket(BUCKET_NAME)

def download_headshot_to_gcs(url, player_id, bucket):
    """Downloads a headshot from a URL and uploads to GCS."""
    if not url or pd.isna(url):
        return False
    
    blob_name = f"headshots/{player_id}.png"
    blob = bucket.blob(blob_name)
    
    if blob.exists():
        return False # Already exists
    
    try:
        response = requests.get(url, timeout=10)
        if response.status_code == 200:
            blob.upload_from_string(response.content, content_type='image/png')
            return True
    except Exception as e:
        print(f"Failed to download/upload {url}: {e}")
    return False

import nfl_data_py as nfl

def fetch_active_players_headshots(years=[2024], min_snaps=50):
    """
    Fetches rosters and downloads headshots for players with significant snap counts.
    """
    bucket = get_bucket()
    if not bucket:
        return

    print("Fetching snap counts to filter active players...")
    try:
        snaps = nfl.import_snap_counts(years)
        # Aggregate snaps by player
        player_snaps = snaps.groupby('player').agg({
            'offense_snaps': 'sum', 
            'defense_snaps': 'sum',
            'team': 'first'
        }).reset_index()
        
        # Filter for significant players
        active_players = player_snaps[
            (player_snaps['offense_snaps'] >= min_snaps) | 
            (player_snaps['defense_snaps'] >= min_snaps)
        ]['player'].tolist()
        
        print(f"Found {len(active_players)} players with > {min_snaps} snaps.")
        
    except Exception as e:
        print(f"Error fetching snaps: {e}. Proceeding with seasonal stats only.")
        # Proceed without snap filter


    print("Fetching rosters...")
    rosters = fetch_rosters(years)
    
    print("Fetching seasonal stats to filter by activity...")
    active_ids = []
    
    try:
        stats = nfl.import_seasonal_data(years)
        
        # QBs
        active_qbs = stats[(stats['attempts'] > 10)]['player_id'].tolist()
        active_ids.extend(active_qbs)
        
        # Defenders
        if 'tackles_solo' in stats.columns:
            active_defs = stats[
                (stats['tackles_solo'] + stats['tackles_assists'] > 10) |
                (stats['sacks'] >= 1)
            ]['player_id'].tolist()
            active_ids.extend(active_defs)
            
    except Exception as e:
        print(f"Error fetching seasonal stats: {e}. Fallback to Active Roster status.")
        # Fallback: Use rosters directly
        try:
            rosters = fetch_rosters(years)
            # Filter for Active players in target positions
            # status == 'ACT'
            active_roster = rosters[rosters['status'] == 'ACT']
            active_ids = active_roster['player_id'].tolist()
            print(f"Fallback: Found {len(active_ids)} active players on roster.")
        except Exception as roster_e:
            print(f"Critical Error fetching rosters: {roster_e}")
            return
        
    print(f"Identified {len(set(active_ids))} active players based on stats.")
    
    target_rosters = rosters[rosters['player_id'].isin(active_ids)].copy()
    
    # Filter for positions
    target_rosters = target_rosters[target_rosters['position'].isin(['QB', 'LB', 'DL', 'DB', 'DT', 'DE', 'CB', 'S', 'SAF'])]
    
    print(f"Filtering to target positions: {len(target_rosters)} players.")
    
    target_rosters = target_rosters.drop_duplicates(subset=['player_id'])
    
    count = 0
    print("Checking GCS and uploading new headshots...")
    
    for _, player in target_rosters.iterrows():
        success = download_headshot_to_gcs(player['headshot_url'], player['player_id'], bucket)
        if success:
            count += 1
            print(f"Uploaded {player['player_id']}")
                
    print(f"Uploaded {count} new headshots to GCS.")

if __name__ == "__main__":
    fetch_active_players_headshots([2023, 2024])


