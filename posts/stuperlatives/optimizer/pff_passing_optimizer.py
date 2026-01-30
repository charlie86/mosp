
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
    REGION_MAPPING, IHOP_TEAMS
)

# --- Configuration ---
TARGET_SEASON = 2025
SUMMARY_TABLE = f"pff_passing_summary_{TARGET_SEASON}"
DEEP_TABLE = f"pff_passing_depth_deep_{TARGET_SEASON}"
PRESSURE_TABLE = f"pff_passing_pressure_general_{TARGET_SEASON}"

# Metrics to Optimize
# format: (metric_sql, sort_direction, min_attempts_col, min_attempts_val)
METRICS = {
    # Summary Metrics
    'Passing Yards': ('SUM(yards)', 'DESC', 'SUM(attempts)', 20),
    'Touchdowns': ('SUM(touchdowns)', 'DESC', 'SUM(attempts)', 20),
    'Big Time Throws': ('SUM(big_time_throws)', 'DESC', 'SUM(attempts)', 20),
    'BTT Rate': ('CAST(SUM(big_time_throws) AS FLOAT) / NULLIF(SUM(attempts), 0)', 'DESC', 'SUM(attempts)', 20),
    'YPA': ('CAST(SUM(yards) AS FLOAT) / NULLIF(SUM(attempts), 0)', 'DESC', 'SUM(attempts)', 20),
    
    # Deep Passing Metrics (20+ yards)
    'Deep Yards': ('SUM(deep_yards)', 'DESC', 'SUM(deep_attempts)', 10),
    'Deep TDs': ('SUM(deep_touchdowns)', 'DESC', 'SUM(deep_attempts)', 10),
    'Deep BTT': ('SUM(deep_big_time_throws)', 'DESC', 'SUM(deep_attempts)', 10),
    'Deep BTT Rate': ('CAST(SUM(deep_big_time_throws) AS FLOAT) / NULLIF(SUM(deep_attempts), 0)', 'DESC', 'SUM(deep_attempts)', 10),
    'Deep YPA': ('CAST(SUM(deep_yards) AS FLOAT) / NULLIF(SUM(deep_attempts), 0)', 'DESC', 'SUM(deep_attempts)', 10),
    'Deep Completion %': ('CAST(SUM(deep_completions) AS FLOAT) / NULLIF(SUM(deep_attempts), 0)', 'DESC', 'SUM(deep_attempts)', 10),

    # Pressure Metrics
    'Pressure Yards': ('SUM(pressure_yards)', 'DESC', 'SUM(pressure_attempts)', 10),
    'Pressure TDs': ('SUM(pressure_touchdowns)', 'DESC', 'SUM(pressure_attempts)', 10),
    'Pressure BTT Rate': ('CAST(SUM(pressure_big_time_throws) AS FLOAT) / NULLIF(SUM(pressure_attempts), 0)', 'DESC', 'SUM(pressure_attempts)', 10),
    'Pressure YPA': ('CAST(SUM(pressure_yards) AS FLOAT) / NULLIF(SUM(pressure_attempts), 0)', 'DESC', 'SUM(pressure_attempts)', 10),
    
    # Clean Pocket Metrics
    'Clean Pocket YPA': ('CAST(SUM(no_pressure_yards) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0)', 'DESC', 'SUM(no_pressure_attempts)', 20),
    'Clean Pocket BTT Rate': ('CAST(SUM(no_pressure_big_time_throws) AS FLOAT) / NULLIF(SUM(no_pressure_attempts), 0)', 'DESC', 'SUM(no_pressure_attempts)', 20),
    
    # Blitz Metrics
    'Blitz YPA': ('CAST(SUM(blitz_yards) AS FLOAT) / NULLIF(SUM(blitz_attempts), 0)', 'DESC', 'SUM(blitz_attempts)', 10),
    'Blitz TDs': ('SUM(blitz_touchdowns)', 'DESC', 'SUM(blitz_attempts)', 10),
    'Blitz BTT Rate': ('CAST(SUM(blitz_big_time_throws) AS FLOAT) / NULLIF(SUM(blitz_attempts), 0)', 'DESC', 'SUM(blitz_attempts)', 10)
}

