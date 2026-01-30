
import json
import os
import itertools
import random
import time
from google.cloud import bigquery
import pandas as pd
import duckdb
from posts.stuperlatives.etl.bq_utils import get_bq_client

# --- Configuration ---

# Geographic Mappings
REGION_MAPPING = {
    'West': ['SEA', 'SF', 'LAR', 'LAC', 'ARI', 'LV', 'DEN', 'OAK', 'SD'],
    'Midwest': ['GB', 'CHI', 'MIN', 'DET', 'IND', 'CIN', 'CLE', 'KC', 'STL'],
    'South': ['DAL', 'HOU', 'NO', 'ATL', 'CAR', 'TB', 'MIA', 'JAX', 'TEN'],
    'NorthEast': ['NE', 'NYJ', 'NYG', 'BUF', 'PHI', 'PIT', 'BAL', 'WAS']
}

# Metric Definitions (SQL fragments)
# FOCUS: Positive Metrics
METRICS = {
    'Passing Yards/Game': ('SUM(yards_gained)/COUNT(DISTINCT game_id)', 'DESC'),
    'TDs/Game': ('SUM(touchdown)/COUNT(DISTINCT game_id)', 'DESC'),
    'Completion %': ('SUM(complete_pass)/COUNT(*)', 'DESC'),
    'Yards/Attempt': ('SUM(yards_gained)/COUNT(*)', 'DESC'),
    'EPA/Play': ('AVG(epa)', 'DESC'),
    'Success Rate': ('SUM(success)/COUNT(*)', 'DESC'),
    'CPOE': ('AVG(cpoe)', 'DESC'),
    'TD/INT Ratio': ('CAST(SUM(touchdown) AS FLOAT64) / NULLIF(SUM(interception), 0)', 'DESC'),
    'Lowest INT Rate': ('SUM(interception)/COUNT(*)', 'ASC')
}

# Filter Definitions
FILTERS = {
    'Game Context': {
        'All': '1=1',
        'Ahead': 'score_differential > 0',
        'Behind': 'score_differential < 0',
        'Trailing': 'score_differential < 0', # Synonym
        'Tied': 'score_differential = 0',
        '4th Quarter': 'qtr = 4',
        'Overtime': 'qtr = 5',
        'One Score Game': 'ABS(score_differential) <= 8'
    },
    'Down': {
        'All': '1=1',
        '1st Down': 'down = 1',
        '2nd Down': 'down = 2',
        '3rd Down': 'down = 3',
        '4th Down': 'down = 4',
        'Money Down': 'down >= 3'
    },
    'Field Position': {
        'All': '1=1',
        'Red Zone': 'yardline_100 <= 20',
        'Own Territory': 'yardline_100 > 50',
        'Opponent Territory': 'yardline_100 <= 50',
        'Deep Own Terr': 'yardline_100 > 80'
    },
    'Opponent': {
        'All': '1=1',
        # DuckDB needs single quotes for strings in list
        'Pirate Teams': "defteam IN ('TB', 'MIN', 'LV', 'OAK')",
        'Bird Teams': "defteam IN ('ARI', 'ATL', 'BAL', 'PHI', 'SEA')",
        'Cat Teams': "defteam IN ('DET', 'JAX', 'CAR', 'CIN')",
        'Division Rivals': 'div_game = 1',
    },
    'Environment': {
        'All': '1=1',
        'Night Game': "start_time > '19:00:00'",
        'Dome': "roof IN ('dome', 'closed')",
        'Outdoors': "roof = 'outdoors'",
    },
    'Direction': {
        'All': '1=1',
        'Left': "pass_location = 'left'",
        'Middle': "pass_location = 'middle'",
        'Right': "pass_location = 'right'"
    }
}

# --- Data Loading ---

