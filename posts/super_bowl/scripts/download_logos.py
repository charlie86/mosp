
import os
import requests
import nfl_data_py as nfl
import pandas as pd

# Configuration
LOGO_DIR = "posts/stuperlatives/super_bowl/logos"

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def download_logos():
    print("Fetching team data...")
    try:
        # Get team data including logo URLs
        teams = nfl.import_team_desc()
    except Exception as e:
        print(f"Error importing nfl_data_py: {e}")
        return

    ensure_dir(LOGO_DIR)
    
    # We need to map team abbreviations to the ones used in our gravity chart
    # Our gravity chart uses Full Names mostly, but let's stick to abbreviations for filenames
    # and we can map them later.
    
    count = 0
    for _, row in teams.iterrows():
        abbr = row['team_abbr']
        logo_url = row['team_logo_espn']
        
        if not logo_url or pd.isna(logo_url):
            print(f"No logo for {abbr}")
            continue
            
        filename = f"{abbr}.png"
        filepath = os.path.join(LOGO_DIR, filename)
        
        if os.path.exists(filepath):
            # print(f"Exists: {filename}")
            continue
            
        try:
            response = requests.get(logo_url)
            if response.status_code == 200:
                with open(filepath, 'wb') as f:
                    f.write(response.content)
                print(f"Downloaded: {filename}")
                count += 1
            else:
                print(f"Failed to download {filename}: {response.status_code}")
        except Exception as e:
            print(f"Error downloading {filename}: {e}")
            
    print(f"Finished. Downloaded {count} new logos.")

if __name__ == "__main__":
    download_logos()
