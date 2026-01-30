
import google.generativeai as genai
import pandas as pd
import os
import time
import json
import typing_extensions as typing

# Constants

from google.cloud import storage
import io

# GCS Config
PROJECT_ROOT = os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../'))
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')
BUCKET_NAME = 'mosp-stuperlatives-data'
LABEL_BLOB_NAME = 'appearance_labels.csv'

class AppearanceAttributes(typing.TypedDict):
    has_beard: bool
    has_mustache: bool
    is_redhead: bool

def get_bucket():
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"Service account not found.")
        return None
    client = storage.Client.from_service_account_json(SERVICE_ACCOUNT_FILE)
    return client.bucket(BUCKET_NAME)

def analyze_image_from_bytes(image_data):
    try:
        model = genai.GenerativeModel('gemini-2.0-flash')
        
        prompt = """
        Analyze this NFL player's headshot. Return a JSON object with the following boolean attributes:
        - "has_beard": Does the player have a visible beard? (Stubble counts if it covers the jawline, goatees count).
        - "has_mustache": Does the player have a visible mustache? (If they have a beard, this is usually True).
        - "is_redhead": Is the player's hair naturally red or ginger? (Be very strict. Strawberry blonde does not count unless very red).
        
        Respond ONLY with the JSON.
        """
        
        response = model.generate_content(
            [
                {'mime_type': 'image/png', 'data': image_data},
                prompt
            ],
            generation_config=genai.GenerationConfig(
                response_mime_type="application/json", response_schema=AppearanceAttributes
            )
        )
        
        return json.loads(response.text)
        
    except Exception as e:
        print(f"Error analyzing image: {e}")
        return None

def main():
    bucket = get_bucket()
    if not bucket:
        return

    # Load existing labels from GCS
    blob_labels = bucket.blob(LABEL_BLOB_NAME)
    if blob_labels.exists():
        content = blob_labels.download_as_text()
        from io import StringIO
        df = pd.read_csv(StringIO(content))
    else:
        df = pd.DataFrame(columns=['player_id', 'player_name', 'position', 'has_beard', 'has_mustache', 'is_redhead'])
        
    labeled_ids = df['player_id'].astype(str).tolist()
    
    # List images in GCS
    print("Listing headshots in bucket...")
    blobs = bucket.list_blobs(prefix="headshots/")
    
    all_blobs = [b for b in blobs if b.name.endswith(".png")]
    print(f"Found {len(all_blobs)} images, {len(labeled_ids)} already labeled.")
    
    while True:
        # Refresh blob list to pick up new uploads
        blobs = bucket.list_blobs(prefix="headshots/")
        all_blobs = [b for b in blobs if b.name.endswith(".png")]
        
        # Refresh labels (in case another process updated it? unlikely, but good practice)
        # Actually, we are the only writer.
        # But we need to know which IDs we've done in this session + previous.
        
        # We can maintain `labeled_ids` in memory if we are the only writer.
        # But let's be safe.
        
        processed_count_in_pass = 0
        
        for blob in all_blobs:
            # Extract ID
            filename = os.path.basename(blob.name)
            p_id = filename.replace(".png", "")
            
            if p_id in labeled_ids:
                continue
                
            processed_count_in_pass += 1
            
            print(f"Analyzing new player {p_id}...", end=" ", flush=True)
            
            # Download bytes
            try:
                image_data = blob.download_as_bytes()
                result = analyze_image_from_bytes(image_data)
                
                if result:
                    print(f"B: {result['has_beard']}, M: {result['has_mustache']}, R: {result['is_redhead']}")
                    new_row = {
                        'player_id': p_id,
                        'player_name': p_id, 
                        'position': 'Unknown',
                        'has_beard': result['has_beard'],
                        'has_mustache': result['has_mustache'],
                        'is_redhead': result['is_redhead']
                    }
                    
                    # Update DataFrame
                    df = pd.concat([df, pd.DataFrame([new_row])], ignore_index=True)
                    labeled_ids.append(p_id)
                    
                    # Save incrementally to GCS
                    csv_buffer = df.to_csv(index=False)
                    blob_labels.upload_from_string(csv_buffer, content_type='text/csv')
                    
                    time.sleep(1)
                else:
                    print("Failed to analyze.")
                    # Mark as failed to avoid infinite loop?
                    # labeled_ids.append(p_id) # Optional: skip next time
            except Exception as e:
                print(f"Error processing {p_id}: {e}")
                
        if processed_count_in_pass == 0:
            print("No new images found. Sleeping 10s...")
            time.sleep(10)
        else:
            print(f"Pass complete. Processed {processed_count_in_pass} images.")

if __name__ == "__main__":
    main()

