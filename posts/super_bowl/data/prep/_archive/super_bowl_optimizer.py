
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

# Passing Tables
PASSING_SUMMARY = f"pff_passing_summary_{TARGET_SEASON}"
PASSING_DEEP = f"pff_passing_depth_deep_{TARGET_SEASON}"
PASSING_SHORT = f"pff_passing_depth_short_{TARGET_SEASON}"
PASSING_MED = f"pff_passing_depth_intermediate_{TARGET_SEASON}"
PASSING_BLOS = f"pff_passing_depth_behind_los_{TARGET_SEASON}"
PASSING_PRESSURE = f"pff_passing_pressure_general_{TARGET_SEASON}"
PASSING_BLITZ = f"pff_passing_pressure_blitz_{TARGET_SEASON}"
PASSING_SCREEN = f"pff_passing_concept_screen_{TARGET_SEASON}"

# Defense Tables
DEFENSE_SUMMARY = f"pff_defense_summary_{TARGET_SEASON}"
DEFENSE_COVERAGE = f"pff_defense_coverage_{TARGET_SEASON}"
DEFENSE_RUSH = f"pff_defense_pass_rush_{TARGET_SEASON}"

# OL Tables
BLOCKING_SUMMARY = f"pff_blocking_summary_{TARGET_SEASON}"

# IHOP Table
IHOP_TABLE = "stuperlatives.ihop_data"

# Metrics Definition

PASSING_METRICS = {
    # --- Summary ---
    'Passing Yards': ('SUM(yards)', 'DESC', 'SUM(attempts)', 20),
    'Touchdowns': ('SUM(touchdowns)', 'DESC', 'SUM(attempts)', 20),
    'Median BTT Rate': ('MEDIAN(btt_rate)', 'DESC', 'SUM(attempts)', 20),
    'Median YPA': ('MEDIAN(ypa)', 'DESC', 'SUM(attempts)', 20),
    'Median Passer Rating': ('MEDIAN(qb_rating)', 'DESC', 'SUM(attempts)', 20),
    'Median Comp %': ('MEDIAN(completion_percent)', 'DESC', 'SUM(attempts)', 20),
    
    # --- Depth ---
    'Median Deep BTT Rate': ('MEDIAN(deep_btt_rate)', 'DESC', 'SUM(deep_attempts)', 5),
    'Median Deep YPA': ('MEDIAN(deep_ypa)', 'DESC', 'SUM(deep_attempts)', 5),
    'Median Medium YPA': ('MEDIAN(medium_ypa)', 'DESC', 'SUM(medium_attempts)', 5),
    'Median Short YPA': ('MEDIAN(short_ypa)', 'DESC', 'SUM(short_attempts)', 10),
    'Median Short Comp %': ('MEDIAN(short_completion_percent)', 'DESC', 'SUM(short_attempts)', 10),
    'Median Behind LOS YPA': ('MEDIAN(behind_los_ypa)', 'DESC', 'SUM(behind_los_attempts)', 5),
    
    # --- Pressure/Pocket ---
    'Median Clean Pocket Grade': ('MEDIAN(no_pressure_grades_pass)', 'DESC', 'SUM(no_pressure_dropbacks)', 20),
    'Median Clean YPA': ('MEDIAN(no_pressure_ypa)', 'DESC', 'SUM(no_pressure_attempts)', 20),
    'Median Pressure Grade': ('MEDIAN(pressure_grades_pass)', 'DESC', 'SUM(pressure_dropbacks)', 10),
    'Median YPA Under Pressure': ('MEDIAN(pressure_ypa)', 'DESC', 'SUM(pressure_attempts)', 10),
    
    # --- Negatives (Default ASC, so Worst = High Values) ---
    'Interceptions': ('SUM(interceptions)', 'ASC', 'SUM(attempts)', 20),
    'Sacks': ('SUM(sacks)', 'ASC', 'SUM(dropbacks)', 20),
    'Turnover Worthy Plays': ('SUM(turnover_worthy_plays)', 'ASC', 'SUM(attempts)', 20),
    
    # --- Blitz ---
    'Median Blitz Grade': ('MEDIAN(blitz_grades_pass)', 'DESC', 'SUM(blitz_dropbacks)', 10),
    'Median YPA vs Blitz': ('MEDIAN(blitz_ypa)', 'DESC', 'SUM(blitz_attempts)', 10),
    
    # --- Concepts ---
    'Median Screen YPA': ('MEDIAN(screen_ypa)', 'DESC', 'SUM(screen_dropbacks)', 5),
}