def load_ihop_teams():
    TEAM_NAME_TO_ABBR = {
        'Arizona Cardinals': 'ARI', 'Atlanta Falcons': 'ATL', 'Baltimore Ravens': 'BAL', 'Buffalo Bills': 'BUF',
        'Carolina Panthers': 'CAR', 'Chicago Bears': 'CHI', 'Cincinnati Bengals': 'CIN', 'Cleveland Browns': 'CLE',
        'Dallas Cowboys': 'DAL', 'Denver Broncos': 'DEN', 'Detroit Lions': 'DET', 'Green Bay Packers': 'GB',
        'Houston Texans': 'HOU', 'Indianapolis Colts': 'IND', 'Jacksonville Jaguars': 'JAX', 'Kansas City Chiefs': 'KC',
        'Las Vegas Raiders': 'LV', 'Los Angeles Chargers': 'LAC', 'Los Angeles Rams': 'LAR', 'Miami Dolphins': 'MIA',
        'Minnesota Vikings': 'MIN', 'New England Patriots': 'NE', 'New Orleans Saints': 'NO', 'New York Giants': 'NYG',
        'New York Jets': 'NYJ', 'Philadelphia Eagles': 'PHI', 'Pittsburgh Steelers': 'PIT', 'San Francisco 49ers': 'SF',
        'Seattle Seahawks': 'SEA', 'Tampa Bay Buccaneers': 'TB', 'Tennessee Titans': 'TEN', 'Washington Commanders': 'WAS',
        'Washington Football Team': 'WAS', 'Washington Redskins': 'WAS' 
    }
    
    json_path = os.path.join(os.path.dirname(__file__), '../../pff_analysis/data/stadium_gravitational_data.json')
    ihop_teams = set()
    try:
        with open(json_path, 'r') as f:
            data = json.load(f)
            for entry in data:
                team_name = entry.get('Team')
                ihops = entry.get('IHOPs', [])
                has_close_ihop = any(i.get('DistanceMiles', 100) < 5.0 for i in ihops)
                if has_close_ihop and team_name in TEAM_NAME_TO_ABBR:
                    ihop_teams.add(TEAM_NAME_TO_ABBR[team_name])
    except Exception as e:
        print(f"Error loading IHOP data: {e}")
        return []
    return list(ihop_teams)

# --- Engine ---

