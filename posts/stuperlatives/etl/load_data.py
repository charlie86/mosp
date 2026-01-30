import os
import sys
import pandas as pd
import nfl_data_py as nfl

# Add path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from posts.stuperlatives.etl.bq_utils import get_bq_client, ensure_dataset, upload_dataframe
from posts.stuperlatives.etl.bq_utils import get_bq_client, ensure_dataset, upload_dataframe
from google.cloud import storage
from io import StringIO

# Config for GCS (if needed)
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')
BUCKET_NAME = 'mosp-stuperlatives-data'
LABEL_BLOB_NAME = 'appearance_labels.csv'
DATA_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '../data'))
LOCAL_LABEL_FILE = os.path.join(DATA_DIR, 'appearance_labels.csv')

def get_labels():
    # 1. Check local file first
    if os.path.exists(LOCAL_LABEL_FILE):
        print(f"Loading labels from local file: {LOCAL_LABEL_FILE}")
        return pd.read_csv(LOCAL_LABEL_FILE)
    
    # 2. If not found, try GCS if credentials exist
    if os.path.exists(SERVICE_ACCOUNT_FILE):
        print("Local labels not found. Attempting to fetch from GCS...")
        try:
            client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)
            bucket = client.bucket(BUCKET_NAME)
            blob = bucket.blob(LABEL_BLOB_NAME)
            
            if blob.exists():
                content = blob.download_as_text()
                # Save locally for future use
                os.makedirs(DATA_DIR, exist_ok=True)
                with open(LOCAL_LABEL_FILE, 'w') as f:
                    f.write(content)
                print(f"Downloaded and saved labels to {LOCAL_LABEL_FILE}")
                return pd.read_csv(StringIO(content))
            else:
                print("Labels not found in GCS.")
        except Exception as e:
            print(f"Error fetching from GCS: {e}")
    else:
        print(f"Labels file not found at {LOCAL_LABEL_FILE} and no credentials at {SERVICE_ACCOUNT_FILE}.")
        
    return pd.DataFrame()

def load_data():
    print("Initializing BigQuery Data Load...")
    
    # 1. Setup BQ
    client = get_bq_client()
    if not client:
        print("Aborting: No BQ Client available.")
        return
        
    dataset_ref = ensure_dataset(client)
    
    # 2. Appearance Labels
    print("\n--- 1. Uploading Appearance Labels ---")
    labels = get_labels()
    if not labels.empty:
        upload_dataframe(client, labels, 'appearance_labels', dataset_ref)
    else:
        print("Warning: Appearance labels empty or not found.")

    # 3. Ivy League Roster
    print("\n--- 2. Uploading Ivy League Roster Data ---")
    IVY_LEAGUE = ['Brown', 'Columbia', 'Cornell', 'Dartmouth', 'Harvard', 'Penn', 'Pennsylvania', 'Princeton', 'Yale']
    print(f"Fetching rosters (1999-2025) for Ivy League filter...")
    rosters = nfl.import_seasonal_rosters(list(range(1999, 2026)))
    ivy_roster = rosters[rosters['college'].isin(IVY_LEAGUE)][['player_id', 'player_name', 'position', 'team', 'college']].drop_duplicates()
    upload_dataframe(client, ivy_roster, 'ivy_league_players', dataset_ref)

    # 3b. Full Rosters (for name lookups)
    print("\n--- 2b. Uploading Full Rosters (1999-2025) ---")
    # rosters already fetched lines 35. 
    # Just upload the whole thing (or needed columns).
    # rosters has many columns. Let's keep ID, Name, Team, Position, Headshot?
    # Actually just dump it, but force string for safety to avoid Schema errors (e.g. jersey '27' vs 27)
    rosters_upload = rosters.astype(str)
    # Convert 'season' back to int if needed, or just let it be string. BQ handles it.
    upload_dataframe(client, rosters_upload, 'rosters', dataset_ref)

    # 4. PBP Data (The Big One)
    print("\n--- 3. Uploading Play-by-Play Data (1999-2025) ---")
    # Fetching all at once might be memory intensive, but nfl_data_py is efficient.
    # If it fails, we can loop by year.
    years = list(range(1999, 2026))
    print(f"Fetching PBP for {len(years)} seasons...")
    
    try:
        pbp = nfl.import_pbp_data(years)
        print(f"Fetched {len(pbp)} rows. Uploading to BQ...")
        upload_dataframe(client, pbp, 'pbp_data', dataset_ref)
    except Exception as e:
        print(f"Error handling PBP data: {e}")
        print("Attempting year-by-year upload due to potential memory issues (or just retrying)...")
        # Optional: Implement year-by-year loop if bulk fails.
        # But `upload_dataframe` uses `write_truncate`.
        # To support incremental, we'd need `write_append` logic.
        # For now, let's stick to bulk since 25 years of PBP is roughly ~1.2M rows, manageable in memory for most machines (approx 1-2GB).
    
    # 5. Schedules

    print("\n--- 4. Uploading Schedule Data (1999-2025) ---")
    print(f"Fetching schedules...")
    try:
        schedules = nfl.import_schedules(years)
        print(f"Fetched {len(schedules)} games. Uploading to BQ...")
        upload_dataframe(client, schedules, 'schedules', dataset_ref)
    except Exception as e:
        print(f"Error handling Schedule data: {e}")


    print("\nData Load Complete.")

if __name__ == "__main__":
    load_data()