DEFENSE_METRICS = {
    # Summary
    'Median Defense Grade': ('MEDIAN(grades_defense)', 'DESC', 'COUNT(*)', 1),
    'Median Coverage Grade': ('MEDIAN(grades_coverage_defense)', 'DESC', 'COUNT(*)', 1),
    'Median Pass Rush Grade': ('MEDIAN(grades_pass_rush_defense)', 'DESC', 'COUNT(*)', 1),
    
    # Production
    'Interceptions': ('SUM(interceptions)', 'DESC', 'COUNT(*)', 1),
    'Total Pressures': ('SUM(total_pressures)', 'DESC', 'COUNT(*)', 1),
    'Sacks': ('SUM(sacks)', 'DESC', 'COUNT(*)', 1),
    'Stops': ('SUM(stops)', 'DESC', 'COUNT(*)', 1),
    
    # Efficiency
    'Median Forced Inc Rate': ('MEDIAN(forced_incompletion_rate)', 'DESC', 'COUNT(*)', 1),
    'Median Yds Per Cov Snap': ('MEDIAN(yards_per_coverage_snap)', 'ASC', 'COUNT(*)', 1),
    'Median PRP': ('MEDIAN(prp)', 'DESC', 'COUNT(*)', 1),
    'Median Win Rate': ('MEDIAN(pass_rush_win_rate)', 'DESC', 'COUNT(*)', 1),
    'Median Missed Tackle Rate': ('MEDIAN(missed_tackle_rate)', 'ASC', 'COUNT(*)', 1),
}

OL_METRICS = {
    # Grades (Median of Unit Averages)
    'Median OL Grade': ('MEDIAN(unit_grade_offense)', 'DESC', 'COUNT(*)', 1),
    'Median Pass Block Grade': ('MEDIAN(unit_grade_pass_block)', 'DESC', 'COUNT(*)', 1),
    'Median Run Block Grade': ('MEDIAN(unit_grade_run_block)', 'DESC', 'COUNT(*)', 1),
    
    # Production (Sums)
    'Sacks Allowed': ('SUM(unit_sacks_allowed)', 'ASC', 'COUNT(*)', 1),
    'Pressures Allowed': ('SUM(unit_pressures_allowed)', 'ASC', 'COUNT(*)', 1),
    
    # Efficiency
    'Median PBE': ('MEDIAN(unit_pbe)', 'DESC', 'COUNT(*)', 1),
}