class DarnoldOptimizer:
    def __init__(self):
        self.bq_client = get_bq_client()
        self.ihop_teams = load_ihop_teams()
        self.con = duckdb.connect(database=':memory:')
        self.flat_filters = self.build_flat_filters()

    def load_data(self):
        print("Downloading data from BigQuery (ALL TIME)...")
        # Removed season >= 2018 filter to inspect full history
        query = "SELECT * FROM `stuperlatives.pbp_data`"
        df = self.bq_client.query(query).to_dataframe()
        print(f"Loaded {len(df)} rows.")
        
        # Determine Active Players (Players who played in the most recent season in DB)
        max_season = df['season'].max()
        print(f"Most recent season in DB: {max_season}")
        active_players = df[df['season'] == max_season]['passer_player_name'].dropna().unique()
        print(f"Found {len(active_players)} active players.")
        
        # Create active players table in DuckDB
        self.con.register('pbp_data', df)
        self.con.execute("CREATE TABLE active_players AS SELECT UNNEST(?) as player", [active_players.tolist()])
        print("Data Ready.")

    def build_flat_filters(self):
        flat_filters = {} 
        for cat, opts in FILTERS.items():
            flat_filters[cat] = list(opts.items())
        
        region_options = [('All', '1=1')]
        for region, teams in REGION_MAPPING.items():
            teams_str = "', '".join(teams)
            region_options.append((region, f"home_team IN ('{teams_str}')"))
        flat_filters['Geography'] = region_options
        
        if self.ihop_teams:
            ihop_str = "', '".join(self.ihop_teams)
            ihop_filter = ('IHOP Proximity', f"home_team IN ('{ihop_str}')")
            flat_filters['Environment'].append(ihop_filter)
        
        return flat_filters

    def generate_permutations(self):
        permutations = []
        
        # Filter Options
        non_default_opts = []
        for cat, opts in self.flat_filters.items():
            for name, sql in opts:
                if name != 'All':
                    non_default_opts.append((cat, name, sql))
        
        print(f"Total Filter Options: {len(non_default_opts)}")
        
        # Cohorts
        cohorts = [
            ('All Time', '1=1'),
            ('Active Players', 'passer_player_name IN (SELECT player FROM active_players)')
        ]

        for metric_name in METRICS:
            for cohort_name, cohort_sql in cohorts:
                
                # Setup base per-metric permutations
                
                # 0-Filter (Just Metric + Cohort)
                permutations.append({
                    'metric': metric_name,
                    'cohort': (cohort_name, cohort_sql),
                    'filters': []
                })

                # 1-Filter combos
                for opt in non_default_opts:
                    permutations.append({
                        'metric': metric_name,
                        'cohort': (cohort_name, cohort_sql),
                        'filters': [opt]
                    })
                
                # 2-Filter combos (Systematic)
                # We limit this to keep runtimes reasonable (~800 per metric/cohort)
                # Total: 9 metrics * 2 cohorts * (800 + 40) ~= 15,000 queries. 
                # might take ~30-40 mins at 7q/s.
                # Let's keep it restricted to cross-category only.
                for combo in itertools.combinations(non_default_opts, 2):
                    if combo[0][0] != combo[1][0]: # Different Categories
                        permutations.append({
                            'metric': metric_name,
                            'cohort': (cohort_name, cohort_sql),
                            'filters': list(combo)
                        })

        print(f"Generated {len(permutations)} permutations.")
        return permutations

    def build_query(self, perm):
        metric_name = perm['metric']
        metric_sql, sort_dir = METRICS[metric_name]
        
        cohort_name, cohort_sql = perm['cohort']
        
        where_clauses = ["(pass_attempt = 1 OR sack = 1)"]
        where_clauses.append(f"({cohort_sql})")
        
        filter_descs = []
        for cat, name, sql in perm['filters']:
            where_clauses.append(f"({sql})")
            filter_descs.append(name)
            
        where_str = "\nAND ".join(where_clauses)
        min_atts = 20
        
        # DuckDB Query
        query = f"""
        SELECT
            passer_player_name as player,
            COUNT(*) as opportunities,
            {metric_sql} as value
        FROM pbp_data
        WHERE {where_str}
        GROUP BY 1
        HAVING opportunities >= {min_atts}
        ORDER BY value {sort_dir}
        LIMIT 5
        """
        
        desc = f"[{cohort_name}] {metric_name} | {', '.join(filter_descs) if filter_descs else 'No Filters'}"
        return query, desc

    def run(self):
        self.load_data()
        perms = self.generate_permutations()
        
        hits = []
        start_time = time.time()
        
        # Randomize to get a spread of results early
        random.shuffle(perms)
        
        print(f"Starting Local Optimization Run ({len(perms)} queries)...")
        
        count = 0
        for perm in perms:
            query, desc = self.build_query(perm)
            try:
                # Execute against DuckDB
                df = self.con.execute(query).fetchdf()
                
                if not df.empty:
                    top_player = df.iloc[0]['player']
                    top_val = df.iloc[0]['value']
                    
                    if top_player and ('Darnold' in str(top_player)):
                        print(f"!!! HIT !!! {desc} -> #1 {top_player} (Val: {top_val})")
                        hits.append(desc)
                
            except Exception as e:
                pass
            
            count += 1
            if count % 1000 == 0:
                 elapsed = time.time() - start_time
                 rate = count / elapsed
                 print(f"Processed {count}/{len(perms)} queries ({rate:.1f} q/s)...")

        print("\n--- Summary ---")
        print(f"Found {len(hits)} hits.")
        for h in hits:
            print(f"- {h}")

if __name__ == "__main__":
    optimizer = DarnoldOptimizer()
    optimizer.run()
