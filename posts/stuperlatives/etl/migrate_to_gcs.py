
from google.cloud import storage
import os
import glob

# Config
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')
BUCKET_NAME = 'mosp-stuperlatives-data'
LOCAL_DATA_DIR = os.path.join(PROJECT_ROOT, 'posts/stuperlatives/data')

def migrate():
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print("Service account not found.")
        return

    client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)
    
    # 1. Create Bucket if not exists
    bucket = client.bucket(BUCKET_NAME)
    if not bucket.exists():
        print(f"Creating bucket {BUCKET_NAME}...")
        bucket = client.create_bucket(BUCKET_NAME, location="US")
    else:
        print(f"Bucket {BUCKET_NAME} exists.")
        
    # 2. Upload Headshots
    headshot_dir = os.path.join(LOCAL_DATA_DIR, 'headshots')
    if os.path.exists(headshot_dir):
        files = glob.glob(os.path.join(headshot_dir, "*.png"))
        print(f"Uploading {len(files)} headshots...")
        for f in files:
            blob_name = f"headshots/{os.path.basename(f)}"
            blob = bucket.blob(blob_name)
            if not blob.exists():
                blob.upload_from_filename(f)
                print(f"Uploaded {blob_name}")
            else:
                # print(f"Skipping {blob_name}")
                pass
    
    # 3. Upload CSVs
    csvs = glob.glob(os.path.join(LOCAL_DATA_DIR, "*.csv"))
    print(f"Uploading {len(csvs)} CSVs...")
    for f in csvs:
        blob_name = os.path.basename(f)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(f)
        print(f"Uploaded {blob_name}")

if __name__ == "__main__":
    migrate()