def load_data(client):
    print("Loading Data...")
    
    # --- Loading Passing ---
    print(f"Loading {PASSING_SUMMARY}...")
    pass_summary = client.query(f"""
        SELECT player, team_name, week, 
            attempts, yards, touchdowns, big_time_throws, turnover_worthy_plays, 
            accuracy_percent, qb_rating, btt_rate, twp_rate, ypa, completion_percent,
            sacks, dropbacks, interceptions
        FROM `pff_analysis.{PASSING_SUMMARY}` WHERE position='QB'
    """).to_dataframe()
    
    def merge_table(base_df, table_name, select_cols):
        try:
            print(f"Loading {table_name}...")
            cols_str = ", ".join(select_cols)
            df = client.query(f"""
                SELECT player, team_name, week, {cols_str}
                FROM `pff_analysis.{table_name}` WHERE position='QB'
            """).to_dataframe()
            return pd.merge(base_df, df, on=['player','team_name','week'], how='left')
        except Exception as e:
            print(f"Could not load {table_name}: {e}")
            return base_df

    # Load Extra Passing Tables
    pass_summary = merge_table(pass_summary, PASSING_DEEP, ['deep_attempts', 'deep_yards', 'deep_touchdowns', 'deep_btt_rate', 'deep_ypa', 'deep_qb_rating'])
    pass_summary = merge_table(pass_summary, PASSING_SHORT, ['short_attempts', 'short_completion_percent', 'short_ypa'])
    pass_summary = merge_table(pass_summary, PASSING_MED, ['medium_attempts', 'medium_ypa', 'medium_qb_rating'])
    pass_summary = merge_table(pass_summary, PASSING_BLOS, ['behind_los_attempts', 'behind_los_ypa'])
    pass_summary = merge_table(pass_summary, PASSING_PRESSURE, ['pressure_grades_pass', 'pressure_dropbacks', 'pressure_attempts', 'pressure_ypa', 'no_pressure_grades_pass', 'no_pressure_dropbacks', 'no_pressure_attempts', 'no_pressure_ypa'])
    pass_summary = merge_table(pass_summary, PASSING_BLITZ, ['blitz_grades_pass', 'blitz_dropbacks', 'blitz_attempts', 'blitz_ypa', 'blitz_btt_rate'])
    pass_summary = merge_table(pass_summary, PASSING_SCREEN, ['screen_grades_pass', 'screen_dropbacks', 'screen_ypa'])
    # Need dropbacks/sacks for 'Sacks' metric if not in summary. 
    # Summary has 'attempts', 'yards', 'touchdowns'. Does it have sacks? 
    # Inspecting load_data query: 'attempts, yards, touchdowns...'. No sacks.
    # 'pff_passing_summary' usually has 'sacks'. Let's add it to the initial load query.

    pass_summary['type'] = 'passing'
    pass_summary['player'] = pass_summary['player'].astype(str)

    # --- Loading Defense ---
    print(f"Loading {DEFENSE_SUMMARY}...")
    def_summary = client.query(f"""
        SELECT team_name as player, team_name, week, 
            grades_defense, grades_coverage_defense, grades_pass_rush_defense,
            interceptions, pass_break_ups, missed_tackle_rate, sacks, stops, total_pressures
        FROM `pff_analysis.{DEFENSE_SUMMARY}`
    """).to_dataframe()
    
    # Load Defense Extra
    try:
        def_cov = client.query(f"SELECT team_name, week, forced_incompletion_rate, yards_per_coverage_snap, qb_rating_against FROM `pff_analysis.{DEFENSE_COVERAGE}`").to_dataframe()
        def_cov_agg = def_cov.groupby(['team_name', 'week']).mean().reset_index()
        def_summary = pd.merge(def_summary, def_cov_agg, on=['team_name','week'], how='left')
    except: pass
    try:
        def_rush = client.query(f"SELECT team_name, week, prp, pass_rush_win_rate FROM `pff_analysis.{DEFENSE_RUSH}`").to_dataframe()
        def_rush_agg = def_rush.groupby(['team_name', 'week']).mean().reset_index()
        def_summary = pd.merge(def_summary, def_rush_agg, on=['team_name','week'], how='left')
    except: pass
    def_summary['type'] = 'defense'
    
    # --- Loading OL ---
    print(f"Loading {BLOCKING_SUMMARY}...")
    # Aggregating Player Stats to Unit Stats per Game
    ol_query = f"""
        SELECT 
            team_name, week,
            AVG(grades_offense) as unit_grade_offense,
            AVG(grades_pass_block) as unit_grade_pass_block,
            AVG(grades_run_block) as unit_grade_run_block,
            SUM(sacks_allowed) as unit_sacks_allowed,
            SUM(pressures_allowed) as unit_pressures_allowed,
            AVG(pbe) as unit_pbe
        FROM `pff_analysis.{BLOCKING_SUMMARY}`
        WHERE position_group = 'OL'
        GROUP BY team_name, week
    """
    ol_summary = client.query(ol_query).to_dataframe()
    ol_summary['player'] = ol_summary['team_name'] # treat team as player for OL
    ol_summary['type'] = 'ol'

    
    # --- Joining Schedule & IHOP ---
    print("Loading Schedule & IHOP Context...")
    schedule_query = f"""
        WITH ihop AS (
            SELECT Team, DistanceMiles FROM `{IHOP_TABLE}`
        )
        SELECT 
            s.season, s.week, s.posteam as team_name, 
            s.defteam as opponent,
            s.home_team, s.away_team,
            CASE WHEN s.posteam = s.home_team THEN 'Home' ELSE 'Away' END as venue,
            s.roof,
            CAST(i.DistanceMiles AS FLOAT64) as dist_to_ihop
        FROM `stuperlatives.pbp_data` s
        LEFT JOIN ihop i ON s.home_team = i.Team
        WHERE s.season = {TARGET_SEASON}
        GROUP BY 1,2,3,4,5,6,7,8,9
    """
    schedule_df = client.query(schedule_query).to_dataframe()
    
    print("Joining Schedule...")
    pass_final = pd.merge(pass_summary, schedule_df, on=['week', 'team_name'], how='inner')
    def_final = pd.merge(def_summary, schedule_df, on=['week', 'team_name'], how='inner')
    ol_final = pd.merge(ol_summary, schedule_df, on=['week', 'team_name'], how='inner')
    
    return pass_final, def_final, ol_final


