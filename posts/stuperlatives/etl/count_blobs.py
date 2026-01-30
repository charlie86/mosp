
import os
from google.cloud import storage

PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')
BUCKET_NAME = 'mosp-stuperlatives-data'

def count_blobs():
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print("Service account not found.")
        return

    client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)
    bucket = client.bucket(BUCKET_NAME)
    
    blobs = bucket.list_blobs(prefix="headshots/")
    count = 0
    for _ in blobs:
        count += 1
    
    print(f"Total headshots in 'headshots/': {count}")

if __name__ == "__main__":
    count_blobs()
