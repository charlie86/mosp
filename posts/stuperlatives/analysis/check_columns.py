
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))
from posts.stuperlatives.etl.fetch_data import fetch_pbp_data

pbp = fetch_pbp_data([2024])
print("Columns containing 'pass':")
for c in pbp.columns:
    if 'pass' in c:
        print(c)

print("\nColumns containing 'defend':")
for c in pbp.columns:
    if 'defend' in c:
        print(c)

print("\nColumns containing 'interception':")
for c in pbp.columns:
    if 'intercep' in c:
        print(c)
