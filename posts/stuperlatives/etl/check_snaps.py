
import nfl_data_py as nfl
try:
    print("Attempting to import snap counts...")
    snaps = nfl.import_snap_counts([2024])
    print(snaps.head())
    print("Columns:", snaps.columns)
except Exception as e:
    print(e)
