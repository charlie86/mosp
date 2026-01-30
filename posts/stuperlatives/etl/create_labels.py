
import os
import pandas as pd
import sys

# Add project root
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from posts.stuperlatives.etl.fetch_data import fetch_rosters

def create_label_template(years=[2023, 2024]):
    """
    Creates a CSV with columns: player_id, player_name, has_beard, has_mustache, is_redhead
    Populates with players who have headshots downloaded.
    """
    headshot_dir = "posts/stuperlatives/data/headshots"
    if not os.path.exists(headshot_dir):
        print("No headshots directory found.")
        return

    # Get list of player IDs from filenames
    downloaded_ids = [f.split('.')[0] for f in os.listdir(headshot_dir) if f.endswith('.png')]
    
    if not downloaded_ids:
        print("No headshots found.")
        return

    # Fetch roster to get names
    rosters = fetch_rosters(years)
    players = rosters[rosters['player_id'].isin(downloaded_ids)][['player_id', 'player_name', 'position']].drop_duplicates(subset=['player_id'])
    
    # Create DataFrame
    df = players.copy()
    df['has_beard'] = False
    df['has_mustache'] = False
    df['is_redhead'] = False
    
    output_path = "posts/stuperlatives/data/appearance_labels.csv"
    
    # If file exists, update it (keep existing labels)
    if os.path.exists(output_path):
        existing = pd.read_csv(output_path)
        # Merge
        merged = df.merge(existing[['player_id', 'has_beard', 'has_mustache', 'is_redhead']], on='player_id', how='left', suffixes=('', '_old'))
        # Fill old values
        for col in ['has_beard', 'has_mustache', 'is_redhead']:
             merged[col] = merged[f'{col}_old'].combine_first(merged[col])
        
        # Drop old cols
        merged = merged.drop(columns=[c for c in merged.columns if '_old' in c])
        merged.to_csv(output_path, index=False)
        print(f"Updated {output_path} with {len(merged)} players.")
    else:
        df.to_csv(output_path, index=False)
        print(f"Created {output_path} with {len(df)} players.")

if __name__ == "__main__":
    create_label_template()
