
import os
import sys
import argparse
import itertools
import pandas as pd
import duckdb
import multiprocessing
from tqdm import tqdm
from google.cloud import bigquery

# Add project root to path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../../../')))

from posts.stuperlatives.etl.bq_utils import get_bq_client
from posts.stuperlatives.optimizer.config_definitions import (
    BASE_FILTERS, REGION_MAPPING, IHOP_TEAMS
)

# --- Configuration ---
TARGET_SEASON = 2025
PFF_TABLE = f"pff_rushing_summary_{TARGET_SEASON}"

# Metrics to Optimize (Positive Only)
# format: (metric_column, sort_direction, min_attempts_col, min_attempts_val)
# Metrics to Optimize
# format: (metric_sql, sort_direction, min_attempts_col, min_attempts_val)
METRICS = {
    'Rushing Yards': ('SUM(yards)', 'DESC', 'SUM(attempts)', 20),
    'Rushing TDs': ('SUM(touchdowns)', 'DESC', 'SUM(attempts)', 20),
    'Breakaway Yards': ('SUM(breakaway_yards)', 'DESC', 'SUM(attempts)', 20),
    'Breakaway %': ('CAST(SUM(breakaway_yards) AS FLOAT) / NULLIF(SUM(yards), 0)', 'DESC', 'SUM(attempts)', 20),
    'Yards After Contact/Att': ('CAST(SUM(yards_after_contact) AS FLOAT) / NULLIF(SUM(attempts), 0)', 'DESC', 'SUM(attempts)', 20),
    'Missed Tackles Forced': ('SUM(avoided_tackles)', 'DESC', 'SUM(attempts)', 20),
    'Explosive Runs (10+ yds)': ('SUM(explosive)', 'DESC', 'SUM(attempts)', 20),
    'Explosive Rate': ('CAST(SUM(explosive) AS FLOAT) / NULLIF(SUM(attempts), 0)', 'DESC', 'SUM(attempts)', 20)
}

def load_and_join_data(client):
    """
    Loads PFF Rushing Data and joins it with Schedule/Game context from PBP data.
    """
    print(f"Loading PFF Data from {PFF_TABLE}...")
    pff_query = f"""
        SELECT 
            player, position, team_name, week, attempts, 
            yards, touchdowns, breakaway_yards, breakaway_percent,
            elusive_rating, yco_attempt, avoided_tackles, explosive,
            yards_after_contact
        FROM `pff_analysis.{PFF_TABLE}`
        WHERE position = 'HB'  -- Filter for Running Backs only usually
    """
    pff_df = client.query(pff_query).to_dataframe()
    
    # Standardize team names if needed, but PFF usually uses 'SEA', 'SF' etc. 
    # Let's check schedule data to match.
    
    print("Loading Schedule Context from PBP Data...")
    # aggregate pbp to game level to get environment vars
    schedule_query = f"""
        SELECT 
            season, week, posteam as team_name, 
            defteam as opponent,
            home_team, away_team,
            CASE WHEN posteam = home_team THEN 'Home' ELSE 'Away' END as venue,
            roof,
            start_time,
            CAST(SPLIT(TRIM(SPLIT(start_time, ',')[SAFE_OFFSET(1)]), ':')[OFFSET(0)] AS INT64) as start_hour,
            div_game
        FROM `stuperlatives.pbp_data`
        WHERE season = {TARGET_SEASON}
        GROUP BY 1,2,3,4,5,6,7,8,9,10,11
    """
    schedule_df = client.query(schedule_query).to_dataframe()
    
    # Rename PFF team_name to match PBP team abbreviations if necessary
    # PFF: 'ARIZONA', 'ATLANTA' ?? Or 'ARI', 'ATL'? 
    # Usually PFF 'team_name' in the summary tables is 'ARI', 'ATL'. 
    # Let's assume abbreviations for now.
    
    print("Joining PFF and Schedule Data...")
    # Join on week and team_name
    merged_df = pd.merge(pff_df, schedule_df, on=['week', 'team_name'], how='inner')
    
    print(f"Merged Data: {len(merged_df)} rows.")
    return merged_df

def build_filters():
    """
    Constructs the filter permutations based on schedule columns.
    """
    # Custom Filters definitions based on the joined columns
    filters = {}
    
    # 1. Opponent Types
    filters['Opponent'] = {
        'Bird Teams': "opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA')",
        'Cat Teams': "opponent IN ('DET', 'JAX', 'CAR', 'CIN')",
        'Pirate Teams': "opponent IN ('TB', 'MIN', 'LV', 'OAK')",
        'Division Rivals': "div_game = 1"
    }
    
    # 2. Environment
    filters['Environment'] = {
        'Night Game': "start_hour >= 19", # PBP start_time is HH:MM:SS
        'Day Game': "start_hour < 19",
        'Dome': "roof IN ('dome', 'closed')",
        'Outdoors': "roof = 'outdoors'"
    }
    
    # 3. Geography
    region_options = {}
    for region, teams in REGION_MAPPING.items():
         teams_str = "', '".join(teams)
         region_options[f"in {region}"] = f"home_team IN ('{teams_str}')"
    filters['Geography'] = region_options
    
    # 4. Venue
    filters['Venue'] = {
        'Home': "venue = 'Home'",
        'Away': "venue = 'Away'"
    }

    # 5. IHOP
    if IHOP_TEAMS:
        teams_formatted = "', '".join(IHOP_TEAMS)
        filters['IHOP'] = {
            'Near IHOP': f"home_team IN ('{teams_formatted}')"
        }

    return filters

