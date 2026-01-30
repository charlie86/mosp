
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from posts.stuperlatives.etl.fetch_data import fetch_rosters

r = fetch_rosters([2023, 2024])
darnold = r[r['player_name'] == 'Sam Darnold'][['player_name', 'player_id', 'team', 'position']].head(1)
print(darnold)
