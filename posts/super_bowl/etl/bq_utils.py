import os
from google.cloud import bigquery
from google.api_core.exceptions import NotFound
from datetime import datetime

# Config
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')
DATASET_ID = 'stuperlatives'

def get_bq_client():
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"Service account not found at {SERVICE_ACCOUNT_FILE}")
        return None
    return bigquery.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)

def ensure_dataset(client):
    dataset_ref = f"{client.project}.{DATASET_ID}"
    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset {dataset_ref} already exists.")
    except NotFound:
        print(f"Dataset {dataset_ref} not found. Creating...")
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = "US"
        client.create_dataset(dataset)
        print(f"Dataset {dataset_ref} created.")
    return dataset_ref

def upload_dataframe(client, df, table_name, dataset_ref, chunk_size=None):
    if df.empty:
        print(f"Skipping {table_name}: DataFrame is empty.")
        return

    table_ref = f"{dataset_ref}.{table_name}"
    
    # Configure job to overwrite table
    job_config = bigquery.LoadJobConfig(
        write_disposition="WRITE_TRUNCATE",
    )
    
    # Clean up columns for BQ
    df = df.copy() # Avoid modifying original
    df.columns = [c.replace(' ', '_').replace('.', '').replace('/', '_per_') for c in df.columns]
    
    # Add upload timestamp
    df['upload_timestamp'] = datetime.now()
    
    # Convert incompatible types if any?
    # nfl_data_py fields are usually fine, but Object types can be tricky.
    # BQ handles most, but ensuring string conversion for complex objects might be needed.
    # For now, we trust BQ's auto-detect.

    print(f"Uploading {len(df)} rows to {table_ref}...")
    try:
        job = client.load_table_from_dataframe(df, table_ref, job_config=job_config)
        job.result()  # Wait for the job to complete.
        print(f"Loaded {job.output_rows} rows to {table_ref}.")
    except Exception as e:
        print(f"Error uploading to {table_ref}: {e}")