def load_and_join_data(client):
    print("Loading PFF Passing Data...")
    
    # Load Summary
    print(f"Loading {SUMMARY_TABLE}...")
    summary_df = client.query(f"""
        SELECT player, team_name, week, attempts, yards, touchdowns, big_time_throws 
        FROM `pff_analysis.{SUMMARY_TABLE}` WHERE position='QB'
    """).to_dataframe()
    
    # Load Deep
    print(f"Loading {DEEP_TABLE}...")
    deep_df = client.query(f"""
        SELECT player, team_name, week, 
            deep_attempts, deep_completions, deep_yards, deep_touchdowns, deep_big_time_throws
        FROM `pff_analysis.{DEEP_TABLE}` WHERE position='QB'
    """).to_dataframe()

    # Load Pressure
    print(f"Loading {PRESSURE_TABLE}...")
    pressure_df = client.query(f"""
        SELECT player, team_name, week,
            pressure_attempts, pressure_yards, pressure_touchdowns, pressure_big_time_throws,
            no_pressure_attempts, no_pressure_yards, no_pressure_big_time_throws,
            blitz_attempts, blitz_yards, blitz_touchdowns, blitz_big_time_throws
        FROM `pff_analysis.{PRESSURE_TABLE}` WHERE position='QB'
    """).to_dataframe()
    
    # Join PFF Tables
    print("Joining PFF Tables...")
    pff_df = pd.merge(summary_df, deep_df, on=['player', 'team_name', 'week'], how='left').fillna(0)
    pff_df = pd.merge(pff_df, pressure_df, on=['player', 'team_name', 'week'], how='left').fillna(0)
    
    # Load Schedule
    print("Loading Schedule Context...")
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
    
    # Join Schedule
    print("Joining Schedule Data...")
    final_df = pd.merge(pff_df, schedule_df, on=['week', 'team_name'], how='inner')
    
    print(f"Final Data: {len(final_df)} rows.")
    return final_df

def build_filters():
    filters = {}
    filters['Opponent'] = {
        'Bird Teams': "opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA')",
        'Cat Teams': "opponent IN ('DET', 'JAX', 'CAR', 'CIN')",
        'Pirate Teams': "opponent IN ('TB', 'MIN', 'LV', 'OAK')",
        'Division Rivals': "div_game = 1"
    }
    filters['Environment'] = {
        'Night Game': "start_hour >= 19",
        'Day Game': "start_hour < 19",
        'Dome': "roof IN ('dome', 'closed')",
        'Outdoors': "roof = 'outdoors'"
    }
    
    region_options = {}
    for region, teams in REGION_MAPPING.items():
         teams_str = "', '".join(teams)
         region_options[f"in {region}"] = f"home_team IN ('{teams_str}')"
    filters['Geography'] = region_options
    
    filters['Venue'] = {'Home': "venue = 'Home'", 'Away': "venue = 'Away'"}
    
    if IHOP_TEAMS:
        teams_formatted = "', '".join(IHOP_TEAMS)
        filters['IHOP'] = {'Near IHOP': f"home_team IN ('{teams_formatted}')"}

    return filters

def process_chunk(args):
    perms, parquet_path, target_player = args
    con = duckdb.connect(database=':memory:')
    con.execute(f"CREATE VIEW data AS SELECT * FROM parquet_scan('{parquet_path}')")
    
    hits = []
    
    for perm in perms:
        metric_name = perm['metric']
        col_sql, sort_dir, min_att_col, min_att_val = METRICS[metric_name]
        
        filter_sql = "1=1"
        for cat, name, sql in perm['filters']:
            filter_sql += f" AND {sql}"
            
        try:
            query = f"""
                SELECT 
                    player,
                    {col_sql} as val,
                    {min_att_col} as opps
                FROM data
                WHERE {filter_sql}
                GROUP BY player
                HAVING opps >= {min_att_val}
                ORDER BY val {sort_dir}
                LIMIT 5
            """
            
            df = con.execute(query).fetchdf()
            if not df.empty:
                top_player = df.iloc[0]['player']
                if target_player.lower() in str(top_player).lower():
                    hits.append(perm)
        except Exception:
            pass
            
    con.close()
    return hits

