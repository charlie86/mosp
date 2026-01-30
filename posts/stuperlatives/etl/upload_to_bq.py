
import os
import sys
import pandas as pd
from datetime import datetime


# Add path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from posts.stuperlatives.etl.fetch_data import fetch_pbp_data
from posts.stuperlatives.analysis.mascot_analysis import (
    analyze_bird_hunters,
    analyze_circus_tamers,
    analyze_social_justice_warriors,
    analyze_deadliest_catch,
    analyze_pirates_booty,
    analyze_schoolyard_bullies
)
from posts.stuperlatives.analysis.appearance_analysis import (
    analyze_grizzly_adams,
    analyze_yosemite_sam,
    analyze_rooster_fever,
    get_labels
)


# Config
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')
DATASET_ID = 'stuperlatives'

from posts.stuperlatives.etl.bq_utils import (
    get_bq_client, 
    ensure_dataset, 
    upload_dataframe
)

def main():
    client = get_bq_client()
    if not client:
        return

    dataset_ref = ensure_dataset(client)
    
    # NOTE: Raw data upload (appearance, ivy league, pbp) is now handled by load_data.py
    # We focus here on uploading the CALCULATED metrics.
    
    print("\n--- 2. Computing and Uploading Metrics ---")

    
    print("Fetching PBP Data...")
    pbp = fetch_pbp_data(list(range(1999, 2026)))
    
    # Metrics Map
    # name -> function
    metrics = {
        'metric_bird_hunters': analyze_bird_hunters,
        'metric_circus_tamers': analyze_circus_tamers,
        'metric_deadliest_catch': analyze_deadliest_catch,
        'metric_pirates_booty': analyze_pirates_booty,
        'metric_schoolyard_bullies': analyze_schoolyard_bullies,
        'metric_grizzly_adams': analyze_grizzly_adams,
        'metric_yosemite_sam': analyze_yosemite_sam,
        'metric_rooster_fever': analyze_rooster_fever
    }
    
    for table_name, func in metrics.items():
        print(f"Running {table_name}...")
        try:
            df = func(pbp)
            upload_dataframe(client, df, table_name, dataset_ref)
        except Exception as e:
            print(f"Error running {table_name}: {e}")
            
    # SJW is special (needs years, not PBP)
    print("Running metric_social_justice_warriors...")
    try:
        df_sjw = analyze_social_justice_warriors(list(range(1999, 2026)))
        upload_dataframe(client, df_sjw, 'metric_social_justice_warriors', dataset_ref)
    except Exception as e:
        print(f"Error running SJW: {e}")

    print("\nBigQuery Upload Complete.")

if __name__ == "__main__":
    main()
