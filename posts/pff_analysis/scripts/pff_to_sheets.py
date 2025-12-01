import gspread
from oauth2client.service_account import ServiceAccountCredentials
import pandas as pd
import sys
import os

# --- Configuration ---
# Path to your Service Account JSON key file
# Resolve paths relative to this script
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
# Go up 3 levels: scripts -> pff_analysis -> posts -> root
PROJECT_ROOT = os.path.abspath(os.path.join(SCRIPT_DIR, "../../../"))
SERVICE_ACCOUNT_FILE = os.path.join(PROJECT_ROOT, 'shhhh/service_account.json')
# The name of the Google Sheet you want to write to
SHEET_NAME = 'PFF Run Blocking Data 2025'
# The CSV file to upload
CSV_FILE = 'pff_run_blocking_data_2025_by_game.csv'

def upload_to_sheets():
    # 1. Check if files exist
    if not os.path.exists(SERVICE_ACCOUNT_FILE):
        print(f"Error: {SERVICE_ACCOUNT_FILE} not found.")
        print("Please download your Service Account JSON key and save it as 'service_account.json' in this directory.")
        return

    if not os.path.exists(CSV_FILE):
        print(f"Error: {CSV_FILE} not found.")
        print("Please run the scraper first to generate the data.")
        return

    print("Authenticating with Google Sheets...")
    try:
        # Define the scope
        scope = ['https://spreadsheets.google.com/feeds', 'https://www.googleapis.com/auth/drive']
        # Add credentials to the account
        creds = ServiceAccountCredentials.from_json_keyfile_name(SERVICE_ACCOUNT_FILE, scope)
        # Authorize the clientsheet
        client = gspread.authorize(creds)
    except Exception as e:
        print(f"Authentication failed: {e}")
        return

    print(f"Opening sheet '{SHEET_NAME}'...")
    try:
        # Open the sheet
        sheet = client.open(SHEET_NAME)
        # Select the first worksheet
        worksheet = sheet.sheet1
    except gspread.SpreadsheetNotFound:
        print(f"Sheet '{SHEET_NAME}' not found.")
        print("Please create a Google Sheet with this exact name and share it with the service account email.")
        print(f"Service Account Email: {creds.service_account_email}")
        return

    print("Reading CSV data...")
    try:
        df = pd.read_csv(CSV_FILE)
        # Replace NaN with empty string for Sheets compatibility
        df = df.fillna('')
    except Exception as e:
        print(f"Error reading CSV: {e}")
        return

    print("Uploading data...")
    try:
        # Clear existing data
        worksheet.clear()
        # Update with new data (list of lists)
        # [df.columns.values.tolist()] + df.values.tolist() creates header + rows
        worksheet.update([df.columns.values.tolist()] + df.values.tolist())
        print("Upload complete!")
    except Exception as e:
        print(f"Error uploading data: {e}")

if __name__ == "__main__":
    upload_to_sheets()
