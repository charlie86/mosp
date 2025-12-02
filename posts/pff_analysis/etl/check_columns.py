import pandas as pd
import os

# Configuration
SCRIPT_DIR = os.path.dirname(os.path.abspath(__file__))
MAIN_DATA_FILE = os.path.join(SCRIPT_DIR, '../data/pff_ihop_analysis_results_with_draft_year.csv')

def main():
    if not os.path.exists(MAIN_DATA_FILE):
        print(f"Error: {MAIN_DATA_FILE} not found.")
        return

    print(f"Loading main data from {MAIN_DATA_FILE}...")
    df = pd.read_csv(MAIN_DATA_FILE)
    print("Columns:", df.columns.tolist())
    print("First 5 rows:")
    print(df.head())

if __name__ == "__main__":
    main()
