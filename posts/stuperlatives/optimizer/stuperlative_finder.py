
import os
import sys
import argparse
import itertools
import random
import time
import duckdb
import pandas as pd
import multiprocessing
import tempfile
import shutil
from tqdm import tqdm

from tqdm import tqdm
from google.cloud import bigquery

# Add project root to path for imports
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from posts.stuperlatives.etl.bq_utils import get_bq_client
from posts.stuperlatives.optimizer.config_definitions import (
    METRICS, BASE_FILTERS, POSITION_FILTERS, REGION_MAPPING
)

# --- Worker Function (Must be top-level for pickling) ---

def process_chunk(args):
    """
    Worker function to process a chunk of permutations.
    args: (permutations, parquet_path, active_players, name_col, target_player_substring, position)
    """
    perms, parquet_path, active_players, name_col, target_player_substring, position = args
    
    # specialized imports for worker if needed, but top level should suffice
    
    # Initialize DuckDB connection for this worker
    con = duckdb.connect(database=':memory:')
    
    # Register Parquet file as a view (Fast, Zero-Copy-ish)
    con.execute(f"CREATE VIEW pbp_data AS SELECT * FROM parquet_scan('{parquet_path}')")
    
    # Register Active Players
    con.execute("CREATE TABLE active_players AS SELECT UNNEST(?) as player", [active_players])
    
    hits = []
    
    for perm in perms:
        query, desc = build_query(perm, name_col, position)
        try:
            df = con.execute(query).fetchdf()
            if not df.empty:
                top_player = df.iloc[0]['player']
                top_val = df.iloc[0]['value']
                
                if top_player and (target_player_substring.lower() in str(top_player).lower()):
                    hit_info = f"!!! HIT !!! {desc} -> #1 {top_player} (Val: {top_val})"
                    hits.append(hit_info)
        except Exception:
            pass
            
    con.close()
    return hits

def build_query(perm, name_col, position):
    """
    Re-implemented build_query as a standalone function (or static method) 
    so it can be used by the worker without passing the whole class instance.
    """
    metric_sql = perm['metric_sql']
    sort_dir = perm['sort_dir']
    cohort_name, cohort_sql = perm['cohort']
    
    # Base opportunity filter
    opp_filter = "1=1"
    if position == 'QB':
        opp_filter = "(pass_attempt = 1 OR sack = 1)"
        min_atts = 20
    elif position == 'RB':
        opp_filter = "rush_attempt = 1"
        min_atts = 20
    elif position == 'WR':
        opp_filter = "pass_attempt = 1" 
        min_atts = 10
    
    where_clauses = [opp_filter]
    where_clauses.append(f"({cohort_sql})")
    
    filter_descs = []
    for cat, name, sql in perm['filters']:
        where_clauses.append(f"({sql})")
        filter_descs.append(name)
        
    where_str = "\nAND ".join(where_clauses)
    
    query = f"""
    SELECT
        {name_col} as player,
        COUNT(*) as opportunities,
        {metric_sql} as value
    FROM pbp_data
    WHERE {where_str}
    GROUP BY 1
    HAVING opportunities >= {min_atts}
    ORDER BY value {sort_dir}
    LIMIT 5
    """
    
    desc = f"[{cohort_name}] {perm['metric']} | {', '.join(filter_descs) if filter_descs else 'No Filters'}"
    return query, desc