def build_filters():
    filters = {}
    filters['Opponent'] = {
        'Bird Teams': "opponent IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA')",
        'Hat Teams': "opponent IN ('NE', 'TB', 'DAL', 'SF', 'PIT', 'WAS', 'MIN', 'LV', 'OAK')"
    }
    filters['Environment'] = {
        'Dome': "roof IN ('dome', 'closed')",
        'Outdoors': "roof = 'outdoors'"
    }
    return filters

def process_chunk(args):
    perms, parquet_path, target_entity, entity_type = args
    con = duckdb.connect(database=':memory:')
    con.execute(f"CREATE VIEW data AS SELECT * FROM parquet_scan('{parquet_path}')")
    
    hits = []
    
    if entity_type == 'passing': metrics = PASSING_METRICS
    elif entity_type == 'defense': metrics = DEFENSE_METRICS
    else: metrics = OL_METRICS
    
    for perm in perms:
        metric_name = perm['metric']
        if metric_name not in metrics: continue
        
        col_sql, default_sort_dir, min_att_col, min_att_val = metrics[metric_name]
        
        filter_sql = "1=1"
        for cat, name, sql in perm['filters']:
            filter_sql += f" AND {sql}"
            
        directions = [
            ('Best', default_sort_dir),
            ('Worst', 'ASC' if default_sort_dir == 'DESC' else 'DESC')
        ]
        
        for rank_type, sort_dir in directions:
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
                    if target_entity.lower() in str(top_player).lower():
                        perm_copy = perm.copy()
                        perm_copy['rank_type'] = rank_type
                        hits.append(perm_copy)
            except Exception:
                pass
            
    con.close()
    return hits

