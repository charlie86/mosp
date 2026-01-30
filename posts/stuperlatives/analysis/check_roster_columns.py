
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from posts.stuperlatives.etl.fetch_data import fetch_rosters

r = fetch_rosters([2024])
print("Roster Columns:")
print(r.columns.tolist())