def process_chunk(args):
    perms, parquet_path, target_player = args
    con = duckdb.connect(database=':memory:')
    con.execute(f"CREATE VIEW data AS SELECT * FROM parquet_scan('{parquet_path}')")
    
    hits = []
    
    for perm in perms:
        metric_name = perm['metric']
        col_name, sort_dir, min_att_col, min_att_val = METRICS[metric_name]
        
        # Build Filter SQL
        filter_sql = "1=1"
        filter_descs = []
        for cat, name, sql in perm['filters']:
            filter_sql += f" AND {sql}"
            filter_descs.append(name)
            
        where_clause = f"WHERE {filter_sql}"
        
        # Query to get ranks
        # Metrics now contain full aggregation logic (e.g. SUM(x) or SUM(x)/SUM(y))
        query = f"""
            SELECT 
                player,
                {col_name} as val,
                {min_att_col} as opps
            FROM data
            {where_clause}
            GROUP BY player
            HAVING opps >= {min_att_val}
            ORDER BY val {sort_dir}
            LIMIT 5
        """
        
        try:
            df = con.execute(query).fetchdf()
            if not df.empty:
                top_player = df.iloc[0]['player']
                top_val = df.iloc[0]['val']
                
                if target_player.lower() in str(top_player).lower():
                    hits.append(perm)
        except Exception as e:
            pass
            
    con.close()
    return hits

class PFFOptimizer:
    def __init__(self, target_player):
        self.target_player = target_player
        self.bq_client = get_bq_client()
        self.filters = build_filters()
        
    def run(self):
        # 1. Load Data
        print("Loading data...")
        self.df = load_and_join_data(self.bq_client)
        
        # 2. Save to Parquet for workers
        import tempfile
        temp_dir = tempfile.mkdtemp()
        parquet_path = os.path.join(temp_dir, 'pff_data.parquet')
        self.df.to_parquet(parquet_path, index=False)
        
        # 3. Generate Permutations
        permutations = []
        # Flatten filters
        adhoc_filters = []
        for cat, opts in self.filters.items():
            for name, sql in opts.items():
                adhoc_filters.append((cat, name, sql))
        
        # Permutation Logic
        # - Metrics x (0 filters, 1 filter, 2 filters)
        for metric in METRICS:
            # 0 filters
            permutations.append({'metric': metric, 'filters': []})
            
            # 1 filter
            for f in adhoc_filters:
                permutations.append({'metric': metric, 'filters': [f]})
                
            # 2 filters (from different categories)
            for f1, f2 in itertools.combinations(adhoc_filters, 2):
                if f1[0] != f2[0]: # Different categories
                    permutations.append({'metric': metric, 'filters': [f1, f2]})

        print(f"Generated {len(permutations)} permutations.")
        
        # 4. Parallel Execution
        num_cores = multiprocessing.cpu_count()
        chunk_size = max(1, len(permutations) // (num_cores * 4))
        chunks = [permutations[i:i + chunk_size] for i in range(0, len(permutations), chunk_size)]
        
        worker_args = [(c, parquet_path, self.target_player) for c in chunks]
        
        winning_perms = []
        print("Starting Optimization...")
        with multiprocessing.Pool(num_cores) as pool:
            for result_perms in tqdm(pool.imap_unordered(process_chunk, worker_args), total=len(chunks)):
                if result_perms:
                    winning_perms.extend(result_perms)
                        
        print(f"\nFound {len(winning_perms)} hits. Generating Report...")
        self.generate_report(winning_perms)
            
        # Cleanup
        import shutil
        shutil.rmtree(temp_dir)

    def generate_report(self, perms):
        output_path = f"pff_stuperlatives_{self.target_player.replace(' ', '_').lower()}.md"
        
        # Use DuckDB on the local self.df
        con = duckdb.connect(database=':memory:')
        con.register('data', self.df)
        
        # deduplicate perms (sometimes overlapping chunks or logic might produce dupes, unlikely here but good practice)
        # Perms are dicts, can't be set members. Use JSON dump or tuple logic if needed. 
        # For now just list.
        
        with open(output_path, 'w') as f:
            f.write(f"# Stuperlatives: {self.target_player}\n\n")
            f.write(f"**Season:** {TARGET_SEASON}\n")
            f.write(f"**Generated:** {pd.Timestamp.now()}\n\n")
            
            for perm in perms:
                metric_name = perm['metric']
                col_name, sort_dir, min_att_col, min_att_val = METRICS[metric_name]
                
                # Reconstruct Filters
                filter_sql = "1=1"
                filter_descs = []
                for cat, name, sql in perm['filters']:
                    filter_sql += f" AND {sql}"
                    filter_descs.append(name)
                
                filters_str = ", ".join(filter_descs) if filter_descs else "All Games"
                
                # Query Top 5
                query = f"""
                    SELECT 
                        player,
                        {col_name} as val,
                        {min_att_col} as opps
                    FROM data
                    WHERE {filter_sql}
                    GROUP BY player
                    HAVING opps >= {min_att_val}
                    ORDER BY val {sort_dir}
                    LIMIT 5
                """
                
                # Execute
                try:
                    top_5_df = con.execute(query).fetchdf()
                except Exception as e:
                    print(f"Error generating table for {metric_name}: {e}")
                    continue

                # Write to Markdown
                f.write(f"## {metric_name}\n")
                f.write(f"**Conditions:** {filters_str}\n\n")
                f.write("### Leaderboard\n")
                f.write(top_5_df.to_markdown(index=False))
                f.write("\n\n")
                f.write("### SQL Query\n")
                f.write(f"```sql\n{query.strip()}\n```\n")
                f.write("---\n\n")
        
        con.close()
        print(f"Report saved to: {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--player', type=str, default='Kenneth Walker', help='Player name to optimize for')
    args = parser.parse_args()
    
    optimizer = PFFOptimizer(args.player)
    optimizer.run()