class SuperBowlOptimizer:
    def __init__(self):
        self.bq_client = get_bq_client()
        self.filters = build_filters()
        
    def run(self):
        pass_df, def_df, ol_df = load_data(self.bq_client)
        
        bird_sql = self.filters['Opponent']['Bird Teams']
        hat_sql = self.filters['Opponent']['Hat Teams']
        
        # 1. Drake Maye (Passing) vs Bird Teams
        print("\n--- Analyzing Drake Maye (Passing) vs Bird Teams ---")
        self.run_optimization(pass_df, 'Drake Maye', 'passing', forced_filter=('Opponent', 'Bird Teams', bird_sql))
        
        # 2. SEA (Defense) vs Hat Teams
        print("\n--- Analyzing SEA (Defense) vs Hat Teams ---")
        self.run_optimization(def_df, 'SEA', 'defense', forced_filter=('Opponent', 'Hat Teams', hat_sql))
        
        # 3. NE (OL) vs Bird Teams
        print("\n--- Analyzing NE (OL) vs Bird Teams ---")
        self.run_optimization(ol_df, 'NE', 'ol', forced_filter=('Opponent', 'Bird Teams', bird_sql))
        
        # 4. SEA (OL) vs Hat Teams
        print("\n--- Analyzing SEA (OL) vs Hat Teams ---")
        self.run_optimization(ol_df, 'SEA', 'ol', forced_filter=('Opponent', 'Hat Teams', hat_sql))

        
    def run_optimization(self, df, target, type_, forced_filter=None):
        import tempfile
        import shutil
        temp_dir = tempfile.mkdtemp()
        parquet_path = os.path.join(temp_dir, f'{type_}.parquet')
        df.to_parquet(parquet_path, index=False)
        
        permutations = []
        adhoc_filters = []
        for cat, opts in self.filters.items():
            for name, sql in opts.items():
                if forced_filter and forced_filter[1] == name:
                    continue
                adhoc_filters.append((cat, name, sql))
        
        if type_ == 'passing': metrics = PASSING_METRICS
        elif type_ == 'defense': metrics = DEFENSE_METRICS
        else: metrics = OL_METRICS

        for metric in metrics:
            base_filters = [forced_filter] if forced_filter else []
            permutations.append({'metric': metric, 'filters': base_filters})
            for f in adhoc_filters:
                new_filters = base_filters + [f]
                permutations.append({'metric': metric, 'filters': new_filters})
            for f1, f2 in itertools.combinations(adhoc_filters, 2):
                if f1[0] != f2[0]:
                    new_filters = base_filters + [f1, f2]
                    permutations.append({'metric': metric, 'filters': new_filters})

        num_cores = multiprocessing.cpu_count()
        chunk_size = max(1, len(permutations) // (num_cores * 4))
        chunks = [permutations[i:i + chunk_size] for i in range(0, len(permutations), chunk_size)]
        
        worker_args = [(c, parquet_path, target, type_) for c in chunks]
        winning_perms = []
        
        with multiprocessing.Pool(num_cores) as pool:
            for result in tqdm(pool.imap_unordered(process_chunk, worker_args), total=len(chunks)):
                if result:
                    winning_perms.extend(result)
        
        print(f"Found {len(winning_perms)} hits for {target}.")
        self.generate_report(winning_perms, df, target, type_)
        shutil.rmtree(temp_dir)

    def generate_report(self, perms, df, target, type_):
        base_name = f"super_bowl_stuperlatives_{target.replace(' ', '_').lower()}.md"
        # Append type to filename if it's OL to avoid overwrite if name conflict
        if type_ == 'ol':
           base_name = f"super_bowl_stuperlatives_{target.replace(' ', '_').lower()}_ol.md"
        
        filename = f"posts/stuperlatives/super_bowl/{base_name}"

        con = duckdb.connect(database=':memory:')
        con.register('data', df)
        
        if type_ == 'passing': metrics = PASSING_METRICS
        elif type_ == 'defense': metrics = DEFENSE_METRICS
        else: metrics = OL_METRICS
        
        with open(filename, 'w') as f:
            f.write(f"# Super Bowl Preview: {target} ({type_.upper()})\n\n")
            f.write(f"**Season:** {TARGET_SEASON}\n\n")
            
            perms_by_type = {'Best': [], 'Worst': []}
            for p in perms:
                perms_by_type[p.get('rank_type', 'Best')].append(p)
            
            for rank_type, p_list in perms_by_type.items():
                if not p_list: continue
                f.write(f"# {rank_type} Stuperlatives\n\n")
                
                for perm in p_list:
                    metric_name = perm['metric']
                    col_sql, default_sort_dir, min_att_col, min_att_val = metrics[metric_name]
                    
                    if rank_type == 'Best':
                        sort_dir = default_sort_dir
                    else:
                        sort_dir = 'ASC' if default_sort_dir == 'DESC' else 'DESC'
                    
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
                        f.write(f"## {metric_name} ({rank_type})\n")
                        f.write(f"**Conditions:** {filters_str}\n\n")
                        f.write(top_5.to_markdown(index=False))
                        f.write("\n\n")
                        f.write(f"```sql\n{query.strip()}\n```\n\n---\n\n")
                    except Exception:
                        pass
        con.close()
        print(f"Saved: {filename}")

if __name__ == "__main__":
    optimizer = SuperBowlOptimizer()
    optimizer.run()
