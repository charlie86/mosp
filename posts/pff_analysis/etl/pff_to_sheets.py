import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import sys
import os
import time
import glob

# --- Configuration ---
# Path to your Service Account JSON key file
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../"))
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')
SHEET_NAME = 'PFF Run Blocking Data'
DATA_DIR = os.path.join(SCRIPT_DIR, '../data')

def get_client():
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"Error: {SERVICE_ACCOUNT_FILE} not found.")
        return None

    try:
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
        client = gspread.authorize(creds)
        return client
    except Exception as e:
        print(f"Authentication failed: {e}")
        return None

def upload_file(client, sheet, tab_name, csv_path):
    print(f"\nProcessing '{tab_name}'...")
    
    if not os.path.exists(csv_path):
        print(f"  Error: {csv_path} not found. Skipping.")
        return

    # Read CSV
    try:
        df = pd.read_csv(csv_path)
        df = df.fillna('') # Replace NaNs
        print(f"  Read {len(df)} rows from CSV.")
    except Exception as e:
        print(f"  Error reading CSV: {e}")
        return

    # Get or Create Worksheet
    try:
        try:
            worksheet = sheet.worksheet(tab_name)
            print(f"  Found existing tab '{tab_name}'. Clearing...")
            worksheet.clear()
        except gspread.WorksheetNotFound:
            print(f"  Tab '{tab_name}' not found. Creating...")
            worksheet = sheet.add_worksheet(title=tab_name, rows=len(df)+100, cols=len(df.columns))
        
        # Upload
        print("  Uploading data...")
        # Update in chunks to avoid timeouts if large
        # Check size limit (Sheets API has limits on payload size)
        # If > 5000 rows, maybe chunk? gspread handles some of this but let's be safe if it's huge.
        # For now, standard update.
        data = [df.columns.values.tolist()] + df.values.tolist()
        worksheet.update(data)
        print(f"  Successfully uploaded to '{tab_name}'.")
        
    except Exception as e:
        print(f"  Error interacting with Sheets: {e}")

def main():
    client = get_client()
    if not client:
        return

    print(f"Opening sheet '{SHEET_NAME}'...")
    try:
        sheet = client.open(SHEET_NAME)
    except gspread.SpreadsheetNotFound:
        print(f"Sheet '{SHEET_NAME}' not found.")
        print("Please create a Google Sheet with this exact name and share it with the service account email.")
        return

    # Find all CSVs
    csv_files = glob.glob(os.path.join(DATA_DIR, "*.csv"))
    print(f"Found {len(csv_files)} CSV files in {DATA_DIR}")

    for csv_path in csv_files:
        filename = os.path.basename(csv_path)
        # Tab name is filename without extension
        tab_name = os.path.splitext(filename)[0]
        
        # Truncate to 100 chars if needed (Sheets limit)
        if len(tab_name) > 100:
            tab_name = tab_name[:100]
            
        upload_file(client, sheet, tab_name, csv_path)
        time.sleep(2) # Rate limit niceness

if __name__ == "__main__":
    main()