class PFFPassingOptimizer:
    def __init__(self, target_player):
        self.target_player = target_player
        self.bq_client = get_bq_client()
        self.filters = build_filters()
        
    def run(self):
        self.df = load_and_join_data(self.bq_client)
        
        # Save Parquet
        import tempfile
        temp_dir = tempfile.mkdtemp()
        parquet_path = os.path.join(temp_dir, 'pff_passing.parquet')
        self.df.to_parquet(parquet_path, index=False)
        
        # Permutations
        permutations = []
        adhoc_filters = []
        for cat, opts in self.filters.items():
            for name, sql in opts.items():
                adhoc_filters.append((cat, name, sql))
        
        for metric in METRICS:
            permutations.append({'metric': metric, 'filters': []})
            for f in adhoc_filters:
                permutations.append({'metric': metric, 'filters': [f]})
            for f1, f2 in itertools.combinations(adhoc_filters, 2):
                if f1[0] != f2[0]:
                    permutations.append({'metric': metric, 'filters': [f1, f2]})
                    
        print(f"Generated {len(permutations)} permutations.")
        
        # Parallel Run
        num_cores = multiprocessing.cpu_count()
        chunk_size = max(1, len(permutations) // (num_cores * 4))
        chunks = [permutations[i:i + chunk_size] for i in range(0, len(permutations), chunk_size)]
        
        worker_args = [(c, parquet_path, self.target_player) for c in chunks]
        winning_perms = []
        
        print("Starting Optimization...")
        with multiprocessing.Pool(num_cores) as pool:
            for result in tqdm(pool.imap_unordered(process_chunk, worker_args), total=len(chunks)):
                if result:
                    winning_perms.extend(result)
                    
        print(f"Found {len(winning_perms)} hits. Generating Report...")
        self.generate_report(winning_perms)
        
        import shutil
        shutil.rmtree(temp_dir)
        
    def generate_report(self, perms):
        output_path = f"pff_stuperlatives_{self.target_player.replace(' ', '_').lower()}.md"
        con = duckdb.connect(database=':memory:')
        con.register('data', self.df)
        
        with open(output_path, 'w') as f:
            f.write(f"# Stuperlatives: {self.target_player}\n\n")
            f.write(f"**Season:** {TARGET_SEASON}\n\n")
            
            for perm in perms:
                metric_name = perm['metric']
                col_sql, sort_dir, min_att_col, min_att_val = METRICS[metric_name]
                
                filter_descs = [f[1] for f in perm['filters']]
                filters_str = ", ".join(filter_descs) if filter_descs else "All Games"
                
                filter_sql = "1=1"
                for cat, name, sql in perm['filters']:
                    filter_sql += f" AND {sql}"
                    
                query = f"""
                    SELECT 
                        player,
                        {col_sql} as val,
                        {min_att_col} as opps
                    FROM data
                    WHERE {filter_sql}
                    GROUP BY player
                    HAVING opps >= {min_att_val}
                    ORDER BY val {sort_dir}
                    LIMIT 5
                """
                
                try:
                    top_5 = con.execute(query).fetchdf()
                    f.write(f"## {metric_name}\n")
                    f.write(f"**Conditions:** {filters_str}\n\n")
                    f.write(top_5.to_markdown(index=False))
                    f.write("\n\n")
                    f.write(f"```sql\n{query.strip()}\n```\n\n---\n\n")
                except Exception:
                    pass
        con.close()
        print(f"Saved report to {output_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument('--player', type=str, default='Sam Darnold', help='Player name to optimize for')
    args = parser.parse_args()
    
    optimizer = PFFPassingOptimizer(args.player)
    optimizer.run()