class StuperlativeFinder:
    def __init__(self, position='QB'):
        self.position = position
        self.bq_client = get_bq_client()
        self.filters = self._build_filters()
        
        # Temp directory for parquet file
        self.temp_dir = tempfile.mkdtemp()
        self.parquet_path = os.path.join(self.temp_dir, 'pbp_data.parquet')

    def _build_filters(self):
        combined_filters = BASE_FILTERS.copy()
        if self.position in POSITION_FILTERS:
            combined_filters.update(POSITION_FILTERS[self.position])
            
        flat_filters = {}
        for cat, opts in combined_filters.items():
            flat_filters[cat] = list(opts.items())
            
        region_options = [('All', '1=1')]
        for region, teams in REGION_MAPPING.items():
            teams_str = "', '".join(teams)
            region_options.append((region, f"home_team IN ('{teams_str}')"))
        flat_filters['Geography'] = region_options

        return flat_filters

    def load_data(self):
        # Cache configuration
        cache_dir = os.path.join(os.path.dirname(__file__), 'data')
        os.makedirs(cache_dir, exist_ok=True)
        self.cache_path = os.path.join(cache_dir, 'pbp_cache.parquet')

        if os.path.exists(self.cache_path):
            print(f"Loading data from local cache: {self.cache_path}")
            df = pd.read_parquet(self.cache_path)
            print(f"Loaded {len(df)} rows from cache.")
        else:
            print("Downloading data from BigQuery (ALL TIME)...")
            query = "SELECT * FROM `stuperlatives.pbp_data` WHERE season_type != 'PRE'"
            df = self.bq_client.query(query).to_dataframe()
            print(f"Loaded {len(df)} rows. Saving to cache...")
            df.to_parquet(self.cache_path, index=False)
            print("Cache saved.")
        
        # Determine Name Column
        name_col = 'passer_player_name'
        if self.position == 'RB':
            name_col = 'rusher_player_name'
        elif self.position == 'WR':
            name_col = 'receiver_player_name'
        self.name_col = name_col
            
        # Determine Active Players
        max_season = df['season'].max()
        print(f"Identifying Active Players using column: {name_col}")
        active_players = df[df['season'] == max_season][name_col].dropna().unique().tolist()
        print(f"Found {len(active_players)} active players.")
        self.active_players = active_players
        
        # Save to Parquet for workers
        print("Exporting data to Parquet for parallel workers...")
        df.to_parquet(self.parquet_path, index=False)
        print("Data Ready.")

    def generate_permutations(self):
        permutations = []
        non_default_opts = []
        for cat, opts in self.filters.items():
            for name, sql in opts:
                if name != 'All':
                    non_default_opts.append((cat, name, sql))
        
        cohorts = [
            ('All Time', '1=1'),
            ('Active Players', f"{self.name_col} IN (SELECT player FROM active_players)")
        ]

        metrics = METRICS.get(self.position, {})
        for metric_name, (metric_sql, sort_dir) in metrics.items():
            for cohort_name, cohort_sql in cohorts:
                # 0-Filter
                permutations.append({
                    'metric': metric_name, 'metric_sql': metric_sql, 'sort_dir': sort_dir,
                    'cohort': (cohort_name, cohort_sql), 'filters': []
                })
                # 1-Filter
                for opt in non_default_opts:
                    permutations.append({
                        'metric': metric_name, 'metric_sql': metric_sql, 'sort_dir': sort_dir,
                        'cohort': (cohort_name, cohort_sql), 'filters': [opt]
                    })
                # 2-Filter
                for combo in itertools.combinations(non_default_opts, 2):
                    if combo[0][0] != combo[1][0]: 
                        permutations.append({
                            'metric': metric_name, 'metric_sql': metric_sql, 'sort_dir': sort_dir,
                            'cohort': (cohort_name, cohort_sql), 'filters': list(combo)
                        })

        print(f"Generated {len(permutations)} permutations.")
        return permutations

    def run(self, target_player_substring):
        try:
            self.load_data()
            perms = self.generate_permutations()
            random.shuffle(perms)
            
            # CPU count for pool
            num_processes = multiprocessing.cpu_count()
            print(f"Starting Parallel Optimization Run using {num_processes} cores...")
            
            # Split perms into chunks
            chunk_size = max(1, len(perms) // (num_processes * 4)) # slightly granular chunks
            chunks = [perms[i:i + chunk_size] for i in range(0, len(perms), chunk_size)]
            
            # Prepare args for workers
            # (chunk, parquet_path, active_players, name_col, target_player_substring, position)
            worker_args = [
                (chunk, self.parquet_path, self.active_players, self.name_col, target_player_substring, self.position) 
                for chunk in chunks
            ]
            
            total_hits = []
            completed_queries = 0
            start_time = time.time()
            

            with multiprocessing.Pool(processes=num_processes) as pool:
                # Use imap_unordered to process results as they come in
                for result_hits in tqdm(pool.imap_unordered(process_chunk, worker_args), total=len(chunks), desc="Optimization Progress", unit="chunk"):
                    if result_hits:
                        for h in result_hits:
                            tqdm.write(h)
                            total_hits.append(h)

            print("\n--- Summary ---")
            print(f"Found {len(total_hits)} hits for {target_player_substring}.")
            for h in total_hits:
                print(f"- {h}")
                
        finally:
            # Cleanup temp directory
            if os.path.exists(self.temp_dir):
                shutil.rmtree(self.temp_dir)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Stuperlative Optimizer')
    parser.add_argument('--player', type=str, required=True, help='Substring of player name to find #1 stats for')
    parser.add_argument('--position', type=str, default='QB', choices=['QB', 'RB', 'WR'], help='Position group')
    
    args = parser.parse_args()
    
    # Needs to be wrapped in main block for multiprocessing safety on macOS/Windows
    try:
        finder = StuperlativeFinder(position=args.position)
        finder.run(args.player)
    except KeyboardInterrupt:
        print("\nOptimization stopped by user.")
